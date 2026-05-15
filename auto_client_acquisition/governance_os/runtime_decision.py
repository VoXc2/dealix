"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    source_passport_valid_for_ai,
)


def governance_decision_from_policy_check(result: PolicyCheckResult) -> GovernanceDecision:
    if not result.allowed:
        return GovernanceDecision.BLOCK
    if result.verdict == PolicyVerdict.ALLOW_WITH_REVIEW:
        return GovernanceDecision.ALLOW_WITH_REVIEW
    return GovernanceDecision.ALLOW


def governance_decision_from_passport_ai_gate(ok: bool, errors: tuple[str, ...]) -> GovernanceDecision:
    """Align passport validation errors with runtime governance vocabulary."""
    if ok:
        return GovernanceDecision.ALLOW
    if errors == ("pii_external_use_requires_approval_workflow",):
        return GovernanceDecision.REQUIRE_APPROVAL
    return GovernanceDecision.BLOCK


@dataclass(frozen=True, slots=True)
class RuntimeDecisionResult:
    decision: GovernanceDecision
    reasons: tuple[str, ...]
    safe_alternative: str


def decide(*, action: str, context: dict[str, Any] | None = None) -> RuntimeDecisionResult:
    """Single entrypoint for router/service governance routing decisions."""
    ctx = context or {}
    normalized_action = action.strip().lower()

    if normalized_action == "run_scoring":
        passport = ctx.get("source_passport")
        if passport is None:
            return RuntimeDecisionResult(
                decision=GovernanceDecision.REQUIRE_APPROVAL,
                reasons=("missing_source_passport",),
                safe_alternative="provide_source_passport_then_retry_scoring",
            )
        ok, errors = source_passport_valid_for_ai(passport)
        decision = governance_decision_from_passport_ai_gate(ok, errors)
        if decision == GovernanceDecision.BLOCK:
            return RuntimeDecisionResult(
                decision=decision,
                reasons=errors or ("source_passport_invalid",),
                safe_alternative="fix_source_passport_before_ai_processing",
            )
        return RuntimeDecisionResult(
            decision=decision if decision != GovernanceDecision.ALLOW else GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=errors or ("source_passport_checked",),
            safe_alternative="founder_review_required_before_external_use",
        )

    text = str(ctx.get("text", "") or "")
    lead_source = str(ctx.get("lead_source", "") or "")
    check = PolicyCheckResult(allowed=True, verdict=PolicyVerdict.ALLOW, issues=())
    if text or lead_source:
        from auto_client_acquisition.governance_os.policy_check import run_policy_check

        check = run_policy_check(
            draft_text=text if text else None,
            lead_source=lead_source if lead_source else None,
        )

    decision = governance_decision_from_policy_check(check)
    reasons = list(check.issues)
    channel = str(ctx.get("channel", "") or "").lower()
    is_cold = bool(ctx.get("is_cold", False))

    if is_cold and channel in {"whatsapp", "linkedin"}:
        return RuntimeDecisionResult(
            decision=GovernanceDecision.BLOCK,
            reasons=(*reasons, "cold_outreach_forbidden_on_channel"),
            safe_alternative="use_warm_intro_or_manual_founder_message",
        )
    if channel in {"whatsapp", "linkedin", "gmail", "email"} and decision != GovernanceDecision.BLOCK:
        return RuntimeDecisionResult(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=tuple(reasons or ["external_action_requires_approval"]),
            safe_alternative="save_draft_and_request_founder_approval",
        )
    if decision == GovernanceDecision.ALLOW:
        decision = GovernanceDecision.ALLOW_WITH_REVIEW
        reasons = reasons or ["allow_with_review_default"]
    return RuntimeDecisionResult(
        decision=decision,
        reasons=tuple(reasons),
        safe_alternative="founder_review_before_publish",
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecisionResult",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
