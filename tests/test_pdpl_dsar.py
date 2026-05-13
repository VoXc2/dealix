"""Tests for PDPL DSAR endpoints (W9.9)."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_submit_access_request_returns_202(async_client):
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "test@example.com", "request_type": "access"},
    )
    assert res.status_code == 202
    body = res.json()
    assert body["request_id"].startswith("dsar_")
    assert body["sla_business_days"] == 5
    assert body["regulatory_max_days"] == 30


@pytest.mark.asyncio
async def test_submit_validates_request_type(async_client):
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "test@example.com", "request_type": "bogus"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_rectify_requires_field_and_value(async_client):
    """Rectification without field+new_value = malformed."""
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "test@example.com", "request_type": "rectify"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_validates_email(async_client):
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "not-an-email", "request_type": "access"},
    )
    assert res.status_code == 422  # Pydantic EmailStr


@pytest.mark.asyncio
async def test_submit_response_never_includes_pii(async_client):
    """The 202 response must NEVER echo the email back — prevents
    identity-enumeration by hitting this endpoint and checking responses."""
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "secret@example.com", "request_type": "access"},
    )
    body_str = str(res.json())
    assert "secret@example.com" not in body_str, (
        "PII leak: submitted email echoed in response"
    )


@pytest.mark.asyncio
async def test_idempotency_same_hour(async_client):
    """Same email + type + hour returns same request_id."""
    payload = {"email": "idem@example.com", "request_type": "erase"}
    res1 = await async_client.post("/api/v1/pdpl/dsar/request", json=payload)
    res2 = await async_client.post("/api/v1/pdpl/dsar/request", json=payload)
    assert res1.json()["request_id"] == res2.json()["request_id"]


@pytest.mark.asyncio
async def test_policy_endpoint_returns_sla_differentiator(async_client):
    res = await async_client.get("/api/v1/pdpl/dsar/policy")
    assert res.status_code == 200
    body = res.json()
    assert body["sla"]["dealix_business_days"] == 5
    assert body["sla"]["pdpl_mandate_days"] == 30
    assert "differentiator" in body["sla"]


@pytest.mark.asyncio
async def test_policy_lists_all_4_request_types(async_client):
    res = await async_client.get("/api/v1/pdpl/dsar/policy")
    types = res.json()["supported_request_types"]
    for t in ("access", "rectify", "port", "erase"):
        assert t in types


@pytest.mark.asyncio
async def test_erasure_spec_transparency(async_client):
    """Public spec of what gets erased — proves the cascade is honest."""
    res = await async_client.get("/api/v1/pdpl/dsar/erasure-cascade-spec")
    assert res.status_code == 200
    body = res.json()
    assert "what_gets_deleted" in body
    assert "what_gets_anonymized_not_deleted" in body
    assert "retention_basis" in body
    # ZATCA + PDPL retention bases must be named
    bases = body["retention_basis"]
    assert "audit_logs_5yr" in bases  # PDPL Art. 18
    assert "payments_6yr" in bases    # ZATCA mandate


@pytest.mark.asyncio
async def test_erasure_spec_documents_atomic_execution(async_client):
    """Spec must say "all-or-nothing" — never partial deletion state."""
    res = await async_client.get("/api/v1/pdpl/dsar/erasure-cascade-spec")
    body = res.json()
    assert "transaction" in body["execution"].lower() or \
           "atomic" in body["execution"].lower()
