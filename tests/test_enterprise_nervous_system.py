"""Tests for Enterprise Nervous System scoring engine."""

from __future__ import annotations

from auto_client_acquisition.enterprise_os import (
    capability_roadmap,
    compute_enterprise_nervous_system,
    executive_scorecard_template,
    normalize_scores,
    systems_blueprint,
)


def test_blueprint_contains_20_systems() -> None:
    blueprint = systems_blueprint()
    assert blueprint["systems_total"] == 20
    tracks = blueprint["tracks"]
    assert len(tracks) == 3
    total = sum(len(track["systems"]) for track in tracks)
    assert total == 20


def test_normalize_scores_clamps_and_ignores_unknown() -> None:
    normalized = normalize_scores(
        {
            "agent_operating_system": 120,
            "execution_system": -20,
            "unknown_key": 88,
        }
    )
    assert normalized["agent_operating_system"] == 100.0
    assert normalized["execution_system"] == 0.0
    assert "unknown_key" not in normalized


def test_compute_enterprise_nervous_system_all_high_scores() -> None:
    payload = {
        "agent_operating_system": 90,
        "workflow_orchestration_system": 92,
        "organizational_memory_system": 88,
        "governance_operating_system": 90,
        "executive_intelligence_system": 86,
        "organizational_graph_system": 82,
        "execution_system": 91,
        "evaluation_system": 85,
        "observability_system": 88,
        "transformation_system": 80,
        "digital_workforce_system": 83,
        "continuous_evolution_system": 81,
        "policy_engine_system": 89,
        "approval_fabric_system": 84,
        "audit_explainability_system": 86,
        "risk_resilience_system": 80,
        "knowledge_quality_system": 84,
        "adoption_change_system": 80,
        "value_realization_system": 87,
        "platform_reliability_system": 85,
    }
    result = compute_enterprise_nervous_system(payload)
    assert result["overall_score"] >= 80
    assert result["ready_for_agentic_enterprise"] is True
    assert result["maturity_band"] in {"agentic_enterprise_ready", "enterprise_nervous_system"}


def test_capability_roadmap_three_phases() -> None:
    roadmap = capability_roadmap({"agent_operating_system": 75, "execution_system": 75})
    assert len(roadmap) == 3
    phase_ids = {phase["phase_id"] for phase in roadmap}
    assert phase_ids == {
        "phase_a_control_plane",
        "phase_b_intelligence_plane",
        "phase_c_execution_scale_plane",
    }


def test_scorecard_template_contains_core_kpis() -> None:
    metrics = executive_scorecard_template()
    assert len(metrics) == 10
    metric_ids = {metric["metric_id"] for metric in metrics}
    assert "policy_compliance_pass_rate" in metric_ids
    assert "workflow_success_rate" in metric_ids
