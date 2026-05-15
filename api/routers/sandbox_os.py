"""System 29 — Enterprise Sandbox Engine router.

Create sandboxes, simulate workflows, run canaries and replay sandbox runs.
Every simulation is stubbed — production is never touched.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.sandbox_os.core import SandboxError, get_sandbox_engine
from auto_client_acquisition.sandbox_os.schemas import SandboxIsolation, SandboxStep

router = APIRouter(prefix="/api/v1/sandbox", tags=["sandbox"])


class SandboxBody(BaseModel):
    name: str = Field(..., min_length=1)
    isolation: SandboxIsolation = SandboxIsolation.FULL


class StepBody(BaseModel):
    step_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    inputs: dict[str, Any] = Field(default_factory=dict)


class SimulateBody(BaseModel):
    workflow_id: str = Field(..., min_length=1)
    steps: list[StepBody] = Field(default_factory=list)
    sandbox_id: str | None = None


class CanaryBody(BaseModel):
    workflow_id: str = Field(..., min_length=1)
    traffic_pct: float = Field(..., ge=0.0, le=100.0)


@router.post("/sandboxes", status_code=201)
async def create_sandbox(body: SandboxBody) -> dict[str, Any]:
    sandbox = get_sandbox_engine().create_sandbox(
        name=body.name, isolation=body.isolation
    )
    return sandbox.model_dump(mode="json")


@router.post("/simulate", status_code=201)
async def simulate(body: SimulateBody) -> dict[str, Any]:
    steps = [SandboxStep(**s.model_dump()) for s in body.steps]
    try:
        run = get_sandbox_engine().simulate(
            workflow_id=body.workflow_id, steps=steps, sandbox_id=body.sandbox_id
        )
    except SandboxError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return run.model_dump(mode="json")


@router.post("/canary", status_code=201)
async def canary(body: CanaryBody) -> dict[str, Any]:
    rollout = get_sandbox_engine().canary(
        workflow_id=body.workflow_id, traffic_pct=body.traffic_pct
    )
    return rollout.model_dump(mode="json")


@router.post("/replay/{run_id}")
async def replay(run_id: str) -> dict[str, Any]:
    try:
        result = get_sandbox_engine().replay(run_id)
    except SandboxError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result.model_dump(mode="json")


@router.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    run = get_sandbox_engine().get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"sandbox run not found: {run_id}")
    return run.model_dump(mode="json")
