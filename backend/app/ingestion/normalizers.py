from __future__ import annotations

from datetime import date
from typing import Any

from app.config import HOURLY_SALARY_HEURISTIC_THRESHOLD
from app.models.job import EmploymentType, JobPosting, Location, Salary, SalaryPeriod


def parse_employment_type(raw: Any) -> EmploymentType:
    if raw is None:
        return EmploymentType.OTHER
    normalized = str(raw).strip().lower().replace("-", " ").replace("_", " ")
    mapping = {
        "full time": EmploymentType.FULL_TIME,
        "part time": EmploymentType.PART_TIME,
        "contract": EmploymentType.CONTRACT,
        "internship": EmploymentType.INTERNSHIP,
    }
    return mapping.get(normalized, EmploymentType.OTHER)


def parse_posting_date(raw: Any) -> date | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def parse_location(raw: Any, remote_flag: bool) -> Location:
    is_remote = bool(remote_flag)
    if raw is None:
        return Location(is_remote=is_remote)
    if isinstance(raw, dict):
        return Location(
            city=str(raw.get("city") or "").strip(),
            state=str(raw.get("state") or "").strip(),
            country=str(raw.get("country") or "").strip(),
            is_remote=is_remote,
        )
    if isinstance(raw, str):
        text = raw.strip()
        if text.lower() == "remote":
            return Location(is_remote=True)
        parts = [part.strip() for part in text.split(",") if part.strip()]
        if not parts:
            return Location(is_remote=is_remote)
        country = parts[-1]
        state = parts[-2] if len(parts) >= 2 else ""
        city = parts[0] if len(parts) >= 3 else (parts[0] if len(parts) == 1 else "")
        if len(parts) == 2:
            city = parts[0]
            state = ""
        return Location(city=city, state=state, country=country, is_remote=is_remote)
    return Location(is_remote=is_remote)


def parse_salary(raw: Any) -> Salary:
    if raw is None:
        return Salary(amount=0.0)
    if isinstance(raw, (int, float)):
        amount = float(raw)
        period = (
            SalaryPeriod.HOURLY
            if amount <= HOURLY_SALARY_HEURISTIC_THRESHOLD
            else SalaryPeriod.ANNUAL
        )
        return Salary(amount=amount, currency="USD", period=period)
    if isinstance(raw, dict):
        amount = float(raw.get("value") or 0)
        currency = str(raw.get("currency") or "USD").strip().upper() or "USD"
        unit = str(raw.get("unit") or "").strip().lower()
        if unit == "hourly":
            period = SalaryPeriod.HOURLY
        elif unit in {"annual", "yearly", "year"}:
            period = SalaryPeriod.ANNUAL
        else:
            period = (
                SalaryPeriod.HOURLY
                if amount <= HOURLY_SALARY_HEURISTIC_THRESHOLD
                else SalaryPeriod.ANNUAL
            )
        return Salary(amount=amount, currency=currency, period=period)
    return Salary(amount=0.0)


def normalize_raw_job(raw: dict[str, Any], index: int, feed_name: str = "") -> JobPosting:
    remote_flag = bool(raw.get("remote", False))
    location = parse_location(raw.get("location"), remote_flag)
    job_id = f"{feed_name}:{index}" if feed_name else str(index)

    return JobPosting(
        id=job_id,
        title=str(raw.get("title") or ""),
        description=str(raw.get("description") or ""),
        company=str(raw.get("company") or ""),
        location=location,
        salary=parse_salary(raw.get("salary")),
        employment_type=parse_employment_type(raw.get("employment_type")),
        posting_date=parse_posting_date(raw.get("posting_date")),
        company_type=str(raw.get("company_type") or ""),
        language=str(raw.get("language") or "").strip(),
        source_index=index,
        source_feed=feed_name,
    )
