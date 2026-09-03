from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException

from api.main import create_app
from api.routers.business import pricing as business_pricing
from api.routers.business import proof_pack_roi, recommend_plan_endpoint


_BLOCKED_RUNTIME_PATHS = {
    "/api/v1/public/services",
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    "/api/v1/invoices/draft",
    "/api/v1/pricing/plans",
    "/api/v1/pricing/usage",
    "/api/v1/pricing/menu",
    "/api/v1/checkout",
    "/api/v1/pricing/outcome-simulate",
    "/api/v1/commercial-map",
    "/api/v1/commercial-map/markdown",
    "/api/v1/billing/plans",
    "/api/v1/billing/subscribe",
    "/api/v1/billing/upgrade",
    "/api/v1/billing/cancel",
    "/api/v1/billing/invoices/{invoice_id}/pay",
}

_REQUIRED_SAFE_PATHS = {
    "/api/v1/webhooks/moyasar",
    "/api/v1/billing/subscription",
    "/api/v1/billing/invoices",
    "/api/v1/billing/features",
    "/api/v1/business/pricing",
    "/api/v1/commercial/status",
}


def test_launch_runtime_does_not_mount_retired_price_or_charge_authority() -> None:
    app = create_app()
    mounted = {getattr(route, "path", "") for route in app.routes}

    assert _BLOCKED_RUNTIME_PATHS.isdisjoint(mounted)
    assert _REQUIRED_SAFE_PATHS <= mounted


def test_business_pricing_compatibility_is_quote_only() -> None:
    payload = asyncio.run(business_pricing())

    assert payload["launch_authority"] == "revenue_command_pilot_30d"
    assert payload["entry_offer_id"] == "free_mini_diagnostic"
    assert payload["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert payload["public_fixed_price"] is False
    assert payload["live_charge_allowed"] is False
    rendered = repr(payload)
    assert "2999" not in rendered
    assert "4999" not in rendered
    assert "7999" not in rendered
    assert "15000" not in rendered


def test_legacy_plan_recommendation_fails_closed() -> None:
    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(recommend_plan_endpoint({"company_size": "sme", "monthly_budget_sar": 999999}))

    assert excinfo.value.status_code == 409
    detail = excinfo.value.detail
    assert detail["reason"] == "legacy_pricing_authority_retired"
    assert detail["public_fixed_price"] is False


def test_roi_summary_requires_customer_specific_quote_amount() -> None:
    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(proof_pack_roi({"influenced_revenue_sar": 100000, "hours_saved": 10}))
    assert excinfo.value.status_code == 422
    assert excinfo.value.detail == "customer_specific_quote_amount_required"

    payload = asyncio.run(
        proof_pack_roi(
            {
                "subscription_sar": 1234.5,
                "influenced_revenue_sar": 100000,
                "hours_saved": 10,
            }
        )
    )
    assert payload["status"] == "internal_estimate_only"
    assert payload["customer_value_claim"] is False
    assert payload["guarantee"] is False
    assert payload["quote_amount_source"] == "caller_supplied_customer_specific_quote"
