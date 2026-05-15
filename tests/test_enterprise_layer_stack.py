"""Tests for enterprise layer stack contracts and validation."""

from __future__ import annotations

from auto_client_acquisition.enterprise_os import (
    compute_cross_plane_health,
    compute_full_enterprise_assessment,
    dependency_graph_payload,
    layer_contracts_payload,
    validate_layer_stack,
)


def test_layer_contracts_cover_all_systems() -> None:
    contracts = layer_contracts_payload()
    assert len(contracts) == 20
    system_ids = {contract["system_id"] for contract in contracts}
    assert "agent_operating_system" in system_ids
    assert "platform_reliability_system" in system_ids


def test_dependency_graph_has_nodes_and_edges() -> None:
    graph = dependency_graph_payload()
    assert len(graph["nodes"]) == 20
    assert len(graph["edges"]) > 0
    assert any(edge["to"] == "execution_system" for edge in graph["edges"])


def test_validate_layer_stack_detects_missing_dependencies() -> None:
    result = validate_layer_stack(
        [
            "workflow_orchestration_system",
            "execution_system",
        ]
    )
    assert result["stack_status"] in {"incomplete", "fragile"}
    assert result["can_run_governed_autonomy"] is False
    assert len(result["dependency_gaps"]) > 0


def test_cross_plane_health_resilient_band() -> None:
    health = compute_cross_plane_health(
        {
            "policy_compliance_rate": 95,
            "trace_coverage_rate": 92,
            "evaluation_coverage_rate": 90,
            "workflow_success_rate": 93,
            "exception_escalation_precision": 91,
            "memory_grounding_score": 90,
            "memory_freshness_hours": 8,
            "incident_mtta_minutes": 15,
        }
    )
    assert health["overall_health_score"] >= 85
    assert health["health_band"] == "resilient"


def test_full_assessment_returns_combined_artifacts() -> None:
    full = compute_full_enterprise_assessment(
        system_scores={"agent_operating_system": 90, "execution_system": 88},
        implemented_system_ids=[
            "agent_operating_system",
            "workflow_orchestration_system",
            "governance_operating_system",
            "policy_engine_system",
            "approval_fabric_system",
            "evaluation_system",
            "observability_system",
            "execution_system",
        ],
        health_signals={
            "policy_compliance_rate": 80,
            "trace_coverage_rate": 80,
            "evaluation_coverage_rate": 80,
            "workflow_success_rate": 80,
            "exception_escalation_precision": 80,
            "memory_grounding_score": 80,
            "memory_freshness_hours": 24,
            "incident_mtta_minutes": 60,
        },
    )
    assert "maturity" in full
    assert "stack_validation" in full
    assert "cross_plane_health" in full
