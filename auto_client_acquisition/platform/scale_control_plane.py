"""Platform control plane snapshot aligned with final scale test."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.agent_registry import list_agents
from auto_client_acquisition.platform.workflow_registry import list_workflows
from auto_client_acquisition.scale_os.scale_dominance_audit import (
    FinalScaleInputs,
    ScaleAuditReport,
    run_final_scale_test,
)


@dataclass(frozen=True, slots=True)
class PlatformReadinessSnapshot:
    audit_report: ScaleAuditReport
    active_agents: int
    active_workflows: int


def run_platform_readiness_snapshot(
    *,
    isolated_clients: int,
    rollback_time_minutes_p95: float,
    proactive_failure_detection_rate: float,
    dangerous_agent_stop_time_seconds_p95: float,
    explainability_coverage_ratio: float,
    executive_insights_emitted_last_30d: int,
    workflow_optimization_improvement_ratio: float,
    business_impact_accuracy_ratio: float,
    governed_agent_ratio: float = 1.0,
    workflow_chaos_incidents_last_30d: int = 0,
    memory_contamination_incidents_last_30d: int = 0,
) -> PlatformReadinessSnapshot:
    workflows_running = len(list_workflows())
    agents_active = len(list_agents())
    report = run_final_scale_test(
        FinalScaleInputs(
            workflows_running=workflows_running,
            workflow_chaos_incidents_last_30d=workflow_chaos_incidents_last_30d,
            agents_active=agents_active,
            governed_agent_ratio=governed_agent_ratio,
            isolated_clients=isolated_clients,
            memory_contamination_incidents_last_30d=memory_contamination_incidents_last_30d,
            rollback_time_minutes_p95=rollback_time_minutes_p95,
            proactive_failure_detection_rate=proactive_failure_detection_rate,
            dangerous_agent_stop_time_seconds_p95=dangerous_agent_stop_time_seconds_p95,
            explainability_coverage_ratio=explainability_coverage_ratio,
            executive_insights_emitted_last_30d=executive_insights_emitted_last_30d,
            workflow_optimization_improvement_ratio=workflow_optimization_improvement_ratio,
            business_impact_accuracy_ratio=business_impact_accuracy_ratio,
        )
    )
    return PlatformReadinessSnapshot(
        audit_report=report,
        active_agents=agents_active,
        active_workflows=workflows_running,
    )


__all__ = ['PlatformReadinessSnapshot', 'run_platform_readiness_snapshot']
