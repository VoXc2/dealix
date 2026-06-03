"""Phase 3 — Customer Portal contract finalization tests.

Asserts:
- 8-section invariant still holds (constitutional)
- All 6 Wave 3 enriched_view keys preserved
- All 8 Wave 4 enriched_view keys preserved
- Phase 3 changes are purely additive (new degraded banner element +
  empty-state CSS classes — no breaking change)
"""
from __future__ import annotations

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_sections_still_8() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/p3-final-1")
    assert len(r.json()["sections"]) == 8


@pytest.mark.asyncio
async def test_wave3_enriched_keys_preserved() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/p3-final-2")
    enriched = r.json()["enriched_view"]
    for key in ["ops_summary", "sequences", "radar_today",
                 "digest_weekly", "digest_monthly",
                 "service_status_for_customer"]:
        assert key in enriched, f"Wave 3 key removed: {key}"


@pytest.mark.asyncio
async def test_wave4_enriched_keys_preserved() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/p3-final-3")
    enriched = r.json()["enriched_view"]
    for key in ["full_ops_score", "weaknesses_summary", "next_3_decisions",
                 "support_summary", "payment_state", "proof_summary",
                 "approval_summary", "executive_command_link"]:
        assert key in enriched, f"Wave 4 key removed: {key}"


def test_html_has_degraded_banner_element() -> None:
    """Phase 3 added a degraded banner — assert HTML contains it."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert 'id="cp-degraded-banner"' in html
    assert 'id="cp-degraded-list"' in html
    assert "cp-degraded-banner__sub" in html


def test_html_has_empty_state_css() -> None:
    """Phase 3 added .cp-empty-state CSS class."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert ".cp-empty-state" in html
    assert ".cp-degraded-banner" in html


def test_js_has_degraded_banner_logic() -> None:
    """customer-dashboard.js must implement maybeShowDegradedBanner."""
    js = Path("landing/assets/js/customer-dashboard.js").read_text(encoding="utf-8")
    assert "maybeShowDegradedBanner" in js
    assert "insufficient_data" in js
    assert "cp-degraded-banner" in js


def test_html_arabic_empty_state_copy() -> None:
    """The degraded banner Arabic copy must be present."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "عرض جزئي" in html
    assert "بيانات DEMO" in html
