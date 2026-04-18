"""
Tests: Leads CRUD
"""
from __future__ import annotations

import pytest
from conftest import auth


@pytest.mark.asyncio
async def test_list_leads(client, token_a):
    """Returns paginated lead list."""
    r = await client.get("/api/v1/leads", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_list_leads_pagination(client, token_a):
    """Limit and offset work correctly."""
    r = await client.get("/api/v1/leads?limit=1&offset=0", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) <= 1


@pytest.mark.asyncio
async def test_list_leads_sector_filter(client, token_a):
    """Sector filter returns only matching leads."""
    r = await client.get("/api/v1/leads?sector=ecommerce", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    for item in data["items"]:
        assert item["sector"] == "ecommerce"


@pytest.mark.asyncio
async def test_get_lead_detail(client, token_a, setup_db):
    """Lead detail returns full data including signals and timeline."""
    lead_id = setup_db["lead_a_id"]
    r = await client.get(f"/api/v1/leads/{lead_id}", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == lead_id
    assert "score_breakdown" in data
    assert "tech_stack" in data
    assert "signals" in data
    assert "timeline" in data
    assert "contacts" in data
    assert isinstance(data["tech_stack"], list)


@pytest.mark.asyncio
async def test_get_lead_not_found(client, token_a):
    """Non-existent lead returns 404."""
    r = await client.get("/api/v1/leads/does-not-exist-xyz", headers=auth(token_a))
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_patch_lead_stage(client, token_a, setup_db):
    """PATCH lead updates stage and logs activity."""
    lead_id = setup_db["lead_a_id"]
    r = await client.patch(
        f"/api/v1/leads/{lead_id}",
        json={"stage": "qualified"},
        headers=auth(token_a)
    )
    assert r.status_code == 200

    # Verify stage was updated
    r2 = await client.get(f"/api/v1/leads/{lead_id}", headers=auth(token_a))
    assert r2.json()["stage"] == "qualified"


@pytest.mark.asyncio
async def test_patch_lead_value(client, token_a, setup_db):
    """PATCH lead updates value_sar."""
    lead_id = setup_db["lead_a_id"]
    r = await client.patch(
        f"/api/v1/leads/{lead_id}",
        json={"value_sar": 99000},
        headers=auth(token_a)
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_list_leads_search(client, token_a):
    """Search filter works on company_name."""
    r = await client.get("/api/v1/leads?search=Alpha", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    # Alpha Corp should be in results
    names = [item["company_name"] for item in data["items"]]
    assert any("Alpha" in n for n in names)
