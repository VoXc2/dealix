"""Tests for sector intelligence report endpoints (W7.2)."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_list_sectors_returns_pricing(async_client):
    res = await async_client.get("/api/v1/sector-intel/sectors")
    assert res.status_code == 200
    body = res.json()
    assert body["currency"] == "SAR"
    keys = {s["key"] for s in body["sectors"]}
    # Core sectors that map to v4 §3 R4 must be present
    assert "saudi_saas" in keys
    assert "real_estate" in keys
    assert "logistics" in keys
    # Each has a positive price
    for sector in body["sectors"]:
        assert sector["price_sar"] > 0


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
async def test_generate_valid_sector_returns_report(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_valid_sector")
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "real_estate"},
        headers={"Authorization": "Bearer test_admin_valid_sector"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "generated"
    report = body["report"]
    assert report["sector"] == "real_estate"
    assert report["price_sar"] == 5000
    # All 6 sections present
    assert "executive_summary" in report["sections"]
    assert "account_landscape" in report["sections"]
    assert "market_signals_30d" in report["sections"]
    assert "compliance_notes" in report["sections"]
    # Each section labels its status honestly
    for section_name, section in report["sections"].items():
        assert "status" in section, f"section {section_name} missing status"
        assert section["status"] in ("real", "empty", "placeholder")


@pytest.mark.asyncio
async def test_generate_includes_compliance_notes(async_client, monkeypatch):
    """Compliance notes must NEVER be a placeholder — they document our PDPL stance."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_compliance")
    res = await async_client.post(
        "/api/v1/sector-intel/generate",
        json={"sector": "fintech"},
        headers={"Authorization": "Bearer test_admin_compliance"},
    )
    assert res.status_code == 200
    compliance = res.json()["report"]["sections"]["compliance_notes"]
    assert compliance["status"] == "real"
    assert "PDPL" in compliance["pdpl"]
    assert "ZATCA" in compliance["zatca"]


@pytest.mark.asyncio
async def test_fetch_report_returns_404_until_persisted(async_client):
    """Persistence is deferred per v4 §7 — until then /reports returns 404."""
    res = await async_client.get("/api/v1/sector-intel/reports/sr_aaaaaaaaaaaaaaaaaaaa")
    assert res.status_code == 404
    detail = res.json()["detail"]
    assert detail["error"] == "report_not_persisted"


@pytest.mark.asyncio
async def test_fetch_report_validates_id_format(async_client):
    """Bad report_id format → 422 (regex pattern enforcement)."""
    res = await async_client.get("/api/v1/sector-intel/reports/bad-format")
    assert res.status_code == 422
