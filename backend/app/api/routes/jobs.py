from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import (
    CatalogStatsResponse,
    JobResponse,
    PaginatedJobsResponse,
    to_job_response,
)
from app.storage.pagination import paginate
from app.storage.query import JobQueryService, SortField, SortOrder
from app.storage.repository import ApprovedJobRepository
from app.storage.stats import summarize_catalog


def build_jobs_router(
    repository: ApprovedJobRepository,
    query_service: JobQueryService,
) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["jobs"])

    @router.get("/jobs", response_model=PaginatedJobsResponse)
    def list_jobs(
        q: str | None = Query(default=None, description="Search by title"),
        country: str | None = Query(default=None, description="Filter by country"),
        sort_by: SortField = Query(default=SortField.POSTING_DATE),
        order: SortOrder = Query(default=SortOrder.DESC),
        page: int = Query(default=1, ge=1, description="1-indexed page number"),
        page_size: int = Query(default=5, ge=1, le=100),
    ) -> PaginatedJobsResponse:
        results = query_service.search(
            repository.list_all(),
            query=q,
            country=country,
            sort_by=sort_by,
            order=order,
        )
        page_result = paginate(results, page=page, page_size=page_size)
        return PaginatedJobsResponse(
            items=[to_job_response(job) for job in page_result.items],
            total=page_result.total,
            page=page_result.page,
            page_size=page_result.page_size,
            total_pages=page_result.total_pages,
            has_next=page_result.has_next,
            has_prev=page_result.has_prev,
        )

    @router.get("/stats", response_model=CatalogStatsResponse)
    def catalog_stats() -> CatalogStatsResponse:
        return CatalogStatsResponse(**summarize_catalog(repository.list_all()))

    @router.get("/jobs/{job_id}", response_model=JobResponse)
    def get_job(job_id: str) -> JobResponse:
        job = repository.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return to_job_response(job)

    return router
