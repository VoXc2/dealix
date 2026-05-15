from __future__ import annotations

from saudi_ai_provider.pricing import compute_roi, get_service_pricing, quote_service


def test_pricing_lookup_customer_portal_gold_mid_market() -> None:
    pricing = get_service_pricing("CUSTOMER_PORTAL_GOLD", "mid_market")
    assert pricing["setup_fee_sar"] == 45000
    assert pricing["monthly_retainer_sar"] == 18000
    assert pricing["minimum_contract_months"] == 6


def test_quote_is_sellable_with_default_discount() -> None:
    quote = quote_service("SECURITY_SILVER", employees=300)
    assert quote.sellable is True
    assert quote.segment == "mid_market"
    assert quote.annual_contract_value_sar > 0


def test_compute_roi_for_customer_portal() -> None:
    roi = compute_roi(
        "CUSTOMER_PORTAL_GOLD",
        {
            "monthly_tickets": 50000,
            "avg_agent_cost_sar": 18,
            "automation_rate": 0.42,
        },
    )
    assert roi.monthly_savings_sar == 378000.0
    assert roi.annual_roi_sar == 4536000.0
