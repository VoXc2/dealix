"""Customer Loop v5 — read-only routes over the journey state machine.

No external send. No live charge. Each ``advance`` returns the next
checklist for a HUMAN to execute.
"""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.customer_loop import (
    JourneyAdvanceRequest,
    JourneyState,
    advance,
    list_states,
    next_actions_for_state,
)

router = APIRouter(prefix="/api/v1/customer-loop", tags=["customer-loop"])


@router.get("/status")
async def customer_loop_status() -> dict:
    """Health probe + safety guardrails."""
    return {
        "module": "customer_loop",
        "states_total": len([s for s in JourneyState]),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
            "all_advances_return_human_checklists": True,
        },
    }


@router.get("/states")
async def get_states() -> dict:
    """Catalog of all states + their allowed transitions + bilingual checklists."""
    return list_states()


@router.get("/states/{state}")
async def get_one_state(state: str) -> dict:
    """Bilingual checklist for one state."""
    try:
        s = JourneyState(state)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return next_actions_for_state(s)


@router.post("/journey/advance")
async def journey_advance(payload: dict = Body(...)) -> dict:
    """Advance the journey by one transition.

    Body must be a ``JourneyAdvanceRequest``: current_state,
    target_state, customer_handle (optional), service_id (optional),
    payload (optional dict).

    Returns the JourneyAdvanceResult — including a rejection_reason
    if the transition isn't allowed by the state machine.
    """
    try:
        req = JourneyAdvanceRequest(**payload)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"invalid payload: {exc}"
        ) from exc
    result = advance(req)
    return result.model_dump(mode="json")
