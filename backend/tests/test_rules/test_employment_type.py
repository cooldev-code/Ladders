from app.approval.rules.employment_type import EmploymentTypeRule
from app.models.job import EmploymentType, JobPosting


def test_full_time_passes():
    job = JobPosting(id="1", title="Eng", employment_type=EmploymentType.FULL_TIME)
    assert EmploymentTypeRule().evaluate(job).passed is True


def test_contract_fails():
    job = JobPosting(id="1", title="Eng", employment_type=EmploymentType.CONTRACT)
    result = EmploymentTypeRule().evaluate(job)
    assert result.passed is False
