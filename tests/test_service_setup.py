"""Tests for bespoke service intake under current quote-only commercial authority."""
from __future__ import annotations

import pytest

VALID_REQUEST = {
    "company_name": "ACME Saudi Co",
    "contact_name": "Ahmed Al-Saudi",
    "contact_email": "ahmed@acme.sa",
    "use_case_summary": (
        "We need a custom AI agent that triages incoming RFP documents from "
        "government tenders and routes them by ministry, deadline, and category."
    ),
    "use_case_category": "ops",
    "complexity": "moderate",
    "integrations_count": 2,
    "data_volume_band": "medium",
    "timeline_weeks": 6,
    "regulated_industry": False,
}


@pytest.mark.asyncio
async def test_submit_returns_request_id_without_automatic_price(async_client):
    res = await async_client.post("/api/v1/service-setup/requests", json=VALID_REQUEST)
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "intake_received"
    assert body["request_id"].startswith("ssr_")
    assert len(body["request_id"]) == len("ssr_") + 20
    assert body["public_fixed_price"] is False
    assert body["automatic_price_estimate"] is False
    assert body["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert body["next_step"] == "free_mini_diagnostic_then_qualified_discovery"
    assert "estimate" not in body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides",
    [
        {"complexity": "simple"},
        {"complexity": "complex"},
        {"regulated_industry": True},
        {
            "complexity": "complex",
            "data_volume_band": "high",
            "integrations_count": 10,
            "regulated_industry": True,
        },
    ],
)
async def test_public_intake_fields_never_generate_price_authority(async_client, overrides):
    payload = {**VALID_REQUEST, **overrides}
    res = await async_client.post("/api/v1/service-setup/requests", json=payload)
    assert res.status_code == 201, res.text
    body = res.json()
    assert body["automatic_price_estimate"] is False
    assert body["public_fixed_price"] is False
    assert "estimate" not in body
    assert "setup_sar" not in body
    assert "monthly_sar" not in body


@pytest.mark.asyncio
async def test_submit_validates_category(async_client):
    bad = {**VALID_REQUEST, "use_case_category": "bogus"}
    res = await async_client.post("/api/v1/service-setup/requests", json=bad)
    assert res.status_code == 400
    assert "use_case_category" in res.json()["detail"]


@pytest.mark.asyncio
async def test_submit_validates_complexity(async_client):
    bad = {**VALID_REQUEST, "complexity": "very_hard"}
    res = await async_client.post("/api/v1/service-setup/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_validates_email(async_client):
    bad = {**VALID_REQUEST, "contact_email": "not-an-email"}
    res = await async_client.post("/api/v1/service-setup/requests", json=bad)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_requires_min_use_case_length(async_client):
    short = {**VALID_REQUEST, "use_case_summary": "too short"}
    res = await async_client.post("/api/v1/service-setup/requests", json=short)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_validates_existing_handle_format(async_client):
    bad = {**VALID_REQUEST, "existing_customer_handle": "BAD-HANDLE"}
    res = await async_client.post("/api/v1/service-setup/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_idempotency_same_hour(async_client):
    res1 = await async_client.post("/api/v1/service-setup/requests", json=VALID_REQUEST)
    res2 = await async_client.post("/api/v1/service-setup/requests", json=VALID_REQUEST)
    assert res1.json()["request_id"] == res2.json()["request_id"]


@pytest.mark.asyncio
async def test_get_status_returns_404_until_persisted(async_client):
    res = await async_client.get("/api/v1/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa")
    assert res.status_code == 404
    assert res.json()["detail"]["error"] == "request_not_persisted"


@pytest.mark.asyncio
async def test_decision_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={
            "decision": "approved",
            "discovery_ref": "discovery:test",
            "quote_id": "quote_test",
            "customer_specific_quote_sar": 10000,
        },
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_decision_validates_decision_field(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_decision")
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={"decision": "maybe"},
        headers={"X-Admin-API-Key": "test_admin_decision"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_approved_decision_requires_discovery_and_customer_specific_quote(
    async_client, monkeypatch
):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_approved_no_quote")
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={"decision": "approved"},
        headers={"X-Admin-API-Key": "test_admin_approved_no_quote"},
    )
    assert res.status_code == 409
    assert res.json()["detail"] == "approved_requires_discovery_ref_and_customer_specific_quote"


@pytest.mark.asyncio
async def test_approved_decision_remains_internal_and_not_sent(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_approved_quote")
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={
            "decision": "approved",
            "discovery_ref": "discovery:test-001",
            "quote_id": "quote_test_001",
            "customer_specific_quote_sar": 12500,
        },
        headers={"X-Admin-API-Key": "test_admin_approved_quote"},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["status"] == "reviewed_not_customer_sent"
    assert body["public_fixed_price"] is False
    assert body["external_send_allowed"] is False
    assert body["quote_id"] == "quote_test_001"
    assert body["customer_specific_quote_sar"] == 12500
