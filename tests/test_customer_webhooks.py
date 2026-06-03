"""Tests for customer webhook subscription endpoints (W12.1)."""
from __future__ import annotations

import pytest

ADMIN_HEADER = "X-Admin-API-Key"
VALID_SUB = {
    "url": "https://example-customer.sa/webhooks/dealix",
    "event_types": ["lead.created", "payment.received"],
}


@pytest.mark.asyncio
async def test_subscribe_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json=VALID_SUB,
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_subscribe_rejects_http_url(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_http_reject")
    bad = {**VALID_SUB, "url": "http://insecure-customer.sa/hook"}
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json=bad,
        headers={ADMIN_HEADER: "test_admin_http_reject"},
    )
    assert res.status_code == 400
    assert "https" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_subscribe_rejects_data_url(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_data_reject")
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json={**VALID_SUB, "url": "data:text/html,<script>alert(1)</script>"},
        headers={ADMIN_HEADER: "test_admin_data_reject"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_subscribe_rejects_unknown_event_type(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_event_reject")
    bad = {**VALID_SUB, "event_types": ["lead.created", "bogus.event"]}
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json=bad,
        headers={ADMIN_HEADER: "test_admin_event_reject"},
    )
    assert res.status_code == 400
    assert "unsupported" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_subscribe_validates_handle_format(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_handle")
    res = await async_client.post(
        "/api/v1/customer-webhooks/BAD-HANDLE/subscribe",
        json=VALID_SUB,
        headers={ADMIN_HEADER: "test_admin_handle"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_supported_events_lists_all_known(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_supported")
    res = await async_client.get(
        "/api/v1/customer-webhooks/_supported-events",
        headers={ADMIN_HEADER: "test_admin_supported"},
    )
    assert res.status_code == 200
    body = res.json()
    expected = {
        "lead.created", "lead.replied", "lead.demo_booked",
        "payment.received", "decision_passport.entry_added",
        "tenant.usage.over_cap", "tenant.health.score_changed",
    }
    assert set(body["event_types"]) == expected
    assert body["signature_header"] == "X-Dealix-Signature"
    assert "HMAC-SHA256" in body["signature_algorithm"]


@pytest.mark.asyncio
async def test_list_validates_handle(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_list_handle")
    res = await async_client.get(
        "/api/v1/customer-webhooks/BAD-HANDLE",
        headers={ADMIN_HEADER: "test_admin_list_handle"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_unsubscribe_validates_subscription_id_format(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_sub_id")
    res = await async_client.delete(
        "/api/v1/customer-webhooks/acme_saas/bad-sub-id",
        headers={ADMIN_HEADER: "test_admin_sub_id"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_subscribe_extra_fields_rejected(async_client, monkeypatch):
    """ConfigDict(extra='forbid') blocks attacker-supplied fields like 'secret'."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_extra")
    bad = {**VALID_SUB, "secret": "attacker-chosen-secret"}
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json=bad,
        headers={ADMIN_HEADER: "test_admin_extra"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_subscribe_event_types_min_length(async_client, monkeypatch):
    """Subscribing to zero events is meaningless — block it."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_empty")
    res = await async_client.post(
        "/api/v1/customer-webhooks/acme_saas/subscribe",
        json={"url": "https://example.sa/hook", "event_types": []},
        headers={ADMIN_HEADER: "test_admin_empty"},
    )
    assert res.status_code == 422
