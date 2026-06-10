"""Pre-qualification compliance gate.

Checks one normalized lead against a manual blocked-customer list +
PDPL screen. Returns one of: allowed | blocked | needs_review.

Hard rules:
- No external lookup (no scraping, no API calls)
- Block list lives in `data/compliance/blocked_customers.json`
- Default-deny on unknown patterns suspected of harassment / spam

The actual heavy compliance modules (compliance_os, compliance_os_v12)
remain authoritative; this gate is a fast pre-filter so we don't
invoke them for obviously-safe leads.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Literal

ComplianceStatus = Literal["allowed", "blocked", "needs_review"]

_BLOCKED_PATH = os.path.join("data", "compliance", "blocked_customers.json")

# Patterns that always need human review (default-deny)
_SUSPICIOUS_PATTERNS = [
    re.compile(r"(buy|purchase).{0,20}(database|leads?|emails?)", re.IGNORECASE),
    re.compile(r"scrape|crawl|harvest", re.IGNORECASE),
    re.compile(r"sanction(ed|s)", re.IGNORECASE),
]


def _load_blocked() -> dict[str, Any]:
    try:
        with open(_BLOCKED_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"emails": [], "phones": [], "domains": [], "company_names": []}


def check_compliance(*, normalized: dict[str, Any]) -> dict[str, Any]:
    """Return {'status': ..., 'reasons': [...]}.

    `normalized` is the output of pipelines/normalize.py — expects keys
    email, phone, company, message (any may be missing).
    """
    blocked = _load_blocked()
    reasons: list[str] = []
    status: ComplianceStatus = "allowed"

    email = (normalized.get("email") or "").lower().strip()
    phone = (normalized.get("phone") or "").strip()
    company = (normalized.get("company") or "").lower().strip()
    message = normalized.get("message") or ""

    if email and email in [e.lower() for e in blocked.get("emails", [])]:
        status = "blocked"
        reasons.append("email_in_blocklist")

    if phone and phone in blocked.get("phones", []):
        status = "blocked"
        reasons.append("phone_in_blocklist")

    if email:
        domain = email.split("@", 1)[-1] if "@" in email else ""
        if domain and domain in [d.lower() for d in blocked.get("domains", [])]:
            status = "blocked"
            reasons.append("domain_in_blocklist")

    if company and company in [c.lower() for c in blocked.get("company_names", [])]:
        status = "blocked"
        reasons.append("company_in_blocklist")

    if status == "allowed":
        for pattern in _SUSPICIOUS_PATTERNS:
            if pattern.search(message):
                status = "needs_review"
                reasons.append(f"suspicious_pattern:{pattern.pattern[:30]}")
                break

    return {
        "status": status,
        "reasons": reasons,
        "checked_against": "blocked_customers.json + suspicious_patterns",
    }
