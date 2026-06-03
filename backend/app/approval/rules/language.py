from app.approval.base import RuleResult
from app.domain.location import is_us_or_canada
from app.models.job import JobPosting


class LanguageRule:
    name = "language"

    def evaluate(self, job: JobPosting) -> RuleResult:
        language = job.language.strip().lower()
        if not language:
            return RuleResult(
                passed=False,
                reason="Job description language must be specified",
            )
        if language == "english":
            return RuleResult(passed=True)
        if language == "french" and is_us_or_canada(job.location.country):
            return RuleResult(passed=True)
        return RuleResult(
            passed=False,
            reason=(
                "Job description must be in English "
                "(or French if the job is in Canada)"
            ),
        )
