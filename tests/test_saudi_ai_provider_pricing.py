from __future__ import annotations

from saudi_ai_provider.pricing import get_service_pricing, quote_service


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
