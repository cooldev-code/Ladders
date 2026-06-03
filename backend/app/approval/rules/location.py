from app.approval.base import RuleResult
from app.domain.location import is_us_or_canada
from app.models.job import JobPosting


class LocationRule:
    name = "location"

    def evaluate(self, job: JobPosting) -> RuleResult:
        if job.location.is_remote:
            return RuleResult(passed=True)
        if is_us_or_canada(job.location.country):
            return RuleResult(passed=True)
        return RuleResult(
            passed=False,
            reason=(
                "Job must be remote or located within the United States or Canada"
            ),
        )
