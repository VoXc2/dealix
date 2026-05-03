"""
Call Recommendation Engine — recommends a call ONLY for high-intent or
support-escalation contexts. Never auto-dials.

Two modes:
  - recommend(reason, context) → CallRecommendation (or refusal)
  - generate_script(call_type, context) → Arabic script

Allowed reasons:
    price_question, meeting_requested, pilot_accepted,
    high_intent_reply, support_p0, renewal_risk_high,
    proof_pack_delay_sensitive, partner_intro_ready

Blocked when:
    no_permission OR unknown_source OR cold_list OR opt_out OR low_intent

The CALLS_ALLOW_LIVE_DIAL setting is hard-gated False — the engine never
actually dials. It only emits a recommendation card.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


ALLOWED_REASONS: frozenset[str] = frozenset({
    "price_question", "meeting_requested", "pilot_accepted",
    "high_intent_reply", "support_p0", "renewal_risk_high",
    "proof_pack_delay_sensitive", "partner_intro_ready",
})

BLOCKED_REASONS: frozenset[str] = frozenset({
    "no_permission", "unknown_source", "cold_list", "opt_out", "low_intent",
})


@dataclass(frozen=True)
class CallRecommendation:
    allowed: bool
    reason: str
    title_ar: str
    why_now_ar: str
    duration_minutes: int
    objective_ar: str
    risk_level: str
    blocked_reason: str | None = None
    refusal_reason_ar: str | None = None


def recommend(
    *,
    reason: str,
    has_user_permission: bool,
    customer_label: str = "العميل",
    deal_amount_sar: float | None = None,
) -> CallRecommendation:
    """Return a recommendation. If unsafe, allowed=False with refusal_reason_ar."""
    reason = (reason or "").lower()

    if reason in BLOCKED_REASONS:
        return CallRecommendation(
            allowed=False,
            reason=reason,
            title_ar="اتصال محظور",
            why_now_ar="—",
            duration_minutes=0,
            objective_ar="—",
            risk_level="high",
            blocked_reason=reason,
            refusal_reason_ar=_refusal_text(reason),
        )

    if not has_user_permission:
        return CallRecommendation(
            allowed=False,
            reason=reason,
            title_ar="اتصال محظور — لا يوجد إذن",
            why_now_ar="—",
            duration_minutes=0,
            objective_ar="—",
            risk_level="high",
            blocked_reason="no_permission",
            refusal_reason_ar="WhatsApp Business Calling يحتاج إذن صريح من المستخدم قبل المكالمة.",
        )

    if reason not in ALLOWED_REASONS:
        return CallRecommendation(
            allowed=False,
            reason=reason,
            title_ar="سبب غير معتمد",
            why_now_ar="—",
            duration_minutes=0,
            objective_ar="—",
            risk_level="medium",
            blocked_reason="unsupported_reason",
            refusal_reason_ar=f"السبب '{reason}' غير ضمن قائمة الـ high-intent المعتمدة.",
        )

    profile = _CALL_PROFILES[reason]
    return CallRecommendation(
        allowed=True,
        reason=reason,
        title_ar=profile["title_ar"].format(customer=customer_label),
        why_now_ar=profile["why_now_ar"].format(amount=deal_amount_sar or "—"),
        duration_minutes=profile["duration_minutes"],
        objective_ar=profile["objective_ar"],
        risk_level=profile["risk_level"],
    )


def can_dial_live(settings) -> tuple[bool, str]:
    """Always returns False unless CALLS_ALLOW_LIVE_DIAL is explicitly True
    AND we've confirmed user permission. Default policy refuses live dial.
    """
    if not bool(getattr(settings, "calls_allow_live_dial", False)):
        return False, "CALLS_ALLOW_LIVE_DIAL=false (live dialing is disabled by policy)"
    if not bool(getattr(settings, "calls_allow_recommend", True)):
        return False, "CALLS_ALLOW_RECOMMEND=false"
    return True, "ok"


# ── Call profiles ────────────────────────────────────────────────


_CALL_PROFILES: dict[str, dict[str, Any]] = {
    "price_question": {
        "title_ar":         "اتصال — تأكيد Pilot 499 مع {customer}",
        "why_now_ar":       "العميل سأل عن السعر — call قصير يحوّل التردد إلى قرار.",
        "duration_minutes": 10,
        "objective_ar":     "تأكيد Pilot 499 + جمع intake (موقع، عرض، عميل مثالي).",
        "risk_level":       "low",
    },
    "meeting_requested": {
        "title_ar":         "اتصال — تأكيد ميعاد اجتماع مع {customer}",
        "why_now_ar":       "العميل طلب اجتماع — تأكيد سريع يقلل no-show.",
        "duration_minutes": 5,
        "objective_ar":     "تأكيد التوقيت + إرسال أجندة + رابط حجز.",
        "risk_level":       "low",
    },
    "pilot_accepted": {
        "title_ar":         "اتصال onboarding — Pilot يبدأ مع {customer}",
        "why_now_ar":       "Pilot وافق — call onboarding يضع expectations + intake.",
        "duration_minutes": 15,
        "objective_ar":     "شرح خطة 7 أيام + تأكيد deliverables + ربط CSM.",
        "risk_level":       "low",
    },
    "high_intent_reply": {
        "title_ar":         "اتصال — رد قوي من {customer}",
        "why_now_ar":       "Reply يدلّ على نية عالية — call يقصّر دورة القرار.",
        "duration_minutes": 10,
        "objective_ar":     "تحويل النية إلى Pilot 499 أو Diagnostic مجاني.",
        "risk_level":       "medium",
    },
    "support_p0": {
        "title_ar":         "اتصال P0 — تصعيد دعم لـ {customer}",
        "why_now_ar":       "P0 = ساعة SLA — call يطمئن العميل + يفتح خط مباشر.",
        "duration_minutes": 15,
        "objective_ar":     "تأكيد الحل + متابعة Postmortem + تأكيد إجراءات منع التكرار.",
        "risk_level":       "high",
    },
    "renewal_risk_high": {
        "title_ar":         "اتصال renewal — {customer} (مخاطرة عالية)",
        "why_now_ar":       "Customer health منخفض قبل تجديد — call يحفظ العقد.",
        "duration_minutes": 20,
        "objective_ar":     "فهم الـ blockers + تجهيز Quarterly Review + خطة إنقاذ.",
        "risk_level":       "high",
    },
    "proof_pack_delay_sensitive": {
        "title_ar":         "اتصال — Proof Pack تأخّر لـ {customer}",
        "why_now_ar":       "تأخير Proof Pack يكسر الثقة — call شخصي يطمئن.",
        "duration_minutes": 10,
        "objective_ar":     "شرح السبب + تقديم ETA دقيق + اعتذار شخصي.",
        "risk_level":       "medium",
    },
    "partner_intro_ready": {
        "title_ar":         "اتصال — مقدمة شراكة مع {customer}",
        "why_now_ar":       "وكالة جاهزة لـ Co-branded Proof — call تعريفي لبدء Pilot.",
        "duration_minutes": 20,
        "objective_ar":     "شرح Agency Partner Pilot + اختيار عميل واحد + revenue share.",
        "risk_level":       "low",
    },
}


# ── Refusal messages ─────────────────────────────────────────────


def _refusal_text(reason: str) -> str:
    table = {
        "no_permission":  "لا يوجد إذن صريح من المستخدم — الاتصال محظور.",
        "unknown_source": "المصدر غير موثق — لا يجوز الاتصال.",
        "cold_list":      "قائمة باردة بدون opt-in — حظر تلقائي.",
        "opt_out":        "العميل سحب الموافقة — ممنوع التواصل.",
        "low_intent":     "النية منخفضة — استخدم Email أو LinkedIn manual بدل الاتصال.",
    }
    return table.get(reason, "السبب غير مقبول للاتصال.")


# ── Script generator ─────────────────────────────────────────────


def generate_script(*, call_reason: str, customer: str = "العميل", offer_sar: float | None = None) -> str:
    """Return an Arabic call script. Pure (no LLM)."""
    profile = _CALL_PROFILES.get(call_reason)
    if profile is None:
        return ""
    sar = offer_sar or 499
    return (
        f"السلام عليكم {customer}، معك [اسمك] من Dealix.\n"
        f"أخذ منك {profile['duration_minutes']} دقائق فقط.\n"
        f"الهدف: {profile['objective_ar']}\n\n"
        f"الأنسب نبدأ Pilot {sar:.0f} ريال لمدة 7 أيام:\n"
        f"  - 10 فرص + رسائل عربية + Proof Pack.\n"
        f"  - بدون التزام شهري.\n\n"
        f"أحتاج فقط: الموقع، العرض الرئيسي، والعميل المثالي.\n"
        f"إذا مناسب، أرسل لك intake form + رابط الفاتورة (manual).\n"
        f"\n"
        f"📌 لا نضمن نتائج محددة — نضمن Proof Pack بأرقام حقيقية."
    )
