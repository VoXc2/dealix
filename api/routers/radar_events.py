"""Radar Events HTTP surface (Phase 9).

  POST /api/v1/radar-events/record
  GET  /api/v1/radar-events/summary
  GET  /api/v1/radar-events/taxonomy
  GET  /api/v1/radar-events/status
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.radar_events import (
    EVENT_TYPES,
    list_recent,
    record_event,
    summary_metrics,
)
from auto_client_acquisition.radar_events.metrics import funnel_health

router = APIRouter(prefix="/api/v1/radar-events", tags=["radar-events"])

_HARD_GATES: dict[str, bool] = {
    "no_pii_in_event_payload": True,
    "redaction_on_insert": True,
    "no_external_analytics_dependency": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "radar_events",
        "version": "1.0.0",
        "event_types_count": len(EVENT_TYPES),
        "hard_gates": _HARD_GATES,
    }


@router.get("/taxonomy")
async def taxonomy() -> dict[str, Any]:
    return {
        "event_types": list(EVENT_TYPES),
        "count": len(EVENT_TYPES),
        "hard_gates": _HARD_GATES,
    }


@router.post("/record")
async def record(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    event_type = payload.get("event_type")
    if not event_type:
        raise HTTPException(status_code=422, detail="event_type required")
    customer_handle = payload.get("customer_handle")
    event_payload = payload.get("payload") or {}
    event = record_event(
        event_type=event_type,
        customer_handle=customer_handle,
        payload=event_payload,
    )
    return {"event": event, "hard_gates": _HARD_GATES}


@router.get("/summary")
async def summary(limit: int = 100) -> dict[str, Any]:
    s = summary_metrics()
    f = funnel_health()
    return {
        "summary": s,
        "funnel_health": f,
        "recent_count": len(list_recent(limit=limit)),
        "hard_gates": _HARD_GATES,
    }
