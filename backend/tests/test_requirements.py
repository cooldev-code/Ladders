"""End-to-end requirement coverage mapped to the take-home specification."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.approval import ApprovalEngine, default_rules
from app.config import FEEDS_DIR
from app.domain.salary import annual_usd_equivalent, convert_to_usd
from app.ingestion.service import ingest_feeds
from app.main import app
from app.models.job import EmploymentType, JobPosting, Location, Salary, SalaryPeriod
from app.pipeline import JobPipeline
from app.storage.query import JobQueryService, SortField, SortOrder
from app.storage.repository import ApprovedJobRepository, RejectionLogger

EXPECTED_APPROVED_TITLES = {
    "Backend Engineer",
    "Machine Learning Engineer",
    "Agile Project Lead",
    "Senior Software Engineer",
    "Data Scientist",
    "QA Automation Engineer",
    "UX Designer",
    "Product Analyst",
    "Cybersecurity Specialist",
    "Growth Marketing Manager",
    "Customer Success Manager",
}


@pytest.fixture
def pipeline_result(tmp_path):
    repo = ApprovedJobRepository()
    logger = RejectionLogger(tmp_path / "rejected.jsonl")
    pipeline = JobPipeline(repo, logger, feeds_dir=FEEDS_DIR)
    return pipeline.run()


class TestDataModeling:
    def test_job_posting_has_required_fields(self):
        job = JobPosting(
            id="feed:0",
            title="Engineer",
            description="Build APIs",
            company="Acme",
            location=Location(city="Austin", state="TX", country="USA"),
            salary=Salary(amount=120000, currency="USD", period=SalaryPeriod.ANNUAL),
            employment_type=EmploymentType.FULL_TIME,
            posting_date=None,
            company_type="Direct Employer",
            language="English",
            source_index=0,
        )
        assert job.location.country == "USA"
        assert job.salary.period == SalaryPeriod.ANNUAL


class TestIngestion:
    def test_reads_all_feed_files(self):
        feeds = list(FEEDS_DIR.glob("*.json"))
        assert feeds, "At least one feed file is required"

    def test_ingests_multiple_jobs_from_mixed_formats(self):
        result = ingest_feeds(FEEDS_DIR)
        assert len(result.jobs) == 20
        assert result.errors == []

    def test_handles_invalid_record_without_crashing_batch(self, tmp_path):
        feed = tmp_path / "bad_feed.json"
        feed.write_text(
            json.dumps([{"title": "Valid", "salary": 150000}, "not-an-object"]),
            encoding="utf-8",
        )
        result = ingest_feeds(tmp_path)
        assert len(result.jobs) == 1
        assert len(result.errors) == 1


class TestApprovalCriteria:
    @pytest.mark.parametrize(
        ("title", "snippet"),
        [
            ("Frontend Developer Intern", "full-time"),
            ("Junior Developer", "staffing firm"),
            ("Project Manager", "salary"),
            ("Mobile Engineer", "English"),
            ("Technical Writer", "full-time"),
            ("Database Administrator", "staffing firm"),
            ("Business Operations Associate", "salary"),
            ("DevOps Consultant", "full-time"),
        ],
    )
    def test_sample_rejections_include_expected_reason(
        self, pipeline_result, title, snippet
    ):
        rejected = {
            entry.job.title: entry.reasons for entry in pipeline_result.rejected
        }
        key = title if title else ""
        if not key:
            rejected_by_title = next(
                (entry for entry in pipeline_result.rejected if not entry.job.title.strip()),
                None,
            )
            assert rejected_by_title is not None
            assert any(snippet.lower() in reason.lower() for reason in rejected_by_title.reasons)
            return
        assert key in rejected
        assert any(snippet.lower() in reason.lower() for reason in rejected[key])

    def test_approved_jobs_meet_all_rules(self, pipeline_result):
        engine = ApprovalEngine(default_rules())
        for job in pipeline_result.approved:
            outcome = engine.evaluate(job)
            assert outcome.approved, f"{job.title} should pass all rules: {outcome.reasons}"


class TestStorageAndLogging:
    def test_approved_jobs_stored_for_search(self, pipeline_result, tmp_path):
        repo = ApprovedJobRepository()
        logger = RejectionLogger(tmp_path / "rejected.jsonl")
        pipeline = JobPipeline(repo, logger, feeds_dir=FEEDS_DIR)
        pipeline.run()

        stored = repo.list_all()
        assert len(stored) == 11
        assert {job.title for job in stored} == EXPECTED_APPROVED_TITLES

    def test_rejected_jobs_logged_with_reasons(self, pipeline_result, tmp_path):
        log_path = tmp_path / "rejected.jsonl"
        logger = RejectionLogger(log_path)
        logger.log_all(pipeline_result.rejected)

        lines = log_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 9
        first = json.loads(lines[0])
        assert "reasons" in first
        assert first["reasons"]


class TestSearchExperience:
    def test_search_filter_and_sort(self, pipeline_result):
        jobs = pipeline_result.approved
        service = JobQueryService()

        engineers = service.search(jobs, query="engineer")
        assert engineers
        assert all("engineer" in job.title.lower() for job in engineers)

        canada = service.search(jobs, country="Canada")
        assert canada
        assert all(job.location.country == "Canada" for job in canada)

        by_salary = service.search(
            jobs, sort_by=SortField.SALARY, order=SortOrder.DESC
        )
        salaries = [annual_usd_equivalent(job.salary) for job in by_salary]
        assert salaries == sorted(salaries, reverse=True)

        by_date = service.search(
            jobs, sort_by=SortField.POSTING_DATE, order=SortOrder.DESC
        )
        dated = [job for job in by_date if job.posting_date]
        undated = [job for job in by_date if not job.posting_date]
        assert by_date == dated + undated


class TestApiUx:
    @pytest.fixture
    def client(self):
        with TestClient(app) as test_client:
            yield test_client

    def test_jobs_endpoint_supports_search_filter_sort(self, client):
        search = client.get("/api/jobs", params={"q": "engineer", "page_size": 100})
        assert search.status_code == 200
        assert search.json()["items"]

        filtered = client.get(
            "/api/jobs", params={"country": "USA", "page_size": 100}
        )
        assert filtered.status_code == 200
        assert all(
            job["location"]["country"] == "USA" for job in filtered.json()["items"]
        )

        sorted_resp = client.get(
            "/api/jobs",
            params={"sort_by": "salary", "order": "desc", "page_size": 100},
        )
        assert sorted_resp.status_code == 200
        amounts = [
            annual_usd_equivalent_from_response(job)
            for job in sorted_resp.json()["items"]
        ]
        assert amounts == sorted(amounts, reverse=True)

    def test_jobs_endpoint_paginates(self, client):
        payload = client.get("/api/jobs", params={"page": 1, "page_size": 5}).json()
        assert payload["total"] == 11
        assert payload["total_pages"] == 3
        assert len(payload["items"]) == 5

    def test_job_detail_endpoint(self, client):
        listing = client.get("/api/jobs")
        job_id = listing.json()["items"][0]["id"]
        detail = client.get(f"/api/jobs/{job_id}")
        assert detail.status_code == 200
        assert detail.json()["id"] == job_id

    def test_rejected_jobs_reviewable(self, client):
        response = client.get("/api/admin/rejected")
        assert response.status_code == 200
        assert len(response.json()) == 9


def annual_usd_equivalent_from_response(job: dict) -> float:
    salary = job["salary"]
    usd = convert_to_usd(salary["amount"], salary["currency"])
    if salary["period"] == SalaryPeriod.HOURLY:
        return usd * 2080
    return usd
