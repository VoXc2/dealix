"""Observability v10 router — trace schema + record endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from auto_client_acquisition.observability_v10 import (
    TraceRecordV10,
    list_v10_traces,
    record_v10_trace,
    validate_trace,
)

router = APIRouter(prefix="/api/v1/observability-v10", tags=["observability-v10"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "observability_v10",
        "guardrails": {
            "no_external_http": True,
            "pii_redacted_on_insert": True,
            "otel_aligned": True,
            "append_only": True,
            "thread_safe": True,
        },
    }


@router.post("/trace/validate")
async def trace_validate(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        validated = validate_trace(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return validated.model_dump(mode="json")


@router.post("/trace/record")
async def trace_record(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        stored = record_v10_trace(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return stored.model_dump(mode="json")


@router.get("/traces")
async def traces(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, Any]:
    rows = list_v10_traces(limit=limit)
    return {"count": len(rows), "traces": [r.model_dump(mode="json") for r in rows]}


@router.get("/schema")
async def schema() -> dict[str, Any]:
    return TraceRecordV10.model_json_schema()
