"""Hard gates for Growth Beast — aligned with compliance_action blocks."""

from __future__ import annotations

import re
from typing import Any

_BLOCKED_PHRASES = (
    "auto_send",
    "live_send",
    "auto_charge",
    "cold whatsapp",
    "scraping",
    "scrape ",
    "linkedin automation",
    "ضمان مبيعات",
    "guaranteed revenue",
    "guaranteed leads",
)

_SENSITIVE_SECTOR_MARKERS = ("health", "طبي", "medical", "bank", "بنك", "finance regulated")


def _contains_blocked(text: str) -> str | None:
    low = text.lower()
    for p in _BLOCKED_PHRASES:
        if p in low:
            return p
    return None


def assess_text_safety(text: str) -> dict[str, Any]:
    hit = _contains_blocked(text)
    if hit:
        return {"safe": False, "reason": f"blocked_phrase:{hit}", "action_mode": "blocked"}
    return {"safe": True, "reason": "ok", "action_mode": "draft_only"}


def sector_requires_escalation(sector: str) -> bool:
    s = (sector or "").lower()
    return any(m in s for m in _SENSITIVE_SECTOR_MARKERS)


def redact_free_text(text: str, max_len: int = 400) -> str:
    """Strip email/phone-like patterns from support-derived summaries."""
    t = (text or "").strip()
    if len(t) > max_len:
        t = t[:max_len] + "…"
    t = re.sub(r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "[redacted_email]", t)
    t = re.sub(r"(\+966|05|5)\d{8,9}", "[redacted_phone]", t)
    return t
