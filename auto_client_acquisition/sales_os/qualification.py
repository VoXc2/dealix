"""Qualification — map discovery answers to a commercial verdict (no LLM)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score


class QualificationVerdict(StrEnum):
    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


def qualify_opportunity(
    *,
    icp: ICPDimensions,
    risk: ClientRiskSignals,
    accepts_governance: bool,
    proof_path_possible: bool,
) -> tuple[QualificationVerdict, tuple[str, ...]]:
    reasons: list[str] = []
    icp_s = icp_score(icp)
    r = client_risk_score(risk)
    if risk.wants_scraping_or_spam or risk.wants_guaranteed_sales:
        return QualificationVerdict.REJECT, ("non_negotiable_risk",)
    if r >= 55:
        return QualificationVerdict.REJECT, ("high_client_risk",)
    if not accepts_governance:
        return QualificationVerdict.REFER_OUT, ("governance_not_accepted",)
    if not proof_path_possible:
        reasons.append("weak_proof_path")
        if icp_s < 50:
            return QualificationVerdict.DIAGNOSTIC_ONLY, tuple(reasons)
        return QualificationVerdict.REFRAME, tuple(reasons)
    if icp_s < 45:
        return QualificationVerdict.DIAGNOSTIC_ONLY, ("icp_low_start_with_diagnostic",)
    if icp_s < 60:
        return QualificationVerdict.REFRAME, ("icp_mid_package_shape",)
    return QualificationVerdict.ACCEPT, ("icp_ok_risk_ok",)


# ── Flat-field qualification scorer ─────────────────────────────────
# Used by the service-setup /qualify endpoint and warm-list outreach
# script: takes the 8 discovery answers plus free-text and runs a
# deterministic score + doctrine-violation text scan.

@dataclass
class QualificationResult:
    decision: QualificationVerdict
    score: int  # 0-100, qualification confidence
    reasons: list[str] = field(default_factory=list)
    doctrine_violations: list[str] = field(default_factory=list)
    safe_alternative: str = ""
    recommended_offer: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "score": self.score,
            "reasons": list(self.reasons),
            "doctrine_violations": list(self.doctrine_violations),
            "safe_alternative": self.safe_alternative,
            "recommended_offer": self.recommended_offer,
        }


# Question weights (0-100 contribution to qualification score).
WEIGHTS = {
    "pain_clear": 15,
    "owner_present": 15,
    "data_available": 15,
    "accepts_governance": 15,
    "has_budget": 10,
    "wants_safe_methods": 10,  # NOT asking for scraping/spam/guarantees
    "proof_path_visible": 10,
    "retainer_path_visible": 10,
}


def qualify(
    *,
    pain_clear: bool,
    owner_present: bool,
    data_available: bool,
    accepts_governance: bool,
    has_budget: bool,
    wants_safe_methods: bool,
    proof_path_visible: bool,
    retainer_path_visible: bool,
    raw_request_text: str = "",
    sector: str = "",
    city: str = "",
) -> QualificationResult:
    """Deterministic qualification scoring.

    Doctrine-violation requests force REJECT regardless of score:
    cold WhatsApp, LinkedIn automation, scraping, guaranteed sales,
    purchased lists — detected heuristically in ``raw_request_text``.
    """
    text = (raw_request_text or "").lower()
    doctrine_violations: list[str] = []

    for needle, label in [
        ("cold whatsapp", "cold_whatsapp"),
        ("واتساب بارد", "cold_whatsapp_ar"),
        ("whatsapp automation", "whatsapp_automation"),
        ("أتمتة واتساب", "whatsapp_automation_ar"),
        ("linkedin automation", "linkedin_automation"),
        ("linkedin auto", "linkedin_automation"),
        ("scraping", "scraping"),
        ("scrape", "scraping"),
        ("سحب البيانات", "scraping_ar"),
        ("guaranteed sales", "guaranteed_sales"),
        ("guarantee sales", "guaranteed_sales"),
        ("ضمان المبيعات", "guaranteed_sales_ar"),
        ("نضمن مبيعات", "guaranteed_sales_ar"),
        ("buy leads", "purchased_list"),
        ("شراء قوائم", "purchased_list_ar"),
    ]:
        if needle in text and label not in doctrine_violations:
            doctrine_violations.append(label)

    if not wants_safe_methods and not doctrine_violations:
        doctrine_violations.append("declined_safe_methods")

    answers = {
        "pain_clear": pain_clear,
        "owner_present": owner_present,
        "data_available": data_available,
        "accepts_governance": accepts_governance,
        "has_budget": has_budget,
        "wants_safe_methods": wants_safe_methods,
        "proof_path_visible": proof_path_visible,
        "retainer_path_visible": retainer_path_visible,
    }
    score = 0
    reasons: list[str] = []
    for q, weight in WEIGHTS.items():
        if answers.get(q):
            score += weight
        else:
            reasons.append(f"missing:{q}")

    if doctrine_violations:
        decision = QualificationVerdict.REJECT
        safe_alt = (
            "Refer to our methodology: draft-only outputs, source passport, "
            "approval-gated outreach. If they want spam/scraping, we cannot help."
        )
        offer = "decline_with_safe_alternative_explanation"
    elif score >= 75:
        decision = QualificationVerdict.ACCEPT
        safe_alt = ""
        if score >= 90 and has_budget and data_available:
            offer = "data_to_revenue_pack_1500_sar"
        else:
            offer = "revenue_intelligence_sprint_499_sar"
    elif score >= 50:
        if not data_available or not owner_present:
            decision = QualificationVerdict.DIAGNOSTIC_ONLY
            offer = "free_diagnostic_first_then_revisit"
            safe_alt = ""
        else:
            decision = QualificationVerdict.REFRAME
            offer = "scope_call_to_align_then_proposal"
            safe_alt = "Tighten the scope to one sector + one owner before proposal."
    elif score >= 30:
        decision = QualificationVerdict.REFER_OUT
        offer = "partner_referral_or_diagnostic_revisit_in_60_days"
        safe_alt = "Better fit for a basic CRM consultant or sector-specific agency."
    else:
        decision = QualificationVerdict.REJECT
        offer = "decline_politely"
        safe_alt = "Not ready for Governed AI Operations yet — revisit when data + owner exist."

    return QualificationResult(
        decision=decision,
        score=score,
        reasons=reasons,
        doctrine_violations=doctrine_violations,
        safe_alternative=safe_alt,
        recommended_offer=offer,
    )


__all__ = [
    "QualificationVerdict",
    "QualificationResult",
    "WEIGHTS",
    "qualify",
    "qualify_opportunity",
]
