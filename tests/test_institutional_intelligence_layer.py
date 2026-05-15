"""Tests for Institutional Intelligence Layer systems 56-65."""

from __future__ import annotations

from auto_client_acquisition.institutional_intelligence_layer import (
    REQUIRED_PLATFORM_SURFACES,
    SYSTEMS_56_TO_65,
    AgentNode,
    AssuranceContract,
    AssuranceRuntimeInput,
    DecisionMemoryRecord,
    DependencyEdge,
    FailureEvent,
    InstitutionalDependencySnapshot,
    LearningSignal,
    OrgReasoningInput,
    PolicyRule,
    SocietyTaskPlan,
    WorkflowControlState,
    WorkflowValueSnapshot,
    agent_society_governed,
    assurance_contract_allows_execution,
    approval_overload,
    build_decision_trace,
    chaos_readiness,
    control_plane_ready,
    detect_policy_conflicts,
    governance_optimization_actions,
    institutional_dependency_score,
    learning_actions,
    learning_error_rate,
    learning_improvement,
    memory_fabric_dependency,
    operating_core_verdict,
    organizational_reasoning_summary,
    resilience_recovery_status,
    runtime_operation_allowed,
    value_engine_status,
    workflow_roi,
)


def test_blueprint_surfaces_cover_all_systems() -> None:
    assert set(REQUIRED_PLATFORM_SURFACES) == set(SYSTEMS_56_TO_65)
    assert "/platform/control_plane" in REQUIRED_PLATFORM_SURFACES["56_control_plane"]


def test_control_plane_all_runtime_operations_available() -> None:
    state = WorkflowControlState(
        workflow_id="wf_1",
        policy_version="policy_v7",
        trace_id="trace_1",
        can_stop=True,
        can_reroute=True,
        can_rollback=True,
        can_policy_patch=True,
        checkpoint_id="cp_1",
    )
    ok, blockers = control_plane_ready(state)
    assert ok and blockers == ()
    assert runtime_operation_allowed(state, "rollback")
    assert not runtime_operation_allowed(state, "unknown")


def test_agent_society_requires_boundary_and_reviewer_for_external() -> None:
    agents = (
        AgentNode("a_exec", "executor", "routing", 3, frozenset({"sales"})),
        AgentNode("a_review", "reviewer", "governance", 2, frozenset({"sales"})),
    )
    out = agent_society_governed(
        agents,
        SocietyTaskPlan(
            requested_action="propose_outreach",
            requires_external_action=True,
            required_boundary_tag="sales",
        ),
    )
    assert out["decision"] == "allow_with_review"
    assert len(out["eligible_agents"]) == 2


def test_assurance_contract_requires_checks_and_approval() -> None:
    contract = AssuranceContract(
        contract_id="ct_1",
        permission_scope=frozenset({"external_message_draft"}),
        execution_checks=("policy_evaluated",),
        approval_checks=("human_approval_required",),
        rollback_checks=("rollback_path_exists",),
        evaluation_checks=("output_reviewed",),
    )
    runtime = AssuranceRuntimeInput(
        action_scope="external_message_draft",
        checks_passed=frozenset({"policy_evaluated", "rollback_path_exists", "output_reviewed"}),
        has_human_approval=False,
    )
    ok, blockers = assurance_contract_allows_execution(contract, runtime)
    assert not ok
    assert "human_approval_required" in blockers


def test_memory_fabric_lineage_and_trace() -> None:
    rows = (
        DecisionMemoryRecord(
            decision_id="d_1",
            timestamp_iso="2026-05-15T10:00:00Z",
            actor_id="agent_1",
            policy_version="p_3",
            data_refs=("src_1",),
            rationale="Based on approved source and policy.",
            workflow_id="wf_1",
        ),
    )
    traces = build_decision_trace(rows)
    assert traces["d_1"]["lineage_complete"] is True
    assert memory_fabric_dependency(rows, min_records=1)


def test_organizational_reasoning_propagates_risk() -> None:
    inp = OrgReasoningInput(
        edges=(
            DependencyEdge("intake", "routing", 0.8),
            DependencyEdge("routing", "delivery", 0.7),
        ),
        bottlenecks=frozenset({"routing"}),
        failed_nodes=frozenset({"intake"}),
    )
    out = organizational_reasoning_summary(inp)
    assert "routing" in out["high_risk_nodes"]
    assert "activate_failover_for_high_risk_nodes" in out["recommendations"]


def test_resilience_and_chaos_readiness() -> None:
    recovery = resilience_recovery_status(
        FailureEvent(
            workflow_id="wf_2",
            failure_type="provider_timeout",
            has_checkpoint=True,
            replay_available=True,
            rollback_available=False,
            blast_radius="bounded",
        ),
    )
    assert recovery["can_recover"] is True
    ready, blockers = chaos_readiness(
        canary_enabled=True,
        replay_tested=True,
        rollback_tested=False,
    )
    assert not ready and "rollback_not_tested" in blockers


def test_meta_governance_conflicts_and_actions() -> None:
    conflicts = detect_policy_conflicts(
        (
            PolicyRule("r1", "sales", 1, "external_action", "ALLOW"),
            PolicyRule("r2", "sales", 2, "external_action", "BLOCK"),
        ),
    )
    overload, blockers = approval_overload(
        total_requests=150,
        approved_with_changes=10,
        median_wait_minutes=180,
    )
    actions = governance_optimization_actions(conflicts, blockers)
    assert overload is True
    assert "run_policy_conflict_resolution" in actions


def test_value_engine_and_roi() -> None:
    snapshot = WorkflowValueSnapshot(
        workflow_id="wf_3",
        kpis={"cycle_time_hours": 6.0},
        baseline={"cycle_time_hours": 10.0},
        cost=1000.0,
        revenue_gain=1800.0,
        risk_reduction_value=400.0,
        executive_visibility=True,
    )
    assert workflow_roi(snapshot) == 1.2
    assert value_engine_status(snapshot) == (True, ())


def test_learning_engine_improvement_and_actions() -> None:
    signals = (
        LearningSignal("wf_1", "approval", "failure", "high"),
        LearningSignal("wf_1", "approval", "rollback", "medium"),
        LearningSignal("wf_2", "routing", "success", "low"),
    )
    assert learning_error_rate(signals) == 66.67
    improvement = learning_improvement(previous_error_rate=80.0, current_error_rate=66.67)
    assert improvement["improved"] is True
    assert "improve:approval" in learning_actions(signals)


def test_operating_core_verdict_requires_systems_and_dependency() -> None:
    snapshot = InstitutionalDependencySnapshot(85, 83, 88, 86, 82, 84)
    verdict = operating_core_verdict(
        snapshot=snapshot,
        systems_ready={name: True for name in SYSTEMS_56_TO_65},
    )
    assert institutional_dependency_score(snapshot) >= 80.0
    assert verdict["infrastructure_status"] is True
