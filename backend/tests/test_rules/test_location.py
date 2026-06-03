import pytest

from app.domain.location import is_us_or_canada
from app.approval.rules.location import LocationRule
from app.models.job import JobPosting, Location


def test_remote_passes():
    job = JobPosting(id="1", title="PM", location=Location(is_remote=True, country="UK"))
    assert LocationRule().evaluate(job).passed is True


def test_us_location_passes():
    job = JobPosting(id="1", title="Eng", location=Location(country="USA"))
    assert LocationRule().evaluate(job).passed is True


def test_canada_location_passes():
    job = JobPosting(id="1", title="Eng", location=Location(country="Canada"))
    assert LocationRule().evaluate(job).passed is True


def test_non_us_ca_in_person_fails():
    job = JobPosting(id="1", title="Eng", location=Location(country="Germany"))
    result = LocationRule().evaluate(job)
    assert result.passed is False


@pytest.mark.parametrize(
    "country",
    ["USA", "US", "United States", "Canada"],
)
def test_country_aliases(country):
    assert is_us_or_canada(country) is True
