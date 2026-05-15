"""Runtime governance decisioning.

Two layers:

1. Adapter helpers (``governance_decision_from_*``) that map lightweight
   policy / passport checks onto the compliance ``GovernanceDecision``
   vocabulary.

2. ``decide()`` — the single runtime entrypoint the control plane calls
   before any non-trivial action. It composes the existing deterministic
   primitives (``approval_matrix.approval_for_action`` + Source Passport
   gating) into one verdict: a low-risk action is allowed, a medium-risk
   action is allowed-with-review, and a high-risk / external / passport-
   missing action escalates to a human approval gate. Nothing here sends,
   charges, or executes — it only routes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.approval_matrix import approval_for_action
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


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
    """The verdict ``decide()`` returns for one runtime action."""

    decision: GovernanceDecision
    reasons: tuple[str, ...]
    risk_level: str = "low"
    approval_required: bool = False
    safe_alternative: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def is_escalation(self) -> bool:
        return self.decision in (
            GovernanceDecision.ESCALATE,
            GovernanceDecision.REQUIRE_APPROVAL,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "risk_level": self.risk_level,
            "approval_required": self.approval_required,
            "safe_alternative": self.safe_alternative,
            "evidence": dict(self.evidence),
        }


# Actions that always require a human approval gate regardless of score.
_HIGH_RISK_ACTIONS: frozenset[str] = frozenset(
    {
        "send_external_message",
        "whatsapp.send_message",
        "send_whatsapp_live",
        "crm.update_deal",
        "pricing_commitment",
        "contract_commitment",
        "refund",
        "delete_customer_data",
        "rollback",
    },
)


def decide(
    *,
    action: str,
    context: dict[str, Any] | None = None,
    actor: str = "system",
    risk_score: float | None = None,
) -> RuntimeDecision:
    """Route one runtime action to a governance verdict.

    ``context`` may carry a ``source_passport`` (data actions): a key
    present but ``None`` means the passport is missing and the action is
    blocked until one is provided. ``contains_pii`` + ``external_use``
    together escalate to a human approval gate.
    """
    ctx = context or {}
    reasons: list[str] = []
    score = float(risk_score if risk_score is not None else ctx.get("risk_score", 0.0))
    evidence: dict[str, Any] = {
        "actor": actor,
        "action": action,
        "risk_score": score,
    }

    # ── Source Passport gate (data actions) ──────────────────────────
    if "source_passport" in ctx and ctx.get("source_passport") is None:
        reasons.append("source_passport_required")
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=tuple(reasons),
            risk_level="high",
            approval_required=False,
            safe_alternative="block_until_source_passport_provided",
            evidence=evidence,
        )
    if ctx.get("contains_pii") and ctx.get("external_use"):
        reasons.append("pii_external_use_requires_approval_workflow")
        return RuntimeDecision(
            decision=GovernanceDecision.ESCALATE,
            reasons=tuple(reasons),
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence=evidence,
        )

    # ── Action risk routing (deterministic matrix) ───────────────────
    risk, gate = approval_for_action(action)
    evidence["matrix_risk"] = risk
    evidence["matrix_gate"] = gate

    if gate == "blocked":
        reasons.append(f"action_blocked_by_policy:{action}")
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=tuple(reasons),
            risk_level="high",
            approval_required=False,
            safe_alternative="draft_only",
            evidence=evidence,
        )

    if action in _HIGH_RISK_ACTIONS or risk == "high" or score >= 0.7:
        reasons.append("high_risk_action_requires_human_approval")
        return RuntimeDecision(
            decision=GovernanceDecision.ESCALATE,
            reasons=tuple(reasons),
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence=evidence,
        )

    if risk == "medium" or score >= 0.4:
        reasons.append("medium_risk_action_allowed_with_review")
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=tuple(reasons),
            risk_level="medium",
            approval_required=False,
            safe_alternative=None,
            evidence=evidence,
        )

    reasons.append("low_risk_action")
    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW,
        reasons=tuple(reasons),
        risk_level="low",
        approval_required=False,
        safe_alternative=None,
        evidence=evidence,
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]
