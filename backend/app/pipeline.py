from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.approval import ApprovalEngine, default_rules
from app.config import FEEDS_DIR, REJECTED_JOBS_LOG
from app.ingestion.service import IngestionResult, ingest_feeds
from app.models.job import JobPosting, RejectedJob
from app.storage.repository import ApprovedJobRepository, RejectionLogger


@dataclass
class PipelineResult:
    ingestion: IngestionResult
    approved: list[JobPosting]
    rejected: list[RejectedJob]


class JobPipeline:
    def __init__(
        self,
        repository: ApprovedJobRepository,
        rejection_logger: RejectionLogger,
        feeds_dir: Path = FEEDS_DIR,
    ) -> None:
        self._repository = repository
        self._rejection_logger = rejection_logger
        self._feeds_dir = feeds_dir
        self._engine = ApprovalEngine(default_rules())

    def run(self) -> PipelineResult:
        ingestion = ingest_feeds(self._feeds_dir)
        approved, rejected = self._engine.process(ingestion.jobs)

        self._repository.clear()
        self._repository.replace_all(approved)

        self._rejection_logger.clear()
        self._rejection_logger.log_all(rejected)

        return PipelineResult(
            ingestion=ingestion,
            approved=approved,
            rejected=rejected,
        )
