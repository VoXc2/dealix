"""Support Inbox HTTP surface.

  POST /api/v1/support-inbox/inbound  — webhook entry; classifies + drafts
  GET  /api/v1/support-inbox/tickets   — list tickets
  GET  /api/v1/support-inbox/tickets/{id}
  POST /api/v1/support-inbox/tickets/{id}/status
  GET  /api/v1/support-inbox/sla-breaches  — tickets past SLA

Hard gates: NO_LIVE_SEND on every draft.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.support_inbox import (
    classify_and_store,
    find_breached_tickets,
    get_ticket,
    list_tickets,
    set_status,
)

router = APIRouter(prefix="/api/v1/support-inbox", tags=["support-inbox"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "drafts_only": True,
    "approval_required_for_external_actions": True,
    "no_fake_proof": True,
    "pii_redacted_before_storage": True,
}


@router.post("/inbound")
async def inbound(body: dict[str, Any]) -> dict[str, Any]:
    """Webhook entry — accepts WhatsApp / email / form payload.

    Body: {
      'message_text': '...',
      'customer_id': 'optional',
      'channel': 'whatsapp' | 'email' | 'form'
    }
    """
    message_text = body.get("message_text") or body.get("text")
    if not message_text:
        raise HTTPException(status_code=422, detail="message_text required")
    result = classify_and_store(
        message_text=message_text,
        customer_id=body.get("customer_id"),
        channel=body.get("channel", "unknown"),
    )
    return {**result, "hard_gates": _HARD_GATES}


@router.get("/tickets")
async def tickets(
    customer_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    rows = list_tickets(
        customer_id=customer_id,
        status=status,  # type: ignore[arg-type]
        limit=limit,
    )
    return {
        "count": len(rows),
        "tickets": [t.model_dump(mode="json") for t in rows],
        "hard_gates": _HARD_GATES,
    }


@router.get("/tickets/{ticket_id}")
async def get_one(ticket_id: str) -> dict[str, Any]:
    t = get_ticket(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    return {
        "ticket": t.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/tickets/{ticket_id}/status")
async def update_status(ticket_id: str, body: dict[str, Any]) -> dict[str, Any]:
    new_status = body.get("status")
    if new_status not in ("open", "in_progress", "waiting_customer", "escalated", "resolved", "closed"):
        raise HTTPException(status_code=422, detail="invalid status")
    t = set_status(ticket_id=ticket_id, status=new_status)  # type: ignore[arg-type]
    if t is None:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    return {
        "ticket": t.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/sla-breaches")
async def sla_breaches(customer_id: str | None = None) -> dict[str, Any]:
    breached = find_breached_tickets(customer_id=customer_id)
    return {
        "count": len(breached),
        "breached": breached,
        "hard_gates": _HARD_GATES,
    }
