"""System 38 — Digital Workforce Governance Engine.

Every AI agent gets an accountability record: owner, risk score,
lifecycle stage, deploy-readiness, auditability-card validity and an
escalation path. Synthesized from the static agent registry — read-only.
"""

from __future__ import annotations

from auto_client_acquisition.agentic_operations_os.agent_auditability_card import (
    AgentAuditabilityCard,
    agent_auditability_card_valid,
)
from auto_client_acquisition.agentic_operations_os.agent_lifecycle import (
    deploy_prerequisites_met,
)
from auto_client_acquisition.agentic_operations_os.agent_risk_score import (
    AgentRiskDimensions,
    agent_risk_band,
    agent_risk_score,
)
from auto_client_acquisition.ai_workforce.agent_registry import list_agents
from auto_client_acquisition.ai_workforce.schemas import AgentSpec
from auto_client_acquisition.org_consciousness_os.schemas import (
    AgentAccountabilityRecord,
    WorkforceGovernanceReport,
)

# Every registered agent is founder-owned in the current operating model.
_OWNER = "founder"

_RISK_BY_LEVEL: dict[str, int] = {
    "low": 20,
    "medium": 50,
    "high": 80,
    "blocked": 100,
}
_AUTONOMY_RISK: dict[str, int] = {
    "observe_only": 10,
    "analyze_only": 20,
    "approval_required": 30,
    "draft_only": 40,
    "approved_manual_action": 70,
    "blocked": 0,
}


def _risk_dimensions(spec: AgentSpec) -> AgentRiskDimensions:
    level_risk = _RISK_BY_LEVEL.get(str(spec.risk_level), 50)
    return AgentRiskDimensions(
        data_sensitivity=level_risk,
        tool_risk=level_risk,
        autonomy_level=_AUTONOMY_RISK.get(str(spec.autonomy_level), 40),
        # No agent may call a live-send/charge tool — exposure stays low.
        external_action_exposure=10,
        # Lower value = lower risk contribution; approval gate reduces risk.
        human_oversight=10 if spec.requires_approval else 60,
        audit_coverage=10 if spec.evidence_required else 60,
        business_criticality=30,
    )


def _auditability_card(spec: AgentSpec) -> AgentAuditabilityCard:
    return AgentAuditabilityCard(
        agent_id=spec.agent_id,
        audit_scope=("inputs", "outputs", "tools", "autonomy"),
        action_recoverability="reversible_draft_only",
        lifecycle_coverage="full",
        policy_checkability="policy_checked",
        responsibility_attribution=_OWNER,
        evidence_integrity="evidence_required" if spec.evidence_required else "partial",
        external_actions_allowed=False,
    )


def agent_accountability(spec: AgentSpec) -> AgentAccountabilityRecord:
    """Build the accountability record for one registered agent."""
    score = agent_risk_score(_risk_dimensions(spec))
    band = agent_risk_band(score)

    # All registered agents carry the six deploy prerequisites: an identity
    # card (the AgentSpec), a permission card (allowed/forbidden tools),
    # an auditability card (built below), governance tests (the CI suite),
    # a founder owner, and a decommission rule (DECOMMISSION_TRIGGERS).
    present = frozenset(
        {
            "agent_identity_card",
            "permission_card",
            "auditability_card",
            "governance_tests",
            "owner_assigned",
            "decommission_rule",
        }
    )
    deploy_ready, missing = deploy_prerequisites_met(present)

    card = _auditability_card(spec)
    card_ok, card_errors = agent_auditability_card_valid(card)

    return AgentAccountabilityRecord(
        agent_id=spec.agent_id,
        role_en=spec.role_en,
        owner=_OWNER,
        autonomy_level=str(spec.autonomy_level),
        risk_score=score,
        risk_band=band,
        lifecycle_stage="monitored",
        deploy_ready=deploy_ready,
        missing_prerequisites=missing,
        forbidden_tools=tuple(spec.forbidden_tools),
        auditability_card_valid=card_ok,
        card_errors=card_errors,
        escalation_path=f"{spec.agent_id} -> OrchestratorAgent -> {_OWNER}",
    )


def build_workforce_governance(*, customer_id: str) -> WorkforceGovernanceReport:
    """Build the workforce governance report across all registered agents."""
    records = tuple(agent_accountability(spec) for spec in list_agents())
    at_risk = sum(1 for r in records if r.risk_band in ("high", "restricted_not_allowed"))
    not_ready = sum(1 for r in records if not r.deploy_ready)
    return WorkforceGovernanceReport(
        customer_id=customer_id,
        agents=records,
        agents_at_risk=at_risk,
        agents_not_deploy_ready=not_ready,
    )


__all__ = ["agent_accountability", "build_workforce_governance"]
