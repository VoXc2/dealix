"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


class _DecisionLabel(str):
    """Compatibility shim: behaves as str and as enum-like `.value`."""

    @property
    def value(self) -> str:
        return str(self)


@dataclass(slots=True)
class RuntimeDecision:
    decision: str
    reason: str
    risk_level: str = "low"
    approval_required: bool = False
    safe_alternative: str | None = None
    evidence: dict[str, Any] | None = None

    @property
    def reasons(self) -> tuple[str, ...]:
        """Back-compat for call-sites expecting iterable reasons."""
        return (self.reason,)


def decide(
    *,
    action_type: str | None = None,
    context: dict[str, Any] | None = None,
    actor: str = "system",
    risk_score: float | None = None,
    action: str | None = None,
) -> RuntimeDecision:
    context = context or {}
    normalized_action = action_type or action or "unknown_action"
    score = float(risk_score if risk_score is not None else context.get("risk_score", 0.0))

    # Scan any free-text payload for forbidden/unsafe claims (guarantees,
    # fabricated proof, …). Unsafe claims always block — this keeps the
    # no-guaranteed-claims doctrine enforced through the runtime path.
    text = str(context.get("text") or "").strip()
    if text:
        from auto_client_acquisition.governance_os.claim_safety import (
            audit_claim_safety,
        )

        claim_result = audit_claim_safety(text)
        claim_hits = [
            i for i in claim_result.issues if i.startswith("forbidden_claim:")
        ]
        if claim_hits:
            return RuntimeDecision(
                decision=_DecisionLabel("block"),
                reason="forbidden claim detected in draft text",
                risk_level="high",
                approval_required=True,
                safe_alternative="rewrite_without_unsafe_claim",
                evidence={
                    "actor": actor,
                    "action_type": normalized_action,
                    "issues": list(claim_result.issues),
                },
            )
        if claim_result.issues:
            return RuntimeDecision(
                decision=_DecisionLabel("redact"),
                reason="forbidden operational term detected in draft text",
                risk_level="medium",
                approval_required=True,
                safe_alternative="draft_only",
                evidence={
                    "actor": actor,
                    "action_type": normalized_action,
                    "issues": list(claim_result.issues),
                },
            )

    high_risk_actions = {
        "send_external_message",
        "whatsapp.send_message",
        "crm.update_deal",
        "pricing_commitment",
        "contract_commitment",
        "refund",
        "delete_customer_data",
    }
    external_use = bool(context.get("external_use") or context.get("external_action_requested"))
    if normalized_action in high_risk_actions or score >= 0.7 or external_use:
        return RuntimeDecision(
            decision=_DecisionLabel("escalate"),
            reason="high-risk action requires human approval",
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence={"actor": actor, "action_type": normalized_action, "risk_score": score},
        )
    if score >= 0.4:
        return RuntimeDecision(
            decision=_DecisionLabel("allow_with_monitoring"),
            reason="medium-risk action allowed with audit and monitoring",
            risk_level="medium",
            approval_required=False,
            evidence={"actor": actor, "action_type": normalized_action, "risk_score": score},
        )
    return RuntimeDecision(
        decision=_DecisionLabel("allow"),
        reason="low-risk action",
        risk_level="low",
        approval_required=False,
        evidence={"actor": actor, "action_type": normalized_action, "risk_score": score},
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
