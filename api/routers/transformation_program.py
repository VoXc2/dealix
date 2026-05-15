"""Transformation Program router — the 45-day enterprise engagement.

Endpoints under /api/v1/transformation/:
    POST /start                  — start a 45-day program for an offering
    GET  /{program_run_id}       — full program state
    GET  /{program_run_id}/timeline  — day-indexed parallel-track view
    POST /{program_run_id}/advance   — move a workstream to a new state
    GET  /                       — list programs (optionally per customer)

No external sends. Every workstream advance is governance-reviewed.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_factory.transformation_program import (
    advance_workstream,
    get_program,
    list_programs,
    start_program,
    timeline,
)

router = APIRouter(prefix="/api/v1/transformation", tags=["transformation-program"])


class StartProgramBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1, max_length=120)
    offering_id: str = Field(..., min_length=1, max_length=64)
    tier_id: str = Field(..., min_length=1, max_length=64)
    duration_days: int = Field(default=45, ge=1, le=180)


class AdvanceBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workstream_name: str = Field(..., min_length=1)
    new_status: str = Field(..., min_length=1)
    outputs: dict[str, Any] | None = None
    notes: str = Field(default="", max_length=2000)


@router.post("/start")
async def start_transformation_program(body: StartProgramBody) -> dict[str, Any]:
    """Start a 45-day enterprise AI transformation program."""
    try:
        program = start_program(
            customer_id=body.customer_id,
            offering_id=body.offering_id,
            tier_id=body.tier_id,
            duration_days=body.duration_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {**program.to_dict(), "progress_pct": program.progress_pct}


@router.get("/")
async def list_transformation_programs(
    customer_id: str | None = Query(default=None),
) -> dict[str, Any]:
    """List transformation programs, optionally scoped to one customer."""
    programs = list_programs(customer_id=customer_id)
    return {
        "count": len(programs),
        "programs": [
            {**p.to_dict(), "progress_pct": p.progress_pct} for p in programs
        ],
    }


@router.get("/{program_run_id}")
async def get_transformation_program(program_run_id: str) -> dict[str, Any]:
    """Full program state."""
    program = get_program(program_run_id)
    if program is None:
        raise HTTPException(
            status_code=404, detail=f"unknown_program_run: {program_run_id}"
        )
    return {**program.to_dict(), "progress_pct": program.progress_pct}


@router.get("/{program_run_id}/timeline")
async def get_transformation_timeline(program_run_id: str) -> dict[str, Any]:
    """Day-indexed parallel-track timeline view."""
    try:
        return timeline(program_run_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/{program_run_id}/advance")
async def advance_transformation_workstream(
    program_run_id: str, body: AdvanceBody
) -> dict[str, Any]:
    """Move one workstream to a new lifecycle state."""
    try:
        program = advance_workstream(
            program_run_id=program_run_id,
            workstream_name=body.workstream_name,
            new_status=body.new_status,
            outputs=body.outputs,
            notes=body.notes,
        )
    except ValueError as e:
        detail = str(e)
        status = 404 if detail.startswith("unknown_program_run") else 422
        raise HTTPException(status_code=status, detail=detail) from e
    return {**program.to_dict(), "progress_pct": program.progress_pct}
