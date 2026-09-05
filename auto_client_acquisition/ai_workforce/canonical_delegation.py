"""Canonical Dealix agent delegation for legacy specialist roles.

Historical AI Workforce, Operating Company, and Revenue Factory modules expose
useful specialist roles. They are bounded workloads delegated to the five
canonical Dealix agents; they are not permanent agents, truth owners,
schedulers, or approval authorities.
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

OPERATING_COMPANY_SPECIALIST_DELEGATION: dict[str, str] = {
    "market_intelligence": "dealix-sales",
    "icp_scoring": "dealix-sales",
    "positioning": "dealix-content",
    "content_strategy": "dealix-content",
    "outreach_drafting": "dealix-sales",
    "reply_classifier": "dealix-sales",
    "meeting_brief": "dealix-sales",
    "sales_call_coach": "dealix-sales",
    "scope_builder": "dealix-sales",
    "billing": "dealix-engineer",
    "delivery_diagnostic": "dealix-delivery",
    "proof_pack": "dealix-delivery",
    "upsell": "dealix-sales",
    "partner": "dealix-content",
    "governance": "dealix-engineer",
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
    """Resolve a specialist role to its only canonical execution owner."""
    for mapping in (
        RUNTIME_SPECIALIST_DELEGATION,
        OPERATING_COMPANY_SPECIALIST_DELEGATION,
        REVENUE_SPECIALIST_DELEGATION,
    ):
        if role_id in mapping:
            return mapping[role_id]
    raise KeyError(f"unmapped Dealix specialist role: {role_id}")


def validate_delegation() -> None:
    allowed = set(CANONICAL_AGENTS)
    mappings = (
        RUNTIME_SPECIALIST_DELEGATION,
        OPERATING_COMPANY_SPECIALIST_DELEGATION,
        REVENUE_SPECIALIST_DELEGATION,
    )
    owners = set().union(*(set(mapping.values()) for mapping in mappings))
    if not owners <= allowed:
        raise AssertionError("specialist role delegated outside canonical Dealix agents")
    if owners != allowed:
        raise AssertionError("all five canonical Dealix agents must own specialist workloads")
    if any(not mapping for mapping in mappings):
        raise AssertionError("specialist delegation map must not be empty")


validate_delegation()
