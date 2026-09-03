"""Canonical Dealix agent delegation for legacy AI Workforce specialist roles.

The historical AI Workforce and Revenue Factory modules expose useful specialist
roles. They are bounded workloads delegated to the five canonical Dealix agents;
they are not a second permanent agent fleet, truth owner, scheduler, or approval
authority.
"""
from __future__ import annotations

CANONICAL_AGENTS: tuple[str, ...] = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)

SPECIALIST_ROLE_SEMANTICS = "BOUNDED_WORKLOAD_NOT_PERMANENT_AGENT"

RUNTIME_SPECIALIST_DELEGATION: dict[str, str] = {
    "OrchestratorAgent": "dealix-pm",
    "CompanyBrainAgent": "dealix-pm",
    "MarketRadarAgent": "dealix-sales",
    "SalesStrategistAgent": "dealix-sales",
    "SaudiCopyAgent": "dealix-content",
    "PartnershipAgent": "dealix-content",
    "DeliveryAgent": "dealix-delivery",
    "ProofAgent": "dealix-delivery",
    "ComplianceGuardAgent": "dealix-engineer",
    "ExecutiveBriefAgent": "dealix-pm",
    "FinanceAgent": "dealix-engineer",
    "CustomerSuccessAgent": "dealix-delivery",
}

REVENUE_SPECIALIST_DELEGATION: dict[str, str] = {
    "MarketIntelligenceAgent": "dealix-sales",
    "IcpScoringAgent": "dealix-sales",
    "PositioningAgent": "dealix-content",
    "ContentEngineAgent": "dealix-content",
    "OutreachPersonalizationAgent": "dealix-sales",
    "LeadCaptureAgent": "dealix-sales",
    "MeetingBriefAgent": "dealix-sales",
    "SalesCallCoachAgent": "dealix-sales",
    "ScopeBuilderAgent": "dealix-sales",
    "BillingAgent": "dealix-engineer",
    "DeliveryDiagnosticAgent": "dealix-delivery",
    "ProofPackAgent": "dealix-delivery",
    "UpsellAgent": "dealix-sales",
    "PartnerAgent": "dealix-content",
    "GovernanceRiskAgent": "dealix-engineer",
}


def canonical_owner_for(role_id: str) -> str:
    """Resolve a specialist role to its only canonical execution owner.

    Fail closed for unknown roles so new specialist capabilities cannot silently
    create new agent ownership or authority.
    """
    if role_id in RUNTIME_SPECIALIST_DELEGATION:
        return RUNTIME_SPECIALIST_DELEGATION[role_id]
    if role_id in REVENUE_SPECIALIST_DELEGATION:
        return REVENUE_SPECIALIST_DELEGATION[role_id]
    raise KeyError(f"unmapped Dealix specialist role: {role_id}")


def validate_delegation() -> None:
    allowed = set(CANONICAL_AGENTS)
    owners = set(RUNTIME_SPECIALIST_DELEGATION.values()) | set(
        REVENUE_SPECIALIST_DELEGATION.values()
    )
    if not owners <= allowed:
        raise AssertionError("specialist role delegated outside canonical Dealix agents")
    if owners != allowed:
        raise AssertionError("all five canonical Dealix agents must own specialist workloads")


validate_delegation()
