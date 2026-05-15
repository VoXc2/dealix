"""API tests for Enterprise Nervous System endpoints."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.enterprise_nervous_system import router


def _build_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.mark.asyncio
async def test_blueprint_endpoint_returns_20_systems() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/blueprint")
    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "enterprise_nervous_system"
    assert body["blueprint"]["systems_total"] == 20


@pytest.mark.asyncio
async def test_roadmap_endpoint_returns_three_phases() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/roadmap")
    assert response.status_code == 200
    body = response.json()
    assert len(body["roadmap"]) == 3


@pytest.mark.asyncio
async def test_assess_endpoint_returns_readiness_flags() -> None:
    app = _build_test_app()
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
    app = _build_test_app()
    transport = ASGITransport(app=app)
    payload = {"system_scores": [{"system_id": "agent_operating_system", "score": 500}]}
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/enterprise-nervous-system/assess", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_layers_contracts_endpoint() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/layers/contracts")
    assert response.status_code == 200
    body = response.json()
    assert body["contracts_total"] == 20


@pytest.mark.asyncio
async def test_layers_dependencies_endpoint() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise-nervous-system/layers/dependencies")
    assert response.status_code == 200
    body = response.json()
    assert body["nodes_total"] == 20
    assert body["edges_total"] > 0


@pytest.mark.asyncio
async def test_layers_validate_endpoint() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    payload = {
        "implemented_system_ids": [
            "workflow_orchestration_system",
            "execution_system",
        ]
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/enterprise-nervous-system/layers/validate",
            json=payload,
        )
    assert response.status_code == 200
    body = response.json()
    assert "validation" in body
    assert body["validation"]["coverage_percent"] > 0


@pytest.mark.asyncio
async def test_health_cross_plane_endpoint() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    payload = {
        "policy_compliance_rate": 90,
        "trace_coverage_rate": 90,
        "evaluation_coverage_rate": 85,
        "workflow_success_rate": 92,
        "exception_escalation_precision": 88,
        "memory_grounding_score": 87,
        "memory_freshness_hours": 10,
        "incident_mtta_minutes": 20,
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/enterprise-nervous-system/health/cross-plane",
            json=payload,
        )
    assert response.status_code == 200
    body = response.json()
    assert body["health"]["overall_health_score"] > 0


@pytest.mark.asyncio
async def test_assess_full_endpoint() -> None:
    app = _build_test_app()
    transport = ASGITransport(app=app)
    payload = {
        "system_scores": [
            {"system_id": "agent_operating_system", "score": 85},
            {"system_id": "workflow_orchestration_system", "score": 82},
            {"system_id": "execution_system", "score": 84},
            {"system_id": "governance_operating_system", "score": 86},
            {"system_id": "policy_engine_system", "score": 85},
            {"system_id": "approval_fabric_system", "score": 85},
            {"system_id": "evaluation_system", "score": 83},
            {"system_id": "observability_system", "score": 84},
        ],
        "implemented_system_ids": [
            "agent_operating_system",
            "workflow_orchestration_system",
            "governance_operating_system",
            "policy_engine_system",
            "approval_fabric_system",
            "evaluation_system",
            "observability_system",
            "execution_system",
        ],
        "health_signals": {
            "policy_compliance_rate": 90,
            "trace_coverage_rate": 90,
            "evaluation_coverage_rate": 85,
            "workflow_success_rate": 90,
            "exception_escalation_precision": 88,
            "memory_grounding_score": 85,
            "memory_freshness_hours": 12,
            "incident_mtta_minutes": 30,
        },
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/enterprise-nervous-system/assess/full",
            json=payload,
        )
    assert response.status_code == 200
    body = response.json()
    assert "assessment" in body
    assert "enterprise_ready" in body["assessment"]
