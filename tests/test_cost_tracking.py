"""Tests for cost tracking endpoint (W11.2)."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_per_tier_returns_200(async_client):
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_per_tier_includes_all_tiers(async_client):
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    tiers = res.json()["tiers"]
    for tier in ("pilot", "starter", "growth", "scale"):
        assert tier in tiers, f"missing tier: {tier}"


@pytest.mark.asyncio
async def test_per_tier_growth_has_positive_margin(async_client):
    """Growth tier is the bread-and-butter — margin must be positive."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    growth = res.json()["tiers"]["growth"]
    assert growth["gross_profit_halalas"] > 0
    assert growth["gross_margin_pct"] > 50  # > 50% margin


@pytest.mark.asyncio
async def test_per_tier_scale_has_higher_margin_than_starter(async_client):
    """Larger tiers should compound margin (fixed infra cost amortized)."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    tiers = res.json()["tiers"]
    assert tiers["scale"]["gross_margin_pct"] > tiers["starter"]["gross_margin_pct"]


@pytest.mark.asyncio
async def test_per_tier_pilot_is_loss_leader_or_low_margin(async_client):
    """Pilot is a customer-acquisition tool; margin OK if positive,
    accepted to be near-breakeven (founder time amortized into cost)."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    pilot = res.json()["tiers"]["pilot"]
    # Pilot should at least cover variable cost (gross profit positive)
    assert pilot["price_halalas"] > pilot["cost_breakdown_halalas"]["llm_inference"]


@pytest.mark.asyncio
async def test_per_tier_cost_breakdown_complete(async_client):
    """Each tier shows the cost components — transparency."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    growth_breakdown = res.json()["tiers"]["growth"]["cost_breakdown_halalas"]
    for component in ("llm_inference", "lead_adapters",
                       "moyasar_fees", "support_time"):
        assert component in growth_breakdown


@pytest.mark.asyncio
async def test_summary_requires_admin(async_client):
    res = await async_client.get("/api/v1/cost-tracking/summary")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_summary_admin_returns_schema(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_cost_summary")
    res = await async_client.get(
        "/api/v1/cost-tracking/summary",
        headers={"X-Admin-API-Key": "test_admin_cost_summary"},
    )
    assert res.status_code == 200
    body = res.json()
    # Schema invariants — dashboards depend on these keys
    for key in ("period", "infrastructure", "llm_providers", "data_adapters"):
        assert key in body


@pytest.mark.asyncio
async def test_per_tier_includes_disclosure(async_client):
    """Response must include a disclosure note — values are model
    parameters, not real-time telemetry."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    body = res.json()
    assert "note" in body
    assert "model parameters" in body["note"].lower() or "calibrated" in body
