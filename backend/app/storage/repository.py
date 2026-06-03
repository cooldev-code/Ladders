from __future__ import annotations

import json
import threading
from pathlib import Path

from app.models.job import JobPosting, RejectedJob


class ApprovedJobRepository:
    def __init__(self) -> None:
        self._jobs: dict[str, JobPosting] = {}
        self._lock = threading.Lock()

    def clear(self) -> None:
        with self._lock:
            self._jobs.clear()

    def replace_all(self, jobs: list[JobPosting]) -> None:
        with self._lock:
            self._jobs = {job.id: job for job in jobs}

    def list_all(self) -> list[JobPosting]:
        with self._lock:
            return list(self._jobs.values())

    def get(self, job_id: str) -> JobPosting | None:
        with self._lock:
            return self._jobs.get(job_id)


class RejectionLogger:
    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._entries: list[RejectedJob] = []
        self._lock = threading.Lock()

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
        if self._log_path.exists():
            self._log_path.unlink()

    def log_all(self, rejected: list[RejectedJob]) -> None:
        with self._lock:
            self._entries = list(rejected)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._log_path.open("w", encoding="utf-8") as handle:
            for entry in rejected:
                payload = {
                    "job_id": entry.job.id,
                    "title": entry.job.title,
                    "company": entry.job.company,
                    "reasons": entry.reasons,
                }
                handle.write(json.dumps(payload) + "\n")

    def list_all(self) -> list[RejectedJob]:
        with self._lock:
            return list(self._entries)
