"""Tests for bespoke AI service setup endpoints (W8.1 / R5 productization)."""
from __future__ import annotations

import pytest

VALID_REQUEST = {
    "company_name": "ACME Saudi Co",
    "contact_name": "Ahmed Al-Saudi",
    "contact_email": "ahmed@acme.sa",
    "use_case_summary": "We need a custom AI agent that triages incoming RFP "
                        "documents from government tenders and routes them by "
                        "ministry, deadline, and category.",
    "use_case_category": "ops",
    "complexity": "moderate",
    "integrations_count": 2,
    "data_volume_band": "medium",
    "timeline_weeks": 6,
    "regulated_industry": False,
}


@pytest.mark.asyncio
async def test_submit_returns_request_id_and_estimate(async_client):
    res = await async_client.post(
        "/api/v1/service-setup/requests", json=VALID_REQUEST,
    )
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "received"
    assert body["request_id"].startswith("ssr_")
    assert len(body["request_id"]) == len("ssr_") + 20  # sha256 prefix
    est = body["estimate"]
    assert est["currency"] == "SAR"
    assert est["setup_sar"] >= 5000  # base floor
    assert est["setup_sar"] <= 25000  # MAX_SETUP cap
    assert est["monthly_sar"] >= 1000


@pytest.mark.asyncio
async def test_submit_estimate_scales_with_complexity(async_client):
    """Complex use cases cost more than simple ones — pricing formula."""
    simple = {**VALID_REQUEST, "complexity": "simple"}
    complex_ = {**VALID_REQUEST, "complexity": "complex"}

    res_simple = await async_client.post("/api/v1/service-setup/requests", json=simple)
    res_complex = await async_client.post("/api/v1/service-setup/requests", json=complex_)

    assert res_simple.status_code == 201
    assert res_complex.status_code == 201
    assert res_complex.json()["estimate"]["setup_sar"] > res_simple.json()["estimate"]["setup_sar"]


@pytest.mark.asyncio
async def test_submit_regulated_industry_adds_premium(async_client):
    """30% premium when regulated_industry=True."""
    standard = {**VALID_REQUEST, "regulated_industry": False}
    regulated = {**VALID_REQUEST, "regulated_industry": True}

    res_standard = await async_client.post("/api/v1/service-setup/requests", json=standard)
    res_regulated = await async_client.post("/api/v1/service-setup/requests", json=regulated)

    assert res_regulated.json()["estimate"]["setup_sar"] > res_standard.json()["estimate"]["setup_sar"]


@pytest.mark.asyncio
async def test_submit_caps_setup_at_25k(async_client):
    """Setup price hard-capped at 25,000 SAR per v4 §3 R5."""
    extreme = {
        **VALID_REQUEST,
        "complexity": "complex",
        "data_volume_band": "high",
        "integrations_count": 10,
        "regulated_industry": True,
    }
    res = await async_client.post("/api/v1/service-setup/requests", json=extreme)
    assert res.status_code == 201
    assert res.json()["estimate"]["setup_sar"] <= 25000


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
    assert res.status_code == 422  # Pydantic EmailStr enforcement


@pytest.mark.asyncio
async def test_submit_requires_min_use_case_length(async_client):
    """Forces customer to describe the use case in at least 20 chars."""
    short = {**VALID_REQUEST, "use_case_summary": "too short"}
    res = await async_client.post("/api/v1/service-setup/requests", json=short)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_validates_existing_handle_format(async_client):
    """Bad handle format → 400 (not 422 — we validate after Pydantic)."""
    bad = {**VALID_REQUEST, "existing_customer_handle": "BAD-HANDLE"}
    res = await async_client.post("/api/v1/service-setup/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_idempotency_same_hour(async_client):
    """Same company within same hour returns the same request_id."""
    res1 = await async_client.post("/api/v1/service-setup/requests", json=VALID_REQUEST)
    res2 = await async_client.post("/api/v1/service-setup/requests", json=VALID_REQUEST)
    assert res1.json()["request_id"] == res2.json()["request_id"]


@pytest.mark.asyncio
async def test_get_status_returns_404_until_persisted(async_client):
    """Per v4 §7, persistence deferred until customer #5."""
    res = await async_client.get("/api/v1/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa")
    assert res.status_code == 404
    assert res.json()["detail"]["error"] == "request_not_persisted"


@pytest.mark.asyncio
async def test_decision_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={"decision": "approved", "quoted_setup_halalas": 1_000_000},
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
async def test_decision_approved_requires_setup_price(async_client, monkeypatch):
    """Approving without a price is operator error — block it."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_approved_no_price")
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={"decision": "approved"},
        headers={"X-Admin-API-Key": "test_admin_approved_no_price"},
    )
    assert res.status_code == 400
    assert "quoted_setup_halalas" in res.json()["detail"]
