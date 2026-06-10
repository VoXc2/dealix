"""Tests for revenue metrics dashboard (W13.7)."""
from __future__ import annotations

import pytest

ADMIN_HEADER = "X-Admin-API-Key"


@pytest.mark.asyncio
async def test_dashboard_requires_admin(async_client):
    res = await async_client.get("/api/v1/revenue-metrics/dashboard")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_dashboard_returns_schema(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_rev_dash")
    res = await async_client.get(
        "/api/v1/revenue-metrics/dashboard",
        headers={ADMIN_HEADER: "test_admin_rev_dash"},
    )
    assert res.status_code == 200
    body = res.json()
    for key in ("period", "mrr", "arr", "customers", "arpa",
                "churn_pct_monthly", "nrr_pct", "plan_distribution",
                "benchmarks", "interpretation"):
        assert key in body, f"missing dashboard key: {key}"


@pytest.mark.asyncio
async def test_dashboard_zero_state_honest(async_client, monkeypatch):
    """When no payments yet, response says 'pre-revenue' — not fake numbers."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_zero_state")
    res = await async_client.get(
        "/api/v1/revenue-metrics/dashboard",
        headers={ADMIN_HEADER: "test_admin_zero_state"},
    )
    body = res.json()
    assert body["customers"]["active"] >= 0
    assert body["mrr"]["sar"] >= 0
    # Interpretation honestly points to v4 §15 truth
    interp = body["interpretation"]
    if body["customers"]["active"] == 0:
        assert "pre-revenue" in interp["headline"].lower() or "first customer" in interp["next_action"].lower()


@pytest.mark.asyncio
async def test_dashboard_includes_benchmarks(async_client, monkeypatch):
    """SaaS industry benchmarks must be in the response for context."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_benchmarks")
    res = await async_client.get(
        "/api/v1/revenue-metrics/dashboard",
        headers={ADMIN_HEADER: "test_admin_benchmarks"},
    )
    body = res.json()
    bench = body["benchmarks"]
    for key in ("saas_unicorn_nrr", "saas_healthy_nrr", "saas_danger_nrr"):
        assert key in bench


@pytest.mark.asyncio
async def test_cohort_validates_month_format(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_cohort_validate")
    res = await async_client.get(
        "/api/v1/revenue-metrics/cohort?cohort_month=bad-month",
        headers={ADMIN_HEADER: "test_admin_cohort_validate"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_cohort_empty_returns_zero_size(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_cohort_empty")
    res = await async_client.get(
        "/api/v1/revenue-metrics/cohort?cohort_month=2025-01",
        headers={ADMIN_HEADER: "test_admin_cohort_empty"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["cohort_size"] == 0
    assert "note" in body


@pytest.mark.asyncio
async def test_cohort_returns_4_retention_points(async_client, monkeypatch):
    """Retention curve must include month +1, +3, +6, +12 markers."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_cohort_curve")
    res = await async_client.get(
        "/api/v1/revenue-metrics/cohort?cohort_month=2026-05",
        headers={ADMIN_HEADER: "test_admin_cohort_curve"},
    )
    body = res.json()
    if body["cohort_size"] > 0:
        curve = body["retention_curve"]
        offsets = {p["month_offset"] for p in curve}
        assert offsets == {1, 3, 6, 12}


@pytest.mark.asyncio
async def test_health_check_returns_status(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_metric_health")
    res = await async_client.get(
        "/api/v1/revenue-metrics/health-check",
        headers={ADMIN_HEADER: "test_admin_metric_health"},
    )
    assert res.status_code == 200
    body = res.json()
    assert "status" in body
    assert "payment_records_loaded" in body
