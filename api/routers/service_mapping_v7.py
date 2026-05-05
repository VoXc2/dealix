"""Service Mapping v7 Router — goal → recommended Dealix service.

Endpoints under /api/v1/services/:
    POST /recommend-v7  — body MapRequest → ServiceRecommendation
    GET  /value-ladder  — the 7-rung founder pitch ladder

Pure local composition: no LLM calls, no external HTTP, no live sends.
Every recommendation is tagged ``approval_required=True``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.service_mapping_v7 import (
    MapRequest,
    map_goal_to_service,
    value_ladder,
)

router = APIRouter(prefix="/api/v1/services", tags=["service-mapping-v7"])


@router.post("/recommend-v7")
async def recommend_v7(payload: MapRequest) -> dict[str, Any]:
    """Map a customer goal + pain points to a recommended service."""
    rec = map_goal_to_service(payload)
    return rec.model_dump(mode="json")


@router.get("/value-ladder")
async def get_value_ladder() -> dict[str, Any]:
    """Return the 7-rung value ladder used by the founder pitch."""
    rungs = value_ladder()
    return {"rungs": rungs, "n_rungs": len(rungs)}
