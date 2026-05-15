"""Observability v6 — read-only trace/audit + incident endpoints."""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query

from auto_client_acquisition.observability_v6 import (
    Incident,
    IncidentSeverity,
    list_audit,
    list_incidents,
    record_incident,
)

router = APIRouter(prefix="/api/v1/observability", tags=["observability-v6"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "observability_v6",
        "guardrails": {
            "no_external_telemetry": True,
            "no_pii_in_audit": True,
            "append_only": True,
            "thread_safe": True,
        },
    }


@router.get("/audit")
async def audit(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, Any]:
    events = list_audit(limit=limit)
    return {"count": len(events), "events": [e.model_dump(mode="json") for e in events]}


@router.get("/incidents")
async def incidents(
    severity: IncidentSeverity | None = Query(default=None),
) -> dict[str, Any]:
    items = list_incidents(severity_filter=severity)
    return {
        "count": len(items),
        "severity_filter": severity.value if severity else None,
        "incidents": [inc.model_dump(mode="json") for inc in items],
    }


@router.post("/incident")
async def file_incident(payload: Incident) -> dict[str, Any]:
    try:
        stored = record_incident(payload)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return stored.model_dump(mode="json")
