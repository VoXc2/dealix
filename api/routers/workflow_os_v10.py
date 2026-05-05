"""Workflow OS v10 — state-machine endpoints (no live action)."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.workflow_os_v10 import (
    ALLOWED_TRANSITIONS,
    GROWTH_STARTER_7_DAY,
    MINI_DIAGNOSTIC,
    PROOF_PACK_ASSEMBLY,
    advance_workflow,
    get_definition,
    get_run,
    list_definitions,
    register_definition,
    restore_checkpoint,
    save_checkpoint,
    start_workflow,
)


def _ensure_canonical_definitions_registered() -> None:
    """Re-register the three pre-defined workflows on every request.

    Tests may call ``_reset_workflow_buffer()`` between cases; this
    guard keeps the API endpoints stable regardless.
    """
    register_definition(GROWTH_STARTER_7_DAY)
    register_definition(PROOF_PACK_ASSEMBLY)
    register_definition(MINI_DIAGNOSTIC)

router = APIRouter(prefix="/api/v1/workflow-os-v10", tags=["workflow-os-v10"])


class StartWorkflowRequest(BaseModel):
    """Body for POST /start."""

    model_config = ConfigDict(extra="forbid")

    workflow_id: str = Field(..., min_length=1)
    customer_handle: str = Field(default="Saudi B2B customer", min_length=1)


@router.get("/status")
async def status() -> dict:
    _ensure_canonical_definitions_registered()
    return {
        "module": "workflow_os_v10",
        "definitions_total": len(list_definitions()),
        "states": sorted({s for src in ALLOWED_TRANSITIONS for s in (src,)} | {
            t for src in ALLOWED_TRANSITIONS for t in ALLOWED_TRANSITIONS[src]
        }),
        "guardrails": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_linkedin_automation": True,
            "approval_required_for_external_actions": True,
            "idempotency_enforced": True,
            "retry_budget_enforced": True,
            "checkpoint_supported": True,
        },
    }


@router.get("/definitions")
async def get_definitions() -> dict:
    _ensure_canonical_definitions_registered()
    defs = list_definitions()
    return {
        "total": len(defs),
        "definitions": [d.to_dict() for d in defs],
    }


@router.post("/start")
async def start(payload: StartWorkflowRequest) -> dict:
    _ensure_canonical_definitions_registered()
    try:
        definition = get_definition(payload.workflow_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    run = start_workflow(definition, customer_handle=payload.customer_handle)
    return run.to_dict()


@router.post("/{run_id}/advance")
async def advance(run_id: str, payload: dict = Body(...)) -> dict:
    step_name = payload.get("step_name")
    idempotency_key = payload.get("idempotency_key")
    result = payload.get("result") or {}
    if not step_name or not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail="step_name and idempotency_key are required",
        )
    try:
        run = get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    try:
        run = advance_workflow(
            run,
            step_name=step_name,
            idempotency_key=idempotency_key,
            result=dict(result) if isinstance(result, dict) else {},
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return run.to_dict()


@router.get("/{run_id}")
async def get_run_endpoint(run_id: str) -> dict:
    try:
        run = get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return run.to_dict()


@router.post("/{run_id}/checkpoint")
async def checkpoint(run_id: str) -> dict:
    try:
        run = get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"checkpoint": save_checkpoint(run)}


@router.post("/{run_id}/restore")
async def restore(run_id: str, payload: dict = Body(...)) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="body must be a JSON object")
    try:
        run = restore_checkpoint(payload)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return run.to_dict()
