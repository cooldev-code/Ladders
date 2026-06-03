from __future__ import annotations

from app.approval.base import ApprovalOutcome, ApprovalRule
from app.models.job import JobPosting, RejectedJob


class ApprovalEngine:
    def __init__(self, rules: list[ApprovalRule]) -> None:
        self._rules = rules

    def evaluate(self, job: JobPosting) -> ApprovalOutcome:
        reasons: list[str] = []
        for rule in self._rules:
            result = rule.evaluate(job)
            if not result.passed and result.reason:
                reasons.append(result.reason)
        return ApprovalOutcome(job=job, approved=len(reasons) == 0, reasons=reasons)

    def process(self, jobs: list[JobPosting]) -> tuple[list[JobPosting], list[RejectedJob]]:
        approved: list[JobPosting] = []
        rejected: list[RejectedJob] = []
        for job in jobs:
            outcome = self.evaluate(job)
            if outcome.approved:
                approved.append(job)
            else:
                rejected.append(RejectedJob(job=job, reasons=outcome.reasons))
        return approved, rejected
