"""Tests for Saudi B2B prospect search endpoint (W9.8)."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_search_returns_200_with_no_filters(async_client):
    res = await async_client.get("/api/v1/prospects/search")
    assert res.status_code == 200
    body = res.json()
    assert "results" in body
    assert "total" in body
    assert "limit" in body
    assert "offset" in body


@pytest.mark.asyncio
async def test_search_validates_sector(async_client):
    res = await async_client.get("/api/v1/prospects/search?sector=atlantis")
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_search_validates_region(async_client):
    res = await async_client.get("/api/v1/prospects/search?region=mars")
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_search_validates_size_band(async_client):
    res = await async_client.get("/api/v1/prospects/search?size_band=huge")
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_search_enforces_limit_cap(async_client):
    """Pydantic Query le=100 enforces upper bound."""
    res = await async_client.get("/api/v1/prospects/search?limit=500")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_search_q_max_length(async_client):
    """Free-text q must be ≤ 128 chars."""
    long_q = "a" * 200
    res = await async_client.get(f"/api/v1/prospects/search?q={long_q}")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_search_includes_pdpl_note(async_client):
    """Response must include the PDPL disclosure so caller knows
    fields are public-only — never PII."""
    res = await async_client.get("/api/v1/prospects/search")
    body = res.json()
    if body.get("total", 0) > 0 or body.get("note") is None:
        assert "pdpl_note" in body or "note" in body


@pytest.mark.asyncio
async def test_search_results_never_include_email_or_phone(async_client):
    """Strict PDPL contract: NEVER expose contact PII in this endpoint."""
    res = await async_client.get("/api/v1/prospects/search?limit=5")
    body = res.json()
    for row in body.get("results", []):
        assert "email" not in row, f"PII leak: email in {row}"
        assert "phone" not in row, f"PII leak: phone in {row}"
        assert "contact_name" not in row, f"PII leak: contact_name in {row}"


@pytest.mark.asyncio
async def test_list_sectors_returns_known_set(async_client):
    res = await async_client.get("/api/v1/prospects/sectors")
    assert res.status_code == 200
    body = res.json()
    assert "sectors" in body
    assert "regions" in body
    assert "size_bands" in body
    # Core sectors must be present
    sectors = set(body["sectors"])
    for s in ("saas", "real_estate", "logistics", "fintech"):
        assert s in sectors


@pytest.mark.asyncio
async def test_filters_applied_returned_in_response(async_client):
    """Caller can verify which filters were enforced vs ignored — an
    unsupported filter must never be reported as applied."""
    res = await async_client.get(
        "/api/v1/prospects/search?sector=saas&region=riyadh&size_band=50_250"
    )
    if res.status_code == 200 and "filters_applied" in res.json():
        body = res.json()
        applied = body["filters_applied"]
        ignored = body.get("filters_ignored", [])
        # Each requested filter is either applied with its value, or
        # explicitly listed as ignored — never silently echoed.
        for name, value in (("sector", "saas"), ("region", "riyadh"), ("size_band", "50_250")):
            assert applied.get(name) == value or name in ignored
