"""Governance Runtime as an enterprise product surface."""

from __future__ import annotations

GOVERNANCE_RUNTIME_PRODUCT_COMPONENTS: tuple[str, ...] = (
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

GOVERNANCE_RUNTIME_DECISIONS: tuple[str, ...] = (
    "ALLOW",
    "ALLOW_WITH_REVIEW",
    "DRAFT_ONLY",
    "REQUIRE_APPROVAL",
    "REDACT",
    "BLOCK",
    "ESCALATE",
)
