from app.approval.base import RuleResult
from app.models.job import JobPosting


class CompanyTypeRule:
    name = "company_type"

    def evaluate(self, job: JobPosting) -> RuleResult:
        if "staffing firm" in job.company_type.lower():
            return RuleResult(
                passed=False,
                reason="Job must not be from a staffing firm",
            )
        return RuleResult(passed=True)
