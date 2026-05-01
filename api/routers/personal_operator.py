"""Arabic Personal Strategic Operator endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.personal_operator import (
    ApprovalDecision,
    build_daily_brief,
    default_sami_profile,
    draft_follow_up,
    draft_intro_message,
    suggest_opportunities,
)
from auto_client_acquisition.personal_operator.operator import apply_decision, launch_readiness_score
from auto_client_acquisition.v3.project_intelligence import explain_project_intelligence_stack

router = APIRouter(prefix="/api/v1/personal-operator", tags=["personal-operator"])


def _opportunity_by_id(opportunity_id: str):
    for opportunity in suggest_opportunities(default_sami_profile()):
        if opportunity.id == opportunity_id:
            return opportunity
    # Demo fallback because deterministic sample IDs change per process.
    opportunities = suggest_opportunities(default_sami_profile())
    return opportunities[0] if opportunities else None


@router.get("/daily-brief")
async def daily_brief() -> dict[str, Any]:
    """Arabic executive daily brief for Sami."""
    return build_daily_brief(default_sami_profile()).to_dict()


@router.get("/opportunities")
async def opportunities() -> dict[str, Any]:
    items = suggest_opportunities(default_sami_profile())
    return {"count": len(items), "items": [item.to_card() for item in items]}


@router.post("/opportunities")
async def create_contextual_opportunities(body: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Return operator opportunities with optional context.

    Later this will use Supabase project memory + relationship graph. For now it
    returns deterministic safe opportunities with the user context echoed.
    """
    items = suggest_opportunities(default_sami_profile())
    return {
        "context_received": body,
        "count": len(items),
        "items": [item.to_card() for item in items],
    }


@router.post("/opportunities/{opportunity_id}/decision")
async def decide_opportunity(opportunity_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    opportunity = _opportunity_by_id(opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    decision = ApprovalDecision(body.get("decision", "draft"))
    return {"opportunity": opportunity.to_card(), "decision": decision.value, "result": apply_decision(opportunity, decision)}


@router.post("/messages/draft")
async def draft_message(body: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    opportunities = suggest_opportunities(default_sami_profile())
    selected = opportunities[0]
    if body.get("opportunity_id"):
        selected = _opportunity_by_id(str(body["opportunity_id"])) or selected
    tone = str(body.get("tone", "warm"))
    return draft_intro_message(selected, tone=tone)


@router.post("/followups/draft")
async def followup(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return draft_follow_up(
        meeting_title=str(body.get("meeting_title", "اجتماع Dealix")),
        outcome=str(body.get("outcome", "اتفقنا على مراجعة الفكرة وإرسال ملخص")),
        next_step=str(body.get("next_step", "إرسال ملخص تنفيذي وتجربة قصيرة")),
    )


@router.get("/project/intelligence")
async def project_intelligence() -> dict[str, Any]:
    return explain_project_intelligence_stack()


@router.post("/project/ask")
async def ask_project(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    question = str(body.get("question", "وش ناقص المشروع؟"))
    readiness = launch_readiness_score()
    return {
        "question": question,
        "answer_ar": (
            "المشروع أساسه قوي، لكن ناقصه قبل الإطلاق: دمج PR v3، اختبارات، "
            "ربط Supabase embeddings، WhatsApp approval buttons، Gmail draft، Calendar schedule، "
            "واجهة Personal Operator، ومراقبة Langfuse/Sentry."
        ),
        "launch_readiness": readiness,
        "recommended_next_files": [
            "auto_client_acquisition/personal_operator/operator.py",
            "api/routers/personal_operator.py",
            "supabase/migrations/202605010001_v3_project_memory.sql",
            "landing/personal-operator.html",
        ],
    }


@router.get("/launch-readiness")
async def launch_readiness() -> dict[str, Any]:
    return launch_readiness_score()


@router.post("/meetings/schedule-draft")
async def schedule_draft(body: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    return {
        "status": "calendar_draft_ready",
        "approval_required": True,
        "title": body.get("title", "Dealix Strategic Intro"),
        "duration_minutes": int(body.get("duration_minutes", 30)),
        "agenda_ar": [
            "تعريف سريع بـ Dealix",
            "أخذ رأي الشخص في التموضع والسوق",
            "تحديد فرصة تعاون أو intro قادمة",
        ],
        "note": "This endpoint prepares the meeting payload. Actual Google Calendar creation should only happen after approval.",
    }
