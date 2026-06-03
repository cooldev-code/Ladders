from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.models.job import JobPosting


@dataclass(frozen=True)
class RuleResult:
    passed: bool
    reason: str | None = None


class ApprovalRule(Protocol):
    name: str

    def evaluate(self, job: JobPosting) -> RuleResult: ...


@dataclass
class ApprovalOutcome:
    job: JobPosting
    approved: bool
    reasons: list[str]
