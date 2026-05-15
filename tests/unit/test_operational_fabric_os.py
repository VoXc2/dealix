"""Regression tests for Systems 26-35 operational fabric foundation."""

from __future__ import annotations

from auto_client_acquisition.operational_fabric_os import (
    AgentDescriptor,
    AgentMesh,
    AssuranceContract,
    DelegationRequest,
    EvolutionCycleInput,
    OperationalMemoryGraph,
    OptimizationProposal,
    RuntimeSafetyPolicy,
    RuntimeSafetyState,
    SandboxExecutionPlan,
    SimulationSpec,
    WorkflowValueInput,
    activate_kill_switch,
    append_checkpoint,
    compute_value_snapshot,
    continuous_optimization_ready,
    create_workflow,
    evaluate_contract,
    evaluate_human_ai_request,
    isolate_agent,
    observe_workflow,
    promote_from_canary,
    recommend_evolution,
    register_execution,
    replay_supported,
    reroute_workflow,
    rollback_workflow,
    run_release_simulation,
    sandbox_gate,
    stop_workflow,
    update_workflow_policy,
    workflow_has_measurable_kpis,
)


def test_system26_control_plane_monitor_stop_rollback_reroute() -> None:
    state = create_workflow(
        workflow_id="wf-1",
        route="pipeline/default",
        policy_version="policy-v1",
        trace_id="trace-123",
    )
    state = append_checkpoint(state, "cp-1")
    state = append_checkpoint(state, "cp-2")
    state = rollback_workflow(state, "cp-1")
    state = reroute_workflow(state, "pipeline/fallback")
    state = update_workflow_policy(state, "policy-v2")
    state = stop_workflow(state)
    obs = observe_workflow(state)
    assert obs["monitorable"] is True
    assert obs["stoppable"] is True
    assert obs["rollbackable"] is True
    assert obs["traceable"] is True
    assert obs["policy_version"] == "policy-v2"
    assert obs["route"] == "pipeline/fallback"
    assert obs["status"] == "stopped"


def test_system27_agent_mesh_discovery_routing_governance() -> None:
    mesh = AgentMesh()
    mesh.register(
        AgentDescriptor(
            agent_id="agent-a",
            capabilities=("score", "trace"),
            trust_boundary="internal",
            health_score=0.6,
        )
    )
    mesh.register(
        AgentDescriptor(
            agent_id="agent-b",
            capabilities=("score",),
            trust_boundary="vendor",
            health_score=0.9,
        )
    )
    assert mesh.route("score") == "agent-b"
    mesh.evaluate("agent-b", observability_score=0.4, policy_compliance=False)
    assert mesh.route("score") == "agent-a"
    isolated = mesh.isolate("agent-a")
    assert isolated.isolated
    assert mesh.route("score") is None
    assert len(mesh.discover(capability="trace", include_isolated=True)) == 1


def test_system28_assurance_contract_blocks_without_checks() -> None:
    contract = AssuranceContract(
        action_name="external_send",
        allow_read=True,
        allow_propose=True,
        allow_execute=True,
        required_checks=("policy_gate", "approval_gate"),
        rollback_required=True,
        governance_policy="external_action_policy_v1",
    )
    blocked = evaluate_contract(
        contract,
        mode="execute",
        provided_checks={"policy_gate"},
        policy_ok=True,
        rollback_available=True,
        trace_id="trace-c1",
    )
    assert blocked.allowed is False
    assert blocked.missing_checks == ("approval_gate",)

    allowed = evaluate_contract(
        contract,
        mode="execute",
        provided_checks={"policy_gate", "approval_gate"},
        policy_ok=True,
        rollback_available=True,
        trace_id="trace-c2",
    )
    assert allowed.allowed is True
    assert allowed.decision == "ALLOW"


def test_system29_sandbox_gate_and_canary_promotion() -> None:
    plan = SandboxExecutionPlan(
        workflow_id="wf-2",
        simulation_passed=True,
        canary_percent=10.0,
        replay_ready=True,
        rollback_ready=True,
        staged_environment="preprod",
    )
    assert sandbox_gate(plan) == (True, ())
    assert promote_from_canary(plan, observed_error_rate=0.01)
    assert not promote_from_canary(plan, observed_error_rate=0.05)


def test_system30_operational_memory_graph_incident_context() -> None:
    graph = OperationalMemoryGraph()
    graph.add_edge(source_id="inc-1", relation="caused_by", target_id="dep:billing")
    graph.add_edge(source_id="inc-1", relation="impacts", target_id="dept:sales")
    graph.add_edge(source_id="inc-1", relation="linked_workflow", target_id="wf-3")
    graph.add_edge(source_id="inc-1", relation="linked_agent", target_id="agent-risk")
    graph.add_edge(source_id="inc-1", relation="introduces_risk", target_id="risk:revenue-loss")
    ctx = graph.incident_context("inc-1")
    assert ctx["root_causes"] == ("dep:billing",)
    assert "wf-3" in ctx["linked_workflows"]
    assert "agent-risk" in ctx["linked_agents"]
    assert "risk:revenue-loss" in ctx["resulting_risks"]


def test_system31_runtime_safety_kill_switch_circuit_breaker_isolation() -> None:
    state = RuntimeSafetyState()
    policy = RuntimeSafetyPolicy(failure_threshold=2, execution_limit=5)

    state, allowed, reason = register_execution(
        state,
        policy,
        action_name="internal_compute",
        success=False,
        agent_id="ag-1",
    )
    assert allowed and reason == "allowed"
    state, allowed, reason = register_execution(
        state,
        policy,
        action_name="internal_compute",
        success=False,
        agent_id="ag-1",
    )
    assert allowed and reason == "allowed"
    _, blocked, blocked_reason = register_execution(
        state,
        policy,
        action_name="internal_compute",
        success=True,
        agent_id="ag-1",
    )
    assert not blocked and blocked_reason == "circuit_breaker_open"

    isolated_state = isolate_agent(RuntimeSafetyState(), "ag-2")
    _, allowed_after_isolation, reason_after_isolation = register_execution(
        isolated_state,
        policy,
        action_name="internal_compute",
        success=True,
        agent_id="ag-2",
    )
    assert not allowed_after_isolation and reason_after_isolation == "agent_isolated"

    ks_state = activate_kill_switch(RuntimeSafetyState())
    _, allowed_after_kill, reason_after_kill = register_execution(
        ks_state,
        policy,
        action_name="internal_compute",
        success=True,
        agent_id="ag-3",
    )
    assert not allowed_after_kill and reason_after_kill == "kill_switch_active"


def test_system32_org_simulation_and_replay() -> None:
    result = run_release_simulation(
        SimulationSpec(
            workflow_steps=5,
            failure_injections=2,
            approval_branches=1,
            load_profile_rps=50,
            incident_scenarios=1,
        )
    )
    assert result.passed is True
    assert result.score == 100.0
    assert replay_supported(3)


def test_system33_human_ai_oversight() -> None:
    decision = evaluate_human_ai_request(
        DelegationRequest(
            task_id="task-1",
            risk_level="high",
            requires_external_action=True,
            confidence=0.82,
            explanation_available=True,
            human_owner="ops-owner",
        )
    )
    assert decision.requires_approval is True
    assert decision.can_human_override is True
    assert decision.can_rollback is True
    assert decision.mode == "human_supervised"


def test_system34_value_engine_kpis_and_roi() -> None:
    snapshot = compute_value_snapshot(
        WorkflowValueInput(
            revenue_before=100_000,
            revenue_after=130_000,
            hours_before=200,
            hours_after=140,
            cycle_time_before=10,
            cycle_time_after=7,
            csat_before=4.1,
            csat_after=4.5,
            cost_of_change=10_000,
        )
    )
    assert snapshot.roi == 200.0
    assert snapshot.revenue_impact == 30_000
    assert workflow_has_measurable_kpis(snapshot)


def test_system35_self_evolving_fabric_safe_gate() -> None:
    proposal = OptimizationProposal(
        proposal_id="opt-1",
        target_workflow="wf-4",
        change_summary="improve approval routing",
        expected_kpi_gain=8.5,
        governance_checks=("policy_gate", "observability_gate"),
        requires_human_approval=True,
        risk_level="high",
    )
    allowed, reason = recommend_evolution(
        EvolutionCycleInput(
            previous_kpi=72.0,
            current_kpi=80.0,
            incident_count=0,
            policy_violations=0,
            proposal=proposal,
        )
    )
    assert allowed
    assert reason == "apply_canary_optimization"
    assert continuous_optimization_ready(pass_rate=0.97, regression_cycles=0)
