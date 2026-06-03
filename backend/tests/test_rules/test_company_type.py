from app.approval.rules.company_type import CompanyTypeRule
from app.models.job import JobPosting


def test_direct_employer_passes():
    job = JobPosting(id="1", title="Eng", company_type="Direct Employer")
    assert CompanyTypeRule().evaluate(job).passed is True


def test_staffing_firm_fails():
    job = JobPosting(id="1", title="Eng", company_type="Staffing Firm")
    result = CompanyTypeRule().evaluate(job)
    assert result.passed is False
