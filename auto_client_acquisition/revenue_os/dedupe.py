"""Dedupe hints — normalization + fingerprint suggestion (pure)."""

from __future__ import annotations

import re
from dataclasses import dataclass

_AR_STOPWORDS = frozenset(
    {
        "شركة",
        "شريك",
        "شركةالمحدودة",
        "مساهمة",
        "مقفلة",
        "ذات",
        "مسؤولية",
        "محدودة",
        "قابضة",
    }
)


def normalize_company_name(name: str) -> str:
    """Normalize Arabic/Latin company names for loose matching."""
    s = name.strip().lower()
    s = re.sub(r"[ًٌٍَُِّْ،؛]+", "", s)
    s = re.sub(r"\s+", " ", s)
    parts = [p for p in s.split() if p not in _AR_STOPWORDS and len(p) > 1]
    return " ".join(parts) if parts else s


def normalize_phone_e164_hint(phone: str | None) -> str | None:
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("966"):
        return digits
    if digits.startswith("0") and len(digits) >= 9:
        return "966" + digits.lstrip("0")
    return digits or None


def normalize_domain(url_or_domain: str | None) -> str | None:
    if not url_or_domain:
        return None
    s = url_or_domain.strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = s.split("/")[0].removeprefix("www.")
    return s or None


@dataclass
class DedupeHint:
    fingerprint_key: str
    normalized_company: str
    domain: str | None
    phone_hint: str | None
    merge_safe: bool
    notes: list[str]


def suggest_dedupe_fingerprint(
    *,
    company_name: str,
    domain: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    external_crm_id: str | None = None,
) -> DedupeHint:
    """Return a deterministic hint key; caller persists merge decision."""
    notes: list[str] = []
    nc = normalize_company_name(company_name)
    dom = normalize_domain(domain)
    ph = normalize_phone_e164_hint(phone)
    email_dom = None
    if email and "@" in email:
        email_dom = email.split("@", 1)[1].strip().lower()

    parts: list[str] = []
    if external_crm_id:
        parts.append(f"crm:{external_crm_id}")
        notes.append("crm_id_primary")
    elif dom:
        parts.append(f"domain:{dom}")
    elif email_dom:
        parts.append(f"email_domain:{email_dom}")
    if ph:
        parts.append(f"phone:{ph}")
    parts.append(f"name:{nc}")

    key = "|".join(parts)
    merge_safe = bool(dom or external_crm_id or ph)
    return DedupeHint(
        fingerprint_key=key,
        normalized_company=nc,
        domain=dom,
        phone_hint=ph,
        merge_safe=merge_safe,
        notes=notes,
    )
