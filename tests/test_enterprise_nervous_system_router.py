"""API tests for Enterprise Nervous System endpoints."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_blueprint_endpoint_returns_20_systems() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/blueprint")
    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "enterprise_nervous_system"
    assert body["blueprint"]["systems_total"] == 20


@pytest.mark.asyncio
async def test_roadmap_endpoint_returns_three_phases() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/roadmap")
    assert response.status_code == 200
    body = response.json()
    assert len(body["roadmap"]) == 3


@pytest.mark.asyncio
async def test_assess_endpoint_returns_readiness_flags() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    payload = {
        "system_scores": [
            {"system_id": "agent_operating_system", "score": 82},
            {"system_id": "workflow_orchestration_system", "score": 80},
            {"system_id": "governance_operating_system", "score": 78},
            {"system_id": "execution_system", "score": 79},
            {"system_id": "evaluation_system", "score": 81},
            {"system_id": "observability_system", "score": 80},
            {"system_id": "digital_workforce_system", "score": 79},
            {"system_id": "executive_intelligence_system", "score": 83},
            {"system_id": "value_realization_system", "score": 80},
            {"system_id": "continuous_evolution_system", "score": 78},
            {"system_id": "policy_engine_system", "score": 77},
            {"system_id": "approval_fabric_system", "score": 77},
            {"system_id": "platform_reliability_system", "score": 78},
        ]
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/enterprise-nervous-system/assess", json=payload)
    assert response.status_code == 200
    body = response.json()
    assessment = body["assessment"]
    assert assessment["overall_score"] > 0
    assert "readiness_gates" in assessment
    assert "top_priorities" in assessment
    assert len(assessment["roadmap"]) == 3


@pytest.mark.asyncio
async def test_assess_endpoint_rejects_invalid_score() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    payload = {"system_scores": [{"system_id": "agent_operating_system", "score": 500}]}
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/enterprise-nervous-system/assess", json=payload)
    assert response.status_code == 422
