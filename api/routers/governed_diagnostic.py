"""Governed Revenue Ops Diagnostic router.

Single-offer commercial funnel with approval-first boundaries.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.governed_revenue_ops_diagnostic import (
    LeadCaptureInput,
    advance_state,
    build_invoice_draft,
    build_meeting_brief,
    build_scope_draft,
    capture_lead,
    daily_dashboard,
    get_record,
    sample_proof_pack,
)

router = APIRouter(prefix="/api/v1/governed-diagnostic", tags=["governed-diagnostic"])


class AdvanceStateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    funnel_id: str
    target_state: str


class FunnelRefBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    funnel_id: str


class ScopeDraftBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    funnel_id: str
    tier: str = "starter"


class InvoiceDraftBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    funnel_id: str
    tier: str = "starter"
    payment_method: str = "payment_link_external"


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "governed_revenue_ops_diagnostic",
        "offer": "Governed Revenue Ops Diagnostic",
        "status": "operational",
        "funnel_states": [
            "visitor",
            "lead_captured",
            "qualified_A",
            "qualified_B",
            "nurture",
            "meeting_booked",
            "meeting_done",
            "scope_requested",
            "scope_sent",
            "invoice_sent",
            "invoice_paid",
            "delivery_started",
            "proof_pack_sent",
            "upsell_sprint",
            "retainer_candidate",
            "closed_lost",
        ],
        "guardrails": {
            "all_external_actions_approval_required": True,
            "no_invoice_sent_before_scope_sent": True,
            "no_delivery_before_invoice_paid": True,
            "no_proof_pack_before_delivery_started": True,
            "no_upsell_before_proof_pack": True,
            "no_case_study_without_written_approval": True,
        },
    }


@router.post("/lead-capture")
async def lead_capture(payload: LeadCaptureInput) -> dict[str, Any]:
    try:
        record = capture_lead(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return record.model_dump(mode="json")


@router.post("/advance-state")
async def advance(body: AdvanceStateBody) -> dict[str, Any]:
    try:
        record = advance_state(funnel_id=body.funnel_id, target_state=body.target_state)  # type: ignore[arg-type]
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return record.model_dump(mode="json")


@router.post("/meeting-brief")
async def meeting_brief(body: FunnelRefBody) -> dict[str, Any]:
    try:
        brief = build_meeting_brief(funnel_id=body.funnel_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"funnel_id": body.funnel_id, "meeting_brief": brief, "action_mode": "approval_required"}


@router.post("/scope-draft")
async def scope_draft(body: ScopeDraftBody) -> dict[str, Any]:
    try:
        scope = build_scope_draft(funnel_id=body.funnel_id, tier=body.tier)  # type: ignore[arg-type]
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"funnel_id": body.funnel_id, "scope_draft": scope}


@router.post("/invoice-draft")
async def invoice_draft(body: InvoiceDraftBody) -> dict[str, Any]:
    try:
        invoice = build_invoice_draft(
            funnel_id=body.funnel_id,
            tier=body.tier,  # type: ignore[arg-type]
            payment_method=body.payment_method,  # type: ignore[arg-type]
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"funnel_id": body.funnel_id, "invoice_draft": invoice}


@router.get("/record")
async def record(funnel_id: str) -> dict[str, Any]:
    try:
        rec = get_record(funnel_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return rec.model_dump(mode="json")


@router.get("/daily-dashboard")
async def dashboard() -> dict[str, Any]:
    return daily_dashboard()


@router.get("/sample-proof-pack")
async def sample_pack() -> dict[str, Any]:
    return sample_proof_pack()
