"""Phase 4 — LeadOps Reliability tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.leadops_reliability import (
    diagnose,
    overall_status,
    queue_health,
    source_health,
    suggest_next_fix,
)


def test_overall_status_returns_dict() -> None:
    s = overall_status()
    assert "records_total" in s
    assert "drafts_pending" in s
    assert "is_healthy" in s


def test_source_health_lists_supported_sources() -> None:
    h = source_health()
    assert h["total"] >= 8
    sources = {s["source"] for s in h["sources"]}
    assert "manual" in sources
    assert "warm_intro" in sources
    assert "form" in sources


def test_manual_source_always_ready() -> None:
    h = source_health()
    manual = next(s for s in h["sources"] if s["source"] == "manual")
    assert manual["ready"] is True
    assert manual["blocker"] is None


def test_whatsapp_source_blocked_without_env() -> None:
    """Without META_WHATSAPP_TOKEN, whatsapp source is not ready."""
    import os
    os.environ.pop("META_WHATSAPP_TOKEN", None)
    h = source_health()
    whatsapp = next(s for s in h["sources"] if s["source"] == "whatsapp")
    assert whatsapp["ready"] is False
    assert "META_WHATSAPP_TOKEN" in whatsapp["blocker"]


def test_queue_health_returns_dict() -> None:
    h = queue_health()
    assert "total" in h
    assert "by_compliance_status" in h
    assert "by_source" in h


def test_diagnose_never_raises() -> None:
    result = diagnose()
    assert "issues_count" in result
    assert "issues" in result
    assert "is_healthy" in result
    assert isinstance(result["issues"], list)


def test_suggest_next_fix_bilingual() -> None:
    fix = suggest_next_fix()
    assert "next_fix_ar" in fix
    assert "next_fix_en" in fix
    assert "severity" in fix


@pytest.mark.asyncio
async def test_reliability_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/reliability")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert "queue_health" in body
    assert "source_health" in body
    assert body["hard_gates"]["read_only"] is True


@pytest.mark.asyncio
async def test_debug_trace_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/debug-trace")
    assert r.status_code == 200
    body = r.json()
    assert "diagnostic" in body
    assert "issues" in body["diagnostic"]


@pytest.mark.asyncio
async def test_next_fix_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/next-fix")
    assert r.status_code == 200
    body = r.json()
    assert "next_fix" in body
    assert "next_fix_ar" in body["next_fix"]


@pytest.mark.asyncio
async def test_existing_leadops_status_still_works() -> None:
    """Phase 4 must NOT shadow the existing /api/v1/leadops/status endpoint."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/status")
    assert r.status_code == 200
    # Original Wave 3 endpoint returns service: leadops_spine
    assert r.json()["service"] == "leadops_spine"


@pytest.mark.asyncio
async def test_existing_leadops_run_still_works() -> None:
    """Phase 4 must NOT break /api/v1/leadops/run."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leadops/run", json={
            "raw_payload": {"company": "Reliability Test", "email": "x@y.sa", "sector": "real_estate"},
            "source": "manual",
        })
    assert r.status_code == 200
    assert r.json()["leadops_id"].startswith("lops_")
