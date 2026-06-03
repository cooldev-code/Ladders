from app.config import CURRENCY_TO_USD
from app.models.job import Salary, SalaryPeriod

HOURS_PER_YEAR = 2080


def convert_to_usd(amount: float, currency: str) -> float:
    rate = CURRENCY_TO_USD.get(currency.upper(), 0.0)
    return amount * rate


def annual_usd_equivalent(salary: Salary) -> float:
    usd = convert_to_usd(salary.amount, salary.currency)
    if salary.period == SalaryPeriod.HOURLY:
        return usd * HOURS_PER_YEAR
    return usd
