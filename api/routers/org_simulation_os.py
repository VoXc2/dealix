"""System 32 — Organizational Simulation Engine router.

Simulate workflow / failure / approval / scale / incident scenarios.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.org_simulation_os.core import (
    SimulationError,
    get_org_simulator,
)
from auto_client_acquisition.org_simulation_os.schemas import (
    ScenarioKind,
    SimulationScenario,
)

router = APIRouter(prefix="/api/v1/org-simulation", tags=["org-simulation"])


class SimulateBody(BaseModel):
    kind: ScenarioKind
    parameters: dict[str, Any] = Field(default_factory=dict)


@router.post("/simulate", status_code=201)
async def simulate(body: SimulateBody) -> dict[str, Any]:
    scenario = SimulationScenario(kind=body.kind, parameters=body.parameters)
    try:
        result = get_org_simulator().simulate(scenario)
    except SimulationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return result.model_dump(mode="json")


@router.get("/results/{scenario_id}")
async def get_result(scenario_id: str) -> dict[str, Any]:
    result = get_org_simulator().get_result(scenario_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"scenario not found: {scenario_id}")
    return result.model_dump(mode="json")


@router.get("/scenarios")
async def list_scenarios() -> dict[str, Any]:
    scenarios = get_org_simulator().list_scenarios()
    return {"count": len(scenarios), "scenario_ids": scenarios}
