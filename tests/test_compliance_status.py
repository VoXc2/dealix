"""Tests for live compliance status endpoint (W9.6)."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_compliance_status_returns_200(async_client):
    """Public endpoint, no auth required."""
    res = await async_client.get("/api/v1/compliance/status")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_compliance_status_includes_all_top_level_sections(async_client):
    """Every section the landing page relies on must be present."""
    res = await async_client.get("/api/v1/compliance/status")
    body = res.json()
    for key in (
        "generated_at",
        "schema_version",
        "overall_posture",
        "pdpl",
        "zatca",
        "security",
        "data_residency",
        "audit_trail",
        "policy_links",
        "disclosure_note",
    ):
        assert key in body, f"missing top-level section: {key}"


@pytest.mark.asyncio
async def test_compliance_status_pdpl_articles_complete(async_client):
    """All 6 PDPL articles we claim to support must appear in the response."""
    res = await async_client.get("/api/v1/compliance/status")
    pdpl = res.json()["pdpl"]
    for article in (
        "art_5_consent",
        "art_13_erasure",
        "art_14_portability",
        "art_18_audit_log",
        "art_21_breach_notification",
        "art_32_dpo",
    ):
        assert article in pdpl, f"missing PDPL article: {article}"
        assert "implemented" in pdpl[article]


@pytest.mark.asyncio
async def test_compliance_status_zatca_features_present(async_client):
    res = await async_client.get("/api/v1/compliance/status")
    zatca = res.json()["zatca"]
    for feature in (
        "phase_2_e_invoice",
        "fatoorah_api",
        "invoice_chaining",
    ):
        assert feature in zatca


@pytest.mark.asyncio
async def test_compliance_status_data_residency_is_gcc(async_client):
    """Saudi sovereign trust requires GCC-only data flow (with disclosed
    cross-border for LLM providers under SCC)."""
    res = await async_client.get("/api/v1/compliance/status")
    residency = res.json()["data_residency"]
    assert residency["no_data_leaves_gcc"] is True
    assert "anthropic" in residency["llm_providers_cross_border"]
    assert "openai" in residency["llm_providers_cross_border"]


@pytest.mark.asyncio
async def test_compliance_status_includes_disclosure_note(async_client):
    """The disclosure note explains the live-state nature — critical for trust."""
    res = await async_client.get("/api/v1/compliance/status")
    note = res.json()["disclosure_note"]
    assert "actual code state" in note.lower() or "live" in note.lower()


@pytest.mark.asyncio
async def test_compliance_status_breach_sla_better_than_mandate(async_client):
    """We commit to 24h breach notification vs PDPL's 72h mandate — that's a
    differentiator that prospects use to evaluate vendors."""
    res = await async_client.get("/api/v1/compliance/status")
    breach = res.json()["pdpl"]["art_21_breach_notification"]
    assert breach.get("sla_hours") == 72  # PDPL mandate
    assert breach.get("dealix_internal_sla_hours") == 24  # our commitment
    assert breach["dealix_internal_sla_hours"] < breach["sla_hours"]
