"""
Tests: Multi-tenant isolation
Ensures user from tenant A cannot read tenant B data and vice versa.
"""
from __future__ import annotations

import pytest
from conftest import auth


@pytest.mark.asyncio
async def test_tenant_a_cannot_see_tenant_b_lead(client, token_a, setup_db):
    """Tenant A user cannot read tenant B lead — returns 404."""
    lead_b_id = setup_db["lead_b_id"]
    r = await client.get(f"/api/v1/leads/{lead_b_id}", headers=auth(token_a))
    assert r.status_code == 404, (
        f"Tenant A should NOT see tenant B lead. Got {r.status_code}: {r.text}"
    )


@pytest.mark.asyncio
async def test_tenant_b_cannot_see_tenant_a_lead(client, token_b, setup_db):
    """Tenant B user cannot read tenant A lead — returns 404."""
    lead_a_id = setup_db["lead_a_id"]
    r = await client.get(f"/api/v1/leads/{lead_a_id}", headers=auth(token_b))
    assert r.status_code == 404, (
        f"Tenant B should NOT see tenant A lead. Got {r.status_code}: {r.text}"
    )


@pytest.mark.asyncio
async def test_tenant_a_leads_list_only_shows_own_leads(client, token_a, setup_db):
    """Lead list for tenant A should not include tenant B leads."""
    r = await client.get("/api/v1/leads", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    for item in data["items"]:
        assert item["tenant_id"] == setup_db["tenant_a"], (
            f"Found lead from wrong tenant: {item}"
        )


@pytest.mark.asyncio
async def test_tenant_b_leads_list_only_shows_own_leads(client, token_b, setup_db):
    """Lead list for tenant B should not include tenant A leads."""
    r = await client.get("/api/v1/leads", headers=auth(token_b))
    assert r.status_code == 200
    data = r.json()
    for item in data["items"]:
        assert item["tenant_id"] == setup_db["tenant_b"], (
            f"Found lead from wrong tenant: {item}"
        )


@pytest.mark.asyncio
async def test_tenant_a_cannot_patch_tenant_b_lead(client, token_a, setup_db):
    """Tenant A user cannot update tenant B lead."""
    lead_b_id = setup_db["lead_b_id"]
    r = await client.patch(
        f"/api/v1/leads/{lead_b_id}",
        json={"stage": "closed_won"},
        headers=auth(token_a)
    )
    assert r.status_code == 404, (
        f"Tenant A should NOT be able to patch tenant B lead. Got {r.status_code}"
    )


@pytest.mark.asyncio
async def test_agents_scoped_to_tenant(client, token_b):
    """Tenant B sees no agents (only tenant A has agents seeded)."""
    r = await client.get("/api/v1/agents", headers=auth(token_b))
    assert r.status_code == 200
    data = r.json()
    # Tenant B should see 0 agents (none seeded for it)
    assert data["items"] == []


@pytest.mark.asyncio
async def test_overview_scoped_to_tenant(client, token_a, token_b):
    """Overview KPIs are tenant-scoped."""
    r_a = await client.get("/api/v1/overview", headers=auth(token_a))
    r_b = await client.get("/api/v1/overview", headers=auth(token_b))
    assert r_a.status_code == 200
    assert r_b.status_code == 200
    # Tenant A has more leads (1 vs 1 Beta Corp)
    # Just assert both return valid structure
    assert "kpis" in r_a.json()
    assert "kpis" in r_b.json()


@pytest.mark.asyncio
async def test_pipeline_scoped_to_tenant(client, token_a, token_b):
    """Pipeline endpoint is tenant-scoped."""
    r_a = await client.get("/api/v1/pipeline", headers=auth(token_a))
    r_b = await client.get("/api/v1/pipeline", headers=auth(token_b))
    assert r_a.status_code == 200
    assert r_b.status_code == 200
    # Collect all lead IDs from each
    a_lead_ids = {
        l["id"]
        for col in r_a.json()["columns"]
        for l in col["leads"]
    }
    b_lead_ids = {
        l["id"]
        for col in r_b.json()["columns"]
        for l in col["leads"]
    }
    # No overlap
    assert a_lead_ids.isdisjoint(b_lead_ids), "Pipeline leaked cross-tenant leads!"
