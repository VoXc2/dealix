"""Tests for R7 Enterprise PMO endpoints (W9.1)."""
from __future__ import annotations

import pytest


VALID_REQUEST = {
    "company_name": "Saudi Mega Corp",
    "contact_name": "Mohammed Al-Saudi",
    "contact_title": "VP Operations",
    "contact_email": "ops@megacorp.sa",
    "org_size": "mid_250_1000",
    "use_case_category": "revenue_ops",
    "use_case_summary": (
        "We need a dedicated Dealix team to run our entire B2B revenue ops: "
        "lead acquisition across 4 channels, AI-assisted reply, weekly exec "
        "briefings to our CEO, and PDPL/ZATCA compliance pack."
    ),
    "regulatory_scope": "pdpl_zatca",
    "target_start_date": "2026-07-01",
    "target_monthly_budget_sar": 40000,
    "contract_length_months": 12,
}


@pytest.mark.asyncio
async def test_submit_returns_request_id_and_readiness(async_client):
    res = await async_client.post(
        "/api/v1/enterprise-pmo/requests", json=VALID_REQUEST,
    )
    assert res.status_code == 201
    body = res.json()
    assert body["request_id"].startswith("epr_")
    assert "readiness" in body
    assert 0 <= body["readiness"]["score"] <= 100
    assert body["readiness"]["band"] in ("high_fit", "moderate_fit", "needs_review")


@pytest.mark.asyncio
async def test_submit_validates_org_size(async_client):
    bad = {**VALID_REQUEST, "org_size": "tiny"}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_validates_use_case_category(async_client):
    bad = {**VALID_REQUEST, "use_case_category": "magic"}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_validates_regulatory_scope(async_client):
    bad = {**VALID_REQUEST, "regulatory_scope": "none"}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_submit_enforces_monthly_budget_min(async_client):
    """R7 floor: 25K SAR/mo. Below that → 422 (Pydantic ge=25000)."""
    bad = {**VALID_REQUEST, "target_monthly_budget_sar": 10000}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_enforces_monthly_budget_cap(async_client):
    """R7 cap: 100K SAR/mo. Above → 422."""
    bad = {**VALID_REQUEST, "target_monthly_budget_sar": 500000}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_enforces_min_contract_length(async_client):
    """Contract minimum 12 months."""
    bad = {**VALID_REQUEST, "contract_length_months": 6}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_validates_use_case_min_length(async_client):
    """Enterprise prospects must describe in ≥ 50 chars (gates seriousness)."""
    bad = {**VALID_REQUEST, "use_case_summary": "We want help"}
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=bad)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_idempotency(async_client):
    """Same company submitting twice in same hour → same request_id."""
    res1 = await async_client.post("/api/v1/enterprise-pmo/requests", json=VALID_REQUEST)
    res2 = await async_client.post("/api/v1/enterprise-pmo/requests", json=VALID_REQUEST)
    assert res1.json()["request_id"] == res2.json()["request_id"]


@pytest.mark.asyncio
async def test_get_engagement_returns_404_deferred(async_client):
    """Engagement persistence deferred until customer #15."""
    res = await async_client.get(
        "/api/v1/enterprise-pmo/engagements/epe_aaaaaaaaaaaaaaaaaaaa"
    )
    assert res.status_code == 404
    assert res.json()["detail"]["error"] == "engagement_not_persisted"


@pytest.mark.asyncio
async def test_create_engagement_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements",
        json={
            "request_id": "epr_aaaaaaaaaaaaaaaaaaaa",
            "tenant_handle": "saudi_mega_corp",
            "monthly_halalas": 4_000_000,
            "contract_start": "2026-07-01",
            "contract_months": 12,
            "exec_sponsor_name": "CEO",
            "exec_sponsor_email": "ceo@megacorp.sa",
        },
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_engagement_admin_succeeds(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_engagement_create")
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements",
        json={
            "request_id": "epr_aaaaaaaaaaaaaaaaaaaa",
            "tenant_handle": "saudi_mega_corp",
            "monthly_halalas": 4_000_000,
            "contract_start": "2026-07-01",
            "contract_months": 12,
            "exec_sponsor_name": "CEO Saudi",
            "exec_sponsor_email": "ceo@megacorp.sa",
        },
        headers={"X-Admin-API-Key": "test_admin_engagement_create"},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["engagement_id"].startswith("epe_")
    assert body["monthly_sar"] == 40000
    assert body["contract_total_sar"] == 40000 * 12


@pytest.mark.asyncio
async def test_create_engagement_enforces_monthly_floor(async_client, monkeypatch):
    """Monthly must be ≥ 25K SAR (2.5M halalas)."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_floor")
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements",
        json={
            "request_id": "epr_aaaaaaaaaaaaaaaaaaaa",
            "tenant_handle": "small_tenant",
            "monthly_halalas": 1_000_000,  # 10K SAR — below floor
            "contract_start": "2026-07-01",
            "contract_months": 12,
            "exec_sponsor_name": "X",
            "exec_sponsor_email": "x@x.sa",
        },
        headers={"X-Admin-API-Key": "test_admin_floor"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_briefing_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements/epe_aaaaaaaaaaaaaaaaaaaa/briefing"
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_briefing_admin_returns_structure(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_briefing")
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements/epe_aaaaaaaaaaaaaaaaaaaa/briefing",
        headers={"X-Admin-API-Key": "test_admin_briefing"},
    )
    assert res.status_code == 200
    body = res.json()
    # All 5 briefing sections present
    for section in ("executive_summary", "revenue_radar", "compliance_ledger",
                    "delivery_ops", "risks_and_decisions"):
        assert section in body["sections"]
