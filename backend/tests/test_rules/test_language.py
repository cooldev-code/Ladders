from app.approval.rules.language import LanguageRule
from app.models.job import JobPosting, Location


def test_english_passes():
    job = JobPosting(id="1", title="Eng", language="English")
    assert LanguageRule().evaluate(job).passed is True


def test_french_in_canada_passes():
    job = JobPosting(
        id="1",
        title="Eng",
        language="French",
        location=Location(country="Canada"),
    )
    assert LanguageRule().evaluate(job).passed is True


def test_french_outside_canada_fails():
    job = JobPosting(
        id="1",
        title="Eng",
        language="French",
        location=Location(country="France"),
    )
    assert LanguageRule().evaluate(job).passed is False


def test_empty_language_fails():
    job = JobPosting(id="1", title="Eng", language="")
    assert LanguageRule().evaluate(job).passed is False
