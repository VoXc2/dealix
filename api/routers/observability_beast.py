"""GenAI / ops observability schema — local counters stub (OTEL-aligned fields)."""
from __future__ import annotations

import os
import time
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/observability-beast", tags=["observability-beast"])

# In-process counters for demo; replace with OTEL exporter in production.
_COUNTERS: dict[str, int] = {
    "gen_ai.operations.total": 0,
    "gen_ai.tokens.prompt": 0,
    "gen_ai.tokens.completion": 0,
}


@router.get("/status")
async def obs_status() -> dict[str, Any]:
    return {
        "service": "observability_beast",
        "status": "operational",
        "schema_version": 1,
        "otel_gen_ai_metrics_reference": "gen_ai.client.token.usage",
        "fields": [
            "trace_id",
            "tenant_id",
            "agent_name",
            "operation_name",
            "model_name",
            "token_usage",
            "latency_ms",
            "cost_estimate",
            "tool_calls",
            "action_mode",
            "policy_result",
            "approval_status",
            "error_type",
            "redacted",
        ],
        "environment_sample": {
            "otel_exporter_configured": bool(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")),
        },
    }


@router.get("/sample-record")
async def sample_record() -> dict[str, Any]:
    """Example payload shape for dashboards — synthetic, no PII."""
    _COUNTERS["gen_ai.operations.total"] += 1
    return {
        "trace_id": f"trace-{int(time.time())}",
        "tenant_id": "redacted",
        "agent_name": "company_growth_beast",
        "operation_name": "draft_generation",
        "model_name": "stub",
        "token_usage": {"prompt": 0, "completion": 0},
        "latency_ms": 0,
        "cost_estimate_sar": 0.0,
        "tool_calls": 0,
        "action_mode": "draft_only",
        "policy_result": "allowed_read_only",
        "approval_status": "pending",
        "error_type": None,
        "redacted": True,
        "counters": dict(_COUNTERS),
    }
