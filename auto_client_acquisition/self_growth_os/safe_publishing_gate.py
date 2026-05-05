"""Safe publishing gate — the runtime side of the forbidden-claims sweep.

Wraps the same vocabulary used by:
  - scripts/verify_service_readiness_matrix.py
  - tests/test_landing_forbidden_claims.py
  - tests/test_no_guaranteed_claims.py

Use this gate before any draft (content, social, partner pitch,
proof snippet) is recorded to the approval queue. It returns a
``SafePublishingResult`` carrying the decision and the offending
tokens so the operator can rephrase.

This module never sends anything externally and never modifies the
input text.
"""
from __future__ import annotations

import re

from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    Language,
    PublishingDecision,
    RiskLevel,
    SafePublishingResult,
    ServiceBundle,
)

# Same patterns as the YAML validator + perimeter test.
FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("نضمن", re.compile(r"نضمن")),
    ("مضمون", re.compile(r"مضمون")),
    ("guaranteed", re.compile(r"\bguaranteed?\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscraping\b", re.IGNORECASE)),
    (
        "cold-channel",
        re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    ),
]


def _excerpt(text: str, match: re.Match, padding: int = 40) -> str:
    start = max(0, match.start() - padding)
    end = min(len(text), match.end() + padding)
    return ("…" if start > 0 else "") + text[start:end] + ("…" if end < len(text) else "")


def check_text(
    text: str,
    *,
    language: Language = Language.AR,
    bundle: ServiceBundle = ServiceBundle.UNKNOWN,
    target_persona: str = "founder",
    source: str = "self_growth_os.safe_publishing_gate",
) -> SafePublishingResult:
    """Score a single piece of copy against the forbidden vocabulary."""

    if not isinstance(text, str):
        raise TypeError("safe_publishing_gate.check_text requires a string")

    found: list[str] = []
    excerpts: list[str] = []
    for token, pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            found.append(token)
            excerpts.append(_excerpt(text, match))

    if not found:
        return SafePublishingResult.new(
            language=language,
            source=source,
            confidence=0.95,
            risk_level=RiskLevel.LOW,
            target_persona=target_persona,
            service_bundle=bundle,
            approval_status=ApprovalStatus.APPROVAL_REQUIRED,
            recommended_action=(
                "send to approval queue — no forbidden vocabulary detected"
            ),
            decision=PublishingDecision.ALLOWED_DRAFT,
            notes="No forbidden vocabulary detected; still requires human approval before any external send.",
        )

    return SafePublishingResult.new(
        language=language,
        source=source,
        confidence=0.99,
        risk_level=RiskLevel.BLOCKED,
        target_persona=target_persona,
        service_bundle=bundle,
        approval_status=ApprovalStatus.BLOCKED,
        recommended_action="rephrase before re-submission",
        decision=PublishingDecision.BLOCKED,
        forbidden_tokens_found=found,
        sample_excerpts=excerpts,
        notes=(
            "Forbidden marketing claims detected. Rephrase the highlighted "
            "passages and re-run the gate. Negation/disclaimer contexts may "
            "be acceptable but are decided per file by the founder, not by "
            "this runtime gate."
        ),
    )


def is_safe(text: str) -> bool:
    """Convenience boolean: True iff no forbidden token is present."""
    return check_text(text).decision == PublishingDecision.ALLOWED_DRAFT.value
