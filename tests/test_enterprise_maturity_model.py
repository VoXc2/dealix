"""Tests for enterprise maturity model (7-stage + 5 verification systems)."""

from __future__ import annotations

from auto_client_acquisition.enterprise_maturity_os import (
    CapabilitySnapshot,
    EnterpriseMaturityStage,
    ExecutiveProofMetrics,
    GovernanceValidationMetrics,
    OperationalEvaluationMetrics,
    ReadinessBand,
    ReadinessGateMetrics,
    VerificationInput,
    WorkflowTestingMetrics,
    assess_enterprise_maturity,
    readiness_band,
)


def _verification(
    *,
    workflow: int,
    governance: int,
    operational: int,
    executive: int,
    gates: int,
) -> VerificationInput:
    return VerificationInput(
        workflow_testing=WorkflowTestingMetrics(
            workflows_end_to_end=workflow,
            approvals_covered=workflow,
            failures_retries_covered=workflow,
            escalations_covered=workflow,
            edge_cases_covered=workflow,
        ),
        governance_validation=GovernanceValidationMetrics(
            approvals_enforced=governance,
            permissions_correct=governance,
            audit_completeness=governance,
            policies_respected=governance,
            boundaries_respected=governance,
        ),
        operational_evaluations=OperationalEvaluationMetrics(
            hallucination_control=operational,
            grounding_accuracy=operational,
            task_success=operational,
            workflow_quality=operational,
            business_roi=operational,
            adoption_strength=operational,
        ),
        executive_proof=ExecutiveProofMetrics(
            revenue_growth_proof=executive,
            time_reduction_proof=executive,
            operations_efficiency_proof=executive,
            approval_speed_proof=executive,
            productivity_proof=executive,
            organizational_leverage_proof=executive,
        ),
        enterprise_readiness_gates=ReadinessGateMetrics(
            architecture_readiness=gates,
            security_readiness=gates,
            governance_readiness=gates,
            workflow_readiness=gates,
            evaluation_readiness=gates,
            operational_readiness=gates,
            delivery_readiness=gates,
            transformation_readiness=gates,
            executive_readiness=gates,
            scale_readiness=gates,
        ),
    )


def _full_caps() -> CapabilitySnapshot:
    return CapabilitySnapshot(
        response_generation=True,
        api_and_tooling=True,
        simple_workflows=True,
        auth_identity=True,
        dashboard_onboarding=True,
        billing_usage=True,
        multi_user_workspaces=True,
        tenant_isolation=True,
        rbac_controls=True,
        governance_audit_policies=True,
        knowledge_layer=True,
        workflow_execution=True,
        operational_evaluations=True,
        agent_lifecycle_management=True,
        workflow_orchestration=True,
        human_approval_routing=True,
        organizational_memory=True,
        operational_intelligence=True,
        distributed_execution=True,
        multi_agent_coordination=True,
        governed_autonomy=True,
        digital_workforce_management=True,
        strategic_intelligence=True,
        continuous_learning_loop=True,
        autonomous_supervision=True,
        simulation_engine=True,
        executive_reasoning=True,
    )


def test_readiness_band_thresholds() -> None:
    assert readiness_band(59) == ReadinessBand.PROTOTYPE
    assert readiness_band(60) == ReadinessBand.INTERNAL_BETA
    assert readiness_band(74) == ReadinessBand.INTERNAL_BETA
    assert readiness_band(75) == ReadinessBand.CLIENT_PILOT
    assert readiness_band(84) == ReadinessBand.CLIENT_PILOT
    assert readiness_band(85) == ReadinessBand.ENTERPRISE_READY
    assert readiness_band(94) == ReadinessBand.ENTERPRISE_READY
    assert readiness_band(95) == ReadinessBand.MISSION_CRITICAL


def test_stage5_reached_with_agentic_enterprise_capabilities() -> None:
    caps = _full_caps()
    ver = _verification(workflow=70, governance=72, operational=74, executive=70, gates=73)
    out = assess_enterprise_maturity(caps, ver)
    assert out.stage == EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE
    assert out.stage_name_en == "Agentic Enterprise Infrastructure"


def test_stage6_requires_enterprise_ready_validation() -> None:
    caps = _full_caps()
    ver = _verification(workflow=85, governance=87, operational=88, executive=86, gates=85)
    out = assess_enterprise_maturity(caps, ver)
    assert out.stage == EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE
    assert out.gate_bands["architecture_readiness"] == ReadinessBand.ENTERPRISE_READY


def test_stage7_requires_mission_critical_validation() -> None:
    caps = _full_caps()
    ver = _verification(workflow=96, governance=97, operational=95, executive=98, gates=95)
    out = assess_enterprise_maturity(caps, ver)
    assert out.stage == EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER
    assert out.missing_for_next_stage == ()


def test_next_stage_gaps_include_capabilities_and_score_requirements() -> None:
    caps = CapabilitySnapshot(
        response_generation=True,
        api_and_tooling=True,
        simple_workflows=True,
        auth_identity=True,
    )
    ver = _verification(workflow=40, governance=50, operational=45, executive=35, gates=30)
    out = assess_enterprise_maturity(caps, ver)
    assert out.stage == EnterpriseMaturityStage.AI_TOOL
    assert "dashboard and onboarding" in out.missing_for_next_stage
