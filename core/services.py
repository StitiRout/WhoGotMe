import re

from .models import Breach, EmailCheck

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

SEVERITY_WEIGHTS = {
    "critical": 40,
    "high": 25,
    "medium": 15,
    "low": 8,
}


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))


def mask_email(email: str) -> str:
    user, _, domain = email.partition("@")
    if not domain:
        return email
    masked = user[:2] + "•" * max(len(user) - 2, 3)
    return f"{masked}@{domain}"


def get_risk_label(score: int) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MEDIUM"
    return "LOW"


def calculate_risk_score(records: list[Breach]) -> int:
    if not records:
        return 8
    score = sum(SEVERITY_WEIGHTS.get(r.severity.lower(), 10) for r in records)
    return min(score, 99)


def _parse_data_types(data_exposed: str) -> list[str]:
    return [part.strip() for part in data_exposed.split(",") if part.strip()]


def check_email(email: str, ip_address: str | None = None) -> dict:
    """Look up email in the breaches table and return results."""
    normalized = email.strip().lower()

    records = list(Breach.objects.filter(email__iexact=normalized).order_by("-breach_date"))
    is_clean = len(records) == 0
    risk_score = 8 if is_clean else calculate_risk_score(records)

    EmailCheck.objects.create(
        email=normalized,
        is_clean=is_clean,
        risk_score=risk_score,
        breach_count=len(records),
        ip_address=ip_address,
    )

    breach_data = [
        {
            "name": record.breach_name,
            "date": record.breach_date.isoformat(),
            "records": "—",
            "severity": record.severity.lower(),
            "dataTypes": _parse_data_types(record.data_exposed),
            "description": record.description,
        }
        for record in records
    ]

    return {
        "email": normalized,
        "maskedEmail": mask_email(normalized),
        "isClean": is_clean,
        "riskScore": risk_score,
        "riskLabel": get_risk_label(risk_score),
        "breaches": breach_data,
        "breachCount": len(breach_data),
    }
