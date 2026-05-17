"""Support ticketing — persisted ticket lifecycle.

create → classify → draft-response (from KB) → escalate / resolve.
Sending a drafted reply is always approval-gated: ``/send-reply`` returns
``approval_required`` and never sends.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auto_client_acquisition.support.lifecycle import (
    classify_ticket,
    create_ticket,
    draft_reply,
    escalate_ticket,
    request_send_reply,
    resolve_ticket,
)
from auto_client_acquisition.support.ticket_store import get_default_ticket_store

router = APIRouter(prefix="/api/v1/support/tickets", tags=["support"])


class TicketCreate(BaseModel):
    subject: str = ""
    message: str
    channel: str = "unknown"
    customer_id: str | None = None
    tenant_id: str | None = None


class EscalateBody(BaseModel):
    reason: str = ""


@router.get("/status")
async def status() -> dict:
    store = get_default_ticket_store()
    tickets = store.list()
    return {
        "module": "support_tickets",
        "backend": "memory_jsonl",
        "open": len([t for t in tickets if t.status == "open"]),
        "escalated": len([t for t in tickets if t.status == "escalated"]),
        "total": len(tickets),
        "guardrails": {
            "support_never_sends": True,
            "send_reply_requires_approval": True,
            "high_risk_categories_force_escalation": True,
        },
    }


@router.post("")
async def create(body: TicketCreate) -> dict:
    tkt = create_ticket(
        subject=body.subject,
        message=body.message,
        channel=body.channel,
        customer_id=body.customer_id,
        tenant_id=body.tenant_id,
    )
    return tkt.model_dump(mode="json")


@router.get("")
async def list_tickets(
    status: str | None = None,
    category: str | None = None,
    risk_level: str | None = None,
    tenant_id: str | None = None,
) -> dict:
    rows = get_default_ticket_store().list(
        status=status, category=category, risk_level=risk_level, tenant_id=tenant_id
    )
    return {"count": len(rows), "tickets": [t.model_dump(mode="json") for t in rows]}


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str) -> dict:
    tkt = get_default_ticket_store().get(ticket_id)
    if tkt is None:
        raise HTTPException(status_code=404, detail="support_ticket_not_found")
    return tkt.model_dump(mode="json")


@router.post("/{ticket_id}/classify")
async def classify(ticket_id: str) -> dict:
    try:
        tkt = classify_ticket(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return tkt.model_dump(mode="json")


@router.post("/{ticket_id}/draft-response")
async def draft_response(ticket_id: str) -> dict:
    try:
        return draft_reply(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{ticket_id}/escalate")
async def escalate(ticket_id: str, body: EscalateBody) -> dict:
    try:
        tkt = escalate_ticket(ticket_id, reason=body.reason)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return tkt.model_dump(mode="json")


@router.post("/{ticket_id}/resolve")
async def resolve(ticket_id: str) -> dict:
    try:
        tkt = resolve_ticket(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return tkt.model_dump(mode="json")


@router.post("/{ticket_id}/send-reply")
async def send_reply(ticket_id: str) -> dict:
    try:
        return request_send_reply(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
