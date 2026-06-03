from fastapi import APIRouter

from app.api.schemas import IngestResponse, RejectedJobResponse
from app.pipeline import JobPipeline
from app.storage.repository import RejectionLogger


def build_admin_router(
    pipeline: JobPipeline,
    rejection_logger: RejectionLogger,
) -> APIRouter:
    router = APIRouter(prefix="/api/admin", tags=["admin"])

    @router.post("/ingest", response_model=IngestResponse)
    def run_ingest() -> IngestResponse:
        result = pipeline.run()
        return IngestResponse(
            ingested=len(result.ingestion.jobs),
            ingestion_errors=len(result.ingestion.errors),
            approved=len(result.approved),
            rejected=len(result.rejected),
        )

    @router.get("/rejected", response_model=list[RejectedJobResponse])
    def list_rejected() -> list[RejectedJobResponse]:
        return [
            RejectedJobResponse(
                job_id=entry.job.id,
                title=entry.job.title,
                company=entry.job.company,
                reasons=entry.reasons,
            )
            for entry in rejection_logger.list_all()
        ]

    return router
