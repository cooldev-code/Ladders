from app.approval import ApprovalEngine, default_rules
from app.models.job import EmploymentType, JobPosting, Location, Salary, SalaryPeriod


def test_multiple_failures_aggregated():
    job = JobPosting(
        id="1",
        title="",
        employment_type=EmploymentType.INTERNSHIP,
        company_type="Staffing Firm",
        salary=Salary(amount=50000, currency="USD", period=SalaryPeriod.ANNUAL),
        language="",
        location=Location(country="Germany"),
    )
    outcome = ApprovalEngine(default_rules()).evaluate(job)
    assert outcome.approved is False
    assert len(outcome.reasons) >= 4
