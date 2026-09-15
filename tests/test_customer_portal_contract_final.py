"""Customer portal contract tests for the current fail-closed public posture.

The historical static customer demo at ``landing/customer-portal.html`` is a
retired public surface. It must redirect to the current proof methodology and
must not resurrect synthetic KPI/demo UI as if it were live customer proof.

The API contract remains independently tested for its eight-section/enriched
shape so internal compatibility is preserved without making the retired HTML
publicly authoritative again.
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
    for key in [
        "ops_summary", "sequences", "radar_today", "digest_weekly",
        "digest_monthly", "service_status_for_customer",
    ]:
        assert key in enriched, f"compatibility key removed: {key}"


@pytest.mark.asyncio
async def test_wave4_enriched_keys_preserved() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/p3-final-3")
    enriched = r.json()["enriched_view"]
    for key in [
        "full_ops_score", "weaknesses_summary", "next_3_decisions",
        "support_summary", "payment_state", "proof_summary",
        "approval_summary", "executive_command_link",
    ]:
        assert key in enriched, f"compatibility key removed: {key}"


def test_retired_customer_demo_redirects_to_proof_methodology() -> None:
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in html
    assert 'http-equiv="refresh" content="0; url=/cases"' in html
    assert 'rel="canonical" href="https://dealix.me/cases"' in html
    assert 'name="robots" content="noindex,nofollow"' in html
    assert "/proof-vault" not in html


def test_retired_customer_demo_labels_synthetic_truth() -> None:
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    low = html.lower()
    assert "synthetic" in low
    assert "ليست دليل عميل" in html
    assert "kpi" in low


def test_retired_customer_demo_does_not_reintroduce_live_dashboard_contract() -> None:
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    for marker in (
        'id="cp-degraded-banner"',
        'class="w13-fourcards"',
        'data-test="w13-card-current-status"',
        "renderW13FourCards",
    ):
        assert marker not in html
