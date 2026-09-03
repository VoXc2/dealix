from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.main import create_app
from api.routers.business import pricing as business_pricing
from api.routers.business import proof_pack_roi, recommend_plan_endpoint


# Paths that must not be mounted at launch because they expose legacy fixed-price,
# checkout/payment mutation, self-serve SaaS, parallel invoice authority, or stale
# parallel agent/economic truth.
_BLOCKED_RUNTIME_PATHS = {
    "/api/v1/pricing/plans",
    "/api/v1/pricing/usage",
    "/api/v1/pricing/menu",
    "/api/v1/checkout",
    "/api/v1/pricing/outcome-simulate",
    "/api/v1/billing/plans",
    "/api/v1/billing/subscribe",
    "/api/v1/billing/upgrade",
    "/api/v1/billing/cancel",
    "/api/v1/billing/invoices/{invoice_id}/pay",
    "/api/v1/finance/pricing",
    "/api/v1/finance/pricing/{tier_id}",
    "/api/v1/finance/invoice/draft",
    "/api/v1/onboarding/plans",
    "/api/v1/onboarding/signup",
    "/api/v1/payments/plans",
    "/api/v1/payments/subscriptions/create",
    "/api/v1/payments/moyasar/charge",
    "/api/v1/payments/stc-pay/create",
    "/api/v1/payments/sadad/create-bill",
    "/api/v1/command-center/agents",
    "/api/v1/command-center/agents/{agent_id}",
    "/api/v1/command-center/leaks",
    "/api/v1/command-center/proof-pack",
}

_REQUIRED_SAFE_PATHS = {
    # Canonical commercial replacements use the same URLs as the retired
    # sources, but the legacy routes are removed before registration.
    "/api/v1/public/services",
    "/api/v1/commercial-map",
    "/api/v1/commercial-map/markdown",
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    "/api/v1/quotes/authority/request",
    "/api/v1/invoices/draft",
    "/api/v1/webhooks/moyasar",
    "/api/v1/billing/subscription",
    "/api/v1/billing/invoices",
    "/api/v1/billing/features",
    "/api/v1/finance/status",
    "/api/v1/business/pricing",
    "/api/v1/commercial/status",
    "/api/v1/services/status",
    "/api/v1/services/catalog",
    "/api/v1/onboarding/wizard",
    "/api/v1/onboarding/invite",
    "/api/v1/sector-intel/sectors",
    "/api/v1/service-setup/requests",
}


def _mounted_paths() -> list[str]:
    return [getattr(route, "path", "") for route in create_app().routes]


def test_create_app_route_registration_is_idempotent() -> None:
    first = _mounted_paths()
    second = _mounted_paths()

    assert first == second
    assert _REQUIRED_SAFE_PATHS <= set(first)
    assert _BLOCKED_RUNTIME_PATHS.isdisjoint(first)


def test_launch_runtime_does_not_mount_retired_price_charge_or_parallel_authority() -> None:
    mounted_list = _mounted_paths()
    mounted = set(mounted_list)

    assert _BLOCKED_RUNTIME_PATHS.isdisjoint(mounted)
    assert _REQUIRED_SAFE_PATHS <= mounted

    # Canonical replacements should be registered exactly once, not alongside
    # retired compatibility functions with the same URL.
    for path in (
        "/api/v1/public/services",
        "/api/v1/commercial-map",
        "/api/v1/commercial-map/markdown",
        "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
        "/api/v1/quotes/authority/request",
        "/api/v1/invoices/draft",
    ):
        assert mounted_list.count(path) == 1, path


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


def test_safe_commercial_map_keeps_compatibility_url_without_price_or_checkout() -> None:
    cli = TestClient(create_app())

    r = cli.get("/api/v1/commercial-map")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["entry_offer"]["id"] == "free_mini_diagnostic"
    assert data["primary_offer"]["id"] == "revenue_command_pilot_30d"
    assert data["primary_offer"]["price_model"] == "customer_specific_quote_only"
    assert data["guardrails"]["no_public_fixed_price"] is True
    assert data["guardrails"]["no_public_checkout"] is True
    assert data["guardrails"]["invoice_requires_approved_quote_fingerprint"] is True
    rendered = repr(data)
    for retired in (
        "seven_day_governance_diagnostic",
        "2999",
        "4999",
        "7999",
        "9999",
        "15000",
        "/api/v1/checkout",
    ):
        assert retired not in rendered

    md = cli.get("/api/v1/commercial-map/markdown")
    assert md.status_code == 200, md.text
    assert "Customer-Specific Quote" in md.text
    assert "Public checkout: false" in md.text


def test_public_service_catalog_exposes_only_launch_authorized_offers_without_prices() -> None:
    cli = TestClient(create_app())

    r = cli.get("/api/v1/services/catalog")
    assert r.status_code == 200, r.text
    data = r.json()
    assert [row["id"] for row in data["offerings"]] == [
        "free_mini_diagnostic",
        "revenue_command_pilot_30d",
    ]
    assert data["count"] == 2
    assert data["hard_gates"]["no_public_fixed_price_catalog"] is True
    assert data["hard_gates"]["no_public_checkout"] is True

    for row in data["offerings"]:
        assert "price_sar" not in row
        assert "price_sar_max" not in row
        assert "price_monthly_sar_min" not in row
        assert "price_monthly_sar_max" not in row
        assert row["public_fixed_price"] is False
        assert row["public_checkout"] is False

    rendered = repr(data)
    for retired_price in ("1500", "2999", "4999", "7500", "15000"):
        assert retired_price not in rendered


def test_expansion_service_is_not_publicly_launch_authorized() -> None:
    cli = TestClient(create_app())
    r = cli.get("/api/v1/services/data_to_revenue_pack_1500")
    assert r.status_code == 404, r.text
    assert r.json()["detail"]["reason"] == "service_not_publicly_launch_authorized"


def test_sector_intelligence_is_capability_not_standalone_priced_product() -> None:
    cli = TestClient(create_app())
    r = cli.get("/api/v1/sector-intel/sectors")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["commercial_authority"]["public_fixed_price"] is False
    assert data["commercial_authority"]["live_charge_allowed"] is False
    assert all("price_sar" not in row for row in data["sectors"])
    rendered = repr(data)
    for retired_price in ("1500", "5000", "7500", "10000"):
        assert retired_price not in rendered


def test_bespoke_service_intake_never_generates_automatic_price() -> None:
    cli = TestClient(create_app())
    r = cli.post(
        "/api/v1/service-setup/requests",
        json={
            "company_name": "Acme Saudi",
            "contact_name": "Owner",
            "contact_email": "owner@example.com",
            "use_case_summary": "We need a governed revenue workflow with source-bound evidence.",
            "use_case_category": "sales",
            "complexity": "moderate",
            "integrations_count": 2,
            "data_volume_band": "medium",
            "timeline_weeks": 4,
            "regulated_industry": False,
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["automatic_price_estimate"] is False
    assert data["public_fixed_price"] is False
    assert data["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert "estimate" not in data
    rendered = repr(data)
    for retired_price in ("5000", "25000", "1000"):
        assert retired_price not in rendered
