"""AI Workforce v7 Phase 1 + Phase 2 orchestrator.

Wires the 12 specialized agents over the existing v5/v6 layers. Pure
local composition: NO LLM, NO external HTTP, NO live send. Each agent
is a thin wrapper over an existing v5/v6 function with hard autonomy
limits and a final ComplianceGuard veto pass.

Public API:
    from auto_client_acquisition.ai_workforce import (
        AgentSpec, AgentTask, AutonomyLevel, RiskLevel,
        WorkforceGoal, WorkforceRun,
        AGENT_REGISTRY, list_agents, get_agent,
        route_for_goal, run_agent, apply_policy,
        run_workforce_goal,
        estimate_cost, enforce_budget,
        summarize_risks, record_evidence, pick_language,
    )
"""
from auto_client_acquisition.ai_workforce.agent_contracts import run_agent
from auto_client_acquisition.ai_workforce.agent_registry import (
    AGENT_REGISTRY,
    get_agent,
    list_agents,
)
from auto_client_acquisition.ai_workforce.cost_guard import (
    enforce_budget,
    estimate_cost,
)
from auto_client_acquisition.ai_workforce.evidence_writer import record_evidence
from auto_client_acquisition.ai_workforce.language_router import pick_language
from auto_client_acquisition.ai_workforce.orchestrator import run_workforce_goal
from auto_client_acquisition.ai_workforce.revenue_factory_blueprint import (
    build_revenue_factory_blueprint,
)
from auto_client_acquisition.ai_workforce.risk_guard import summarize_risks
from auto_client_acquisition.ai_workforce.schemas import (
    AgentSpec,
    AgentTask,
    AutonomyLevel,
    RiskLevel,
    WorkforceGoal,
    WorkforceRun,
)
from auto_client_acquisition.ai_workforce.task_router import route_for_goal
from auto_client_acquisition.ai_workforce.workforce_policy import apply_policy

__all__ = [
    "AGENT_REGISTRY",
    "AgentSpec",
    "AgentTask",
    "AutonomyLevel",
    "RiskLevel",
    "WorkforceGoal",
    "WorkforceRun",
    "apply_policy",
    "enforce_budget",
    "estimate_cost",
    "get_agent",
    "list_agents",
    "pick_language",
    "record_evidence",
    "route_for_goal",
    "run_agent",
    "run_workforce_goal",
    "build_revenue_factory_blueprint",
    "summarize_risks",
]
