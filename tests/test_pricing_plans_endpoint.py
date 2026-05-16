"""Tests for the /api/v1/pricing/plans listing + LaaS usage recording.

These tests exercise the public plans endpoint to verify:
  - pilot_1sar is hidden (test-only plan)
  - all customer-facing plans are listed (subscription, one_off, metered)
  - LaaS plans surface their `kind=metered` and `unit` fields
  - usage recording is idempotent per event_id

They run synchronously via httpx ASGITransport — no real DB or Redis required.
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_list_plans_hides_pilot_1sar(async_client):
    res = await async_client.get("/api/v1/pricing/plans")
    assert res.status_code == 200
    body = res.json()
    assert body["currency"] == "SAR"
    assert "pilot_1sar" not in body["plans"]


@pytest.mark.asyncio
async def test_list_plans_includes_managed_ops_subscription(async_client):
    """Rung 3 — Managed Revenue Ops — is the recurring subscription plan."""
    res = await async_client.get("/api/v1/pricing/plans")
    plans = res.json()["plans"]
    assert "managed_ops" in plans
    assert plans["managed_ops"]["kind"] == "subscription"
    assert plans["managed_ops"]["amount_sar"] == 2999.0


@pytest.mark.asyncio
async def test_list_plans_includes_ladder_one_off_rungs(async_client):
    """Rung 1 (Sprint, 499) and Rung 2 (Data Pack, 1,500) are one-off plans."""
    res = await async_client.get("/api/v1/pricing/plans")
    plans = res.json()["plans"]
    assert plans["sprint"]["kind"] == "one_off"
    assert plans["sprint"]["amount_sar"] == 499.0
    assert plans["data_pack"]["kind"] == "one_off"
    assert plans["data_pack"]["amount_sar"] == 1500.0


@pytest.mark.asyncio
async def test_list_plans_includes_metered_laas(async_client):
    res = await async_client.get("/api/v1/pricing/plans")
    plans = res.json()["plans"]
    assert "laas_per_reply" in plans
    assert plans["laas_per_reply"]["kind"] == "metered"
    assert plans["laas_per_reply"]["unit"] == "arabic_replied_lead"
    assert plans["laas_per_reply"]["amount_sar"] == 25.0
    assert "laas_per_demo" in plans
    assert plans["laas_per_demo"]["amount_sar"] == 150.0


@pytest.mark.asyncio
async def test_usage_record_requires_metered_plan(async_client):
    res = await async_client.post(
        "/api/v1/pricing/usage",
        json={"plan": "growth", "customer_handle": "acme", "event_id": "x1"},
    )
    assert res.status_code == 400
    assert "metered" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_usage_record_requires_event_id(async_client):
    res = await async_client.post(
        "/api/v1/pricing/usage",
        json={"plan": "laas_per_reply", "customer_handle": "acme"},
    )
    assert res.status_code == 400
    assert "event_id" in res.json()["detail"]


@pytest.mark.asyncio
async def test_usage_record_idempotent(async_client):
    payload = {
        "plan": "laas_per_reply",
        "customer_handle": "test_handle_idem",
        "event_id": "test_msg_001",
    }
    res1 = await async_client.post("/api/v1/pricing/usage", json=payload)
    assert res1.status_code == 200
    assert res1.json()["status"] == "recorded"
    # Same event_id replay → marked duplicate, not double-charged
    res2 = await async_client.post("/api/v1/pricing/usage", json=payload)
    assert res2.status_code == 200
    assert res2.json()["status"] == "duplicate"
    # Amount fields remain consistent across both calls (auditability)
    assert res1.json()["amount_halalas"] == res2.json()["amount_halalas"]
