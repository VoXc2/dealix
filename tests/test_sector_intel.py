"""Tests for sector intelligence as research/delivery capability, not price authority."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_list_sectors_exposes_research_scope_not_pricing(async_client):
    res = await async_client.get("/api/v1/sector-intel/sectors")
    assert res.status_code == 200
    body = res.json()
    keys = {s["key"] for s in body["sectors"]}
    assert {"saudi_saas", "real_estate", "logistics"}.issubset(keys)
    assert "currency" not in body
    for sector in body["sectors"]:
        assert "price_sar" not in sector
        assert sector["data_maturity"] in {"partial", "placeholder"}
    authority = body["commercial_authority"]
    assert authority["mode"] == "internal_research_delivery_capability"
    assert authority["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert authority["public_fixed_price"] is False
    assert authority["live_charge_allowed"] is False


@pytest.mark.asyncio
async def test_generate_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "saudi_saas"},
    )
    assert res.status_code in (401, 503)


@pytest.mark.asyncio
async def test_generate_rejects_unknown_sector(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_sector_validation")
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "atlantis"},
        headers={"Authorization": "Bearer test_admin_sector_validation"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_generate_valid_sector_returns_source_bound_report(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_valid_sector")
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "real_estate"},
        headers={"Authorization": "Bearer test_admin_valid_sector"},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["status"] == "generated"
    report = body["report"]
    assert report["sector"] == "real_estate"
    assert "price_sar" not in report
    authority = report["commercial_authority"]
    assert authority["public_fixed_price"] is False
    assert authority["live_charge_allowed"] is False
    assert "executive_summary" in report["sections"]
    assert "account_landscape" in report["sections"]
    assert "market_signals_30d" in report["sections"]
    assert "compliance_notes" in report["sections"]
    for section_name, section in report["sections"].items():
        assert "status" in section, f"section {section_name} missing status"
        assert section["status"] in ("real", "empty", "placeholder")


@pytest.mark.asyncio
async def test_generate_includes_real_compliance_and_commercial_boundaries(
    async_client, monkeypatch
):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_compliance")
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "fintech"},
        headers={"Authorization": "Bearer test_admin_compliance"},
    )
    assert res.status_code == 200
    compliance = res.json()["report"]["sections"]["compliance_notes"]
    assert compliance["status"] == "real"
    assert "lawful/public/first-party" in compliance["pdpl"]
    assert "public business data does not imply consent or relationship" in compliance["pdpl"]
    assert "No standalone report price" in compliance["commercial"]
    assert "customer-specific quote" in compliance["commercial"]


@pytest.mark.asyncio
async def test_fetch_report_returns_404_until_persisted(async_client):
    res = await async_client.get("/api/v1/sector-intel/reports/sr_aaaaaaaaaaaaaaaaaaaa")
    assert res.status_code == 404
    detail = res.json()["detail"]
    assert detail["error"] == "report_not_persisted"


@pytest.mark.asyncio
async def test_fetch_report_validates_id_format(async_client):
    res = await async_client.get("/api/v1/sector-intel/reports/bad-format")
    assert res.status_code == 422
