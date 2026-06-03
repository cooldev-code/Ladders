from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.admin import build_admin_router
from app.api.routes.jobs import build_jobs_router
from app.config import REJECTED_JOBS_LOG
from app.pipeline import JobPipeline
from app.storage.query import JobQueryService
from app.storage.repository import ApprovedJobRepository, RejectionLogger

repository = ApprovedJobRepository()
rejection_logger = RejectionLogger(REJECTED_JOBS_LOG)
query_service = JobQueryService()
pipeline = JobPipeline(repository, rejection_logger)


@asynccontextmanager
async def lifespan(_: FastAPI):
    pipeline.run()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Ladders Job Ingestion API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(build_jobs_router(repository, query_service))
    app.include_router(build_admin_router(pipeline, rejection_logger))

    @app.get("/api/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
