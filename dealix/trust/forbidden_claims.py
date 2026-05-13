"""Forbidden Claims — blocks unverifiable / non-compliant marketing language.

فلاتر الادعاءات الممنوعة — تمنع المبالغات وغير المتحقق منها قبل أي إرسال.
"""
from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict


_BANNED_AR = (
    "أفضل", "الأفضل", "الأقوى", "ضمان", "نضمن", "حصري", "الوحيد", "100%", "مجاني تمامًا",
    "ربح مضمون", "أرخص", "بدون مخاطر",
)
_BANNED_EN = (
    r"\bguarantee\w*\b", r"\bbest in (?:saudi|kingdom|region)\b",
    r"\b100%\s+(?:satisfaction|success|secure)\b", r"\brisk[- ]free\b",
    r"\bonly (?:provider|company|solution)\b", r"\bfree forever\b",
    r"\bunbeatable\b",
)

_BANNED_EN_RE = [re.compile(p, re.IGNORECASE) for p in _BANNED_EN]


class ClaimHit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: str
    pattern: str
    snippet: str


class ClaimsScan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    has_forbidden: bool
    hits: list[ClaimHit]


def scan_text(text: str) -> ClaimsScan:
    hits: list[ClaimHit] = []
    for word in _BANNED_AR:
        if word in text:
            hits.append(ClaimHit(language="ar", pattern=word, snippet=word))
    for rx in _BANNED_EN_RE:
        for m in rx.findall(text):
            hits.append(
                ClaimHit(
                    language="en",
                    pattern=rx.pattern,
                    snippet=str(m)[:80],
                )
            )
    return ClaimsScan(has_forbidden=bool(hits), hits=hits)


def assert_clean(text: str) -> None:
    """Raise ValueError if text contains a forbidden claim."""
    scan = scan_text(text)
    if scan.has_forbidden:
        raise ValueError(
            "forbidden_claim: " + ", ".join(h.pattern for h in scan.hits[:5])
        )
