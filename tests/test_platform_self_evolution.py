from __future__ import annotations

from auto_client_acquisition.platform.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.platform.agent_registry import (
    AgentRegistration,
    clear_agent_registry_for_tests,
    register_agent,
)
from auto_client_acquisition.platform.bottleneck_detection import WorkflowPerformance
from auto_client_acquisition.platform.executive_os import build_executive_insight_pack
from auto_client_acquisition.platform.meta_tools import propose_meta_tools
from auto_client_acquisition.platform.org_intelligence import build_org_intelligence
from auto_client_acquisition.platform.process_optimization import build_process_optimization
from auto_client_acquisition.platform.risk_forecasting import RiskSignal
from auto_client_acquisition.platform.scale_control_plane import run_platform_readiness_snapshot
from auto_client_acquisition.platform.self_evolving_core import run_self_evolving_core
from auto_client_acquisition.platform.workflow_learning import WorkflowRunStat, learn_workflow_patterns
from auto_client_acquisition.platform.workflow_registry import (
    WorkflowRegistration,
    clear_workflow_registry_for_tests,
    register_workflow,
)


def setup_function() -> None:
    clear_agent_registry_for_tests()
    clear_workflow_registry_for_tests()


def test_org_intelligence_to_executive_and_self_evolving_core_cycle() -> None:
    org_report = build_org_intelligence(
        performance_rows=(
            WorkflowPerformance(
                workflow_id="wf-acquire",
                latency_minutes_p95=42.0,
                sla_minutes=30.0,
                retry_rate=0.24,
                queue_wait_minutes=20.0,
            ),
            WorkflowPerformance(
                workflow_id="wf-deliver",
                latency_minutes_p95=25.0,
                sla_minutes=30.0,
                retry_rate=0.05,
                queue_wait_minutes=4.0,
            ),
        ),
        risk_signal=RiskSignal(
            open_incidents=4,
            policy_violations_last_7d=3,
            failure_rate=0.11,
            trend_acceleration=0.4,
        ),
    )
    assert org_report.bottlenecks
    assert org_report.risk_band in {"low", "medium", "high", "critical"}

    insight_pack = build_executive_insight_pack(
        week_label="2026-W20",
        revenue_growth_ratio=0.35,
        cost_efficiency_ratio=0.28,
        sla_hit_ratio=0.86,
        governance_coverage_ratio=0.97,
        org_report=org_report,
    )
    assert insight_pack.recommendations
    assert insight_pack.week_label == "2026-W20"

    patterns = learn_workflow_patterns(
        (
            WorkflowRunStat(workflow_id="wf-acquire", latency_ms=3200, cost_usd=0.4, success=True),
            WorkflowRunStat(workflow_id="wf-acquire", latency_ms=3800, cost_usd=0.45, success=False),
            WorkflowRunStat(workflow_id="wf-deliver", latency_ms=2400, cost_usd=0.31, success=True),
        )
    )
    proposals = propose_meta_tools(llm_calls_per_run=12, failure_rate=0.12)
    optimization = build_process_optimization(patterns=patterns, meta_tools=proposals)
    core_report = run_self_evolving_core(
        cycle_id="cycle-2026-05-15",
        process_optimization=optimization,
        strategic_recommendations=insight_pack.recommendations,
        policy_violation_rate=0.02,
        unaudited_action_rate=0.0,
        approval_sla_miss_rate=0.03,
    )
    assert core_report.optimization_summary.optimization_score >= 0.5
    assert core_report.ready_for_next_cycle is True


def test_platform_readiness_snapshot_hits_scale_ready_threshold() -> None:
    for index in range(20):
        register_agent(
            AgentRegistration(
                agent_id=f"agent-{index}",
                version="1.0.0",
                owner="platform-team",
                permissions=("memory:read", "external:execute:approved"),
                memory_scope=f"tenant-{index % 3}",
                lifecycle=AgentLifecycleState.PRODUCTION,
                observable=True,
                rollbackable=True,
            )
        )
    for index in range(10):
        register_workflow(
            WorkflowRegistration(
                workflow_id=f"workflow-{index}",
                version="1.0.0",
                owner="platform-team",
                sla_minutes=30,
                metrics=("latency", "retries", "failures"),
                rollbackable=True,
                evals_enabled=True,
            )
        )

    snapshot = run_platform_readiness_snapshot(
        isolated_clients=3,
        rollback_time_minutes_p95=4.2,
        proactive_failure_detection_rate=0.96,
        dangerous_agent_stop_time_seconds_p95=20.0,
        explainability_coverage_ratio=0.995,
        executive_insights_emitted_last_30d=4,
        workflow_optimization_improvement_ratio=0.08,
        business_impact_accuracy_ratio=0.92,
    )
    assert snapshot.active_agents == 20
    assert snapshot.active_workflows == 10
    assert snapshot.audit_report.verdict == "scale_ready"
    assert snapshot.audit_report.passed_count == 10
