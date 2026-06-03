import pytest
from fastapi.testclient import TestClient

from app.domain.salary import convert_to_usd
from app.main import app
from app.models.job import SalaryPeriod


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def fetch_all_jobs(client, **params):
    response = client.get("/api/jobs", params={"page_size": 100, **params})
    assert response.status_code == 200
    return response.json()


def effective_salary(job):
    usd = convert_to_usd(job["salary"]["amount"], job["salary"]["currency"])
    if job["salary"]["period"] == SalaryPeriod.HOURLY:
        return usd * 2080
    return usd


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_jobs_returns_approved_only(client):
    payload = fetch_all_jobs(client)
    assert payload["total"] == 11
    titles = {job["title"] for job in payload["items"]}
    assert "Backend Engineer" in titles
    assert "Frontend Developer Intern" not in titles


def test_search_jobs_by_title(client):
    jobs = fetch_all_jobs(client, q="engineer")["items"]
    assert all("engineer" in job["title"].lower() for job in jobs)
    assert len(jobs) >= 1


def test_filter_jobs_by_country(client):
    jobs = fetch_all_jobs(client, country="Canada")["items"]
    assert len(jobs) >= 1
    assert all(job["location"]["country"] == "Canada" for job in jobs)


def test_sort_jobs_by_salary(client):
    jobs = fetch_all_jobs(client, sort_by="salary", order="desc")["items"]
    salaries = [effective_salary(job) for job in jobs]
    assert salaries == sorted(salaries, reverse=True)


def test_pagination_splits_results_and_reports_meta(client):
    first = client.get("/api/jobs", params={"page": 1, "page_size": 5}).json()
    assert first["page"] == 1
    assert first["page_size"] == 5
    assert first["total"] == 11
    assert first["total_pages"] == 3
    assert first["has_prev"] is False
    assert first["has_next"] is True
    assert len(first["items"]) == 5

    last = client.get("/api/jobs", params={"page": 3, "page_size": 5}).json()
    assert last["has_next"] is False
    assert last["has_prev"] is True
    assert len(last["items"]) == 1

    first_ids = {job["id"] for job in first["items"]}
    last_ids = {job["id"] for job in last["items"]}
    assert first_ids.isdisjoint(last_ids)


def test_pagination_rejects_invalid_page(client):
    response = client.get("/api/jobs", params={"page": 0})
    assert response.status_code == 422


def test_catalog_stats_endpoint(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 11
    assert stats["remote"] >= 1
    assert stats["countries"] >= 1


def test_rejected_admin_endpoint(client):
    response = client.get("/api/admin/rejected")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_ingest_endpoint(client):
    response = client.post("/api/admin/ingest")
    assert response.status_code == 200
    payload = response.json()
    assert payload["approved"] == 11
    assert payload["rejected"] == 9
