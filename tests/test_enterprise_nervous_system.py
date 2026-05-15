"""Tests for Enterprise Nervous System assessment."""

from __future__ import annotations

from dataclasses import replace

from auto_client_acquisition.enterprise_maturity_os import (
    CoreSystem,
    CoreSystemsSnapshot,
    OrganizationalCapabilitySnapshot,
    ReadinessBand,
    assess_enterprise_nervous_system,
)


def _systems(score: int) -> CoreSystemsSnapshot:
    return CoreSystemsSnapshot(
        agent_operating_system=score,
        workflow_orchestration_system=score,
        organizational_memory_system=score,
        governance_operating_system=score,
        executive_intelligence_system=score,
        organizational_graph_system=score,
        execution_system=score,
        evaluation_system=score,
        observability_system=score,
        transformation_system=score,
        digital_workforce_system=score,
        continuous_evolution_system=score,
        identity_access_system=score,
        integration_fabric_system=score,
        approval_escalation_system=score,
        policy_risk_compliance_system=score,
        knowledge_retrieval_system=score,
        value_proof_system=score,
        adoption_enablement_system=score,
        enterprise_scaling_system=score,
    )


def _capabilities(score: int) -> OrganizationalCapabilitySnapshot:
    return OrganizationalCapabilitySnapshot(
        workflow_redesign=score,
        workflow_execution=score,
        workflow_governance=score,
        workflow_evaluation=score,
        workflow_scaling=score,
        agent_supervision=score,
        digital_workforce_management=score,
        executive_intelligence_generation=score,
        operational_impact_measurement=score,
        continuous_improvement=score,
    )


def test_core_system_enum_has_20_systems() -> None:
    assert len(tuple(CoreSystem)) == 20


def test_agentic_enterprise_ready_requires_all_85_plus() -> None:
    out = assess_enterprise_nervous_system(_systems(85), _capabilities(85))
    assert out.is_agentic_enterprise_ready is True
    assert out.is_mission_critical_ready is False
    assert out.combined_band == ReadinessBand.ENTERPRISE_READY


def test_mission_critical_requires_all_95_plus() -> None:
    out = assess_enterprise_nervous_system(_systems(96), _capabilities(95))
    assert out.is_agentic_enterprise_ready is True
    assert out.is_mission_critical_ready is True
    assert out.combined_band == ReadinessBand.MISSION_CRITICAL


def test_weakness_detection_and_actions() -> None:
    systems = _systems(82)
    systems = replace(
        systems,
        governance_operating_system=55,
        workflow_orchestration_system=58,
    )
    caps = _capabilities(82)
    caps = replace(
        caps,
        workflow_execution=60,
        operational_impact_measurement=62,
        continuous_improvement=65,
    )
    out = assess_enterprise_nervous_system(systems, caps)
    assert out.is_agentic_enterprise_ready is False
    assert CoreSystem.GOVERNANCE_OPERATING_SYSTEM in out.weak_systems
    assert "workflow_execution" in out.weak_capabilities
    assert any("feedback loop" in action for action in out.next_actions_ar)
