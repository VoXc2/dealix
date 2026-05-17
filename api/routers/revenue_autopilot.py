"""Revenue Autopilot router — governed funnel endpoints.

Triggers the 10 automations, advances the funnel, and reads engagement
state. Every external / sensitive action produced here is a draft routed
to the Approval Command Center — this router never executes a live send.

Doctrine: docs/REVENUE_AUTOPILOT.md
"""
from __future__ import annotations

from typing import Any, get_args

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.revenue_autopilot.automations import AUTOMATIONS
from auto_client_acquisition.revenue_autopilot.funnel import (
    REVENUE_STAGES,
    FunnelStage,
    valid_transitions,
)
from auto_client_acquisition.revenue_autopilot.lead_scorer import LeadSignals
from auto_client_acquisition.revenue_autopilot.orchestrator import (
    advance_funnel,
    capture_lead,
    get_engagement,
    list_engagements,
    run_automation,
)
from auto_client_acquisition.revenue_autopilot.records import Contact

router = APIRouter(prefix="/api/v1/revenue-autopilot", tags=["revenue-autopilot"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_proof": True,
    "no_unbounded_agents": True,
    "approval_required_for_external_actions": True,
}


class _CaptureLeadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contact: Contact = Field(default_factory=Contact)
    signals: LeadSignals = Field(default_factory=LeadSignals)


class _AdvanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target: FunnelStage
    actor: str = "founder"


def _pending_for(engagement_id: str) -> list[dict[str, Any]]:
    """Pending approvals in the Approval Command Center for this engagement."""
    store = get_default_approval_store()
    return [
        a.model_dump(mode="json")
        for a in store.list_pending()
        if a.object_id == engagement_id
    ]


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "revenue_autopilot",
        "status": "operational",
        "active_engagements": len(list_engagements(limit=10_000)),
        "automations": ["lead_capture", *sorted(AUTOMATIONS)],
        "hard_gates": _HARD_GATES,
    }


@router.get("/funnel/stages")
async def funnel_stages() -> dict[str, Any]:
    stages = list(get_args(FunnelStage))
    return {
        "stages": stages,
        "revenue_stages": sorted(REVENUE_STAGES),
        "transitions": {s: sorted(valid_transitions(s)) for s in stages},
        "hard_gates": _HARD_GATES,
    }


@router.post("/lead")
async def create_lead(req: _CaptureLeadRequest) -> dict[str, Any]:
    """Automation 1 — capture a lead, score it, draft a first response."""
    engagement, result = capture_lead(
        contact=req.contact.model_dump(),
        signals=req.signals.model_dump(),
    )
    return {
        "engagement": engagement.model_dump(mode="json"),
        "result": result.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/engagements/{engagement_id}/automations/{automation_name}")
async def trigger_automation(
    engagement_id: str,
    automation_name: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run automations 2-10 against an existing engagement."""
    try:
        engagement, result = run_automation(
            automation_name, engagement_id, payload or {}
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "engagement": engagement.model_dump(mode="json"),
        "result": result.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/engagements/{engagement_id}/advance")
async def advance(engagement_id: str, req: _AdvanceRequest) -> dict[str, Any]:
    """Founder-driven explicit funnel advance (e.g. scope_sent → invoice_sent)."""
    try:
        engagement = advance_funnel(
            engagement_id, req.target, actor=req.actor
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "engagement": engagement.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/engagements")
async def list_all(limit: int = 50) -> dict[str, Any]:
    return {
        "engagements": [
            e.model_dump(mode="json") for e in list_engagements(limit=limit)
        ],
    }


@router.get("/engagements/{engagement_id}")
async def read_engagement(engagement_id: str) -> dict[str, Any]:
    engagement = get_engagement(engagement_id)
    if engagement is None:
        raise HTTPException(status_code=404, detail=f"unknown engagement: {engagement_id}")
    return {
        "engagement": engagement.model_dump(mode="json"),
        "pending_approvals": _pending_for(engagement_id),
        "hard_gates": _HARD_GATES,
    }
