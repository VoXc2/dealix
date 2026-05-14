"""Claim safety — deterministic scan for misrepresentation / forbidden marketing claims."""

from __future__ import annotations

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


def contains_unsafe_claim(text: str) -> tuple[bool, list[str]]:
    """Boolean + reasons variant used by the runtime governance authority.

    Returns ``(True, [reasons...])`` whenever ``audit_claim_safety`` raises
    any flagged claim — both forbidden-claim hits and operational issues —
    so the caller can decide to REDACT / DRAFT_ONLY / BLOCK accordingly.
    """
    result = audit_claim_safety(text)
    return bool(result.issues), list(result.issues)


__all__ = ["ClaimSafetyResult", "audit_claim_safety", "contains_unsafe_claim"]
