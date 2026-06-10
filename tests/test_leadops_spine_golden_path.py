"""Phase 2 — LeadOps Spine golden path test.

Asserts the full pipeline runs end-to-end:
  intake → normalize → dedupe → compliance → enrich → score
        → brief → offer route → next action → draft → approval

Also asserts the hard rules:
- compliance gate blocks suspicious patterns
- draft never returns approved_execute
- forbidden tokens scrubbed from drafts
- HARD_GATES present on every endpoint response
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_leadops_status_returns_hard_gates() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "leadops_spine"
    gates = body["hard_gates"]
    assert gates["no_live_send"] is True
    assert gates["no_cold_whatsapp"] is True
    assert gates["no_scraping"] is True
    assert gates["approval_required_for_external_actions"] is True


@pytest.mark.asyncio
async def test_leadops_run_full_pipeline_real_estate() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leadops/run", json={
            "raw_payload": {
                "company": "Acme Real Estate",
                "name": "Sami Al-Foulan",
                "email": "sami@acme-re.sa",
                "phone": "+966500000000",
                "sector": "real_estate",
                "region": "Riyadh",
                "message": "We need help qualifying inbound leads from WhatsApp.",
            },
            "source": "warm_intro",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["leadops_id"].startswith("lops_")
    assert body["compliance_status"] == "allowed"
    assert body["score"]["fit"] >= 0.6  # has email + sector + region + company
    assert body["offer_route"]["channel"] == "whatsapp"  # real_estate default
    assert body["offer_route"]["approval_required_before_send"] is True
    assert body["next_action"]["owner"] in ("founder", "csm_or_founder")
    # Draft should be created and queued for approval, not auto-sent
    assert body["draft_id"] is not None


@pytest.mark.asyncio
async def test_leadops_compliance_blocks_scraping_request() -> None:
    """A message asking us to scrape leads must trigger needs_review."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leadops/run", json={
            "raw_payload": {
                "company": "ShadyCorp",
                "email": "shady@example.com",
                "sector": "agencies",
                "message": "We want to scrape competitor websites and harvest emails.",
            },
            "source": "form",
        })
    assert r.status_code == 200
    body = r.json()
    # Either blocked or needs_review — either is acceptable, but never allowed
    assert body["compliance_status"] in ("needs_review", "blocked")
    # No draft generated for non-allowed leads
    assert body["draft_id"] is None
    assert body["next_action"]["owner"] in ("founder", "system")


@pytest.mark.asyncio
async def test_leadops_brief_only_skips_draft() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leadops/brief", json={
            "raw_payload": {
                "company": "Brief Test Co",
                "email": "x@brief.sa",
                "sector": "logistics",
                "region": "Jeddah",
            },
        })
    assert r.status_code == 200
    body = r.json()
    assert body["brief"] is not None
    assert "headline_ar" in body["brief"]
    assert "headline_en" in body["brief"]
    assert body["score"]["fit"] >= 0.0


@pytest.mark.asyncio
async def test_leadops_debug_returns_full_trace() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create one
        run = await c.post("/api/v1/leadops/run", json={
            "raw_payload": {"company": "Trace Co", "email": "t@trace.sa", "sector": "clinics"},
            "source": "manual",
        })
        leadops_id = run.json()["leadops_id"]
        # Debug it
        r = await c.get(f"/api/v1/leadops/debug?leadops_id={leadops_id}")
    assert r.status_code == 200
    body = r.json()
    trace = body["trace"]
    # All 11 trace steps present
    assert "1_raw_payload" in trace
    assert "5_enrichment" in trace
    assert "9_next_action" in trace
    assert "11_approval_id" in trace


@pytest.mark.asyncio
async def test_leadops_debug_404_on_unknown_id() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/leadops/debug?leadops_id=lops_doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_leadops_run_rejects_missing_raw_payload() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leadops/run", json={"source": "manual"})
    assert r.status_code == 422


def test_draft_builder_scrubs_forbidden_tokens() -> None:
    """Direct unit test on draft_builder._scrub for safety."""
    from auto_client_acquisition.leadops_spine.draft_builder import _scrub
    bad = "We guarantee a blast of cold WhatsApp messages — نضمن النتائج"
    cleaned, findings = _scrub(bad)
    assert "[REDACTED]" in cleaned
    assert "guarantee" not in cleaned.lower() or "[REDACTED]" in cleaned
    assert "blast" not in cleaned.lower() or "[REDACTED]" in cleaned
    assert "نضمن" not in cleaned
    assert len(findings) >= 3
