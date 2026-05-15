"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import (
    PolicyCheckResult,
    PolicyVerdict,
    run_policy_check,
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
class RuntimeDecision:
    decision: GovernanceDecision
    reasons: tuple[str, ...]
    safe_alternative: str


def decide(*, action: str, context: dict[str, Any]) -> RuntimeDecision:
    """Single-call runtime decision helper for routers/orchestrators."""
    text = str(context.get("text", "") or "")
    lead_source = context.get("lead_source")
    external_use = bool(context.get("external_use", False))
    contains_pii = bool(context.get("contains_pii", False))

    check = run_policy_check(
        draft_text=text if text else None,
        lead_source=str(lead_source) if lead_source else None,
    )
    mapped = governance_decision_from_policy_check(check)

    # External actions over PII always require explicit approval workflow.
    if external_use and contains_pii:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("pii_external_use_requires_approval_workflow",),
            safe_alternative="draft_only_internal_review",
        )

    if "send" in action.lower() and external_use:
        return RuntimeDecision(
            decision=GovernanceDecision.DRAFT_ONLY,
            reasons=("external_send_draft_only",),
            safe_alternative="prepare_draft_for_human_approval",
        )

    if mapped == GovernanceDecision.BLOCK:
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=check.issues,
            safe_alternative="fix_policy_issues_and_retry",
        )

    if mapped == GovernanceDecision.ALLOW_WITH_REVIEW:
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=check.issues,
            safe_alternative="run_with_human_review",
        )

    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW,
        reasons=(),
        safe_alternative="proceed",
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
