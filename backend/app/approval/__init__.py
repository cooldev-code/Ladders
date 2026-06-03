from app.approval.base import ApprovalRule, ApprovalOutcome, RuleResult
from app.approval.engine import ApprovalEngine
from app.approval.rules.company_type import CompanyTypeRule
from app.approval.rules.employment_type import EmploymentTypeRule
from app.approval.rules.language import LanguageRule
from app.approval.rules.location import LocationRule
from app.approval.rules.salary import SalaryRule
from app.approval.rules.title import TitleRule

__all__ = [
    "ApprovalEngine",
    "ApprovalOutcome",
    "ApprovalRule",
    "RuleResult",
    "CompanyTypeRule",
    "EmploymentTypeRule",
    "LanguageRule",
    "LocationRule",
    "SalaryRule",
    "TitleRule",
]


def default_rules() -> list[ApprovalRule]:
    return [
        TitleRule(),
        LocationRule(),
        EmploymentTypeRule(),
        SalaryRule(),
        CompanyTypeRule(),
        LanguageRule(),
    ]
