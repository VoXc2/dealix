"""Privacy-by-runtime — deterministic policy outcome from intake flags."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.endgame_os.governance_product import GovernanceDecision


@dataclass(frozen=True, slots=True)
class PrivacyRuntimeResult:
    decision: GovernanceDecision
    required_action: str


def privacy_runtime_outcome(
    *,
    input_contains_pii: bool,
    allowed_use: frozenset[str],
    external_use_allowed: bool,
) -> PrivacyRuntimeResult:
    """Map passport/use flags to a governance-style outcome (no external side effects)."""
    if not allowed_use:
        return PrivacyRuntimeResult(
            GovernanceDecision.BLOCK,
            "define_allowed_use_before_ai_processing",
        )
    if input_contains_pii and not external_use_allowed:
        return PrivacyRuntimeResult(
            GovernanceDecision.DRAFT_ONLY,
            "human_review_before_any_external_use",
        )
    if input_contains_pii:
        return PrivacyRuntimeResult(
            GovernanceDecision.ALLOW_WITH_REVIEW,
            "review_pii_handling_and_channel_before_release",
        )
    return PrivacyRuntimeResult(GovernanceDecision.ALLOW, "routine_internal_or_client_review")


def privacy_runtime_audit_payload(
    *,
    input_contains_pii: bool,
    allowed_use: frozenset[str],
    external_use_allowed: bool,
) -> dict[str, Any]:
    """JSON-shaped payload for logs / governance UI (matches doctrine example)."""
    result = privacy_runtime_outcome(
        input_contains_pii=input_contains_pii,
        allowed_use=allowed_use,
        external_use_allowed=external_use_allowed,
    )
    return {
        "input_contains_pii": input_contains_pii,
        "allowed_use": sorted(allowed_use),
        "external_use_allowed": external_use_allowed,
        "decision": result.decision.value,
        "required_action": result.required_action,
    }
