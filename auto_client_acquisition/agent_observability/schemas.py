"""Schemas for the agent_observability shim (Phase 11)."""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ActionMode = Literal[
    "draft_only",
    "approval_required",
    "approved_execute",
    "approved_manual",
    "blocked",
]


class AgentTrace(BaseModel):
    """Agent execution trace. Redacted on insert; never carries raw
    prompts, tool args/results, PII, or secrets. Unknown sensitivity
    => omit the field or record HOLD."""

    model_config = ConfigDict(extra="forbid")

    trace_id: str
    customer_handle: str | None = None
    agent_name: str
    workflow: str = ""
    action_mode: ActionMode
    input_kind: str = ""
    output_kind: str = ""
    latency_ms: int | None = None
    cost_estimate: float | None = None
    guardrail_result: str = "ok"
    approval_status: str = "pending"
    degraded: bool = False
    error_type: str | None = None
    # ── Omega5 execution-contract extensions (optional, backward compat) ──
    case_id: str = ""
    job_id: str = ""
    owner: str = ""
    effect_class: str = "none"
    authority: str = ""
    model_provider_class: str = ""
    tool_name: str = ""
    action_name: str = ""
    verifier: str = ""
    result: str = "unknown"
    cost_known_state: str = "unknown"
    evidence_refs: list[str] = Field(default_factory=list)
    release_sha: str = ""
    redacted_payload: dict[str, Any] = Field(default_factory=dict)
    safety_summary: str = "no_pii_no_secrets_no_full_transcripts"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
