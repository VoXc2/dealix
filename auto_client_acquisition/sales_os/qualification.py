"""Sales qualification scorer — 8 questions, deterministic decision.

Decisions:
  ACCEPT          → start with paid 499 SAR sprint
  DIAGNOSTIC_ONLY → free diagnostic only; revisit after 2-4 weeks
  REFRAME         → conversation needed; their ask is partially in-scope
  REJECT          → not a fit; doctrine violations or no proof path
  REFER_OUT       → out of Dealix scope; suggest a partner

Pure function. No DB. Used by the diagnostic intake router + the
proposal router to gate scope.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class Decision(StrEnum):
    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


@dataclass
class QualificationResult:
    decision: Decision
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
    # 8 qualification questions (each True/False or a short string).
    pain_clear: bool,
    owner_present: bool,
    data_available: bool,
    accepts_governance: bool,
    has_budget: bool,
    wants_safe_methods: bool,
    proof_path_visible: bool,
    retainer_path_visible: bool,
    # Optional context — strings that may include doctrine-violating
    # requests (e.g., "we want cold WhatsApp automation"). Detected
    # heuristically and added to doctrine_violations.
    raw_request_text: str = "",
    sector: str = "",
    city: str = "",
) -> QualificationResult:
    """Deterministic qualification scoring.

    Doctrine-violation requests force REJECT regardless of score:
    - "cold whatsapp" / "واتساب بارد"
    - "linkedin automation" / "أتمتة لينكدإن"
    - "scraping" / "سحب البيانات"
    - "guaranteed sales" / "ضمان المبيعات"
    """
    text = (raw_request_text or "").lower()
    doctrine_violations: list[str] = []

    # Hard doctrine violations.
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

    # If wants_safe_methods is False, that's a soft violation hint.
    if not wants_safe_methods and not doctrine_violations:
        doctrine_violations.append("declined_safe_methods")

    score = 0
    reasons: list[str] = []
    for q, weight in WEIGHTS.items():
        if locals().get(q):
            score += weight
        else:
            reasons.append(f"missing:{q}")

    # Decision logic.
    if doctrine_violations:
        decision = Decision.REJECT
        safe_alt = (
            "Refer to our methodology: draft-only outputs, source passport, "
            "approval-gated outreach. If they want spam/scraping, we cannot help."
        )
        offer = "decline_with_safe_alternative_explanation"
    elif score >= 75:
        decision = Decision.ACCEPT
        safe_alt = ""
        if score >= 90 and has_budget and data_available:
            offer = "data_to_revenue_pack_1500_sar"  # straight to higher offer
        else:
            offer = "revenue_intelligence_sprint_499_sar"
    elif score >= 50:
        # Partial fit — could become a customer after a diagnostic.
        if not data_available or not owner_present:
            decision = Decision.DIAGNOSTIC_ONLY
            offer = "free_diagnostic_first_then_revisit"
            safe_alt = ""
        else:
            decision = Decision.REFRAME
            offer = "scope_call_to_align_then_proposal"
            safe_alt = "Tighten the scope to one sector + one owner before proposal."
    elif score >= 30:
        decision = Decision.REFER_OUT
        offer = "partner_referral_or_diagnostic_revisit_in_60_days"
        safe_alt = "Better fit for a basic CRM consultant or sector-specific agency."
    else:
        decision = Decision.REJECT
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


__all__ = ["Decision", "QualificationResult", "WEIGHTS", "qualify"]
