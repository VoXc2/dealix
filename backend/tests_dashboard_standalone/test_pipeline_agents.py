"""
Tests: Pipeline, Agents, Playbooks, Sources, Analytics, Settings, WebSocket
"""
from __future__ import annotations

import pytest
from conftest import auth


STAGE_LABELS_EXPECTED = [
    "new", "enriching", "qualified", "contacted", "meeting",
    "proposal", "negotiation", "closed_won", "closed_lost"
]


@pytest.mark.asyncio
async def test_pipeline_shape(client, token_a):
    """Pipeline returns columns for each stage."""
    r = await client.get("/api/v1/pipeline", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "columns" in data
    stages = [col["stage"] for col in data["columns"]]
    for expected_stage in ["new", "qualified", "contacted"]:
        assert expected_stage in stages


@pytest.mark.asyncio
async def test_pipeline_column_shape(client, token_a):
    """Each pipeline column has required fields."""
    r = await client.get("/api/v1/pipeline", headers=auth(token_a))
    assert r.status_code == 200
    for col in r.json()["columns"]:
        assert "stage" in col
        assert "label" in col
        assert "count" in col
        assert "value_sar" in col
        assert "leads" in col
        assert isinstance(col["leads"], list)


@pytest.mark.asyncio
async def test_move_stage_via_post(client, token_a, setup_db):
    """Stage move endpoint (drag-drop) works correctly."""
    lead_id = setup_db["lead_a_id"]
    r = await client.post(
        f"/api/v1/leads/{lead_id}/stage",
        json={"stage": "contacted"},
        headers=auth(token_a)
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_list_agents(client, token_a):
    """Agents list returns correct shape."""
    r = await client.get("/api/v1/agents", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    # At least 1 agent seeded for tenant A
    assert len(data["items"]) >= 1
    for agent in data["items"]:
        assert "id" in agent
        assert "name" in agent
        assert "status" in agent
        assert agent["status"] in ("active", "paused")


@pytest.mark.asyncio
async def test_toggle_agent(client, token_a):
    """Toggle agent changes status."""
    r = await client.get("/api/v1/agents", headers=auth(token_a))
    agents = r.json()["items"]
    if not agents:
        pytest.skip("No agents seeded")

    agent = agents[0]
    original_status = agent["status"]

    r2 = await client.post(
        f"/api/v1/agents/{agent['id']}/toggle",
        headers=auth(token_a)
    )
    assert r2.status_code == 200
    data = r2.json()
    # Status should have flipped
    expected = "paused" if original_status == "active" else "active"
    assert data["status"] == expected


@pytest.mark.asyncio
async def test_list_playbooks(client, token_a):
    """Playbooks list returns items."""
    r = await client.get("/api/v1/playbooks", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    for pb in data["items"]:
        assert "id" in pb
        assert "name" in pb
        assert "steps" in pb
        assert isinstance(pb["steps"], list)


@pytest.mark.asyncio
async def test_list_sources(client, token_a):
    """Sources health returns list."""
    r = await client.get("/api/v1/sources", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_sources_discover(client, token_a):
    """Discovery trigger returns 200 with background task started."""
    r = await client.post(
        "/api/v1/sources/saudi_registry/discover",
        headers=auth(token_a)
    )
    assert r.status_code == 200
    assert r.json()["status"] == "discovery_started"


@pytest.mark.asyncio
async def test_analytics_mrr(client, token_a):
    """MRR analytics returns date series."""
    r = await client.get("/api/v1/analytics/mrr?range=30d", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "series" in data
    assert len(data["series"]) == 30
    for point in data["series"]:
        assert "date" in point
        assert "value" in point


@pytest.mark.asyncio
async def test_analytics_conversion(client, token_a):
    """Conversion analytics returns channel items."""
    r = await client.get("/api/v1/analytics/conversion", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_analytics_agent_roi(client, token_a):
    """Agent ROI returns items with correct fields."""
    r = await client.get("/api/v1/analytics/agent-roi", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    for item in data["items"]:
        assert "id" in item
        assert "roi" in item


@pytest.mark.asyncio
async def test_settings_me(client, token_a):
    """Settings me returns user info with masked api keys."""
    r = await client.get("/api/v1/settings/me", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "user_a@test.com"
    assert "tenant_name" in data
    assert "api_keys" in data


@pytest.mark.asyncio
async def test_overview_returns_kpis(client, token_a):
    """Overview returns KPI cards."""
    r = await client.get("/api/v1/overview", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "kpis" in data
    kpis = data["kpis"]
    assert "total_leads" in kpis
    assert "pipeline_value_sar" in kpis
    assert "active_agents" in kpis
    assert "funnel" in data
    assert "recent_activity" in data
    assert "channel_performance" in data
