from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from app.models.job import EmploymentType, JobPosting, SalaryPeriod


class LocationResponse(BaseModel):
    city: str
    state: str
    country: str
    is_remote: bool


class SalaryResponse(BaseModel):
    amount: float
    currency: str
    period: SalaryPeriod
    display: str


class JobResponse(BaseModel):
    id: str
    title: str
    description: str
    company: str
    location: LocationResponse
    salary: SalaryResponse
    employment_type: EmploymentType
    posting_date: date | None
    company_type: str
    language: str


class PaginatedJobsResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class CatalogStatsResponse(BaseModel):
    total: int
    remote: int
    countries: int


class RejectedJobResponse(BaseModel):
    job_id: str
    title: str
    company: str
    reasons: list[str]


class IngestResponse(BaseModel):
    ingested: int
    ingestion_errors: int
    approved: int
    rejected: int


def format_salary(job: JobPosting) -> str:
    salary = job.salary
    is_usd = salary.currency.upper() == "USD"
    prefix = "$" if is_usd else ""
    suffix = "" if is_usd else f" {salary.currency.upper()}"
    if salary.period == SalaryPeriod.HOURLY:
        return f"{prefix}{salary.amount:,.2f}{suffix}/hr"
    return f"{prefix}{salary.amount:,.0f}{suffix}/yr"


def to_job_response(job: JobPosting) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        company=job.company,
        location=LocationResponse(
            city=job.location.city,
            state=job.location.state,
            country=job.location.country,
            is_remote=job.location.is_remote,
        ),
        salary=SalaryResponse(
            amount=job.salary.amount,
            currency=job.salary.currency,
            period=job.salary.period,
            display=format_salary(job),
        ),
        employment_type=job.employment_type,
        posting_date=job.posting_date,
        company_type=job.company_type,
        language=job.language,
    )
