"""Integration tests for api/routers/billing.py + dealix/payments/stripe_client.py."""

from __future__ import annotations

import os

import pytest


@pytest.mark.asyncio
async def test_billing_health_shape(async_client) -> None:
    r = await async_client.get("/api/v1/billing/health")
    assert r.status_code == 200
    body = r.json()
    for key in ("moyasar_configured", "stripe_configured", "primary"):
        assert key in body


@pytest.mark.asyncio
async def test_stripe_checkout_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("STRIPE_API_KEY", raising=False)
    # Force the singleton client to re-read env.
    from dealix.payments import stripe_client as sc

    sc._singleton = None

    r = await async_client.post(
        "/api/v1/billing/checkout/stripe",
        json={
            "tenant_id": "ten_test",
            "plan": "starter",
            "amount_cents": 1000,
            "currency": "usd",
            "email": "buyer@example.com",
            "success_url": "https://x.com/ok",
            "cancel_url": "https://x.com/cancel",
            "mode": "payment",
        },
    )
    assert r.status_code == 503
    assert r.json()["detail"] == "stripe_disabled"


def test_stripe_webhook_signature_helper() -> None:
    import hmac
    import time
    import hashlib
    from dealix.payments.stripe_client import StripeClient

    secret = "whsec_test_seed"
    client = StripeClient(secret_key="sk_test", webhook_secret=secret)
    ts = str(int(time.time()))
    payload = b'{"id":"evt_1","type":"payment_intent.succeeded"}'
    sig = hmac.new(
        secret.encode(), f"{ts}.".encode() + payload, hashlib.sha256
    ).hexdigest()
    assert client.verify_webhook(payload, f"t={ts},v1={sig}") is True
    assert client.verify_webhook(payload, f"t={ts},v1=deadbeef") is False
