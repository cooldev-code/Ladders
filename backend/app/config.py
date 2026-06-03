import os
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_project_root() -> Path:
    candidates = (
        _BACKEND_ROOT,
        _REPO_ROOT,
        _BACKEND_ROOT.parent,
        Path.cwd(),
    )
    for candidate in candidates:
        if (candidate / "data" / "feeds").is_dir():
            return candidate
    return _BACKEND_ROOT


def _resolve_rejected_jobs_log(project_root: Path) -> Path:
    if os.getenv("VERCEL"):
        return Path("/tmp/rejected_jobs.jsonl")
    return project_root / "data" / "rejected_jobs.jsonl"


PROJECT_ROOT = _resolve_project_root()
FEEDS_DIR = PROJECT_ROOT / "data" / "feeds"
REJECTED_JOBS_LOG = _resolve_rejected_jobs_log(PROJECT_ROOT)
# Vercel Services mount this app at routePrefix "/api" and strip that prefix
# before the request reaches FastAPI. Local dev keeps the "/api" path on the app.
API_PREFIX = "" if os.getenv("VERCEL") else "/api"
# Static USD conversion rates (mock rates for salary normalization).
CURRENCY_TO_USD: dict[str, float] = {
    "USD": 1.0,
    "CAD": 0.74,
    "GBP": 1.27,
    "EUR": 1.09,
}

MIN_ANNUAL_SALARY_USD = 100_000
MIN_HOURLY_SALARY_USD = 45
HOURLY_SALARY_HEURISTIC_THRESHOLD = 500

US_COUNTRY_ALIASES = frozenset({"usa", "us", "united states", "united states of america"})
CANADA_COUNTRY_ALIASES = frozenset({"canada", "ca"})
