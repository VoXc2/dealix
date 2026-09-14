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

    Omega5 execution contract (all optional, backward compatible):
    never store raw prompts / tool args / raw results or PII/secrets
    in ``redacted_payload``. Unknown sensitivity => omit the field or
    record ``HOLD``. Semantic fields are OpenTelemetry-compatible
    (trace_id/correlation + span-style attributes).
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
    # ── Omega5 execution-contract extensions (optional) ──────────
    # case/job identity (one or both may be set; correlation_id stays canonical)
    case_id: str = ""
    job_id: str = ""
    # human-readable owner / logical agent (Agentic Holding logical name;
    # agent_id remains the machine key; legacy executor names are aliases only)
    owner: str = ""
    # effect class / authority: effect_class in {none,read,draft,
    # internal_execute,repo_execute,material}; authority in {L0..L5,HOLD}
    effect_class: Literal["none", "read", "draft", "internal_execute", "repo_execute", "material"] = "none"
    authority: str = ""
    # model/provider class WITHOUT secrets (e.g. local-loopback,
    # trusted-remote-metered, unknown). Never a key, endpoint secret, or prompt.
    model_provider_class: str = ""
    # tool/action executed (names only; args are never stored by default)
    tool_name: str = ""
    action_name: str = ""
    # independent verifier identity (name/role only) + inspectable result
    verifier: str = ""
    result: Literal["ok", "blocked", "error", "hold", "unknown"] = "unknown"
    # latency/cost known-state: known | estimated | unknown
    cost_known_state: Literal["known", "estimated", "unknown"] = "unknown"
    # evidence references (receipt paths, proof event ids, digest refs — no payloads)
    evidence_refs: list[str] = Field(default_factory=list)
    # release SHA the emitting code ran from (exact-head identity, not a claim)
    release_sha: str = ""
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
