from app.approval.base import RuleResult
from app.config import CURRENCY_TO_USD, MIN_ANNUAL_SALARY_USD, MIN_HOURLY_SALARY_USD
from app.domain.salary import convert_to_usd
from app.models.job import JobPosting, SalaryPeriod


class SalaryRule:
    name = "salary"

    def evaluate(self, job: JobPosting) -> RuleResult:
        salary = job.salary
        currency = salary.currency.upper()
        if currency not in CURRENCY_TO_USD:
            return RuleResult(
                passed=False,
                reason=f"Unsupported salary currency: {currency}",
            )

        usd_amount = convert_to_usd(salary.amount, currency)
        if salary.period == SalaryPeriod.HOURLY:
            if usd_amount > MIN_HOURLY_SALARY_USD:
                return RuleResult(passed=True)
            return RuleResult(
                passed=False,
                reason=(
                    f"Hourly salary must exceed ${MIN_HOURLY_SALARY_USD}/hour USD "
                    f"(got ${usd_amount:.2f}/hour USD equivalent)"
                ),
            )

        if usd_amount > MIN_ANNUAL_SALARY_USD:
            return RuleResult(passed=True)
        return RuleResult(
            passed=False,
            reason=(
                f"Annual salary must exceed ${MIN_ANNUAL_SALARY_USD:,} USD "
                f"(got ${usd_amount:,.2f} USD equivalent)"
            ),
        )
