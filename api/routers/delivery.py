"""
Delivery router — service sessions + state machine + SLA + QA.

Endpoints:
    POST /api/v1/delivery/sessions       open a new ServiceSession
    GET  /api/v1/delivery/sessions/{id}  retrieve
    POST /api/v1/delivery/sessions/{id}/transition
                                          move to a new status
    GET  /api/v1/delivery/sessions/{id}/qa
                                          DoD checklist before delivery
    GET  /api/v1/delivery/sla-summary    SLA bucket counts (operator view)
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.proof_ledger import fetch_for_session
from auto_client_acquisition.service_delivery.qa_checklist import check_ready_to_deliver
from auto_client_acquisition.service_delivery.service_session import (
    allowed_transitions, get, list_for_customer, open_session, transition,
)
from auto_client_acquisition.service_delivery.sla_tracker import status_for, summarize
from auto_client_acquisition.service_tower.contracts import get_contract
from db.models import ServiceSessionRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/delivery", tags=["delivery"])


@router.post("/sessions")
async def create_session(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    service_id = str(body.get("service_id") or "")
    if not service_id:
        raise HTTPException(status_code=400, detail="service_id_required")
    async with get_session() as s:
        try:
            row = await open_session(
                s,
                service_id=service_id,
                customer_id=body.get("customer_id"),
                partner_id=body.get("partner_id"),
                owner=body.get("owner"),
                inputs=body.get("inputs") or {},
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "session_id": row.id,
        "service_id": row.service_id,
        "status": row.status,
        "deadline_at": row.deadline_at.isoformat() if row.deadline_at else None,
        "next_step": row.next_step,
    }


@router.get("/sessions/{session_id}")
async def get_session_detail(session_id: str) -> dict[str, Any]:
    async with get_session() as s:
        row = await get(s, session_id)
    if row is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    sla = status_for(row.deadline_at)
    return {
        "session_id": row.id,
        "service_id": row.service_id,
        "status": row.status,
        "owner": row.owner,
        "started_at": row.started_at.isoformat() if row.started_at else None,
        "deadline_at": row.deadline_at.isoformat() if row.deadline_at else None,
        "delivered_at": row.delivered_at.isoformat() if row.delivered_at else None,
        "next_step": row.next_step,
        "deliverables": row.deliverables_json or [],
        "proof_pack_url": row.proof_pack_url,
        "sla": {
            "deadline_at": sla.deadline_at.isoformat() if sla.deadline_at else None,
            "is_breached": sla.is_breached,
            "hours_remaining": sla.hours_remaining,
            "risk_level": sla.risk_level,
        },
        "allowed_transitions": allowed_transitions(row.status),
    }


@router.post("/sessions/{session_id}/transition")
async def post_transition(session_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    to_status = str(body.get("to") or "")
    if not to_status:
        raise HTTPException(status_code=400, detail="to_required")
    async with get_session() as s:
        try:
            row = await transition(
                s,
                session_id=session_id,
                to_status=to_status,
                actor=str(body.get("actor") or "system"),
                next_step=body.get("next_step"),
                deliverables=body.get("deliverables"),
                proof_pack_url=body.get("proof_pack_url"),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"session_id": row.id, "status": row.status, "next_step": row.next_step}


@router.get("/sessions/{session_id}/qa")
async def qa(session_id: str) -> dict[str, Any]:
    async with get_session() as s:
        row = await get(s, session_id)
        if row is None:
            raise HTTPException(status_code=404, detail="session_not_found")
        events = await fetch_for_session(s, session_id)
    contract = get_contract(row.service_id)
    result = check_ready_to_deliver(row, contract, events)
    return {
        "session_id": session_id,
        "passed": result.passed,
        "missing": list(result.missing),
        "warnings": list(result.warnings),
    }


@router.get("/sla-summary")
async def sla_summary(
    customer_id: str | None = Query(default=None),
) -> dict[str, Any]:
    async with get_session() as s:
        if customer_id:
            rows = await list_for_customer(s, customer_id)
        else:
            rows = list((await s.execute(select(ServiceSessionRecord).limit(500))).scalars().all())
    return {"buckets": summarize(rows), "session_count": len(rows)}
