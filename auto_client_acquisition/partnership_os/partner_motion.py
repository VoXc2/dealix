"""V12 Partnership OS — recommend the right motion for a partner.

Hard constraints:
- NO white-label motion before 3 paid pilots are archived
- NO revenue-share motion until referral tracking has live data
- NO exclusivity ever
"""
from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.partnership_os.partner_profile import Partner


@dataclass
class MotionRecommendation:
    motion: str
    reason_ar: str
    reason_en: str
    action_mode: str  # suggest_only / draft_only / approval_required / blocked
    blocked: bool


def recommend_motion(
    *,
    partner: Partner,
    fit_score: int,
    paid_pilots_count: int = 0,
    has_referral_data: bool = False,
) -> MotionRecommendation:
    """Pick the right motion based on fit + maturity."""
    if fit_score < 40:
        return MotionRecommendation(
            motion="no_fit",
            reason_ar="درجة المطابقة منخفضة — لا شراكة مقترحة الآن",
            reason_en="Fit score too low — no partnership recommended now.",
            action_mode="blocked",
            blocked=True,
        )
    if fit_score < 60:
        return MotionRecommendation(
            motion="referral_only",
            reason_ar="إحالة فقط — جرّب 2-3 إحالات قبل أي شراكة أعمق",
            reason_en="Referral-only — try 2–3 referrals before deeper engagement.",
            action_mode="suggest_only",
            blocked=False,
        )
    if fit_score < 80:
        return MotionRecommendation(
            motion="co_branded_diagnostic",
            reason_ar="Diagnostic مشترك بالعلامتين — منخفض المخاطرة",
            reason_en="Co-branded Diagnostic — low risk, high learning.",
            action_mode="draft_only",
            blocked=False,
        )
    if paid_pilots_count < 3:
        return MotionRecommendation(
            motion="proof_pack_co_author",
            reason_ar=(
                "Proof Pack بتأليف مشترك — لا white-label قبل 3 pilots مدفوعة موثّقة"
            ),
            reason_en=(
                "Proof-pack co-author — NO white-label before 3 paid pilots."
            ),
            action_mode="approval_required",
            blocked=False,
        )
    if not has_referral_data:
        return MotionRecommendation(
            motion="proof_pack_co_author",
            reason_ar="مؤهَّل لـ white-label لكن لا توجد بيانات إحالات لتفعيل revenue share",
            reason_en="Eligible for white-label but no referral data to activate revenue share.",
            action_mode="approval_required",
            blocked=False,
        )
    return MotionRecommendation(
        motion="white_label_with_revenue_share",
        reason_ar="مؤهَّل بالكامل — white-label + revenue share بموافقة المؤسس",
        reason_en="Fully eligible — white-label + revenue share with founder approval.",
        action_mode="approval_required",
        blocked=False,
    )
