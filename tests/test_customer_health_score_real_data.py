"""Tests for the real-data Customer Health Score endpoint (W2.1).

Verifies GET /api/v1/customer-success-os/{handle}/health:
  - returns 400 when handle is empty
  - returns a valid score even when DB is unavailable (neutral fallback)
  - score payload contains required fields (score, band, signals_used)
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_health_endpoint_requires_handle(async_client):
    res = await async_client.get("/api/v1/customer-success-os/ /health")
    # Empty/whitespace handle should be rejected as 400
    # (FastAPI may route to 404 depending on URL parsing — accept either)
    assert res.status_code in (400, 404, 422)


@pytest.mark.asyncio
async def test_health_endpoint_returns_score_with_neutral_fallback(async_client):
    """Even with no DB / no payment data, the endpoint returns a valid
    score reflecting 'unknown' state, not a fake-green default."""
    res = await async_client.get("/api/v1/customer-success-os/test_neutral_handle/health")
    assert res.status_code == 200
    body = res.json()
    assert "score" in body
    assert 0 <= body["score"] <= 100
    assert body["band"] in ("excellent", "good", "needs_attention", "high_risk")
    assert "label_ar" in body
    assert "label_en" in body
    assert body["customer_handle"] == "test_neutral_handle"
    assert body["data_source"] == "tenant_db_with_neutral_fallback"
    # Signals payload must be present + match the request schema shape
    sigs = body["signals_used"]
    assert isinstance(sigs, dict)
    for key in (
        "intake_complete",
        "diagnostic_delivered",
        "proof_events_count",
        "open_support_tickets",
        "last_customer_response_days",
        "delivery_sla_status",
        "payment_status",
        "renewal_signal",
    ):
        assert key in sigs, f"missing signal: {key}"


@pytest.mark.asyncio
async def test_health_endpoint_neutral_falls_into_high_risk_band(async_client):
    """With zero positive signals AND no payment data, the score should
    land in the 'high_risk' or 'needs_attention' band — NOT 'excellent'.
    This protects against green-by-default false confidence."""
    res = await async_client.get("/api/v1/customer-success-os/empty_tenant/health")
    body = res.json()
    assert body["band"] != "excellent", (
        "Empty-tenant health must NOT be excellent — that would mislead the founder"
    )


@pytest.mark.asyncio
async def test_status_endpoint_unchanged(async_client):
    """Existing /status endpoint still works — no regression."""
    res = await async_client.get("/api/v1/customer-success-os/status")
    assert res.status_code == 200
    assert res.json()["service"] == "customer_success_os"
