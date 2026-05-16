"""Evidence router — record Commercial Evidence State Machine transitions.

Endpoint (prefix /api/v1/evidence):
  POST /events — validate a CEL transition; on success append a
                 `commercial.*` event to the store; an illegal transition
                 returns 422.

Tenant-scoped via `customer_id` in the body.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.commercial_os.engine import CommercialEngine
from auto_client_acquisition.revenue_memory.event_store import get_default_store

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])

_GOVERNANCE_DECISION = "approval_required"


def _engine() -> CommercialEngine:
    """Engine bound to the shared default event store."""
    return CommercialEngine(store=get_default_store())


class EvidenceEventBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1)
    subject_type: str = Field(default="account", min_length=1)
    subject_id: str = Field(..., min_length=1)
    next_state: str = Field(..., min_length=1)
    founder_confirmed: bool = False
    used_in_meeting: bool = False
    scope_or_intro_requested: bool = False
    invoice_paid: bool = False
    actor: str = "system"
    payload: dict[str, Any] = Field(default_factory=dict)


@router.post("/events")
async def record_evidence_event(body: EvidenceEventBody) -> dict[str, Any]:
    """Record a CEL transition; an illegal transition returns 422."""
    engine = _engine()
    try:
        recorded = engine.record_transition(
            customer_id=body.customer_id,
            subject_type=body.subject_type,
            subject_id=body.subject_id,
            next_state=body.next_state,
            founder_confirmed=body.founder_confirmed,
            used_in_meeting=body.used_in_meeting,
            scope_or_intro_requested=body.scope_or_intro_requested,
            invoice_paid=body.invoice_paid,
            actor=body.actor,
            payload=body.payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "event_id": recorded.event.event_id,
        "event_type": recorded.event.event_type,
        "commercial_state": recorded.state,
        "cel": recorded.cel,
        "governance_decision": _GOVERNANCE_DECISION,
    }
