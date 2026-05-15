"""Agent loop trace — the per-iteration audit record.

Every loop produces exactly one ``LoopTrace`` with one ``LoopStep`` per
iteration. Nothing the loop does is unaudited (``no_unaudited_changes``)
and every loop records *why* it stopped (``no_silent_failures``).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

__all__ = ["LoopStep", "LoopTrace", "TERMINATION_REASONS"]

# Every reason a loop can stop. A trace always carries one of these.
TERMINATION_REASONS: tuple[str, ...] = (
    "goal_met",
    "max_iterations",
    "budget_exhausted",
    "tool_error",
    "unknown_tool",
    "kill_switch",
    "needs_approval",
)


@dataclass(frozen=True, slots=True)
class LoopStep:
    """One plan→act→observe iteration."""

    iteration: int
    thought: str
    tool_name: str | None
    tool_args: dict[str, Any]
    observation: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LoopTrace:
    """The complete, immutable record of one agent loop."""

    loop_id: str = field(default_factory=lambda: f"loop_{uuid4().hex[:16]}")
    customer_id: str = ""
    goal: str = ""
    steps: tuple[LoopStep, ...] = ()
    final_answer: str = ""
    terminated_reason: str = "max_iterations"
    insufficient_evidence: bool = False
    tool_call_count: int = 0
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def iteration_count(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict[str, Any]:
        return {
            "loop_id": self.loop_id,
            "customer_id": self.customer_id,
            "goal": self.goal,
            "steps": [s.to_dict() for s in self.steps],
            "final_answer": self.final_answer,
            "terminated_reason": self.terminated_reason,
            "insufficient_evidence": self.insufficient_evidence,
            "tool_call_count": self.tool_call_count,
            "iteration_count": self.iteration_count,
            "occurred_at": self.occurred_at,
        }


def trace_valid(trace: LoopTrace) -> bool:
    """A trace is valid iff it identifies a tenant and stopped for a known
    reason — used by the doctrine evals."""
    return bool(
        trace.loop_id.strip()
        and trace.customer_id.strip()
        and trace.terminated_reason in TERMINATION_REASONS
    )
