from app.config import CANADA_COUNTRY_ALIASES, US_COUNTRY_ALIASES


def normalize_country(country: str) -> str:
    return country.strip().lower()


def is_us_or_canada(country: str) -> bool:
    normalized = normalize_country(country)
    if not normalized:
        return False
    return normalized in US_COUNTRY_ALIASES or normalized in CANADA_COUNTRY_ALIASES


def country_bucket(country: str) -> str:
    normalized = normalize_country(country)
    if normalized in US_COUNTRY_ALIASES:
        return "usa"
    if normalized in CANADA_COUNTRY_ALIASES:
        return "canada"
    return normalized
