"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict
from auto_client_acquisition.saudi_layer.forbidden_claims import (
    forbidden_arabic_claim_detected,
)

# Negated forms — a guarantee word preceded by a negation is a compliant
# disclaimer, not an affirmative claim. Stripped before the affirmative check.
_NEGATED_AR = re.compile(r"(?:لا|لن|لم|ما)\s*نضمن")
_NEGATED_EN = re.compile(
    r"\b(?:no|not|never|without|cannot|can't|don't|won't|doesn't|"
    r"wouldn't)\s+guarantee",
    re.IGNORECASE,
)

# Affirmative English guarantee — the verb/adjective near an outcome noun,
# or a first-person promise. Matches "we/I guarantee revenue", "guarantee
# results", "guaranteed sales", "100% guaranteed", etc.
_AFFIRMATIVE_GUARANTEE_EN = re.compile(
    r"guarantee[ds]?\b[\w%\s-]{0,20}?\b"
    r"(revenue|sales?|results?|roi|growth|deals?|leads?|customers?|"
    r"conversions?|profit|income|outcomes?)\b"
    r"|\b(?:we|i)\s+guarantee\b"
    r"|100\s*%?\s*guarantee[ds]?|guarantee[ds]?\s+100",
    re.IGNORECASE,
)


def _contains_guaranteed_claim(text: str) -> bool:
    """True when text makes an affirmative guaranteed-outcome promise.

    Negated forms ("لا نضمن" / "no guarantee" / "without guarantee") are
    stripped first, so a doctrine-compliant disclaimer is not mistaken for an
    affirmative claim.
    """
    blob = text.lower()
    if forbidden_arabic_claim_detected(blob):
        return True
    if "نضمن" in _NEGATED_AR.sub(" ", text):
        return True
    en = _NEGATED_EN.sub(" ", blob)
    return _AFFIRMATIVE_GUARANTEE_EN.search(en) is not None


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

    # Content gate: an affirmative guaranteed-outcome claim is a hard
    # NO_GUARANTEED_CLAIMS violation regardless of the action type.
    text = str(context.get("text") or "")
    if text and _contains_guaranteed_claim(text):
        return RuntimeDecision(
            decision=_DecisionLabel("block"),
            reason="content makes a guaranteed-outcome claim (NO_GUARANTEED_CLAIMS)",
            risk_level="high",
            approval_required=True,
            safe_alternative="draft_only",
            evidence={"actor": actor, "action_type": normalized_action},
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
