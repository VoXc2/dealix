"""Service Sessions HTTP surface.

5 endpoints:
  POST /api/v1/service-sessions/start
  GET  /api/v1/service-sessions/{id}
  POST /api/v1/service-sessions/{id}/advance
  POST /api/v1/service-sessions/{id}/attach-deliverable
  POST /api/v1/service-sessions/{id}/complete

Hard rule: any transition into 'active' requires an approval_id.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.service_sessions import store as session_store

router = APIRouter(prefix="/api/v1/service-sessions", tags=["service-sessions"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "approval_required_for_active_state": True,
    "no_fake_proof": True,
}


_VALID_SERVICE_TYPES = {
    "diagnostic",
    "leadops_sprint",
    "growth_proof_sprint",
    "support_ops_setup",
    "customer_portal_setup",
    "executive_pack",
    "proof_pack",
    "agency_partner_pack",
}


@router.post("/start")
async def start(body: dict[str, Any]) -> dict[str, Any]:
    customer_handle = body.get("customer_handle")
    service_type = body.get("service_type")
    if not customer_handle:
        raise HTTPException(status_code=422, detail="customer_handle required")
    if service_type not in _VALID_SERVICE_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"service_type must be one of {sorted(_VALID_SERVICE_TYPES)}",
        )
    rec = session_store.start_session(
        customer_handle=customer_handle,
        service_type=service_type,
        inputs=body.get("inputs"),
    )
    return {
        "session": rec.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{session_id}")
async def get(session_id: str) -> dict[str, Any]:
    rec = session_store.get_session(session_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    return {
        "session": rec.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{session_id}/advance")
async def advance(session_id: str, body: dict[str, Any]) -> dict[str, Any]:
    target = body.get("target")
    approval_id = body.get("approval_id")
    if not target:
        raise HTTPException(status_code=422, detail="target required")
    rec, reason = session_store.transition_session(
        session_id=session_id,
        target=target,
        approval_id=approval_id,
    )
    if rec is None:
        raise HTTPException(status_code=409, detail=reason)
    return {
        "session": rec.model_dump(mode="json"),
        "transition_reason": reason,
        "hard_gates": _HARD_GATES,
    }


@router.post("/{session_id}/attach-deliverable")
async def attach(session_id: str, body: dict[str, Any]) -> dict[str, Any]:
    deliverable = body.get("deliverable")
    if not isinstance(deliverable, dict):
        raise HTTPException(status_code=422, detail="deliverable dict required")
    rec = session_store.attach_deliverable(
        session_id=session_id,
        deliverable=deliverable,
    )
    if rec is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    return {
        "session": rec.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{session_id}/complete")
async def complete(session_id: str) -> dict[str, Any]:
    rec, reason = session_store.complete_session(session_id=session_id)
    if rec is None:
        raise HTTPException(status_code=409, detail=reason)
    return {
        "session": rec.model_dump(mode="json"),
        "transition_reason": reason,
        "hard_gates": _HARD_GATES,
    }
