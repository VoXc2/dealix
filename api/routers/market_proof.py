"""Market-proof lifecycle router.

Surfaces the L2 to L7 state machine that tracks a warm contact from a
prepared (not sent) outreach message to confirmed revenue. The system
prepares, suggests, logs and verifies — the founder approves every
external action. No autonomous send path exists here.

Doctrine breaches and guard-rule violations raise ValueError and are
mapped to HTTP 403 with the structured bilingual detail.
"""

from __future__ import annotations

import ast
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.revenue_os.market_proof_lifecycle import (
    ledger,
    record_transition,
    snapshot,
    state_machine_definition,
)

router = APIRouter(prefix="/api/v1/market-proof", tags=["market-proof"])


class TransitionEventBody(BaseModel):
    contact_id: str = Field(..., min_length=1)
    from_state: str = Field(..., min_length=1)
    to_state: str = Field(..., min_length=1)
    founder_confirmed: bool = False
    payment_confirmed: bool = False
    scope_or_intro_request: str | None = None
    evidence_ref: str | None = None
    doctrine_flags: dict[str, bool] = Field(default_factory=dict)


class TransitionRecordResponse(BaseModel):
    contact_id: str
    from_state: str
    to_state: str
    from_level: str | None
    to_level: str | None
    founder_confirmed: bool
    payment_confirmed: bool
    scope_or_intro_request: str | None
    evidence_ref: str | None
    revenue_counted: bool
    recorded_at: str


def _detail_from_value_error(exc: ValueError) -> Any:
    """Return a structured detail if the ValueError carries a dict, else its text."""
    text = str(exc)
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, dict):
            return parsed
    except (ValueError, SyntaxError):
        pass
    return text


@router.get("/stages")
async def get_stages() -> dict[str, Any]:
    """Return the state machine definition: states, levels, allowed transitions."""
    return state_machine_definition()


@router.post("/events", response_model=TransitionRecordResponse)
async def post_event(body: TransitionEventBody) -> dict[str, Any]:
    """Record a lifecycle transition.

    Guard-rule violations and doctrine breaches map to HTTP 403.
    """
    try:
        record = record_transition(
            body.contact_id,
            body.from_state,
            body.to_state,
            founder_confirmed=body.founder_confirmed,
            payment_confirmed=body.payment_confirmed,
            scope_or_intro_request=body.scope_or_intro_request,
            evidence_ref=body.evidence_ref,
            doctrine_flags=body.doctrine_flags,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=403,
            detail=_detail_from_value_error(exc),
        ) from exc
    return record


@router.get("/ledger")
async def get_ledger() -> dict[str, Any]:
    """Return the full append-only transition ledger."""
    return {"ledger": ledger()}


@router.get("/command-center/snapshot")
async def get_command_center_snapshot() -> dict[str, Any]:
    """Return L4/L5/L6/L7 counts, current state per contact, blocked items, revenue.

    Revenue stays 0 until a contact reaches invoice_paid.
    """
    return snapshot()
