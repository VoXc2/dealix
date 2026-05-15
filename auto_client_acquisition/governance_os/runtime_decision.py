"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


@dataclass(frozen=True, slots=True)
class RuntimeDecision:
    decision: GovernanceDecision
    reasons: tuple[str, ...]
    safe_alternative: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "safe_alternative": self.safe_alternative,
        }


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


def decide(*, action: str, context: dict[str, Any] | None = None) -> RuntimeDecision:
    """Deterministic runtime governance guard for operational actions."""
    ctx = context or {}
    action_norm = (action or "").strip().lower()

    if action_norm in {"send_whatsapp", "send_linkedin_dm"} and bool(ctx.get("is_cold", False)):
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=("cold_outreach_forbidden",),
            safe_alternative="draft_for_founder_review",
        )

    source_passport = ctx.get("source_passport")
    contains_pii = bool(ctx.get("contains_pii", False))
    external_use = bool(ctx.get("external_use", False))

    if source_passport is None and action_norm in {"run_scoring", "generate_draft"}:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("source_passport_missing",),
            safe_alternative="capture_source_passport_then_retry",
        )

    if contains_pii and external_use:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("pii_external_use_requires_approval_workflow",),
            safe_alternative="use_internal_analysis_only",
        )

    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW_WITH_REVIEW,
        reasons=("human_review_recommended",),
        safe_alternative="",
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
