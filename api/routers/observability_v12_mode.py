"""Observability v12 naming — delegates to observability_v10."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/observability-v12", tags=["observability-v12"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "observability_v12",
        "delegate": "observability_v10",
        "primary": "/api/v1/observability-v10/status",
        "trace_fields_recommended": [
            "trace_id",
            "agent_name",
            "os_type",
            "latency_ms",
            "cost_estimate",
            "safety_result",
            "action_mode",
            "redacted",
        ],
    }
