"""Claim safety — deterministic scan for misrepresentation / forbidden marketing claims."""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text


@dataclass(frozen=True, slots=True)
class ClaimSafetyResult:
    """Structured outcome for client-facing or outbound-bound copy."""

    issues: tuple[str, ...]
    suggested_decision: GovernanceDecision


def audit_claim_safety(text: str) -> ClaimSafetyResult:
    """
    Map ``audit_draft_text`` issues to a single suggested governance decision.

    - Forbidden *claims* (guarantees, fake proof) → BLOCK
    - Forbidden operational terms (scraping, auto-send, …) → DRAFT_ONLY / review path
    """
    raw = audit_draft_text(text)
    issues = tuple(dict.fromkeys(raw))
    claim_hits = [i for i in issues if i.startswith("forbidden_claim:")]
    if claim_hits:
        return ClaimSafetyResult(issues, GovernanceDecision.BLOCK)
    if issues:
        return ClaimSafetyResult(issues, GovernanceDecision.DRAFT_ONLY)
    return ClaimSafetyResult((), GovernanceDecision.ALLOW)


# Forbidden guarantee / unsupported-outcome patterns (bilingual).
FORBIDDEN_CLAIM_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bguarantee[ds]?\b", "guarantee language"),
    (r"\bguaranteed\s+(sales|revenue|leads|deals)\b", "guaranteed business outcome"),
    (r"\b100\s*%\s*(success|guaranteed|certain)\b", "100% outcome claim"),
    (r"\brisk[- ]free\s+(sales|revenue|outcome)\b", "risk-free outcome claim"),
    (r"\bzero[- ]?risk\b", "zero-risk claim"),
    (r"نضمن", "ضمان عربي"),
    (r"مضمون(ة|ون)?\s*(المبيعات|الإيراد|العملاء)?", "ضمان نتيجة عربي"),
    (r"١٠٠\s*%\s*(ضمان|نجاح|مؤكد)", "ادعاء ١٠٠٪"),
    (r"بدون\s+مخاطر", "ادعاء بدون مخاطر"),
)


def contains_unsafe_claim(text: str) -> tuple[bool, list[str]]:
    """Returns (has_unsafe, reasons). Empty reasons list iff clean."""
    if not text:
        return False, []
    reasons: list[str] = []
    for pattern, label in FORBIDDEN_CLAIM_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            reasons.append(label)
    return bool(reasons), reasons


__all__ = [
    "FORBIDDEN_CLAIM_PATTERNS",
    "ClaimSafetyResult",
    "audit_claim_safety",
    "contains_unsafe_claim",
]
