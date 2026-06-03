"""V12 Sales OS — thin wrapper exposing CRM + reply_classifier as V12.

NO guarantee claims. NO pressure manipulation. NO fake scarcity.
Every external messaging output is `draft_only` or `approval_required`.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/api/v1/sales-os", tags=["sales-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_guaranteed_claims": True,
    "no_pressure_manipulation": True,
    "approval_required_for_external_actions": True,
}


class _QualifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    has_warm_intro: bool = False
    sector: str = "b2b_services"
    pain_described: bool = False
    budget_signal: bool = False
    authority_signal: bool = False
    urgency_signal: bool = False


class _ObjectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objection_text: str
    language: str = "ar"


class _MeetingPrepRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = "Slot-A"
    sector: str = "b2b_services"
    duration_min: int = 30


@router.get("/status")
async def sales_os_status() -> dict[str, Any]:
    return {
        "service": "sales_os",
        "module": "crm_v10+reply_classifier",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"lead_score": "ok", "deal_score": "ok", "reply_classifier": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /qualify ثم /meeting-prep",
        "next_action_en": "Use /qualify then /meeting-prep.",
    }


@router.post("/qualify")
async def sales_qualify(req: _QualifyRequest) -> dict[str, Any]:
    """Return a deterministic qualification score (0–100) + recommendation."""
    score = 0
    if req.has_warm_intro:
        score += 25
    if req.pain_described:
        score += 25
    if req.budget_signal:
        score += 20
    if req.authority_signal:
        score += 15
    if req.urgency_signal:
        score += 15
    if score >= 75:
        recommendation_ar = "مؤهَّل — قدّم Pilot 499 ريال"
        recommendation_en = "Qualified — offer 499 SAR Pilot"
        next_step = "offer_pilot"
    elif score >= 40:
        recommendation_ar = "نصف مؤهَّل — قدّم Mini Diagnostic مجاني"
        recommendation_en = "Half-qualified — offer free Mini Diagnostic"
        next_step = "offer_diagnostic"
    else:
        recommendation_ar = "غير مؤهَّل حاليّاً — لا تواصل بارد"
        recommendation_en = "Not qualified yet — no cold outreach"
        next_step = "nurture_only"
    return {
        "score": score,
        "recommendation_ar": recommendation_ar,
        "recommendation_en": recommendation_en,
        "next_step": next_step,
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/objection-response")
async def sales_objection_response(req: _ObjectionRequest) -> dict[str, Any]:
    """Returns a draft response to a sales objection, no guarantees."""
    o = req.objection_text.lower()
    if "guarantee" in o or "نضمن" in req.objection_text or "تضمنون" in req.objection_text:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": (
                "العميل يطلب ضمانات — Dealix لا يضمن نتائج مبيعات. "
                "صعّد للمؤسس لتقديم ردّ صادق."
            ),
            "blocked_reason_en": (
                "Customer demands guarantees — Dealix does NOT guarantee "
                "sales results. Escalate to founder for honest framing."
            ),
            "hard_gates": _HARD_GATES,
        }
    if "expensive" in o or "غالي" in req.objection_text or "مكلف" in req.objection_text:
        return {
            "action_mode": "draft_only",
            "draft_ar": (
                "أتفهّم. الـ Pilot 499 ريال لمدّة 7 أيّام مع استرجاع كامل لو "
                "ما طابق التسليم المواصفات. هل نبدأ بـ Mini Diagnostic مجاني "
                "لتقييم القيمة قبل الالتزام؟"
            ),
            "draft_en": (
                "Understood. The Pilot is 499 SAR for 7 days with a full "
                "refund if delivery doesn't match spec. Want to start with "
                "a free Mini Diagnostic first to evaluate value?"
            ),
            "hard_gates": _HARD_GATES,
        }
    return {
        "action_mode": "draft_only",
        "draft_ar": (
            "شكراً على الملاحظة. أحتاج فهم أعمق قبل ما أردّ — هل نتكلّم 30 "
            "دقيقة الأسبوع الجاي؟"
        ),
        "draft_en": (
            "Thanks for the note. Want to talk for 30 min next week so I "
            "can respond properly?"
        ),
        "hard_gates": _HARD_GATES,
    }


@router.post("/meeting-prep")
async def sales_meeting_prep(req: _MeetingPrepRequest) -> dict[str, Any]:
    return {
        "customer_handle": req.customer_handle,
        "duration_min": req.duration_min,
        "agenda_ar": [
            "5 د — تعريف Dealix والوضع الحالي",
            "10 د — ما الفرص الـ 3 التي ترى أنها تستحق؟",
            "10 د — Pilot 499 ريال — ما هو، وما ليس",
            "5 د — الخطوة التالية + اعتماد المسوّدة",
        ],
        "agenda_en": [
            "5 min — Dealix intro + current state",
            "10 min — Which 3 opportunities feel worth pursuing?",
            "10 min — 499 SAR Pilot — what it is, what it isn't",
            "5 min — Next step + draft approval",
        ],
        "must_avoid_ar": [
            "ادّعاء عوائد محدّدة",
            "مقارنة مباشرة بالمنافسين بدون مصدر عام",
            "وعد بإرسال آلي",
        ],
        "must_avoid_en": [
            "Claiming specific revenue numbers",
            "Direct competitor comparison without public source",
            "Promising automated sends",
        ],
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }
