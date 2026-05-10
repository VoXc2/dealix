"""Wave 13 Phase 4 — Deliverables HTTP surface.

- POST /api/v1/deliverables/create
- GET  /api/v1/deliverables/{deliverable_id}
- GET  /api/v1/deliverables/by-session/{session_id}
- POST /api/v1/deliverables/{deliverable_id}/advance
- GET  /api/v1/deliverables/status

Wraps ``auto_client_acquisition.deliverables`` package.

Hard rules:
  Article 4: customer_visible=False blocks portal display
  Article 8: proof_related=True + status='delivered' requires proof_event_id
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.deliverables import (
    Deliverable,
    DeliverableStatus,
    DeliverableType,
    InvalidTransitionError,
    advance,
    create_deliverable,
    get_deliverable,
    list_by_session,
)

router = APIRouter(prefix="/api/v1/deliverables", tags=["Deliverables"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_proof": True,
    "customer_visible_false_blocks_portal": True,
    "proof_related_requires_proof_event_id_on_delivered": True,
}


class CreateDeliverableRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    customer_handle: str = Field(..., min_length=1)
    type: DeliverableType
    title_ar: str = Field(..., min_length=1, max_length=200)
    title_en: str = Field(..., min_length=1, max_length=200)
    customer_visible: bool = True
    approval_required: bool = True
    proof_related: bool = False
    proof_event_id: str | None = None
    artifact_uri: str | None = None


class AdvanceDeliverableRequest(BaseModel):
    target_status: DeliverableStatus
    reason: str = ""


def _serialize(d: Deliverable) -> dict[str, Any]:
    return d.model_dump(mode="json")


@router.get("/status")
async def deliverables_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "wave": "wave13_phase_4_deliverables",
        "hard_gates": _HARD_GATES,
    }


@router.post("/create")
async def create_endpoint(req: CreateDeliverableRequest) -> dict[str, Any]:
    if req.proof_related and not req.proof_event_id:
        # Allow creation in draft state — but flag warning
        pass  # will be enforced on transition to 'delivered'
    rec = create_deliverable(
        session_id=req.session_id,
        customer_handle=req.customer_handle,
        type=req.type,
        title_ar=req.title_ar,
        title_en=req.title_en,
        customer_visible=req.customer_visible,
        approval_required=req.approval_required,
        proof_related=req.proof_related,
        proof_event_id=req.proof_event_id,
        artifact_uri=req.artifact_uri,
    )
    return {
        "deliverable": _serialize(rec),
        "hard_gates": _HARD_GATES,
    }


@router.get("/by-session/{session_id}")
async def by_session_endpoint(
    session_id: str,
    customer_visible_only: bool = False,
) -> dict[str, Any]:
    items = list_by_session(session_id, customer_visible_only=customer_visible_only)
    return {
        "session_id": session_id,
        "count": len(items),
        "deliverables": [_serialize(d) for d in items],
        "hard_gates": _HARD_GATES,
    }


@router.get("/{deliverable_id}")
async def get_endpoint(deliverable_id: str) -> dict[str, Any]:
    rec = get_deliverable(deliverable_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="deliverable_not_found")
    return {
        "deliverable": _serialize(rec),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{deliverable_id}/advance")
async def advance_endpoint(
    deliverable_id: str,
    req: AdvanceDeliverableRequest,
) -> dict[str, Any]:
    rec = get_deliverable(deliverable_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="deliverable_not_found")
    try:
        advance(rec, target=req.target_status, reason=req.reason)
    except InvalidTransitionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {
        "deliverable": _serialize(rec),
        "hard_gates": _HARD_GATES,
    }
