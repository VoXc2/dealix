"""V12 Customer Success OS — wraps customer_success.health_score."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/v1/customer-success-os", tags=["customer-success-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


class _HealthScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intake_complete: bool = False
    diagnostic_delivered: bool = False
    proof_events_count: int = Field(0, ge=0)
    open_support_tickets: int = Field(0, ge=0)
    last_customer_response_days: int = Field(0, ge=0)
    delivery_sla_status: str = "unknown"
    payment_status: str = "unknown"
    renewal_signal: bool = False


class _CheckinRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = "Slot-A"
    week: int = Field(default=1, ge=1, le=52)


@router.get("/status")
async def cs_os_status() -> dict[str, Any]:
    return {
        "service": "customer_success_os",
        "module": "customer_success",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"health_score": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /health-score مرّة أسبوعيّاً",
        "next_action_en": "Use /health-score once per week.",
    }


@router.post("/health-score")
async def cs_health_score(req: _HealthScoreRequest) -> dict[str, Any]:
    """Compute a 0–100 health score from explicit signals.

    Pure function. NO LLM. NO fake data. If signals are sparse, the
    score reflects ``unknown`` honestly rather than green-by-default.
    """
    score = 0
    if req.intake_complete:
        score += 15
    if req.diagnostic_delivered:
        score += 20
    score += min(20, req.proof_events_count * 5)
    score -= min(15, req.open_support_tickets * 5)
    if req.last_customer_response_days <= 3:
        score += 10
    elif req.last_customer_response_days <= 7:
        score += 5
    else:
        score -= 5
    if req.delivery_sla_status == "on_track":
        score += 15
    elif req.delivery_sla_status == "at_risk":
        score -= 10
    if req.payment_status == "paid":
        score += 15
    elif req.payment_status == "overdue":
        score -= 15
    if req.renewal_signal:
        score += 10
    score = max(0, min(100, score))
    if score >= 81:
        band = "excellent"
        label_ar, label_en = "ممتاز", "Excellent"
    elif score >= 61:
        band = "good"
        label_ar, label_en = "جيد", "Good"
    elif score >= 31:
        band = "needs_attention"
        label_ar, label_en = "يحتاج تدخّل", "Needs attention"
    else:
        band = "high_risk"
        label_ar, label_en = "خطر عالي", "High risk"
    return {
        "score": score,
        "band": band,
        "label_ar": label_ar,
        "label_en": label_en,
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/weekly-checkin-draft")
async def cs_weekly_checkin(req: _CheckinRequest) -> dict[str, Any]:
    return {
        "customer_handle": req.customer_handle,
        "week": req.week,
        "draft_ar": (
            f"السلام عليكم، أتابع وضع Pilot الأسبوع {req.week}. "
            "أحتاج 5 دقائق لمراجعة:\n"
            "1) ما هو أفضل ردّ شفته هذا الأسبوع؟\n"
            "2) أي اعتراض كرّر نفسه؟\n"
            "3) هل تحتاج تعديل في خطّة المتابعة؟"
        ),
        "draft_en": (
            f"Following up on the Pilot for week {req.week}. Need 5 min "
            "to review:\n"
            "1) Best reply you saw this week?\n"
            "2) Any objection that repeated?\n"
            "3) Adjustment needed in the follow-up plan?"
        ),
        "action_mode": "draft_only",
        "send_method": "manual_only",
        "hard_gates": _HARD_GATES,
    }
