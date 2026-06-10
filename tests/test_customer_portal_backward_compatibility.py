"""Phase 10 — Customer Portal backward compatibility.

Asserts:
- 8-section `sections` invariant still holds
- All 6 existing enriched_view keys still present
- Old clients won't break (response shape preserved)
- No internal terms in customer-facing fields
"""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_sections_count_still_8() -> None:
    """Constitutional: exactly 8 sections."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/back-compat-1")
    assert r.status_code == 200
    sections = r.json()["sections"]
    assert len(sections) == 8


@pytest.mark.asyncio
async def test_existing_enriched_view_keys_preserved() -> None:
    """Wave 3 keys MUST still be present after Wave 4."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/back-compat-2")
    enriched = r.json()["enriched_view"]
    wave3_keys = [
        "ops_summary", "sequences", "radar_today",
        "digest_weekly", "digest_monthly", "service_status_for_customer",
    ]
    for k in wave3_keys:
        assert k in enriched, f"Wave 3 key {k} removed — backwards compat broken!"


@pytest.mark.asyncio
async def test_root_endpoint_still_returns_slot_a() -> None:
    """Existing test_portal_root_returns_slot_a contract still holds."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/")
    assert r.status_code == 200
    assert r.json()["customer_handle"] == "Slot-A"


@pytest.mark.asyncio
async def test_promise_ar_en_present() -> None:
    """Bilingual promise still required."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/promise-test")
    body = r.json()
    assert body["promise_ar"]
    assert body["promise_en"]


@pytest.mark.asyncio
async def test_no_internal_terms_after_wave4_changes() -> None:
    """Wave 4 must not introduce internal-term leaks into the portal."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/leak-w4")
    serialized = json.dumps(r.json(), ensure_ascii=False).lower()
    forbidden = [
        "v11", "v12.5", "agent", "router",
        "verifier", "growth_beast", "revops", "compliance_os_v12",
        "auto_client_acquisition", "_safe", "endpoint",
    ]
    for f in forbidden:
        assert f not in serialized, f"Wave 4 portal change leaks: {f}"


@pytest.mark.asyncio
async def test_sections_have_title_ar_en() -> None:
    """Constitutional: every section bilingual."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/bilingual-w4")
    sections = r.json()["sections"]
    for sec in sections.values():
        assert "title_ar" in sec
        assert "title_en" in sec
