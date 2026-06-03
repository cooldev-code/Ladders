from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_project_root() -> Path:
    for candidate in (_REPO_ROOT, _BACKEND_ROOT):
        if (candidate / "data" / "feeds").is_dir():
            return candidate
    return _REPO_ROOT


PROJECT_ROOT = _resolve_project_root()
FEEDS_DIR = PROJECT_ROOT / "data" / "feeds"
REJECTED_JOBS_LOG = PROJECT_ROOT / "data" / "rejected_jobs.jsonl"

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
