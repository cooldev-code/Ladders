from app.approval.rules.salary import SalaryRule
from app.models.job import JobPosting, Salary, SalaryPeriod


def test_annual_above_threshold_passes():
    job = JobPosting(
        id="1",
        title="Eng",
        salary=Salary(amount=120000, currency="USD", period=SalaryPeriod.ANNUAL),
    )
    assert SalaryRule().evaluate(job).passed is True


def test_annual_below_threshold_fails():
    job = JobPosting(
        id="1",
        title="Eng",
        salary=Salary(amount=90000, currency="USD", period=SalaryPeriod.ANNUAL),
    )
    assert SalaryRule().evaluate(job).passed is False


def test_hourly_above_threshold_passes():
    job = JobPosting(
        id="1",
        title="Eng",
        salary=Salary(amount=62.5, currency="USD", period=SalaryPeriod.HOURLY),
    )
    assert SalaryRule().evaluate(job).passed is True


def test_hourly_below_threshold_fails():
    job = JobPosting(
        id="1",
        title="Eng",
        salary=Salary(amount=40, currency="USD", period=SalaryPeriod.HOURLY),
    )
    assert SalaryRule().evaluate(job).passed is False
