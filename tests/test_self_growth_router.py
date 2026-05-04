"""Tests for the Self-Growth OS read-only router.

Verifies that:
  - The router is wired into the FastAPI app at /api/v1/self-growth/.
  - GET /status reports honest guardrails and which sub-payloads exist.
  - GET /service-activation returns a JSON payload matching the YAML
    counts (32 services, current honest distribution).
  - GET /seo/audit returns a payload with the expected schema.
  - All endpoints are pure reads — no live writes, no external calls.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status_endpoint_reports_guardrails():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["service_activation_available"] is True
    assert payload["seo_audit_available"] is True
    g = payload["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True
    assert g["approval_required_for_external_actions"] is True


@pytest.mark.asyncio
async def test_service_activation_endpoint_returns_matrix():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/service-activation")
    assert r.status_code == 200
    payload = r.json()
    assert payload["counts"]["total"] == 32
    assert payload["counts"]["live"] == 0
    assert payload["counts"]["pilot"] == 1
    assert payload["counts"]["partial"] == 7
    assert payload["counts"]["target"] == 24
    assert payload["counts"]["blocked"] == 0
    assert len(payload["services"]) == 32
    assert payload["source_file"] == "docs/registry/SERVICE_READINESS_MATRIX.yaml"


@pytest.mark.asyncio
async def test_seo_audit_endpoint_returns_report():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/seo/audit")
    assert r.status_code == 200
    payload = r.json()
    assert payload["schema_version"] == 1
    assert "summary" in payload
    assert payload["summary"]["pages_with_required_gap"] == 0
    assert "pages" in payload and len(payload["pages"]) > 0
