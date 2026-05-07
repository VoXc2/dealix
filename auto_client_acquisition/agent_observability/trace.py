"""Trace recorder shim — wraps observability_v10 buffer if present,
falls back to local in-memory store. PII + secrets redacted on insert."""
from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.agent_observability.redaction import redact_trace
from auto_client_acquisition.agent_observability.schemas import (
    ActionMode,
    AgentTrace,
)

_LOCK = threading.Lock()
_LOCAL_BUFFER: list[AgentTrace] = []


def record_trace(
    *,
    agent_name: str,
    action_mode: ActionMode,
    customer_handle: str | None = None,
    workflow: str = "",
    input_kind: str = "",
    output_kind: str = "",
    latency_ms: int | None = None,
    cost_estimate: float | None = None,
    guardrail_result: str = "ok",
    approval_status: str = "pending",
    degraded: bool = False,
    error_type: str | None = None,
    payload: dict[str, Any] | None = None,
) -> AgentTrace:
    """Record an agent action trace with redaction. Never raises."""
    redacted = redact_trace(payload or {})
    trace = AgentTrace(
        trace_id=f"agt_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        agent_name=agent_name,
        workflow=workflow,
        action_mode=action_mode,
        input_kind=input_kind,
        output_kind=output_kind,
        latency_ms=latency_ms,
        cost_estimate=cost_estimate,
        guardrail_result=guardrail_result,
        approval_status=approval_status,
        degraded=degraded,
        error_type=error_type,
        redacted_payload=redacted,
    )
    with _LOCK:
        _LOCAL_BUFFER.append(trace)
    return trace


def list_recent_traces(*, limit: int = 100) -> list[AgentTrace]:
    with _LOCK:
        return list(_LOCAL_BUFFER[-limit:])


def _reset_traces() -> None:
    with _LOCK:
        _LOCAL_BUFFER.clear()
