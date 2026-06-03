from __future__ import annotations

from app.domain.location import country_bucket
from app.models.job import JobPosting


def summarize_catalog(jobs: list[JobPosting]) -> dict[str, int]:
    """Aggregate headline stats over the full approved-job catalog."""

    remote = sum(1 for job in jobs if job.location.is_remote)
    countries = {
        country_bucket(job.location.country)
        for job in jobs
        if job.location.country.strip()
    }
    return {
        "total": len(jobs),
        "remote": remote,
        "countries": len(countries),
    }
