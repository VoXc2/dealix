"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict

# --- Guaranteed-outcome claim detection (NO_GUARANTEED_CLAIMS gate) ----------
# Strategy: neutralize negated and refund forms first, then detect affirmative
# claims on what survives — so disclaimers ("لا نضمن", "no/without guarantee")
# and refund guarantees ("نضمن استرجاع") are never mistaken for a claim.

# Negated guarantee forms — a negator within a few words before the guarantee
# word, including multi-word constructions ("لا يمكننا أن نضمن", "we cannot
# really guarantee").
_NEGATED_AR = re.compile(
    r"(?:لا|لن|لم|ما|بدون|دون)(?:\s+\S+){0,3}?\s*(?:نضمن|ضمان)"
)
_NEGATED_EN = re.compile(
    r"\b(?:no|not|never|without|cannot|can't|don't|won't|doesn't|wouldn't)"
    r"\s+(?:\w+\s+){0,3}?guarantee",
    re.IGNORECASE,
)
# A refund / money-back guarantee is a service guarantee, not a guaranteed
# sales OUTCOME — permitted, so neutralized before the affirmative check.
_REFUND_AR = re.compile(r"نضمن\s*استرجاع")

_AR_OUTCOME = r"نتائج|نتيجة|مبيعات|أرباح|إيرادات|إيراد|عوائد|نمو|صفقات|عملاء"
# Affirmative Arabic guarantee — the verb نضمن, an outcome noun paired with
# the adjective مضمون or the noun ضمان (either order), or the "ربح مؤكد" idiom.
_AFFIRMATIVE_GUARANTEE_AR = re.compile(
    rf"نضمن"
    rf"|(?:{_AR_OUTCOME})\s*مضمون"
    rf"|مضمون[ةه]?\s*(?:{_AR_OUTCOME})"
    rf"|ضمان\s*(?:{_AR_OUTCOME})"
    rf"|(?:{_AR_OUTCOME})\s*ضمان"
    rf"|ربح\s*مؤكد"
)
_EN_OUTCOME = (
    r"revenue|sales?|results?|roi|growth|deals?|leads?|customers?|"
    r"conversions?|profit|income|outcomes?"
)
# Affirmative English guarantee — verb/adjective near an outcome noun in
# EITHER order ("guarantee revenue" / "revenue is guaranteed"), or a
# first-person promise.
_AFFIRMATIVE_GUARANTEE_EN = re.compile(
    rf"guarantee[ds]?\b[\w%\s-]{{0,20}}?\b(?:{_EN_OUTCOME})\b"
    rf"|\b(?:{_EN_OUTCOME})\b[\w%\s-]{{0,15}}?\bguarantee[ds]\b"
    rf"|\b(?:we|i)\s+guarantee\b"
    rf"|100\s*%?\s*guarantee[ds]?|guarantee[ds]?\s+100",
    re.IGNORECASE,
)


def _contains_guaranteed_claim(text: str) -> bool:
    """True when text makes an affirmative guaranteed-OUTCOME promise.

    Negated forms ("لا نضمن", "no/without ... guarantee") and refund
    guarantees ("نضمن استرجاع" — a service guarantee, not an outcome) are
    neutralized first, so a doctrine-compliant disclaimer is not blocked.
    """
    neutral_ar = _REFUND_AR.sub(" ", _NEGATED_AR.sub(" ", text))
    if _AFFIRMATIVE_GUARANTEE_AR.search(neutral_ar):
        return True
    neutral_en = _NEGATED_EN.sub(" ", text.lower())
    return _AFFIRMATIVE_GUARANTEE_EN.search(neutral_en) is not None


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
