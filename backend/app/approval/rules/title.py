from app.approval.base import RuleResult
from app.models.job import JobPosting


class TitleRule:
    name = "title"

    def evaluate(self, job: JobPosting) -> RuleResult:
        if job.title.strip():
            return RuleResult(passed=True)
        return RuleResult(passed=False, reason="Title must not be null or empty")
