"""
Forbidden Claims scanner — extracted from scripts/forbidden_claims_audit.py
so it's reusable at runtime (draft generation, operator chat, proof_ledger
record).

Usage:
    from auto_client_acquisition.compliance.forbidden_claims import (
        scan, assert_safe, ForbiddenClaimError,
    )

    matches = scan("نضمن لك نتائج")
    # matches[0] is a ForbiddenMatch(claim="نضمن", line="نضمن لك نتائج", ...)

    assert_safe("نضمن لك نتائج")
    # raises ForbiddenClaimError

    assert_safe("✗ لا نضمن نتائج")
    # OK — negative-context marker present

The two constants (FORBIDDEN_CLAIMS + NEGATIVE_MARKERS) match the existing
landing audit (scripts/forbidden_claims_audit.py) so behavior is consistent.
Both code paths can import the same source eventually.
"""

from __future__ import annotations

from dataclasses import dataclass


# Forbidden marketing claims — case-insensitive match
FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "نضمن",
    "ضمان نتائج",
    "guaranteed results",
    "guaranteed revenue",
    "scrape",
    "scraping",
    "نسحب البيانات",
    "auto-dm",
    "auto dm",
    "رسائل آلية",
    "cold whatsapp",
    "واتساب بارد",
    "إرسال جماعي",
    "mass send",
    "100% automation",
    "أتمتة كاملة",
)


# Negative-context markers — if line contains one of these, the forbidden
# claim is documented avoidance (e.g., "لا نضمن نتائج") and allowed.
NEGATIVE_MARKERS: tuple[str, ...] = (
    "✗", "✘", "❌",
    " لا ", "لا أقدر", "لا نُرسل", "لا نسحب", "لا وعود", "لا نضمن",
    "لسنا", "نمنع", "يمنع", "ممنوع", "محظور",
    "بدون", "بلا", "دون", "غير",
    "يحرق", "يخالف",
    "يرفض", "يصدّ", "يحظر", "البديل الآمن",
    " no ", " not ", " never ", " without ", " forbids ", " prohibits ",
    " rejects ", " refuses ",
    "forbidden", "blocked", "anti-claim", "anti_claim",
)


class ForbiddenClaimError(ValueError):
    """Raised by assert_safe() when active (non-negated) forbidden claim found."""

    def __init__(self, claim: str, snippet: str):
        self.claim = claim
        self.snippet = snippet
        super().__init__(f"forbidden_claim_detected: {claim!r} in {snippet[:120]!r}")


@dataclass(frozen=True)
class ForbiddenMatch:
    claim: str
    line: str
    line_no: int
    is_negated: bool


def _has_negative_marker(text: str) -> bool:
    low = text.lower()
    return any(m.lower() in low for m in NEGATIVE_MARKERS)


def scan(text: str) -> list[ForbiddenMatch]:
    """Return all forbidden-claim matches in text. Each match flags whether
    the line containing it has a negation marker (is_negated=True means
    the claim is documented avoidance, not active marketing)."""
    if not text:
        return []
    out: list[ForbiddenMatch] = []
    for ln_no, line in enumerate(text.splitlines() or [text], start=1):
        low = line.lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim.lower() in low:
                out.append(ForbiddenMatch(
                    claim=claim,
                    line=line.strip(),
                    line_no=ln_no,
                    is_negated=_has_negative_marker(line),
                ))
    return out


def assert_safe(text: str) -> None:
    """Raise ForbiddenClaimError if any active (non-negated) forbidden
    claim is present. No-op if all matches are negated or text is empty.
    """
    if not text:
        return
    for m in scan(text):
        if not m.is_negated:
            raise ForbiddenClaimError(m.claim, m.line)


def is_safe(text: str) -> bool:
    """Boolean variant of assert_safe — for callers that don't want to handle exceptions."""
    try:
        assert_safe(text)
        return True
    except ForbiddenClaimError:
        return False
