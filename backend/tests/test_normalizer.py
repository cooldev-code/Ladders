from datetime import date

import pytest

from app.ingestion.normalizers import normalize_raw_job
from app.models.job import EmploymentType, SalaryPeriod


def test_structured_location_and_salary():
    raw = {
        "title": "Backend Engineer",
        "location": {"city": "Austin", "state": "TX", "country": "USA"},
        "salary": {"value": 145000, "currency": "USD"},
        "employment_type": "Full-Time",
        "posting_date": "2023-10-03",
        "remote": False,
    }
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.title == "Backend Engineer"
    assert job.location.city == "Austin"
    assert job.location.country == "USA"
    assert job.salary.amount == 145000
    assert job.salary.period == SalaryPeriod.ANNUAL
    assert job.employment_type == EmploymentType.FULL_TIME
    assert job.posting_date == date(2023, 10, 3)


def test_flat_location_string():
    raw = {
        "title": "Product Analyst",
        "location": "Boston, MA, USA",
        "salary": 120000,
        "employment_type": "Full-Time",
    }
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.location.city == "Boston"
    assert job.location.state == "MA"
    assert job.location.country == "USA"
    assert job.salary.amount == 120000
    assert job.salary.period == SalaryPeriod.ANNUAL


def test_remote_location_string():
    raw = {"title": "Writer", "location": "Remote", "salary": 90000}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.location.is_remote is True


def test_hourly_heuristic_for_bare_number():
    raw = {"title": "Data Scientist", "location": "Montreal, QC, Canada", "salary": 62.5}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.salary.period == SalaryPeriod.HOURLY
    assert job.salary.amount == 62.5


def test_hourly_object_salary():
    raw = {"title": "DevOps", "salary": {"value": 65, "currency": "USD", "unit": "hourly"}}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.salary.period == SalaryPeriod.HOURLY


def test_null_location_with_remote_flag():
    raw = {"title": "Support", "location": None, "remote": True, "salary": 50000}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.location.is_remote is True
    assert job.location.country == ""


def test_missing_language_defaults_empty():
    raw = {"title": "Dev", "language": "", "salary": 150000}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.language == ""


def test_empty_posting_date():
    raw = {"title": "Manager", "posting_date": "", "salary": 125000}
    job = normalize_raw_job(raw, 0, "feed_a.json")
    assert job.posting_date is None
