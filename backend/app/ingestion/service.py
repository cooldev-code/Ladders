from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.ingestion.normalizers import normalize_raw_job
from app.ingestion.reader import IngestionError, read_all_feeds
from app.models.job import JobPosting


@dataclass
class IngestionResult:
    jobs: list[JobPosting]
    errors: list[IngestionError]


def ingest_feeds(feeds_dir: Path) -> IngestionResult:
    jobs: list[JobPosting] = []
    errors: list[IngestionError] = []

    for feed_name, records in read_all_feeds(feeds_dir):
        for index, raw in enumerate(records):
            if not isinstance(raw, dict):
                errors.append(
                    IngestionError(
                        feed=feed_name,
                        index=index,
                        error="Record is not a JSON object",
                    )
                )
                continue
            try:
                jobs.append(normalize_raw_job(raw, index, feed_name))
            except (TypeError, ValueError) as exc:
                errors.append(
                    IngestionError(feed=feed_name, index=index, error=str(exc))
                )

    return IngestionResult(jobs=jobs, errors=errors)
