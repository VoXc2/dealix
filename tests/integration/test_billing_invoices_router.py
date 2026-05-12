"""Integration tests for /api/v1/billing/invoices/{invoice_id} (T13b)."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_invoice_download_requires_token(async_client) -> None:
    r = await async_client.get("/api/v1/billing/invoices/inv_no_token")
    assert r.status_code == 401
    assert r.json()["detail"] == "invoice_token_required"


@pytest.mark.asyncio
async def test_invoice_download_rejects_bad_token(async_client) -> None:
    r = await async_client.get(
        "/api/v1/billing/invoices/inv_x?t=deadbeef"
    )
    assert r.status_code in {401, 404}


@pytest.mark.asyncio
async def test_invoice_download_with_valid_token_returns_synthetic_invoice(
    async_client,
) -> None:
    """If no row exists in InvoiceRecord, the router falls back to the
    in-process payment_state index. We seed one + verify the signed
    URL serves the rendered invoice."""
    from auto_client_acquisition.payment_ops import create_invoice_intent

    rec = create_invoice_intent(
        customer_handle="buyer@example.sa",
        amount_sar=499.0,
        method="moyasar_test",
        service_session_id="sprint_499",
    )
    from api.routers.billing_invoices import sign_invoice_token

    token = sign_invoice_token(rec.payment_id)
    r = await async_client.get(
        f"/api/v1/billing/invoices/{rec.payment_id}?t={token}"
    )
    # Either a real PDF or the HTML fallback — both are acceptable.
    assert r.status_code == 200
    assert r.headers["content-type"].startswith(("application/pdf", "text/html"))
    assert len(r.content) > 200


@pytest.mark.asyncio
async def test_invoice_token_signing_is_deterministic() -> None:
    from api.routers.billing_invoices import sign_invoice_token

    a = sign_invoice_token("inv_abc")
    b = sign_invoice_token("inv_abc")
    c = sign_invoice_token("inv_xyz")
    assert a == b
    assert a != c
    assert len(a) == 32
