from __future__ import annotations

from enum import Enum

from app.domain.location import country_bucket
from app.domain.salary import annual_usd_equivalent
from app.models.job import JobPosting


class SortField(str, Enum):
    SALARY = "salary"
    POSTING_DATE = "posting_date"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class JobQueryService:
    def search(
        self,
        jobs: list[JobPosting],
        *,
        query: str | None = None,
        country: str | None = None,
        sort_by: SortField = SortField.POSTING_DATE,
        order: SortOrder = SortOrder.DESC,
    ) -> list[JobPosting]:
        results = jobs

        if query:
            needle = query.strip().lower()
            if needle:
                results = [job for job in results if needle in job.title.lower()]

        if country:
            bucket = country_bucket(country)
            if bucket:
                results = [
                    job for job in results if country_bucket(job.location.country) == bucket
                ]

        reverse = order == SortOrder.DESC

        if sort_by == SortField.SALARY:
            return sorted(
                results,
                key=lambda job: annual_usd_equivalent(job.salary),
                reverse=reverse,
            )

        dated = [job for job in results if job.posting_date is not None]
        undated = [job for job in results if job.posting_date is None]
        dated.sort(key=lambda job: job.posting_date, reverse=reverse)  # type: ignore[arg-type]
        return dated + undated
