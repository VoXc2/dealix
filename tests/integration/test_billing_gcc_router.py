"""Integration tests for api/routers/billing_gcc.py."""

from __future__ import annotations

import pytest


def _reset_clients() -> None:
    from dealix.payments import benefit_client, knet_client, magnati_client

    benefit_client._singleton = None
    knet_client._singleton = None
    magnati_client._singleton = None


@pytest.mark.asyncio
async def test_gcc_health_reports_three_gateways(async_client, monkeypatch) -> None:
    for v in (
        "KNET_TRANPORTAL_ID",
        "KNET_RESOURCE_KEY",
        "BENEFIT_API_KEY",
        "BENEFIT_MERCHANT_ID",
        "MAGNATI_API_KEY",
        "MAGNATI_MERCHANT_ID",
    ):
        monkeypatch.delenv(v, raising=False)
    _reset_clients()

    r = await async_client.get("/api/v1/billing/gcc/health")
    assert r.status_code == 200
    body = r.json()
    # Honest health: report what's available + keep back-compat booleans.
    assert body["available"] == []
    assert body["configured_count"] == 0
    assert body["knet_configured"] is False
    assert body["benefit_configured"] is False
    assert body["magnati_configured"] is False


@pytest.mark.asyncio
async def test_gcc_health_full_lists_all_gateways(async_client, monkeypatch) -> None:
    for v in (
        "KNET_TRANPORTAL_ID",
        "KNET_RESOURCE_KEY",
        "BENEFIT_API_KEY",
        "BENEFIT_MERCHANT_ID",
        "MAGNATI_API_KEY",
        "MAGNATI_MERCHANT_ID",
    ):
        monkeypatch.delenv(v, raising=False)
    _reset_clients()
    r = await async_client.get("/api/v1/billing/gcc/health/full")
    assert r.status_code == 200
    body = r.json()
    for gw in ("knet", "benefit", "magnati"):
        assert body[gw]["configured"] is False
        assert body[gw]["status"] == "pending_merchant_onboarding"


@pytest.mark.asyncio
async def test_knet_checkout_503_without_keys(async_client, monkeypatch) -> None:
    monkeypatch.delenv("KNET_TRANPORTAL_ID", raising=False)
    monkeypatch.delenv("KNET_RESOURCE_KEY", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/checkout/knet",
        json={
            "tenant_id": "ten_test",
            "plan": "growth",
            "amount_minor": 1500,
            "order_id": "ORD-1",
            "email": "buyer@example.kw",
            "success_url": "https://app.dealix.me/checkout/ok",
            "cancel_url": "https://app.dealix.me/checkout/cancel",
        },
    )
    assert r.status_code == 503
    assert r.json()["detail"] == "knet_disabled"


@pytest.mark.asyncio
async def test_benefit_checkout_503_without_keys(async_client, monkeypatch) -> None:
    monkeypatch.delenv("BENEFIT_API_KEY", raising=False)
    monkeypatch.delenv("BENEFIT_MERCHANT_ID", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/checkout/benefit",
        json={
            "tenant_id": "ten_test",
            "plan": "growth",
            "amount_minor": 1500,
            "order_id": "ORD-1",
            "email": "buyer@example.bh",
            "success_url": "https://app.dealix.me/ok",
            "cancel_url": "https://app.dealix.me/cancel",
        },
    )
    assert r.status_code == 503
    assert r.json()["detail"] == "benefit_disabled"


@pytest.mark.asyncio
async def test_magnati_checkout_503_without_keys(async_client, monkeypatch) -> None:
    monkeypatch.delenv("MAGNATI_API_KEY", raising=False)
    monkeypatch.delenv("MAGNATI_MERCHANT_ID", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/checkout/magnati",
        json={
            "tenant_id": "ten_test",
            "plan": "growth",
            "amount_minor": 5000,
            "order_id": "ORD-1",
            "email": "buyer@example.ae",
            "success_url": "https://app.dealix.me/ok",
            "cancel_url": "https://app.dealix.me/cancel",
        },
    )
    assert r.status_code == 503
    assert r.json()["detail"] == "magnati_disabled"


@pytest.mark.asyncio
async def test_knet_webhook_rejects_bad_signature(async_client, monkeypatch) -> None:
    """The webhook should refuse without the secret (no auth = no MAC match)."""
    monkeypatch.delenv("KNET_RESOURCE_KEY", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/webhooks/knet",
        content=b'{"event":"test"}',
        headers={"x-knet-signature": "deadbeef"},
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "invalid_signature"


@pytest.mark.asyncio
async def test_benefit_webhook_rejects_bad_signature(async_client, monkeypatch) -> None:
    monkeypatch.delenv("BENEFIT_WEBHOOK_SECRET", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/webhooks/benefit",
        content=b'{"event":"test"}',
        headers={"x-benefit-signature": "deadbeef"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_magnati_webhook_rejects_bad_signature(async_client, monkeypatch) -> None:
    monkeypatch.delenv("MAGNATI_WEBHOOK_SECRET", raising=False)
    _reset_clients()
    r = await async_client.post(
        "/api/v1/billing/gcc/webhooks/magnati",
        content=b'{"event":"test"}',
        headers={"x-magnati-signature": "deadbeef"},
    )
    assert r.status_code == 401
