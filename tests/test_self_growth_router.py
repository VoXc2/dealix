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


@pytest.mark.asyncio
async def test_health_endpoint_exposes_git_sha_field():
    """Phase C1 — /health must expose a git_sha field. Defaults to
    "unknown" locally; production sets it via Dockerfile ARG GIT_SHA
    or Railway's RAILWAY_GIT_COMMIT_SHA env."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    payload = r.json()
    assert "git_sha" in payload, "HealthResponse must surface git_sha"
    assert isinstance(payload["git_sha"], str) and payload["git_sha"]


@pytest.mark.asyncio
async def test_service_activation_one_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/service-activation/lead_intake_whatsapp")
    assert r.status_code == 200
    payload = r.json()
    assert payload["service_id"] == "lead_intake_whatsapp"
    assert payload["status"] == "partial"
    assert payload["eight_gate_block_present"] is False
    assert any(r.startswith("gate_missing:") for r in payload["blocking_reasons"])


@pytest.mark.asyncio
async def test_service_activation_one_404_for_unknown():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/service-activation/__no_such_id__")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_service_activation_candidates_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/service-activation-candidates")
    assert r.status_code == 200
    payload = r.json()
    assert payload["count"] >= 1
    statuses = {c["status"] for c in payload["candidates"]}
    assert statuses.issubset({"partial", "pilot"})


@pytest.mark.asyncio
async def test_tooling_endpoint_lists_known_tools():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/tooling")
    assert r.status_code == 200
    payload = r.json()
    names = {t["tool_name"] for t in payload["tools"]}
    assert {"pyyaml", "fastapi", "redis"} <= names
    assert payload["summary"]["total"] > 0
    # In CI, all required-for-core tools are installed
    assert payload["core_required_missing"] == []


@pytest.mark.asyncio
async def test_seo_audit_summary_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/seo/audit/summary")
    assert r.status_code == 200
    payload = r.json()
    assert payload["perimeter_clean"] is True
    assert isinstance(payload["advisory_gap_breakdown"], dict)


@pytest.mark.asyncio
async def test_publishing_check_blocks_guaranteed():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/publishing/check",
            json={"text": "We guarantee revenue growth", "language": "en"},
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["decision"] == "blocked"
    assert "guaranteed" in payload["forbidden_tokens_found"]


@pytest.mark.asyncio
async def test_publishing_check_passes_clean_arabic():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/publishing/check",
            json={"text": "صفحة هبوط آمنة جاهزة للمراجعة", "language": "ar"},
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["decision"] == "allowed_draft"
    assert payload["approval_status"] == "approval_required"


@pytest.mark.asyncio
async def test_publishing_check_400_on_missing_text():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/publishing/check",
            json={"language": "ar"},
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_publishing_check_400_on_invalid_language():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/publishing/check",
            json={"text": "x", "language": "fr"},
        )
    assert r.status_code == 400
