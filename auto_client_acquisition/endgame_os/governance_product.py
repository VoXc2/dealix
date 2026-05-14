"""Governance Runtime as product — components and decision vocabulary."""

from __future__ import annotations

from enum import StrEnum

GOVERNANCE_RUNTIME_COMPONENTS: tuple[str, ...] = (
    "policy_engine",
    "pii_detection",
    "allowed_use_checker",
    "claim_safety_checker",
    "channel_risk_checker",
    "approval_engine",
    "audit_log",
    "ai_run_ledger",
    "risk_index",
    "escalation_rules",
)


class GovernanceDecision(StrEnum):
    ALLOW = "ALLOW"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    DRAFT_ONLY = "DRAFT_ONLY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


def governance_runtime_maturity_score(components_implemented: frozenset[str]) -> int:
    """0–100 based on share of required components present."""
    if not GOVERNANCE_RUNTIME_COMPONENTS:
        return 0
    present = sum(1 for c in GOVERNANCE_RUNTIME_COMPONENTS if c in components_implemented)
    return (present * 100) // len(GOVERNANCE_RUNTIME_COMPONENTS)
