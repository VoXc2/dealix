"""Support Journey HTTP surface (Phase 7 Wave 5).

  GET  /api/v1/support-journey/status
  POST /api/v1/support-journey/answer
  GET  /api/v1/support-journey/stages
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.support_journey import (
    JOURNEY_STAGES,
    STAGE_SLA_HOURS,
    classify_with_stage,
    draft_stage_reply,
    is_known_stage,
    stage_escalation_policy,
)

router = APIRouter(prefix="/api/v1/support-journey", tags=["support-journey"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "drafts_only": True,
    "no_guaranteed_claims": True,
    "approval_required_for_external_actions": True,
    "billing_privacy_renewal_always_escalate_to_founder": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "support_journey",
        "version": "1.0.0",
        "stages": list(JOURNEY_STAGES),
        "stage_count": len(JOURNEY_STAGES),
        "sla_hours_per_stage": STAGE_SLA_HOURS,
        "hard_gates": _HARD_GATES,
    }


@router.get("/stages")
async def stages() -> dict[str, Any]:
    return {
        "stages": list(JOURNEY_STAGES),
        "sla_hours": STAGE_SLA_HOURS,
        "hard_gates": _HARD_GATES,
    }


@router.post("/answer")
async def answer(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    message_text = payload.get("message_text") or payload.get("text")
    if not message_text:
        raise HTTPException(status_code=422, detail="message_text required")
    customer_handle = payload.get("customer_handle")

    classification = classify_with_stage(message_text)
    stage = classification["journey_stage"]
    if not is_known_stage(stage):
        stage = "pre_sales"

    draft = draft_stage_reply(
        message_text=message_text,
        journey_stage=stage,
        customer_handle=customer_handle,
    )
    escalation = stage_escalation_policy(journey_stage=stage)

    return {
        "classification": classification,
        "draft": draft,
        "escalation": escalation,
        "hard_gates": _HARD_GATES,
    }
