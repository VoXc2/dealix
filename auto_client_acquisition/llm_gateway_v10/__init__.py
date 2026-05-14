"""LLM Gateway v10 — LiteLLM-style cost router.

Pure native Python. NO live LLM calls, NO external HTTP. The module
maps a ``RoutingPolicy`` (intent + language + bounds) onto a
``RoutingDecision`` (tier + cost estimate + bilingual reason) and
gates total spend with ``BudgetPolicy``.

Public API::

    from auto_client_acquisition.llm_gateway_v10 import (
        ModelTier,
        RoutingPolicy,
        BudgetPolicy,
        CostEstimate,
        RoutingDecision,
        route,
        estimate_cost,
        enforce_budget,
        route_with_text_audit,
        assert_agent_plan_includes_compliance_guard,
    )
"""
from auto_client_acquisition.llm_gateway_v10.budget_policy import enforce_budget
from auto_client_acquisition.llm_gateway_v10.governance_shim import (
    assert_agent_plan_includes_compliance_guard,
    route_with_text_audit,
)
from auto_client_acquisition.llm_gateway_v10.routing_policy import (
    estimate_cost,
    route,
)
from auto_client_acquisition.llm_gateway_v10.schemas import (
    BudgetPolicy,
    CostEstimate,
    ModelTier,
    RoutingDecision,
    RoutingPolicy,
)

__all__ = [
    "BudgetPolicy",
    "CostEstimate",
    "ModelTier",
    "RoutingDecision",
    "RoutingPolicy",
    "assert_agent_plan_includes_compliance_guard",
    "enforce_budget",
    "estimate_cost",
    "route",
    "route_with_text_audit",
]
