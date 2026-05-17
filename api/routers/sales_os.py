"""V12 Sales OS — thin wrapper exposing CRM + reply_classifier as V12.

NO guarantee claims. NO pressure manipulation. NO fake scarcity.
Every external messaging output is `draft_only` or `approval_required`.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.sales_os.founder_revenue_machine import (
    MACHINE_GUARDRAILS,
    PIPELINE_STATES,
    SALES_MACHINE_CONFIG,
    RiskScoreInput,
    compute_ops_risk_score,
    score_lead_fit,
    transitions,
    validate_transition,
)

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


class _LeadScoreSignals(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision_maker: bool = False
    b2b_company: bool = False
    has_crm_or_revenue_process: bool = False
    uses_or_plans_ai: bool = False
    saudi_or_gcc: bool = True
    urgency_within_30_days: bool = False
    budget_5k_sar_plus: bool = False
    no_company: bool = False
    student_or_job_seeker: bool = False
    vague_curiosity: bool = False


class _RiskScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    has_crm: bool = False
    uses_ai: bool = False
    has_external_approval_gate: bool = False
    can_link_workflow_to_financial_outcome: bool = False
    follow_up_is_documented: bool = False
    source_clarity_for_decisions: bool = False
    has_evidence_pack: bool = False


class _PipelineTransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_state: str
    target_state: str
    context: dict[str, Any] = Field(default_factory=dict)


@router.get("/status")
async def sales_os_status() -> dict[str, Any]:
    return {
        "service": "sales_os",
        "module": "crm_v10+reply_classifier+founder_revenue_machine",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"lead_score": "ok", "deal_score": "ok", "reply_classifier": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /qualify ثم /meeting-prep",
        "next_action_en": "Use /qualify then /meeting-prep.",
    }


@router.get("/machine-config")
async def machine_config() -> dict[str, Any]:
    return {
        **SALES_MACHINE_CONFIG,
        "pipeline_states": list(PIPELINE_STATES),
        "transitions": transitions(),
        "strict_rules": list(MACHINE_GUARDRAILS),
        "hard_gates": _HARD_GATES,
        "action_mode": "draft_only_or_approval_required",
    }


@router.get("/pipeline-states")
async def pipeline_states() -> dict[str, Any]:
    return {
        "states": list(PIPELINE_STATES),
        "transitions": transitions(),
        "strict_rules": list(MACHINE_GUARDRAILS),
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


@router.post("/lead-score")
async def lead_score(req: _LeadScoreSignals) -> dict[str, Any]:
    result = score_lead_fit(signals=req.model_dump())
    return {
        **result,
        "offer": SALES_MACHINE_CONFIG["offer_name"],
        "pricing_sar": SALES_MACHINE_CONFIG["pricing_sar"],
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/risk-score")
async def risk_score(req: _RiskScoreRequest) -> dict[str, Any]:
    score = compute_ops_risk_score(
        RiskScoreInput(
            has_crm=req.has_crm,
            uses_ai=req.uses_ai,
            has_external_approval_gate=req.has_external_approval_gate,
            can_link_workflow_to_financial_outcome=req.can_link_workflow_to_financial_outcome,
            follow_up_is_documented=req.follow_up_is_documented,
            source_clarity_for_decisions=req.source_clarity_for_decisions,
            has_evidence_pack=req.has_evidence_pack,
        )
    )
    return {
        **score,
        "offer": SALES_MACHINE_CONFIG["offer_name"],
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/pipeline-transition")
async def pipeline_transition(req: _PipelineTransitionRequest) -> dict[str, Any]:
    verdict = validate_transition(
        current_state=req.current_state,
        target_state=req.target_state,
        context=req.context,
    )
    return {
        **verdict,
        "from": req.current_state,
        "to": req.target_state,
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
