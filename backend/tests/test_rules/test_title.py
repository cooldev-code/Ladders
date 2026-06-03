from app.approval.rules.title import TitleRule
from app.models.job import JobPosting


def test_title_rule_passes():
    job = JobPosting(id="1", title="Engineer")
    assert TitleRule().evaluate(job).passed is True


def test_title_rule_rejects_empty():
    job = JobPosting(id="1", title="   ")
    result = TitleRule().evaluate(job)
    assert result.passed is False
    assert "empty" in result.reason.lower()
