"""ICP Score — pure function 0-100 over weighted signals."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ICPScore:
    score: int  # 0-100
    pain_intensity: int
    ability_to_pay: int
    urgency: int
    proof_potential: int
    founder_access: int
    referral_potential: int
    sector_repeatability: int
    delivery_complexity_penalty: int
    compliance_risk_penalty: int
    reason_ar: str
    reason_en: str


def compute_icp_score(
    *,
    pain_intensity: int = 0,         # 0-20
    ability_to_pay: int = 0,         # 0-15
    urgency: int = 0,                # 0-15
    proof_potential: int = 0,        # 0-15
    founder_access: int = 0,         # 0-15
    referral_potential: int = 0,     # 0-10
    sector_repeatability: int = 0,   # 0-10
    delivery_complexity: int = 0,    # 0-15 (subtracted)
    compliance_risk: int = 0,        # 0-15 (subtracted)
) -> ICPScore:
    """All inputs are 0-N integer bands the founder estimates from a
    lead's profile. Defaults of 0 mean 'unknown' — no fake green."""

    raw = (
        pain_intensity + ability_to_pay + urgency + proof_potential
        + founder_access + referral_potential + sector_repeatability
        - delivery_complexity - compliance_risk
    )
    score = max(0, min(100, raw))

    if score >= 80:
        reason_ar = "مرشح عالي الجودة — ابدأ Mini Diagnostic فوراً"
        reason_en = "High-quality candidate — start Mini Diagnostic now."
    elif score >= 60:
        reason_ar = "مرشح جيد — تحقّق من signal آخر قبل التشخيص"
        reason_en = "Good candidate — verify another signal before diagnostic."
    elif score >= 40:
        reason_ar = "مرشح متوسط — أخّره حتى تظهر إشارة أقوى"
        reason_en = "Mid candidate — hold until a stronger signal appears."
    else:
        reason_ar = "غير مرشح حالياً — لا تستهدف"
        reason_en = "Not a candidate now — do not target."

    return ICPScore(
        score=score,
        pain_intensity=pain_intensity,
        ability_to_pay=ability_to_pay,
        urgency=urgency,
        proof_potential=proof_potential,
        founder_access=founder_access,
        referral_potential=referral_potential,
        sector_repeatability=sector_repeatability,
        delivery_complexity_penalty=delivery_complexity,
        compliance_risk_penalty=compliance_risk,
        reason_ar=reason_ar,
        reason_en=reason_en,
    )
