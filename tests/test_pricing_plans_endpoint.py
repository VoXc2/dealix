"""Launch commercial-truth tests for pricing and checkout quarantine.

The current launch app intentionally filters legacy fixed-plan pricing/checkout
routes out of the Sales domain. Customer-facing authority is the quote-only
``commercial_runtime_truth`` surface. Legacy pricing helpers remain unit-tested
as future/internal machinery but cannot become public merely by existing.
"""
from __future__ import annotations

import pytest

from api.routers import pricing


LEGACY_LAUNCH_PATHS = (
    "/api/v1/pricing/plans",
    "/api/v1/pricing/usage",
    "/api/v1/pricing/menu",
    "/api/v1/checkout",
    "/api/v1/pricing/outcome-simulate",
)


@pytest.mark.asyncio
@pytest.mark.parametrize("path", LEGACY_LAUNCH_PATHS)
async def test_legacy_pricing_and_checkout_paths_are_not_mounted(async_client, path):
    if path in {"/api/v1/checkout", "/api/v1/pricing/usage"}:
        response = await async_client.post(path, json={})
    else:
        response = await async_client.get(path)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_canonical_public_commercial_map_is_quote_only(async_client):
    response = await async_client.get("/api/v1/public/services")
    assert response.status_code == 200, response.text
    body = response.json()
    primary = body["primary_offer"]
    guardrails = body["guardrails"]
    assert primary["id"] == "revenue_command_pilot_30d"
    assert primary["duration_days"] is None
    assert primary["duration_policy"] == "customer_specific_after_qualified_discovery"
    assert primary["price_model"] == "customer_specific_quote_only"
    assert primary["public_fixed_pricing"] is False
    assert primary["public_checkout"] is False
    assert guardrails["no_public_fixed_price"] is True
    assert guardrails["no_public_checkout"] is True
    assert guardrails["invoice_is_not_payment"] is True


@pytest.mark.asyncio
async def test_legacy_module_public_plan_helper_fails_closed_by_default(monkeypatch):
    monkeypatch.delenv("DEALIX_PUBLIC_PRICING_ENABLED", raising=False)
    monkeypatch.delenv("DEALIX_PUBLIC_PLAN_IDS", raising=False)
    body = await pricing.list_plans()
    assert body["currency"] == "SAR"
    assert body["plans"] == {}
    assert body["public_pricing_enabled"] is False
    assert body["status"] == "founder_approval_required"


def test_test_plan_is_never_a_normal_checkout_plan():
    assert "pilot_1sar" not in pricing.ALLOWED_PLANS
    assert pricing.ALLOWED_PLANS == frozenset()


def test_legacy_checkout_flag_fails_closed(monkeypatch):
    monkeypatch.delenv("DEALIX_CHECKOUT_ENABLED", raising=False)
    assert pricing._checkout_enabled() is False


def test_1sar_gate_is_impossible_in_production(monkeypatch):
    monkeypatch.setenv("DEALIX_ENABLE_1SAR_CHECKOUT", "true")
    monkeypatch.setenv("APP_ENV", "production")
    assert pricing._test_checkout_enabled() is False
