"""Pydantic v2 schemas for observability_v10.

Extends the v6 trace contract with cost + risk + model fields,
inspired by the Langfuse + OpenTelemetry trace shapes. Pure
in-memory; no external telemetry exporter.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class TraceRecordV10(BaseModel):
    """A single rich trace record (cost + risk + model aware).

    ``redacted_payload`` is expected to be PII-redacted *before*
    insert via :func:`trace_schema.validate_trace`. The buffer also
    re-runs the redactor on insert as a defence-in-depth measure.
    """

    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(default_factory=lambda: f"trc_{uuid4().hex[:16]}")
    correlation_id: str
    customer_id: str = ""
    agent_id: str = ""
    workflow_id: str = ""
    action_mode: str = "draft_only"
    approval_status: str = "pending"
    risk_level: str = "low"
    model_name: str = ""
    prompt_version: str = ""
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    latency_ms: float = Field(default=0.0, ge=0.0)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    proof_event_id: str = ""
    redacted_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SpanRecord(BaseModel):
    """OpenTelemetry-aligned span — children of a trace."""

    model_config = ConfigDict(extra="forbid")

    span_id: str = Field(default_factory=lambda: f"spn_{uuid4().hex[:16]}")
    trace_id: str
    name: str
    start_ms: float = Field(ge=0.0)
    end_ms: float = Field(ge=0.0)
    attributes: dict[str, Any] = Field(default_factory=dict)
    status: Literal["ok", "blocked", "error"] = "ok"
