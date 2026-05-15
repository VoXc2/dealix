"""Governed routing shim — wraps llm_gateway_v10.route with compliance checks."""

from __future__ import annotations

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.llm_gateway_v10.routing_policy import route
from auto_client_acquisition.llm_gateway_v10.schemas import RoutingDecision, RoutingPolicy


def route_with_text_audit(
    policy: RoutingPolicy,
    *,
    draft_text_to_scan: str = "",
) -> tuple[RoutingDecision, list[str]]:
    """Return routing decision plus ``audit_draft_text`` issues for optional copy."""
    decision = route(policy)
    issues = audit_draft_text(draft_text_to_scan) if draft_text_to_scan else []
    return decision, issues


def assert_agent_plan_includes_compliance_guard(agent_ids: list[str]) -> list[str]:
    """Enforce ComplianceGuardAgent as final step in ordered agent plans."""
    if not agent_ids:
        raise ValueError("agent_ids must be non-empty")
    if agent_ids[-1] != "ComplianceGuardAgent":
        raise ValueError("last agent must be ComplianceGuardAgent")
    return agent_ids
