"""
Close Plan — given the deal context + open objections, propose a close path.

Pure deterministic policy: maps {objection class, deal stage, has_pilot_offer}
to one of:
  - offer_pilot_499        : safest first-touch close
  - offer_data_to_revenue  : when customer already has a list
  - offer_proof_review     : when customer needs more proof
  - schedule_team_meeting  : when there's a need_team_approval gate
  - polite_followup_30d    : when timing/not-priority
  - escalate_human         : trust + want_guarantee + complex
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ClosePlan:
    plan_id: str
    title_ar: str
    rationale_ar: str
    next_action_ar: str
    fallback_action_ar: str
    risk_level: str  # low | medium | high
    proof_impact: tuple[str, ...]


_PLANS: dict[str, ClosePlan] = {
    "offer_pilot_499": ClosePlan(
        plan_id="offer_pilot_499",
        title_ar="عرض Pilot 499 (الأسرع للقرار)",
        rationale_ar="العميل يحتاج Proof قبل الالتزام — Pilot 499 يعطيه Proof خلال 7 أيام بدون مخاطرة.",
        next_action_ar="جهّز رابط الفاتورة (manual) + intake form + خطة 7 أيام.",
        fallback_action_ar="إذا رفض، اعرض Free Diagnostic.",
        risk_level="low",
        proof_impact=("pilot_offer_ready", "payment_link_drafted"),
    ),
    "offer_data_to_revenue": ClosePlan(
        plan_id="offer_data_to_revenue",
        title_ar="عرض Data to Revenue (1,500 SAR)",
        rationale_ar="عند العميل قائمة جاهزة — أكبر قيمة من تنظيفها + رسائل عربية + Top 50.",
        next_action_ar="اطلب عينة من القائمة + ابعث intake + ضع SLA 10 أيام.",
        fallback_action_ar="إذا تردد، اعرض Pilot 499 لقطعة صغيرة من القائمة.",
        risk_level="low",
        proof_impact=("opportunity_created", "draft_created"),
    ),
    "offer_proof_review": ClosePlan(
        plan_id="offer_proof_review",
        title_ar="مراجعة Proof Pack مع المجلس",
        rationale_ar="ينقص العميل ثقة — Proof Pack sample يحل اعتراض trust.",
        next_action_ar="أرسل Proof Pack sample + احجز اجتماع 20 دقيقة.",
        fallback_action_ar="إذا الجلسة تأخرت، أرسل reference customer للاتصال.",
        risk_level="low",
        proof_impact=("meeting_drafted",),
    ),
    "schedule_team_meeting": ClosePlan(
        plan_id="schedule_team_meeting",
        title_ar="اجتماع فريق صانع القرار",
        rationale_ar="القرار يحتاج موافقة فريق — اجتماع 30 دقيقة مع ديك مختصر يحل العقدة.",
        next_action_ar="جهّز deck (5 شرائح) + احجز اجتماع خلال 7 أيام.",
        fallback_action_ar="أرسل Proof Pack sample للمجلس بدون اجتماع.",
        risk_level="medium",
        proof_impact=("meeting_drafted",),
    ),
    "polite_followup_30d": ClosePlan(
        plan_id="polite_followup_30d",
        title_ar="متابعة بعد 30 يوماً",
        rationale_ar="الوقت ليس مناسباً الآن — احترم القرار + احتفظ بالـ Diagnostic.",
        next_action_ar="جدول follow-up بعد 30 يوماً + سجّل لا outbound في هذه الفترة.",
        fallback_action_ar="إذا تواصلوا قبل، حوّل لـ Pilot 499 مباشرة.",
        risk_level="low",
        proof_impact=("followup_created",),
    ),
    "escalate_human": ClosePlan(
        plan_id="escalate_human",
        title_ar="تصعيد لإنسان (founder/sales lead)",
        rationale_ar="الاعتراض معقّد (ضمان نتائج / ثقة عالية) — يحتاج محادثة بشرية.",
        next_action_ar="احجز call founder + جهّز ملخص الاعتراض + سجل في deal notes.",
        fallback_action_ar="إذا يصعب الـ call، أرسل founder note مكتوبة.",
        risk_level="medium",
        proof_impact=("call_recommended",),
    ),
}


def recommend(
    *,
    objection_class: str,
    has_list: bool = False,
    deal_stage: str = "new",
) -> ClosePlan:
    if objection_class == "want_guarantee":
        return _PLANS["escalate_human"]
    if objection_class == "trust" and deal_stage in ("late", "demo_done"):
        return _PLANS["offer_proof_review"]
    if objection_class == "need_team_approval":
        return _PLANS["schedule_team_meeting"]
    if objection_class in ("timing", "not_priority"):
        return _PLANS["polite_followup_30d"]
    if has_list:
        return _PLANS["offer_data_to_revenue"]
    if objection_class == "send_details":
        return _PLANS["offer_pilot_499"]
    # Default safe close: Pilot 499
    return _PLANS["offer_pilot_499"]


def all_plans() -> tuple[ClosePlan, ...]:
    return tuple(_PLANS.values())


def to_dict(p: ClosePlan) -> dict[str, Any]:
    return {
        "plan_id": p.plan_id,
        "title_ar": p.title_ar,
        "rationale_ar": p.rationale_ar,
        "next_action_ar": p.next_action_ar,
        "fallback_action_ar": p.fallback_action_ar,
        "risk_level": p.risk_level,
        "proof_impact": list(p.proof_impact),
    }
