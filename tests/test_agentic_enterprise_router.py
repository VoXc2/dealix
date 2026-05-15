"""Tests for Enterprise Nervous System router."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_framework_lists_phase_one_core_systems(async_client) -> None:
    res = await async_client.get("/api/v1/agentic-enterprise/framework")
    assert res.status_code == 200
    body = res.json()
    assert body["systems_assessed"] == 12
    assert body["systems_target_default"] == 20
    assert len(body["systems"]) == 12
    assert "hard_gates" in body


@pytest.mark.asyncio
async def test_maturity_assessment_returns_scored_payload(async_client) -> None:
    payload = {
        "system_scores": {
            "agent_operating_system": 72,
            "workflow_orchestration_system": 75,
            "organizational_memory_system": 70,
            "governance_operating_system": 68,
            "executive_intelligence_system": 64,
            "organizational_graph_system": 58,
            "execution_system": 66,
            "evaluation_system": 70,
            "observability_system": 71,
            "transformation_system": 62,
            "digital_workforce_system": 63,
            "continuous_evolution_system": 60,
        }
    }
    res = await async_client.post(
        "/api/v1/agentic-enterprise/maturity-assessment",
        json=payload,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["overall_score"] > 0
    assert body["maturity_band"] in {
        "feature_led",
        "workflow_enabled",
        "system_led",
        "agentic_operator",
        "enterprise_nervous_system_ready",
    }
    assert len(body["systems"]) == 12
    assert len(body["prioritized_next_moves_ar"]) == 5


@pytest.mark.asyncio
async def test_maturity_assessment_rejects_unknown_system_ids(async_client) -> None:
    res = await async_client.post(
        "/api/v1/agentic-enterprise/maturity-assessment",
        json={"system_scores": {"unknown_system": 50}},
    )
    assert res.status_code == 400
    assert res.json()["detail"]["error"] == "unknown_system_ids"
