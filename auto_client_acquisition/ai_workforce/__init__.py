"""AI Workforce compatibility layer over Dealix's five canonical agents.

The historical runtime exposes 12 specialist role handlers plus a 15-role
Revenue Factory blueprint. They remain bounded workloads delegated to
`dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, and
`dealix-content`; they are not a second permanent agent fleet.

Pure local composition: NO LLM, NO external HTTP, NO live send. External effects
remain governed by the canonical authority/consent/proof gates.
"""
from auto_client_acquisition.ai_workforce.agent_contracts import run_agent
from auto_client_acquisition.ai_workforce.agent_registry import AGENT_REGISTRY, get_agent, list_agents
from auto_client_acquisition.ai_workforce.canonical_delegation import (
    CANONICAL_AGENTS,
    REVENUE_SPECIALIST_DELEGATION,
    RUNTIME_SPECIALIST_DELEGATION,
    SPECIALIST_ROLE_SEMANTICS,
    canonical_owner_for,
)
from auto_client_acquisition.ai_workforce.canonical_revenue_factory import (
    build_canonical_revenue_factory_blueprint as build_revenue_factory_blueprint,
)
from auto_client_acquisition.ai_workforce.cost_guard import enforce_budget, estimate_cost
from auto_client_acquisition.ai_workforce.evidence_writer import record_evidence
from auto_client_acquisition.ai_workforce.language_router import pick_language
from auto_client_acquisition.ai_workforce.orchestrator import run_workforce_goal
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
    "CANONICAL_AGENTS",
    "REVENUE_SPECIALIST_DELEGATION",
    "RUNTIME_SPECIALIST_DELEGATION",
    "SPECIALIST_ROLE_SEMANTICS",
    "AgentSpec",
    "AgentTask",
    "AutonomyLevel",
    "RiskLevel",
    "WorkforceGoal",
    "WorkforceRun",
    "apply_policy",
    "build_revenue_factory_blueprint",
    "canonical_owner_for",
    "enforce_budget",
    "estimate_cost",
    "get_agent",
    "list_agents",
    "pick_language",
    "record_evidence",
    "route_for_goal",
    "run_agent",
    "run_workforce_goal",
    "summarize_risks",
]
