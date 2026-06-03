from datetime import date

from app.models.job import JobPosting, Location, Salary, SalaryPeriod
from app.storage.query import JobQueryService, SortField, SortOrder


def make_job(
    job_id: str,
    title: str,
    country: str,
    amount: float,
    posting_date: date | None,
) -> JobPosting:
    return JobPosting(
        id=job_id,
        title=title,
        location=Location(country=country),
        salary=Salary(amount=amount, currency="USD", period=SalaryPeriod.ANNUAL),
        posting_date=posting_date,
    )


def test_search_by_title():
    jobs = [
        make_job("1", "Backend Engineer", "USA", 120000, date(2023, 10, 1)),
        make_job("2", "Product Analyst", "USA", 110000, date(2023, 10, 2)),
    ]
    results = JobQueryService().search(jobs, query="engineer")
    assert len(results) == 1
    assert results[0].title == "Backend Engineer"


def test_filter_by_country():
    jobs = [
        make_job("1", "A", "USA", 120000, None),
        make_job("2", "B", "Canada", 120000, None),
    ]
    results = JobQueryService().search(jobs, country="Canada")
    assert len(results) == 1
    assert results[0].title == "B"


def test_sort_by_salary_desc():
    jobs = [
        make_job("1", "Low", "USA", 110000, None),
        make_job("2", "High", "USA", 150000, None),
    ]
    results = JobQueryService().search(jobs, sort_by=SortField.SALARY, order=SortOrder.DESC)
    assert results[0].title == "High"


def test_sort_by_posting_date_nulls_last():
    jobs = [
        make_job("1", "NoDate", "USA", 120000, None),
        make_job("2", "Old", "USA", 120000, date(2023, 10, 1)),
        make_job("3", "New", "USA", 120000, date(2023, 10, 10)),
    ]
    results = JobQueryService().search(
        jobs,
        sort_by=SortField.POSTING_DATE,
        order=SortOrder.DESC,
    )
    assert results[0].title == "New"
    assert results[-1].title == "NoDate"
