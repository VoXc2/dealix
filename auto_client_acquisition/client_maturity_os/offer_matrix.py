"""Maturity-to-offer matrix — blocked offers and primary offer by ladder level."""

from __future__ import annotations

PRIMARY_OFFER_BY_LEVEL: tuple[str, ...] = (
    "AI Governance & Readiness Diagnostic",
    "Capability Diagnostic",
    "Productized Sprint (Revenue / Brain / Quick Win)",
    "Governance Runtime Setup + Proof Pack System + Monthly Operating Cadence",
    "Monthly Retainer (RevOps / Governance / Company Brain / AI Ops)",
    "Client Workspace + Proof Timeline + Value Dashboard + Approval Center",
    "Enterprise AI Operations Program",
    "AI Control Plane + Enterprise Governance Program",
)

BLOCKED_OFFERS_BY_LEVEL: tuple[frozenset[str], ...] = (
    frozenset(
        {
            "Autonomous Agents",
            "Platform",
            "Enterprise AI Control Plane",
            "External Automation Without Approval",
        }
    ),
    frozenset({"Platform", "Enterprise AI Control Plane", "Autonomous Agents"}),
    frozenset({"Enterprise AI Control Plane", "White-label", "Autonomous Agents"}),
    frozenset(
        {
            "Autonomous Agents",
            "Enterprise AI Control Plane",
            "External Automation Without Approval",
            "External automation without approval",
        }
    ),
    frozenset({"Autonomous Agents"}),
    frozenset({"Complex Enterprise Features Without Foundation"}),
    frozenset({"White-label"}),
    frozenset(),  # L7: enterprise — gate by eligibility not blanket block
)


def primary_offer_for_level(level: int) -> str:
    if level < 0:
        level = 0
    if level > 7:
        level = 7
    return PRIMARY_OFFER_BY_LEVEL[level]


def blocked_offers_for_level(level: int) -> frozenset[str]:
    if level < 0:
        level = 0
    if level > 7:
        level = 7
    return BLOCKED_OFFERS_BY_LEVEL[level]


def retainer_eligibility_met(
    *,
    proof_score: int,
    adoption_score: int,
    workflow_owner_exists: bool,
    monthly_cadence_active: bool,
    governance_risk_controlled: bool,
) -> bool:
    return (
        proof_score >= 80
        and adoption_score >= 70
        and workflow_owner_exists
        and monthly_cadence_active
        and governance_risk_controlled
    )


def level7_entry_gates_met(
    *,
    workflow_count: int,
    has_executive_sponsor: bool,
    has_governance_owner: bool,
    requires_audit: bool,
    monthly_cadence_active: bool,
    clear_budget: bool,
) -> bool:
    return (
        workflow_count >= 3
        and has_executive_sponsor
        and has_governance_owner
        and requires_audit
        and monthly_cadence_active
        and clear_budget
    )


def level1_first_track(
    *,
    pain_near_revenue: bool,
    risk_higher_than_value: bool,
    scattered_knowledge: bool,
) -> str:
    """After Capability Diagnostic — pick first sprint / review track (Level 1 routing)."""
    if risk_higher_than_value:
        return "AI Governance Review"
    if scattered_knowledge:
        return "Company Brain Sprint"
    if pain_near_revenue:
        return "Revenue Intelligence Sprint"
    return "Capability Diagnostic (defer sprint until a clear signal)"
