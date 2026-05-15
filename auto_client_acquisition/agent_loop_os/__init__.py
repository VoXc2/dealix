"""Agent Loop OS — the bounded, audited, agentic runtime.

Upgrades the single-pass orchestrator with a real plan→act→observe→replan
loop: tools, iteration, budget ceilings, kill switch, and full per-step
audit traces.
"""

from auto_client_acquisition.agent_loop_os.agent_loop_ledger import (
    clear_for_test,
    emit_loop,
    list_loops,
)
from auto_client_acquisition.agent_loop_os.loop import AgentLoop, PlanDecision, deterministic_planner
from auto_client_acquisition.agent_loop_os.loop_budget import (
    LoopBudget,
    LoopUsage,
    budget_from_policy_limit,
)
from auto_client_acquisition.agent_loop_os.orchestrator_bridge import (
    AGENTIC_RESOLVE_ACTION,
    agentic_resolve_executor,
    register_agent_loop_executor,
)
from auto_client_acquisition.agent_loop_os.tool_registry import (
    Tool,
    ToolRegistry,
    ToolResult,
    default_tool_registry,
)
from auto_client_acquisition.agent_loop_os.trace import LoopStep, LoopTrace, trace_valid

__all__ = [
    "AGENTIC_RESOLVE_ACTION",
    "AgentLoop",
    "LoopBudget",
    "LoopStep",
    "LoopTrace",
    "LoopUsage",
    "PlanDecision",
    "Tool",
    "ToolRegistry",
    "ToolResult",
    "agentic_resolve_executor",
    "budget_from_policy_limit",
    "clear_for_test",
    "default_tool_registry",
    "deterministic_planner",
    "emit_loop",
    "list_loops",
    "register_agent_loop_executor",
    "trace_valid",
]
