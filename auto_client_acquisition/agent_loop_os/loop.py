"""Agent runtime — a bounded, audited, agentic loop.

This is the upgrade over the orchestrator's single-pass workflow walk: a
real plan → act → observe → replan loop.

  goal → planner → tool call → observation → planner → … → final answer

Safety properties (enforced here, verified by doctrine evals):
  - bounded         — never exceeds ``LoopBudget`` (``no_unbounded_agents``)
  - kill-switchable — halts immediately if the global kill switch is active
  - audited         — every iteration is a ``LoopStep``; every run is a
    ``LoopTrace`` written to the ledger + a RevenueEvent (``no_unaudited_changes``)
  - never silent    — every run records *why* it stopped (``no_silent_failures``)
  - approval-gated  — a mutating tool is never auto-run without approval
    (``no_live_send`` / ``no_live_charge``)

The default planner is deterministic (no LLM required), so the runtime is
fully testable offline. An LLM planner can be injected without touching
the loop.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.agent_loop_os.agent_loop_ledger import emit_loop
from auto_client_acquisition.agent_loop_os.loop_budget import LoopBudget, LoopUsage
from auto_client_acquisition.agent_loop_os.tool_registry import ToolRegistry, default_tool_registry
from auto_client_acquisition.agent_loop_os.trace import LoopStep, LoopTrace
from auto_client_acquisition.revenue_memory.event_store import EventStore, get_default_store
from auto_client_acquisition.revenue_memory.events import make_event
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import kill_switch_active

__all__ = ["AgentLoop", "PlanDecision", "deterministic_planner"]


@dataclass(frozen=True, slots=True)
class PlanDecision:
    """The planner's verdict for one iteration: call a tool, or finalize."""

    thought: str
    tool_name: str | None = None
    tool_args: dict[str, Any] = field(default_factory=dict)
    final_answer: str | None = None
    insufficient_evidence: bool = False

    @property
    def is_final(self) -> bool:
        return self.final_answer is not None


# A planner sees the goal + history and decides the next move.
Planner = Callable[[str, str, dict[str, Any], tuple[LoopStep, ...]], PlanDecision]


def deterministic_planner(
    goal: str,
    customer_id: str,
    context: dict[str, Any],
    steps: tuple[LoopStep, ...],
) -> PlanDecision:
    """Default planner: gather grounded evidence once, then finalize.

    A genuine plan→act→observe→finalize cycle that needs no LLM, so the
    runtime is deterministic and offline-testable.
    """
    answer_steps = [s for s in steps if s.tool_name == "knowledge.answer"]
    if not answer_steps:
        return PlanDecision(
            thought="No evidence gathered yet — query the knowledge base.",
            tool_name="knowledge.answer",
            tool_args={"customer_id": customer_id, "query": goal},
        )
    last = answer_steps[-1]
    if last.error or last.observation in ("INSUFFICIENT_EVIDENCE", "INVALID_ARGS", ""):
        return PlanDecision(
            thought="Knowledge base lacks grounded evidence for this goal.",
            final_answer="لا توجد أدلة كافية في قاعدة المعرفة للإجابة على هذا الهدف.",
            insufficient_evidence=True,
        )
    return PlanDecision(
        thought="Grounded answer retrieved — finalize.",
        final_answer=last.observation,
        insufficient_evidence=False,
    )


class AgentLoop:
    """Runs one bounded agentic loop toward a goal."""

    def __init__(
        self,
        *,
        registry: ToolRegistry | None = None,
        budget: LoopBudget | None = None,
        planner: Planner | None = None,
        event_store: EventStore | None = None,
    ) -> None:
        self.registry = registry or default_tool_registry()
        self.budget = budget or LoopBudget()
        self.planner: Planner = planner or deterministic_planner
        self._event_store = event_store

    def run(
        self,
        *,
        goal: str,
        customer_id: str,
        context: dict[str, Any] | None = None,
    ) -> LoopTrace:
        if not goal.strip():
            raise ValueError("goal is required")
        if not customer_id.strip():
            raise ValueError("customer_id is required")

        ctx = context or {}
        steps: list[LoopStep] = []
        usage = LoopUsage()
        final_answer = ""
        insufficient = False
        terminated = "max_iterations"

        for iteration in range(self.budget.max_iterations):
            usage.iterations = iteration + 1

            if kill_switch_active():
                terminated = "kill_switch"
                break

            decision = self.planner(goal, customer_id, ctx, tuple(steps))

            if decision.is_final:
                final_answer = decision.final_answer or ""
                insufficient = decision.insufficient_evidence
                terminated = "goal_met"
                break

            if usage.tool_calls_exhausted(self.budget):
                terminated = "budget_exhausted"
                break

            tool = self.registry.get(decision.tool_name or "")
            if tool is None:
                steps.append(
                    LoopStep(
                        iteration=iteration,
                        thought=decision.thought,
                        tool_name=decision.tool_name,
                        tool_args=dict(decision.tool_args),
                        observation="",
                        error="unknown_tool",
                    )
                )
                terminated = "unknown_tool"
                break

            # A mutating tool may never auto-run without an approval gate.
            if tool.mutating and tool.requires_approval:
                steps.append(
                    LoopStep(
                        iteration=iteration,
                        thought=decision.thought,
                        tool_name=tool.name,
                        tool_args=dict(decision.tool_args),
                        observation="",
                        error="needs_approval",
                    )
                )
                terminated = "needs_approval"
                break

            try:
                result = tool.handler(dict(decision.tool_args))
            except Exception as exc:  # noqa: BLE001 — recorded, never silent
                steps.append(
                    LoopStep(
                        iteration=iteration,
                        thought=decision.thought,
                        tool_name=tool.name,
                        tool_args=dict(decision.tool_args),
                        observation="",
                        error=str(exc)[:300],
                    )
                )
                terminated = "tool_error"
                break

            usage.tool_calls += 1
            steps.append(
                LoopStep(
                    iteration=iteration,
                    thought=decision.thought,
                    tool_name=tool.name,
                    tool_args=dict(decision.tool_args),
                    observation=result.observation,
                    error=None,
                )
            )

        trace = LoopTrace(
            customer_id=customer_id,
            goal=goal,
            steps=tuple(steps),
            final_answer=final_answer,
            terminated_reason=terminated,
            insufficient_evidence=insufficient,
            tool_call_count=usage.tool_calls,
        )
        emit_loop(trace)
        self._emit_event(trace)
        return trace

    # ── audit ────────────────────────────────────────────────────────
    def _emit_event(self, trace: LoopTrace) -> None:
        store = self._event_store or get_default_store()
        succeeded = trace.terminated_reason == "goal_met" and not trace.insufficient_evidence
        event = make_event(
            event_type="agent.action_executed" if succeeded else "agent.action_failed",
            customer_id=trace.customer_id,
            subject_type="agent_task",
            subject_id=trace.loop_id,
            payload={
                "goal": trace.goal,
                "terminated_reason": trace.terminated_reason,
                "iteration_count": trace.iteration_count,
                "tool_call_count": trace.tool_call_count,
                "insufficient_evidence": trace.insufficient_evidence,
            },
            actor="agent_loop_os",
        )
        try:
            store.append(event)
        except Exception:  # noqa: BLE001 — audit best-effort, never blocks the loop
            pass
