"""Schemas for the agent_observability shim (Phase 11)."""
from __future__ import annotations

from datetime import datetime, timezone
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
    redacted_payload: dict[str, Any] = Field(default_factory=dict)
    safety_summary: str = "no_pii_no_secrets_no_full_transcripts"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
