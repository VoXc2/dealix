"""V12 Growth OS — thin wrapper over ``growth_v10`` modules.

Exposes a V12-shape `/status` + `/daily-plan` + `/outreach-draft`.
NO scraping. NO automation. Outreach is always ``draft_only``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/v1/growth-os", tags=["growth-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_linkedin_automation": True,
    "approval_required_for_external_actions": True,
}


class _DailyPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str = "b2b_services"
    region: str = "riyadh"


class _OutreachDraftRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str
    audience: str = "warm_intro"
    language: str = "ar"
    placeholder_name: str = Field(default="[الاسم]", max_length=80)


@router.get("/status")
async def growth_os_status() -> dict[str, Any]:
    return {
        "service": "growth_os",
        "module": "growth_v10",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"campaign_lifecycle": "ok", "content_calendar": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /daily-plan أو /outreach-draft",
        "next_action_en": "Use /daily-plan or /outreach-draft.",
    }


@router.post("/daily-plan")
async def growth_daily_plan(req: _DailyPlanRequest) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "sector": req.sector,
        "region": req.region,
        "target_segment_ar": f"{req.sector} في {req.region}",
        "target_segment_en": f"{req.sector} in {req.region}",
        "why_now_ar": "بناء على تحليل النمو اليومي والـ Self-Growth OS",
        "why_now_en": "Based on daily growth analysis + Self-Growth OS signals.",
        "safe_channels": ["warm_intro", "referral", "inbound_dm"],
        "blocked_channels": [
            "cold_whatsapp", "cold_email", "linkedin_dm_automation",
        ],
        "manual_action_checklist": [
            "Pick 3 warm intros from your network",
            "Send manually using template 02_FIRST_10_WARM_MESSAGES_AR_EN",
            "Wait 7 days before any follow-up",
        ],
        "experiment_hypothesis": (
            "If we focus on warm intros only, response rate exceeds 30%."
        ),
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/outreach-draft")
async def growth_outreach_draft(req: _OutreachDraftRequest) -> dict[str, Any]:
    if req.audience not in {"warm_intro", "referral", "inbound_reply"}:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": "القناة غير آمنة للتواصل البارد",
            "blocked_reason_en": "Unsafe audience for cold outreach.",
            "hard_gates": _HARD_GATES,
        }
    ar = (
        f"السلام عليكم {req.placeholder_name}،\n"
        f"أنا [اسمك] من Dealix. عندي قراءة نمو مجانيّة لـ {req.sector} "
        "تشمل 3 فرص ومسوّدة رسالة وتوصية قناة. هل أرسلها؟"
    )
    en = (
        f"Hi {req.placeholder_name},\n"
        f"I'm [Your Name] from Dealix. I have a free growth read for "
        f"{req.sector}: 3 opportunities + 1 draft + safe-channel "
        "recommendation. May I send it?"
    )
    return {
        "action_mode": "draft_only",
        "audience": req.audience,
        "language": req.language,
        "draft_ar": ar,
        "draft_en": en,
        "send_method": "manual_only",
        "hard_gates": _HARD_GATES,
    }
