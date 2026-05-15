"""Runtime governance mapping and deterministic action decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


class DecisionToken(str):
    """String decision token with enum-like `.value` compatibility."""

    @property
    def value(self) -> str:
        return str(self)


@dataclass(slots=True)
class RuntimeDecision:
    decision: DecisionToken
    reason: str
    risk_level: str = "low"
    approval_required: bool = False
    safe_alternative: str | None = None
    evidence: dict[str, Any] | None = None

    @property
    def reasons(self) -> tuple[str, ...]:
        return (self.reason,)


def decide(
    *,
    action_type: str | None = None,
    action: str | None = None,
    context: dict[str, Any] | None = None,
    actor: str = "system",
    risk_score: float | None = None,
    **_: Any,
) -> RuntimeDecision:
    """Return a deterministic runtime decision for a requested action."""
    context = context or {}
    resolved_action = (action_type or action or "unknown_action").strip()
    raw_score = float(risk_score if risk_score is not None else context.get("risk_score", 0.0))
    score = raw_score / 100.0 if raw_score > 1.0 else raw_score
    high_risk_actions = {
        "send_external_message",
        "whatsapp.send_message",
        "crm.update_deal",
        "pricing_commitment",
        "contract_commitment",
        "refund",
        "delete_customer_data",
    }
    if resolved_action in high_risk_actions or score >= 0.7:
        return RuntimeDecision(
            decision=DecisionToken("escalate"),
            reason="high-risk action requires human approval",
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )
    if score >= 0.4:
        return RuntimeDecision(
            decision=DecisionToken("allow_with_monitoring"),
            reason="medium-risk action allowed with audit and monitoring",
            risk_level="medium",
            approval_required=False,
            evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
        )
    return RuntimeDecision(
        decision=DecisionToken("allow"),
        reason="low-risk action",
        risk_level="low",
        approval_required=False,
        evidence={"actor": actor, "action_type": resolved_action, "risk_score": score},
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


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
