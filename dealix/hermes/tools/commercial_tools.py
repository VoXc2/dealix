"""Commercial tool functions — diagnostic, sprint, proof pack, upsell, and market intel."""

from __future__ import annotations


async def run_commercial_diagnostic(
    company_name: str,
    sector: str = "b2b_services",
    pain_points: list[str] | None = None,
    notes: str = "",
) -> dict:
    """Run the commercial DiagnosticEngine for a company."""
    from dealix.hermes.bridges.commercial_bridge import CommercialBridge

    return await CommercialBridge.instance().run_diagnostic(
        company_name=company_name,
        sector=sector,
        pain_points=pain_points,
        notes=notes,
    )


async def run_commercial_sprint(
    engagement_id: str,
    customer_id: str,
    customer_name: str = "",
    sector: str = "b2b_services",
    pain_summary: str = "",
    founder_approved: bool = False,
) -> dict:
    """Run the 7-day Revenue Intelligence Sprint."""
    from dealix.hermes.bridges.commercial_bridge import CommercialBridge

    return await CommercialBridge.instance().run_sprint(
        engagement_id=engagement_id,
        customer_id=customer_id,
        customer_name=customer_name,
        sector=sector,
        pain_summary=pain_summary,
        founder_approved=founder_approved,
    )


async def build_commercial_proof_pack(
    account_id: str,
    company_name: str,
    events: list[dict] | None = None,
    approved_by_founder: bool = False,
    customer_consent: bool = False,
) -> dict:
    """Build a proof pack for an account."""
    from dealix.hermes.bridges.commercial_bridge import CommercialBridge

    return await CommercialBridge.instance().build_proof_pack(
        account_id=account_id,
        company_name=company_name,
        events=events,
        approved_by_founder=approved_by_founder,
        customer_consent=customer_consent,
    )


async def check_commercial_upsell(
    account_id: str,
    company_name: str,
    proof_event_count: int = 0,
    current_tier: str = "",
) -> dict:
    """Check upsell eligibility for an account."""
    from dealix.hermes.bridges.commercial_bridge import CommercialBridge

    return await CommercialBridge.instance().check_upsell_eligibility(
        account_id=account_id,
        company_name=company_name,
        proof_event_count=proof_event_count,
        current_tier=current_tier,
    )


async def get_commercial_market_intel(
    sector: str,
    city: str = "Riyadh",
) -> dict:
    """Get Saudi market intelligence for a sector."""
    from dealix.hermes.bridges.commercial_bridge import CommercialBridge

    return await CommercialBridge.instance().get_market_intelligence(
        sector=sector,
        city=city,
    )


__all__ = [
    "build_commercial_proof_pack",
    "check_commercial_upsell",
    "get_commercial_market_intel",
    "run_commercial_diagnostic",
    "run_commercial_sprint",
]
