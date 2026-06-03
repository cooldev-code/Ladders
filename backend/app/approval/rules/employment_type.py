from app.approval.base import RuleResult
from app.models.job import EmploymentType, JobPosting


class EmploymentTypeRule:
    name = "employment_type"

    def evaluate(self, job: JobPosting) -> RuleResult:
        if job.employment_type == EmploymentType.FULL_TIME:
            return RuleResult(passed=True)
        return RuleResult(
            passed=False,
            reason="Job must be a full-time position",
        )
