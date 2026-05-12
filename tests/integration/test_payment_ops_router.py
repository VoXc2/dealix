"""Integration tests for /api/v1/payment-ops/invoice-intent (T13a).

Two key contracts:
1. Hard gates from the constitution are preserved
   (no_live_charge, no_fake_revenue, evidence_reference, delivery_requires_payment_confirmed).
2. When MOYASAR_SECRET_KEY is unset the `payment.checkout_url` is None
   so the landing form falls back to the bank-transfer copy. When set,
   the response carries a `checkout_url` and `checkout_mode: moyasar_test`.
"""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_invoice_intent_requires_fields(async_client) -> None:
    r = await async_client.post("/api/v1/payment-ops/invoice-intent", json={})
    assert r.status_code == 422
    assert "required" in r.json()["detail"]


@pytest.mark.asyncio
async def test_invoice_intent_rejects_invalid_method(async_client) -> None:
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "buyer@example.sa",
            "amount_sar": 499,
            "method": "rumple-stiltskin",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_invoice_intent_test_mode_returns_no_checkout_url(
    async_client, monkeypatch
) -> None:
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "buyer@example.sa",
            "amount_sar": 499,
            "method": "moyasar_test",
            "service_session_id": "sprint_499",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["payment"]["payment_id"].startswith("pay_")
    assert body["payment"].get("checkout_url") is None
    assert body["payment"].get("checkout_mode") == "test_no_gateway"
    # The hard-gates block must still be returned every call.
    assert body["hard_gates"]["no_live_charge"] is True
    assert body["hard_gates"]["evidence_reference_required_for_confirm"] is True
    # Revenue must not be claimed.
    assert body["warning_invoice_not_revenue"] == "invoice_intent != revenue"


@pytest.mark.asyncio
async def test_invoice_intent_bank_transfer_skips_moyasar_branch(
    async_client, monkeypatch
) -> None:
    """Even with MOYASAR_SECRET_KEY set, bank-transfer must NOT call
    Moyasar — that path is intentionally manual."""
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_fake_xxx")
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "buyer@example.sa",
            "amount_sar": 999,
            "method": "bank_transfer",
            "service_session_id": "growth_os_monthly",
        },
    )
    assert r.status_code == 200
    body = r.json()
    # No moyasar enrichment for non-moyasar methods.
    assert "checkout_url" not in body["payment"] or body["payment"]["checkout_url"] is None
    assert "moyasar_invoice_id" not in body["payment"]


@pytest.mark.asyncio
async def test_invoice_intent_moyasar_live_gated_without_env(
    async_client, monkeypatch
) -> None:
    """moyasar_live MUST be blocked without DEALIX_MOYASAR_MODE=live —
    constitutional NO_LIVE_CHARGE gate."""
    monkeypatch.delenv("DEALIX_MOYASAR_MODE", raising=False)
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "buyer@example.sa",
            "amount_sar": 499,
            "method": "moyasar_live",
            "service_session_id": "sprint_499",
        },
    )
    assert r.status_code == 403
    assert "NO_LIVE_CHARGE" in r.json()["detail"] or "moyasar_live" in r.json()["detail"]
