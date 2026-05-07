"""Case Study Engine HTTP surface.

  POST /api/v1/case-study/candidate    — check ≥1 publishable event
  POST /api/v1/case-study/build         — build a case study draft
  POST /api/v1/case-study/request-quote — flip to consent_requested
  POST /api/v1/case-study/approve       — final approval (after consent)
  GET  /api/v1/case-study/library       — paginated library

Hard rules: NO_PUBLISH_WITHOUT_CONSENT, NO_FAKE_PROOF, FORBIDDEN_TOKENS_SCRUB.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.case_study_engine import (
    approve_candidate,
    build_candidate,
    list_library,
    request_quote,
    select_publishable,
)

router = APIRouter(prefix="/api/v1/case-study", tags=["case-study-engine"])

_HARD_GATES: dict[str, bool] = {
    "no_fake_proof": True,
    "no_publish_without_consent": True,
    "no_publish_without_approval": True,
    "pii_redacted_required": True,
    "forbidden_tokens_scrubbed": True,
}


@router.post("/candidate")
async def candidate(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Check if a customer has enough publishable events for a case study."""
    events = payload.get("events", [])
    if not isinstance(events, list):
        raise HTTPException(status_code=422, detail="events must be a list")
    selection = select_publishable(events)
    return {
        **selection,
        "candidate": selection["publishable_count"] >= 1,
        "hard_gates": _HARD_GATES,
    }


@router.post("/build")
async def build(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    customer_handle = payload.get("customer_handle")
    events = payload.get("events", [])
    sector = payload.get("sector")
    objection = payload.get("objection_addressed")
    if not customer_handle or not events:
        raise HTTPException(
            status_code=422,
            detail="customer_handle + events list required",
        )
    try:
        result = build_candidate(
            customer_handle=customer_handle,
            events=events,
            sector=sector,
            objection_addressed=objection,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {**result, "hard_gates": _HARD_GATES}


@router.post("/request-quote")
async def request_quote_endpoint(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    candidate_id = payload.get("candidate_id")
    if not candidate_id:
        raise HTTPException(status_code=422, detail="candidate_id required")
    try:
        result = request_quote(candidate_id=candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {**result, "hard_gates": _HARD_GATES}


@router.post("/approve")
async def approve_endpoint(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    candidate_id = payload.get("candidate_id")
    approver = payload.get("approver")
    if not candidate_id or not approver:
        raise HTTPException(
            status_code=422,
            detail="candidate_id + approver required",
        )
    try:
        result = approve_candidate(candidate_id=candidate_id, approver=approver)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {**result, "hard_gates": _HARD_GATES}


@router.get("/library")
async def library(sector: str | None = None, limit: int = 50) -> dict[str, Any]:
    entries = list_library(sector=sector, limit=limit)
    return {
        "count": len(entries),
        "entries": entries,
        "hard_gates": _HARD_GATES,
    }
