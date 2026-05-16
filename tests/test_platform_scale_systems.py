from __future__ import annotations

from auto_client_acquisition.platform.accountability import (
    clear_audit_log_for_tests,
    list_audit_events,
)
from auto_client_acquisition.platform.agent_governance import (
    AgentGovernanceStatus,
    assess_agent_governance,
)
from auto_client_acquisition.platform.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.platform.agent_registry import (
    AgentRegistration,
    clear_agent_registry_for_tests,
    register_agent,
    rollback_agent,
)
from auto_client_acquisition.platform.alerts import evaluate_threshold_alert
from auto_client_acquisition.platform.approval_engine import (
    clear_approval_requests_for_tests,
    list_pending_approvals,
)
from auto_client_acquisition.platform.circuit_breakers import CircuitBreaker, CircuitState
from auto_client_acquisition.platform.compensation_logic import CompensationAction
from auto_client_acquisition.platform.freshness import compute_freshness_score
from auto_client_acquisition.platform.incident_tracking import (
    Incident,
    IncidentStatus,
    clear_incidents_for_tests,
    open_incident,
    update_incident_status,
)
from auto_client_acquisition.platform.lineage import (
    LineageEdge,
    build_lineage_index,
    trace_lineage_to_roots,
)
from auto_client_acquisition.platform.memory_governance import (
    MemoryRecord,
    MemorySensitivity,
    memory_confidence_score,
    validate_memory_record,
)
from auto_client_acquisition.platform.metrics import (
    MetricPoint,
    clear_metrics_for_tests,
    metric_summary,
    record_metric,
)
from auto_client_acquisition.platform.operational_analytics import build_operational_analytics
from auto_client_acquisition.platform.policy_engine import ActionRisk, PolicyDecision
from auto_client_acquisition.platform.recovery_engine import execute_recovery
from auto_client_acquisition.platform.retrieval_policies import RetrievalRequest, permission_aware_retrieval
from auto_client_acquisition.platform.reversibility import (
    clear_executions_for_tests,
    rollback_execution,
)
from auto_client_acquisition.platform.runtime_governance import RuntimeActionRequest, govern_action
from auto_client_acquisition.platform.tracing import (
    TraceSpan,
    clear_spans_for_tests,
    list_spans,
    record_span,
)
from auto_client_acquisition.platform.workflow_governance import (
    WorkflowGovernanceStatus,
    assess_workflow_governance,
)
from auto_client_acquisition.platform.workflow_registry import (
    WorkflowRegistration,
    clear_workflow_registry_for_tests,
    list_workflows,
    register_workflow,
    rollback_workflow,
)


def setup_function() -> None:
    clear_agent_registry_for_tests()
    clear_workflow_registry_for_tests()
    clear_approval_requests_for_tests()
    clear_executions_for_tests()
    clear_audit_log_for_tests()
    clear_spans_for_tests()
    clear_metrics_for_tests()
    clear_incidents_for_tests()


def test_agent_and_workflow_sprawl_control_supports_registration_and_rollback() -> None:
    register_agent(
        AgentRegistration(
            agent_id="strategy-agent",
            version="1.0.0",
            owner="ops",
            permissions=("memory:read",),
            memory_scope="tenant",
            lifecycle=AgentLifecycleState.PRODUCTION,
            observable=True,
            rollbackable=True,
        )
    )
    register_agent(
        AgentRegistration(
            agent_id="strategy-agent",
            version="1.1.0",
            owner="ops",
            permissions=("memory:read", "external:execute:approved"),
            memory_scope="tenant",
            lifecycle=AgentLifecycleState.PRODUCTION,
            observable=True,
            rollbackable=True,
        ),
        allow_replace=True,
    )
    restored = rollback_agent("strategy-agent", "1.0.0")
    assert restored.version == "1.0.0"

    ok, errors = assess_agent_governance(
        AgentGovernanceStatus(
            registered=True,
            versioned=True,
            governed=True,
            observable=True,
            evaluated_score=0.92,
            rollbackable=True,
            memory_scope="tenant",
        )
    )
    assert ok is True
    assert errors == ()

    for index in range(10):
        register_workflow(
            WorkflowRegistration(
                workflow_id=f"wf-{index}",
                version="1.0.0",
                owner="ops",
                sla_minutes=30,
                metrics=("latency_ms", "failure_rate"),
                rollbackable=True,
                evals_enabled=True,
            )
        )

    register_workflow(
        WorkflowRegistration(
            workflow_id="wf-0",
            version="1.1.0",
            owner="ops",
            sla_minutes=25,
            metrics=("latency_ms", "failure_rate"),
            rollbackable=True,
            evals_enabled=True,
        ),
        allow_replace=True,
    )
    restored_workflow = rollback_workflow("wf-0", "1.0.0")
    assert restored_workflow.version == "1.0.0"
    assert len(list_workflows()) == 10

    wf_ok, wf_errors = assess_workflow_governance(
        WorkflowGovernanceStatus(
            owner="ops",
            sla_minutes=25,
            metrics_available=True,
            rollbackable=True,
            evals_enabled=True,
        )
    )
    assert wf_ok is True
    assert wf_errors == ()


def test_memory_governance_enforces_lineage_freshness_permissions_and_tenant_isolation() -> None:
    now = 1_000_000
    record_1 = MemoryRecord(
        memory_id="m-1",
        tenant_id="tenant-a",
        source="crm",
        created_at_epoch=now - 100,
        sensitivity=MemorySensitivity.INTERNAL,
        permissions=("memory:read",),
        lineage_id="l-1",
        confidence=0.85,
    )
    record_2 = MemoryRecord(
        memory_id="m-2",
        tenant_id="tenant-b",
        source="notes",
        created_at_epoch=now - 100,
        sensitivity=MemorySensitivity.INTERNAL,
        permissions=("memory:read",),
        lineage_id="l-2",
        confidence=0.9,
    )
    ok_1, errors_1 = validate_memory_record(record_1)
    ok_2, errors_2 = validate_memory_record(record_2)
    assert ok_1 and ok_2
    assert errors_1 == ()
    assert errors_2 == ()

    lineage = build_lineage_index(
        (
            LineageEdge(parent_id="source-1", child_id="m-1", relation="derived_from"),
            LineageEdge(parent_id="source-2", child_id="source-1", relation="derived_from"),
        )
    )
    chain = trace_lineage_to_roots("m-1", lineage)
    assert chain[0] == "m-1"
    assert "source-1" in chain
    assert "source-2" in chain

    retrieved = permission_aware_retrieval(
        (record_1, record_2),
        RetrievalRequest(
            tenant_id="tenant-a",
            actor_permissions=("memory:read",),
            max_sensitivity=MemorySensitivity.INTERNAL,
            now_epoch=now,
            min_freshness=0.2,
        ),
    )
    assert tuple(item.memory_id for item in retrieved) == ("m-1",)

    freshness = compute_freshness_score(now_epoch=now, created_at_epoch=now - 100, ttl_seconds=1_000)
    confidence = memory_confidence_score(source_reliability=0.9, freshness_score=freshness, lineage_score=0.95)
    assert confidence > 0.8


def test_runtime_resilience_and_observability_create_governed_recoverable_execution() -> None:
    request = RuntimeActionRequest(
        action_id="a-1",
        action_name="send_external_email",
        actor="agent-alpha",
        is_external=True,
        risk=ActionRisk.HIGH,
        permissions=("memory:read",),
        requires_data_access=True,
        now_epoch=12345,
        trace_id="trace-1",
        rollback_steps=("revoke_email",),
    )
    result = govern_action(request)
    assert result.decision == PolicyDecision.APPROVAL_REQUIRED
    assert result.approval_request_id.startswith("approval:")
    assert len(list_pending_approvals()) == 1

    allowed_result = govern_action(
        RuntimeActionRequest(
            action_id="a-2",
            action_name="update_internal_plan",
            actor="agent-beta",
            is_external=False,
            risk=ActionRisk.LOW,
            permissions=("memory:read", "external:execute:approved"),
            requires_data_access=True,
            now_epoch=12346,
            trace_id="trace-2",
            rollback_steps=("undo_plan",),
        )
    )
    assert allowed_result.decision == PolicyDecision.ALLOW
    assert allowed_result.reversible_registered is True
    rolled_back, rollback_steps = rollback_execution("a-2")
    assert rolled_back is True
    assert rollback_steps == ("undo_plan",)
    assert len(list_audit_events()) == 2

    breaker = CircuitBreaker(name="integration-api", failure_threshold=2, recovery_timeout_seconds=10)
    breaker.record_failure(now_epoch=100)
    breaker.record_failure(now_epoch=101)
    assert breaker.state == CircuitState.OPEN
    assert breaker.allow_request(now_epoch=105) is False
    assert breaker.allow_request(now_epoch=112) is True

    recovery = execute_recovery(
        failure_code="non_retryable_error",
        retryable_errors=("timeout",),
        executed_actions=(
            CompensationAction(action_id="x", undo_action="undo_x", reversible=True),
            CompensationAction(action_id="y", undo_action="undo_y", reversible=False),
        ),
    )
    assert recovery.strategy == "compensate"
    assert recovery.compensation_steps == ("manual_intervention_required", "undo_x")

    record_span(
        TraceSpan(
            trace_id="trace-1",
            span_id="span-1",
            name="pipeline",
            start_epoch_ms=1_000,
            end_epoch_ms=1_400,
            status="ok",
        )
    )
    record_span(
        TraceSpan(
            trace_id="trace-2",
            span_id="span-2",
            name="pipeline",
            start_epoch_ms=2_000,
            end_epoch_ms=2_900,
            status="error",
        )
    )
    open_incident(
        Incident(
            incident_id="inc-1",
            title="queue lag",
            severity="high",
            status=IncidentStatus.OPEN,
        )
    )
    update_incident_status("inc-1", IncidentStatus.MITIGATED)

    analytics = build_operational_analytics(
        spans=list_spans(),
        open_incidents=1,
        policy_violations=1,
        total_actions=20,
    )
    assert analytics.failure_rate == 0.5
    assert analytics.open_incidents == 1

    record_metric(MetricPoint(metric_name="latency_ms_p95", value=3400, timestamp_epoch=99))
    summary = metric_summary("latency_ms_p95")
    alert = evaluate_threshold_alert(
        metric_name="latency_ms_p95",
        value=summary["avg"],
        warning_threshold=2000,
        critical_threshold=3000,
    )
    assert alert is not None
    assert alert.severity == "critical"
