"""Agent run trace — observability scaffold (pure, no I/O).
أثر تشغيل الوكيل — هيكل المراقبة (نقي، بدون إدخال/إخراج).

Contract for capturing a single agent run: latency, tool calls, retries,
escalations, and a token-usage placeholder. No live capture in the scaffold.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TraceStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    FAILED = "failed"


class AgentStepRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(..., min_length=1)
    step_index: int = Field(default=0, ge=0)
    tool_called: str = ""
    latency_ms: float = Field(default=0.0, ge=0.0)
    retries: int = Field(default=0, ge=0)
    escalated: bool = False
    token_usage: int = Field(default=0, ge=0)
    note: str = ""


class AgentRunTrace(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    trace_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    status: TraceStatus = TraceStatus.STARTED
    steps: list[AgentStepRecord] = Field(default_factory=list)
    total_latency_ms: float = Field(default=0.0, ge=0.0)
    escalation_count: int = Field(default=0, ge=0)


def new_trace(trace_id: str, agent_id: str) -> AgentRunTrace:
    """Return an empty trace in the ``STARTED`` state."""
    return AgentRunTrace(trace_id=trace_id, agent_id=agent_id, status=TraceStatus.STARTED)


def append_step(trace: AgentRunTrace, step: AgentStepRecord) -> AgentRunTrace:
    """Return a NEW trace with ``step`` appended and totals recomputed.

    # LATER WAVE: wire to the ``agent_observability`` module and the
    # ``orchestrator.queue`` task statuses; populate ``token_usage`` from
    # ``llm_gateway_v10``.
    """
    steps = [*trace.steps, step]
    return AgentRunTrace(
        trace_id=trace.trace_id,
        agent_id=trace.agent_id,
        status=trace.status,
        steps=steps,
        total_latency_ms=sum(s.latency_ms for s in steps),
        escalation_count=sum(1 for s in steps if s.escalated),
    )


def summarize_trace(trace: AgentRunTrace) -> dict:
    """Return a small counts / escalation-rate summary."""
    step_count = len(trace.steps)
    return {
        "trace_id": trace.trace_id,
        "agent_id": trace.agent_id,
        "step_count": step_count,
        "total_latency_ms": trace.total_latency_ms,
        "escalation_count": trace.escalation_count,
        "escalation_rate": (
            float(trace.escalation_count) / float(step_count) if step_count else 0.0
        ),
    }


__all__ = [
    "AgentRunTrace",
    "AgentStepRecord",
    "TraceStatus",
    "append_step",
    "new_trace",
    "summarize_trace",
]
