"""Governance / approval decision vocabulary for runtime policy engine."""

from __future__ import annotations

from enum import StrEnum


class GovernanceDecision(StrEnum):
    ALLOW = "ALLOW"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    DRAFT_ONLY = "DRAFT_ONLY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


def governance_decision_for_pii_external(
    *,
    contains_pii: bool,
    external_action_requested: bool,
    passport_external_allowed: bool,
) -> GovernanceDecision:
    """Minimal deterministic router for tests and docs alignment."""
    if not passport_external_allowed and external_action_requested:
        return GovernanceDecision.BLOCK
    if contains_pii and external_action_requested:
        return GovernanceDecision.REQUIRE_APPROVAL
    if contains_pii:
        return GovernanceDecision.DRAFT_ONLY
    if external_action_requested:
        return GovernanceDecision.REQUIRE_APPROVAL
    return GovernanceDecision.ALLOW
