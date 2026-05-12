"""Integration tests for api/routers/skills.py and verticals.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_skills_list_returns_catalog(async_client) -> None:
    r = await async_client.get("/api/v1/skills")
    assert r.status_code == 200
    body = r.json()
    assert "skills" in body
    assert len(body["skills"]) >= 12
    ids = {s["id"] for s in body["skills"]}
    assert "sales_qualifier" in ids
    assert "proposal_writer" in ids


@pytest.mark.asyncio
async def test_skills_by_id_returns_one(async_client) -> None:
    r = await async_client.get("/api/v1/skills/proposal_writer")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "proposal_writer"
    assert body["description"]


@pytest.mark.asyncio
async def test_skills_unknown_404(async_client) -> None:
    r = await async_client.get("/api/v1/skills/not-a-real-skill")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_verticals_list_returns_eight(async_client) -> None:
    r = await async_client.get("/api/v1/verticals")
    assert r.status_code == 200
    body = r.json()
    assert len(body["verticals"]) == 8
    ids = {v["id"] for v in body["verticals"]}
    assert ids >= {
        "real-estate",
        "hospitality",
        "construction",
        "healthcare",
        "education",
        "food-and-beverage",
        "legal",
        "financial-services",
    }


@pytest.mark.asyncio
async def test_vertical_by_id(async_client) -> None:
    r = await async_client.get("/api/v1/verticals/real-estate")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "real-estate"
    assert body["label_ar"]
    assert body["label_en"]
    assert isinstance(body["lead_form_fields"], list)


@pytest.mark.asyncio
async def test_vertical_unknown_404(async_client) -> None:
    r = await async_client.get("/api/v1/verticals/not-a-vertical")
    assert r.status_code == 404
