"""Bridge: expose the agent runtime as an orchestrator executor.

The orchestrator dispatches a ``WorkflowStep`` whose ``action_type`` is
``"agentic_resolve"`` to this executor. Approval + budget gating already
flow through the orchestrator's existing ``requires_approval`` /
``within_budget`` checks — this bridge adds the agentic loop without
restructuring the runtime.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.agent_loop_os.loop import AgentLoop
from auto_client_acquisition.orchestrator.queue import AgentTask

__all__ = ["AGENTIC_RESOLVE_ACTION", "agentic_resolve_executor", "register_agent_loop_executor"]

AGENTIC_RESOLVE_ACTION = "agentic_resolve"


def _extract_goal(payload: dict[str, Any]) -> str:
    inputs = payload.get("inputs", {}) or {}
    candidates = [
        payload.get("goal"),
        inputs.get("goal"),
        (inputs.get("initial", {}) or {}).get("goal"),
    ]
    for c in candidates:
        if isinstance(c, str) and c.strip():
            return c.strip()
    return ""


def agentic_resolve_executor(task: AgentTask) -> dict[str, Any]:
    """Run a bounded agent loop for the task's goal; return the trace dict."""
    goal = _extract_goal(task.payload or {})
    if not goal:
        return {"error": "no_goal_provided", "terminated_reason": "tool_error"}
    trace = AgentLoop().run(
        goal=goal,
        customer_id=task.customer_id,
        context=(task.payload or {}).get("inputs", {}) or {},
    )
    return trace.to_dict()


def register_agent_loop_executor(registry: dict[str, Any]) -> dict[str, Any]:
    """Add the ``agentic_resolve`` executor to an executor registry in place."""
    registry[AGENTIC_RESOLVE_ACTION] = agentic_resolve_executor
    return registry
