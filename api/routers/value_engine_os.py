"""System 34 — Business Value Engine router.

Record workflow value metrics and read ROI. `measured` metrics must carry a
verifiable source_ref or the request is rejected (422).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.value_engine_os.core import (
    ValueDisciplineError,
    get_value_engine,
)
from auto_client_acquisition.value_engine_os.schemas import ValueTier

router = APIRouter(prefix="/api/v1/value-engine", tags=["value-engine"])


class MetricBody(BaseModel):
    run_id: str = Field(..., min_length=1)
    workflow_id: str = Field(..., min_length=1)
    revenue_impact_sar: float = 0.0
    time_saved_minutes: float = 0.0
    execution_speed_ms: float = 0.0
    efficiency_gain_pct: float = 0.0
    tier: ValueTier = ValueTier.ESTIMATED
    source_ref: str = ""


@router.post("/metrics", status_code=201)
async def record_metric(body: MetricBody) -> dict[str, Any]:
    try:
        metric = get_value_engine().record_metric(**body.model_dump())
    except ValueDisciplineError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return metric.model_dump(mode="json")


@router.get("/workflows/{workflow_id}/roi")
async def workflow_roi(
    workflow_id: str, period: str = "all-time", cost_sar: float = 0.0
) -> dict[str, Any]:
    report = get_value_engine().roi_for_workflow(
        workflow_id, period=period, cost_sar=cost_sar
    )
    return report.model_dump(mode="json")


@router.get("/optimization-candidates")
async def optimization_candidates(efficiency_threshold: float = 20.0) -> dict[str, Any]:
    candidates = get_value_engine().optimization_candidates(
        efficiency_threshold=efficiency_threshold
    )
    return {"count": len(candidates), "workflow_ids": candidates}
