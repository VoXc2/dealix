"""Business strategy API and modules under current quote-only authority."""

from __future__ import annotations

import pytest

from auto_client_acquisition.business.gtm_plan import first_10_customers_plan
from auto_client_acquisition.business.launch_metrics import north_star_metrics
from auto_client_acquisition.business.market_positioning import compare_competitors
from auto_client_acquisition.business.pricing_strategy import (
    calculate_performance_fee,
    estimate_roi,
    get_pricing_tiers,
    recommend_plan,
)


def test_legacy_pricing_tiers_are_retired():
    data = get_pricing_tiers()
    assert data["status"] == "quote_only"
    assert data["tiers"] == []
    assert data["public_fixed_price"] is False
    assert data["live_charge_allowed"] is False
    assert data["price_authority"] == "customer_specific_quote_after_qualified_discovery"


def test_recommend_plan_routes_to_discovery_without_auto_package():
    r = recommend_plan(company_size="sme", monthly_budget_sar=3500, goal="pipeline")
    assert r["recommended_plan"] is None
    assert r["automatic_plan_selection"] is False
    assert r["public_fixed_price"] is False
    assert r["recommended_next_step"] == "free_mini_diagnostic_then_qualified_discovery"


def test_roi_is_internal_scenario_from_caller_supplied_quote():
    r = estimate_roi(
        plan_price_sar=3000,
        expected_pipeline_sar=90000,
        expected_revenue_sar=20000,
    )
    assert r["status"] == "internal_estimate_only"
    assert r["customer_value_claim"] is False
    assert r["guarantee"] is False
    assert r["quote_amount_source"] == "caller_supplied_customer_specific_quote"
    assert r["revenue_to_subscription_multiple"] > 0


def test_performance_fee_compatibility_surface_does_not_create_billable_fee():
    r = calculate_performance_fee(
        qualified_leads=10,
        booked_meetings=3,
        won_revenue_sar=50000,
        lead_fee_sar=40,
        meeting_fee_sar=250,
        success_fee_pct=5,
    )
    assert r["status"] == "retired_commercial_authority"
    assert r["total_performance_fees_sar"] is None
    assert r["automatic_billing_allowed"] is False
    assert r["live_charge_allowed"] is False


def test_competitor_list_includes_major_players():
    names = {c["name"].lower() for c in compare_competitors()}
    assert "hubspot" in names
    assert "gong" in names
    assert "salesforce" in names
    assert any("whatsapp" in n for n in names)


def test_gtm_first_10_returns_actions():
    plan = first_10_customers_plan()
    assert "actions" in plan
    assert plan["actions"]


def test_launch_metrics_exist():
    assert "primary" in north_star_metrics()


@pytest.mark.asyncio
async def test_business_pricing_endpoint_is_quote_only(async_client):
    r = await async_client.get("/api/v1/business/pricing")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "quote_only"
    assert body["entry_offer_id"] == "free_mini_diagnostic"
    assert body["launch_authority"] == "revenue_command_pilot_30d"
    assert body["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert body["public_fixed_price"] is False
    assert body["live_charge_allowed"] is False
    assert "tiers" not in body
