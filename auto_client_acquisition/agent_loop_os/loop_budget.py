"""Loop budget — the hard ceiling that makes the agent bounded.

``no_unbounded_agents``: a loop may never run forever. ``LoopBudget`` caps
iterations, tool calls, and token spend. ``LoopUsage`` tracks consumption;
the loop stops the moment any ceiling is reached.
"""
from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.orchestrator.policies import BudgetLimit

__all__ = ["LoopBudget", "LoopUsage", "budget_from_policy_limit"]


@dataclass(frozen=True, slots=True)
class LoopBudget:
    """Per-loop ceilings. Defaults are deliberately conservative."""

    max_iterations: int = 8
    max_tool_calls: int = 16
    max_llm_tokens: int = 60_000

    def __post_init__(self) -> None:
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        if self.max_tool_calls < 1:
            raise ValueError("max_tool_calls must be >= 1")
        if self.max_llm_tokens < 0:
            raise ValueError("max_llm_tokens must be >= 0")


@dataclass
class LoopUsage:
    """Mutable consumption counters for a single loop run."""

    iterations: int = 0
    tool_calls: int = 0
    llm_tokens: int = 0

    def tool_calls_exhausted(self, budget: LoopBudget) -> bool:
        return self.tool_calls >= budget.max_tool_calls

    def tokens_exhausted(self, budget: LoopBudget) -> bool:
        return budget.max_llm_tokens > 0 and self.llm_tokens >= budget.max_llm_tokens


def budget_from_policy_limit(limit: BudgetLimit) -> LoopBudget:
    """Derive a per-loop budget from a customer's daily ``BudgetLimit`` so the
    orchestrator's daily caps and the loop's per-run caps stay consistent."""
    return LoopBudget(
        max_iterations=8,
        max_tool_calls=16,
        # A single loop may spend at most a tenth of the daily token budget.
        max_llm_tokens=max(1_000, limit.max_llm_tokens_per_day // 10),
    )
