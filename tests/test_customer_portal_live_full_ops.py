"""Phase 10 — Customer Portal live wiring tests.

Asserts:
- 8-section invariant still holds (constitutional)
- enriched_view populated when customer has data
- No internal terms leaked (extends test_constitution_closure)
"""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_portal_8_section_invariant_still_holds() -> None:
    """Constitutional invariant: exactly 8 sections in `sections`."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/portal-test-1")
    assert r.status_code == 200
    body = r.json()
    assert len(body["sections"]) == 8
    assert "1_start_diagnostic" in body["sections"]
    assert "8_next_decision" in body["sections"]


@pytest.mark.asyncio
async def test_enriched_view_present_with_keys() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/portal-test-2")
    body = r.json()
    enriched = body["enriched_view"]
    for key in (
        "ops_summary", "sequences", "radar_today",
        "digest_weekly", "digest_monthly", "service_status_for_customer",
    ):
        assert key in enriched, f"missing enriched key: {key}"


@pytest.mark.asyncio
async def test_enriched_ops_summary_reflects_leadops() -> None:
    """Create a leadops record + service session → ops_summary should reflect."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create a leadops record
        await c.post("/api/v1/leadops/run", json={
            "raw_payload": {
                "company": "Portal Test Co",
                "email": "x@portal.sa",
                "sector": "real_estate",
                "region": "Riyadh",
            },
            "source": "manual",
            "customer_handle": "portal-live-1",
        })
        # Create a service session
        await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "portal-live-1",
            "service_type": "diagnostic",
        })
        # Fetch portal
        r = await c.get("/api/v1/customer-portal/portal-live-1")
    body = r.json()
    ops = body["enriched_view"]["ops_summary"]
    assert ops["leads_today"] >= 1
    assert ops["drafts_pending"] >= 1
    # in_pipeline counts active+delivered+proof_pending; new session is draft
    assert ops["in_pipeline"] == 0


@pytest.mark.asyncio
async def test_enriched_sequences_reflects_session_state() -> None:
    """Service session status flows into enriched_view.sequences."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "portal-seq-test",
            "service_type": "leadops_sprint",
        })
        r = await c.get("/api/v1/customer-portal/portal-seq-test")
    seq = r.json()["enriched_view"]["sequences"]
    assert seq["current_state"] == "draft"


@pytest.mark.asyncio
async def test_enriched_digest_weekly_uses_executive_pack() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/portal-digest-test")
    digest = r.json()["enriched_view"]["digest_weekly"]
    assert "executive_pack_v2" in digest.get("source", "") or "wins" in digest


@pytest.mark.asyncio
async def test_portal_no_internal_term_leak() -> None:
    """Same gate as test_constitution_closure.test_portal_no_internal_leakage —
    verify it still passes after Phase 10 wiring."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/leak-test")
    body = r.json()
    serialized = json.dumps(body, ensure_ascii=False).lower()
    forbidden = [
        "v11", "v12.5", "agent", "router",
        "verifier", "growth_beast", "revops", "compliance_os_v12",
        "auto_client_acquisition", "_safe", "endpoint",
    ]
    for f in forbidden:
        assert f not in serialized, f"customer portal leaks: {f}"


@pytest.mark.asyncio
async def test_portal_each_section_bilingual() -> None:
    """Same gate as test_constitution_closure.test_portal_is_bilingual."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/bilingual-test")
    sections = r.json()["sections"]
    for sec in sections.values():
        assert "title_ar" in sec
        assert "title_en" in sec
