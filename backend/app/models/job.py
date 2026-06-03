from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class SalaryPeriod(str, Enum):
    ANNUAL = "annual"
    HOURLY = "hourly"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    OTHER = "other"


class Location(BaseModel):
    city: str = ""
    state: str = ""
    country: str = ""
    is_remote: bool = False


class Salary(BaseModel):
    amount: float
    currency: str = "USD"
    period: SalaryPeriod = SalaryPeriod.ANNUAL


class JobPosting(BaseModel):
    id: str
    title: str = ""
    description: str = ""
    company: str = ""
    location: Location = Field(default_factory=Location)
    salary: Salary = Field(default_factory=lambda: Salary(amount=0.0))
    employment_type: EmploymentType = EmploymentType.OTHER
    posting_date: date | None = None
    company_type: str = ""
    language: str = ""
    source_index: int = 0
    source_feed: str = ""


class RejectedJob(BaseModel):
    job: JobPosting
    reasons: list[str]
