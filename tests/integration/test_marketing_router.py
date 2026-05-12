"""Integration tests for /api/v1/marketing/brochure/{vertical_id}.* (T13e)."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_brochure_pdf_returns_bytes_for_known_vertical(async_client) -> None:
    r = await async_client.get("/api/v1/marketing/brochure/real-estate.pdf")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith(("application/pdf", "text/html"))
    assert len(r.content) > 500


@pytest.mark.asyncio
async def test_brochure_html_serves_html_only(async_client) -> None:
    r = await async_client.get("/api/v1/marketing/brochure/hospitality.html?locale=ar")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert b"<html" in r.content


@pytest.mark.asyncio
async def test_brochure_arabic_locale_renders_rtl(async_client) -> None:
    r = await async_client.get(
        "/api/v1/marketing/brochure/real-estate.html?locale=ar"
    )
    assert r.status_code == 200
    assert b'dir="rtl"' in r.content
    assert b'lang="ar"' in r.content


@pytest.mark.asyncio
async def test_brochure_unknown_vertical_404(async_client) -> None:
    r = await async_client.get("/api/v1/marketing/brochure/imaginary.pdf")
    assert r.status_code == 404
    assert r.json()["detail"] == "vertical_not_found"


@pytest.mark.asyncio
async def test_brochure_lists_only_registered_agents(async_client) -> None:
    """The brochure splits 'today' vs 'roadmap' based on the handler
    registry. The legal vertical claims contract_analyst + compliance_reviewer
    which T9 ships — both must appear in the rendered HTML."""
    r = await async_client.get("/api/v1/marketing/brochure/legal.html?locale=en")
    assert r.status_code == 200
    body = r.content.decode("utf-8")
    assert "contract_analyst" in body
    assert "compliance_reviewer" in body
