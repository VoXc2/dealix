"""Maps lightweight policy checks to compliance runtime decisions.

Backward-compat contract:
- Existing callers use ``decide(action=..., context=...)`` and expect
  ``decision.value`` + ``reasons``.
- Legacy callers may pass ``action_type``/``risk_score`` and expect
  reason/risk/approval metadata fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


@dataclass(frozen=True, slots=True)
class RuntimeDecision:
    decision: GovernanceDecision
    reasons: tuple[str, ...] = ()
    reason: str = ""
    risk_level: str = "low"
    approval_required: bool = False
    safe_alternative: str = ""
    evidence: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "reason": self.reason,
            "risk_level": self.risk_level,
            "approval_required": self.approval_required,
            "safe_alternative": self.safe_alternative,
            "evidence": dict(self.evidence or {}),
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


def _normalize_risk_score(raw: float | int | str | None) -> float:
    if raw is None:
        return 0.0
    try:
        score = float(raw)
    except Exception:  # noqa: BLE001
        return 0.0
    # Accept either 0..1 or 0..100 scale.
    if score > 1.0:
        score = score / 100.0
    return max(0.0, min(1.0, score))


def decide(
    *,
    action: str | None = None,
    action_type: str | None = None,
    context: dict[str, Any] | None = None,
    actor: str = "system",
    risk_score: float | None = None,
) -> RuntimeDecision:
    """Deterministic runtime governance guard for operational actions."""
    ctx = context or {}
    resolved_action = (action_type or action or "").strip()
    action_norm = resolved_action.lower()
    score = _normalize_risk_score(
        risk_score if risk_score is not None else ctx.get("risk_score")
    )
    high_risk_actions = {
        "send_external_message",
        "whatsapp.send_message",
        "crm.update_deal",
        "pricing_commitment",
        "contract_commitment",
        "refund",
        "delete_customer_data",
        "self_evolving.apply_patch",
    }

    if action_norm in {"send_whatsapp", "send_linkedin_dm"} and bool(ctx.get("is_cold", False)):
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=("cold_outreach_forbidden",),
            reason="cold outreach forbidden",
            risk_level="high",
            approval_required=False,
            safe_alternative="draft_for_founder_review",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )

    source_passport = ctx.get("source_passport")
    contains_pii = bool(ctx.get("contains_pii", False))
    external_use = bool(ctx.get("external_use", False))

    if action_norm in high_risk_actions or score >= 0.7:
        return RuntimeDecision(
            decision=GovernanceDecision.ESCALATE,
            reasons=("high_risk_requires_human_approval",),
            reason="high-risk action requires human approval",
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )

    if source_passport is None and action_norm in {"run_scoring", "generate_draft"}:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("source_passport_missing",),
            reason="source passport required before AI action",
            risk_level="medium",
            approval_required=True,
            safe_alternative="capture_source_passport_then_retry",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )

    if contains_pii and external_use:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("pii_external_use_requires_approval_workflow",),
            reason="PII external use requires approval",
            risk_level="high",
            approval_required=True,
            safe_alternative="use_internal_analysis_only",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )

    if score >= 0.4:
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=("medium_risk_monitoring",),
            reason="medium-risk action allowed with monitoring",
            risk_level="medium",
            approval_required=False,
            safe_alternative="",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )

    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW,
        reasons=("low_risk_allow",),
        reason="low-risk action",
        risk_level="low",
        approval_required=False,
        safe_alternative="",
        evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
