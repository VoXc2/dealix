"""Enterprise Nervous System layer contracts and cross-plane operations.

This module moves beyond scoring into operational stack mechanics:
- Layer contracts for each of the 20 systems
- Dependency graph + stack validation
- Cross-plane health scoring (control/intelligence/execution)
- Full readiness assessment aggregator
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from auto_client_acquisition.enterprise_os.nervous_system import (
    CORE_SYSTEMS,
    SYSTEM_IDS,
    compute_enterprise_nervous_system,
)


@dataclass(frozen=True)
class LayerSystemContract:
    """Contract for a single organizational system in the stack."""

    system_id: str
    name: str
    track: str
    risk_tier: str
    default_owner_role: str
    dependencies: tuple[str, ...]
    required_inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    governance_controls: tuple[str, ...]
    primary_kpis: tuple[str, ...]


_META: dict[str, dict[str, Any]] = {
    "agent_operating_system": {
        "risk_tier": "critical",
        "default_owner_role": "agent_platform_lead",
        "dependencies": ("policy_engine_system", "audit_explainability_system"),
        "required_inputs": ("agent_identity", "role_policy", "runtime_scope"),
        "outputs": ("agent_registry", "agent_policy_binding"),
        "governance_controls": ("identity_required", "least_privilege", "kill_switch"),
        "primary_kpis": ("agent_registry_completeness", "policy_binding_success"),
    },
    "workflow_orchestration_system": {
        "risk_tier": "critical",
        "default_owner_role": "workflow_architect",
        "dependencies": ("agent_operating_system", "approval_fabric_system"),
        "required_inputs": ("event_stream", "workflow_templates", "routing_rules"),
        "outputs": ("workflow_runs", "execution_plan", "retry_events"),
        "governance_controls": ("idempotency", "retry_budget", "approval_gate"),
        "primary_kpis": ("workflow_success_rate", "cycle_time_reduction"),
    },
    "organizational_memory_system": {
        "risk_tier": "high",
        "default_owner_role": "knowledge_architect",
        "dependencies": ("knowledge_quality_system", "audit_explainability_system"),
        "required_inputs": ("events", "documents", "policy_updates"),
        "outputs": ("memory_fabric", "retrieval_context"),
        "governance_controls": ("source_traceability", "retention_policy"),
        "primary_kpis": ("memory_grounding_score", "memory_freshness_hours"),
    },
    "governance_operating_system": {
        "risk_tier": "critical",
        "default_owner_role": "governance_officer",
        "dependencies": ("policy_engine_system", "approval_fabric_system"),
        "required_inputs": ("policies", "risk_profile", "regulatory_requirements"),
        "outputs": ("governance_decisions", "approval_routes"),
        "governance_controls": ("human_in_loop", "policy_enforcement"),
        "primary_kpis": ("policy_compliance_pass_rate", "approval_sla"),
    },
    "executive_intelligence_system": {
        "risk_tier": "high",
        "default_owner_role": "strategy_office",
        "dependencies": ("organizational_memory_system", "value_realization_system"),
        "required_inputs": ("ops_signals", "financial_signals", "risk_signals"),
        "outputs": ("executive_briefs", "strategic_alerts"),
        "governance_controls": ("decision_trace", "recommendation_confidence"),
        "primary_kpis": ("executive_signal_latency_hours", "brief_accuracy"),
    },
    "organizational_graph_system": {
        "risk_tier": "high",
        "default_owner_role": "graph_engineering",
        "dependencies": ("organizational_memory_system",),
        "required_inputs": ("entity_events", "workflow_links"),
        "outputs": ("organization_graph", "graph_queries"),
        "governance_controls": ("entity_lineage", "tenant_boundary"),
        "primary_kpis": ("graph_coverage", "relationship_accuracy"),
    },
    "execution_system": {
        "risk_tier": "critical",
        "default_owner_role": "operations_runtime_lead",
        "dependencies": (
            "workflow_orchestration_system",
            "governance_operating_system",
            "observability_system",
        ),
        "required_inputs": ("approved_actions", "tool_adapters", "workflow_context"),
        "outputs": ("execution_events", "action_results"),
        "governance_controls": ("approval_before_external_action", "audit_log_required"),
        "primary_kpis": ("execution_success_rate", "action_error_rate"),
    },
    "evaluation_system": {
        "risk_tier": "critical",
        "default_owner_role": "evaluation_lead",
        "dependencies": ("observability_system", "knowledge_quality_system"),
        "required_inputs": ("runs", "traces", "ground_truth"),
        "outputs": ("quality_scores", "policy_eval_results"),
        "governance_controls": ("eval_required_for_release", "regression_guard"),
        "primary_kpis": ("evaluation_coverage_rate", "hallucination_incidence"),
    },
    "observability_system": {
        "risk_tier": "critical",
        "default_owner_role": "platform_observability",
        "dependencies": (),
        "required_inputs": ("runtime_telemetry", "workflow_events"),
        "outputs": ("traces", "alerts", "health_panels"),
        "governance_controls": ("trace_required", "incident_alerting"),
        "primary_kpis": ("trace_coverage_rate", "incident_mtta_minutes"),
    },
    "transformation_system": {
        "risk_tier": "high",
        "default_owner_role": "transformation_office",
        "dependencies": ("governance_operating_system", "adoption_change_system"),
        "required_inputs": ("baseline_assessment", "target_model"),
        "outputs": ("transformation_roadmap", "playbooks"),
        "governance_controls": ("stage_gate_reviews",),
        "primary_kpis": ("maturity_progress_velocity", "transformation_completion"),
    },
    "digital_workforce_system": {
        "risk_tier": "high",
        "default_owner_role": "digital_workforce_manager",
        "dependencies": ("agent_operating_system", "evaluation_system"),
        "required_inputs": ("agent_roles", "org_structure", "kpi_targets"),
        "outputs": ("ai_org_chart", "agent_performance_reports"),
        "governance_controls": ("role_scoping", "supervision_chain"),
        "primary_kpis": ("digital_workforce_uptime", "agent_goal_attainment"),
    },
    "continuous_evolution_system": {
        "risk_tier": "high",
        "default_owner_role": "continuous_improvement_lead",
        "dependencies": ("evaluation_system", "organizational_memory_system"),
        "required_inputs": ("evaluation_feedback", "incident_postmortems"),
        "outputs": ("approved_improvements", "policy_refinements"),
        "governance_controls": ("change_review_board",),
        "primary_kpis": ("continuous_improvement_velocity", "regression_rate"),
    },
    "policy_engine_system": {
        "risk_tier": "critical",
        "default_owner_role": "policy_engineering",
        "dependencies": (),
        "required_inputs": ("policy_rules", "risk_taxonomy"),
        "outputs": ("policy_decisions", "policy_versions"),
        "governance_controls": ("immutable_policy_versioning",),
        "primary_kpis": ("policy_resolution_latency", "policy_conflict_rate"),
    },
    "approval_fabric_system": {
        "risk_tier": "critical",
        "default_owner_role": "approval_operations",
        "dependencies": ("policy_engine_system",),
        "required_inputs": ("approval_policies", "routing_context"),
        "outputs": ("approval_decisions", "approval_audit"),
        "governance_controls": ("approval_required_external_action",),
        "primary_kpis": ("approval_turnaround_time", "approval_accuracy"),
    },
    "audit_explainability_system": {
        "risk_tier": "critical",
        "default_owner_role": "audit_officer",
        "dependencies": ("observability_system",),
        "required_inputs": ("decisions", "events", "policy_references"),
        "outputs": ("audit_ledger", "explainability_records"),
        "governance_controls": ("append_only_audit", "traceable_decisions"),
        "primary_kpis": ("audit_trace_completeness", "explainability_coverage"),
    },
    "risk_resilience_system": {
        "risk_tier": "high",
        "default_owner_role": "risk_resilience_lead",
        "dependencies": ("observability_system", "governance_operating_system"),
        "required_inputs": ("risk_signals", "incident_events"),
        "outputs": ("risk_register", "resilience_actions"),
        "governance_controls": ("incident_runbook_required",),
        "primary_kpis": ("open_risk_burden", "incident_recovery_time"),
    },
    "knowledge_quality_system": {
        "risk_tier": "high",
        "default_owner_role": "knowledge_quality_lead",
        "dependencies": ("organizational_memory_system",),
        "required_inputs": ("source_catalog", "retrieval_logs"),
        "outputs": ("grounding_scores", "source_quality_alerts"),
        "governance_controls": ("source_passport_required",),
        "primary_kpis": ("source_trust_score", "grounding_recall"),
    },
    "adoption_change_system": {
        "risk_tier": "medium",
        "default_owner_role": "adoption_manager",
        "dependencies": ("transformation_system",),
        "required_inputs": ("training_plans", "change_requests"),
        "outputs": ("adoption_playbooks", "enablement_metrics"),
        "governance_controls": ("change_approval_required",),
        "primary_kpis": ("adoption_rate", "operator_readiness"),
    },
    "value_realization_system": {
        "risk_tier": "high",
        "default_owner_role": "value_operations",
        "dependencies": ("execution_system", "executive_intelligence_system"),
        "required_inputs": ("revenue_metrics", "efficiency_metrics"),
        "outputs": ("value_dashboard", "impact_reports"),
        "governance_controls": ("value_claim_evidence_required",),
        "primary_kpis": ("revenue_leakage_prevented_sar", "net_value_realized"),
    },
    "platform_reliability_system": {
        "risk_tier": "high",
        "default_owner_role": "site_reliability_engineering",
        "dependencies": ("observability_system", "risk_resilience_system"),
        "required_inputs": ("slo_targets", "capacity_metrics"),
        "outputs": ("reliability_reports", "capacity_plans"),
        "governance_controls": ("slo_error_budget_policy",),
        "primary_kpis": ("platform_uptime", "slo_compliance_rate"),
    },
}

_SYSTEM_DEF_BY_ID = {system.system_id: system for system in CORE_SYSTEMS}


def _build_contracts() -> tuple[LayerSystemContract, ...]:
    contracts: list[LayerSystemContract] = []
    for system in CORE_SYSTEMS:
        meta = _META[system.system_id]
        contracts.append(
            LayerSystemContract(
                system_id=system.system_id,
                name=system.name,
                track=system.track,
                risk_tier=meta["risk_tier"],
                default_owner_role=meta["default_owner_role"],
                dependencies=tuple(meta["dependencies"]),
                required_inputs=tuple(meta["required_inputs"]),
                outputs=tuple(meta["outputs"]),
                governance_controls=tuple(meta["governance_controls"]),
                primary_kpis=tuple(meta["primary_kpis"]),
            )
        )
    return tuple(contracts)


LAYER_SYSTEM_CONTRACTS = _build_contracts()

if set(_META) != SYSTEM_IDS:
    raise ValueError("Layer stack metadata must define all core systems exactly once.")


def layer_contracts_payload() -> list[dict[str, Any]]:
    """Serializable contract payload."""
    return [
        {
            "system_id": contract.system_id,
            "name": contract.name,
            "track": contract.track,
            "risk_tier": contract.risk_tier,
            "default_owner_role": contract.default_owner_role,
            "dependencies": list(contract.dependencies),
            "required_inputs": list(contract.required_inputs),
            "outputs": list(contract.outputs),
            "governance_controls": list(contract.governance_controls),
            "primary_kpis": list(contract.primary_kpis),
        }
        for contract in LAYER_SYSTEM_CONTRACTS
    ]


def dependency_graph_payload() -> dict[str, Any]:
    """Graph payload for visualization and topology checks."""
    nodes = [
        {
            "id": system.system_id,
            "name": system.name,
            "track": system.track,
        }
        for system in CORE_SYSTEMS
    ]
    edges = [
        {
            "from": dependency,
            "to": contract.system_id,
        }
        for contract in LAYER_SYSTEM_CONTRACTS
        for dependency in contract.dependencies
    ]
    return {"nodes": nodes, "edges": edges}


def _percent(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100.0, 2)


def validate_layer_stack(implemented_system_ids: Iterable[str]) -> dict[str, Any]:
    """Validate stack completeness, dependency readiness, and plane coverage."""
    raw = {item.strip() for item in implemented_system_ids if item and item.strip()}
    known = {item for item in raw if item in SYSTEM_IDS}
    unknown = sorted(raw - SYSTEM_IDS)
    missing = sorted(SYSTEM_IDS - known)

    dependency_gaps = [
        {"system_id": contract.system_id, "missing_dependency": dependency}
        for contract in LAYER_SYSTEM_CONTRACTS
        if contract.system_id in known
        for dependency in contract.dependencies
        if dependency not in known
    ]

    critical_blockers = [
        gap
        for gap in dependency_gaps
        if _SYSTEM_DEF_BY_ID[gap["system_id"]].track == "control_plane"
    ]

    by_track: dict[str, dict[str, float]] = {}
    for track in ("control_plane", "intelligence_plane", "execution_plane"):
        track_ids = {system.system_id for system in CORE_SYSTEMS if system.track == track}
        by_track[track] = {
            "implemented": float(len(known & track_ids)),
            "total": float(len(track_ids)),
            "coverage_percent": _percent(len(known & track_ids), len(track_ids)),
        }

    core_runtime_requirements = {
        "agent_operating_system",
        "workflow_orchestration_system",
        "governance_operating_system",
        "policy_engine_system",
        "approval_fabric_system",
        "evaluation_system",
        "observability_system",
        "execution_system",
    }
    can_run_governed_autonomy = core_runtime_requirements.issubset(known)

    coverage_percent = _percent(len(known), len(SYSTEM_IDS))
    if coverage_percent >= 85 and not dependency_gaps:
        stack_status = "operational"
    elif coverage_percent >= 60:
        stack_status = "fragile"
    else:
        stack_status = "incomplete"

    return {
        "implemented_count": len(known),
        "systems_total": len(SYSTEM_IDS),
        "coverage_percent": coverage_percent,
        "stack_status": stack_status,
        "can_run_governed_autonomy": can_run_governed_autonomy,
        "missing_systems": missing,
        "unknown_system_ids": unknown,
        "dependency_gaps": dependency_gaps,
        "critical_blockers": critical_blockers,
        "coverage_by_track": by_track,
    }


def _bounded(value: float) -> float:
    return max(0.0, min(100.0, round(float(value), 2)))


def default_health_signals() -> dict[str, float]:
    """Neutral defaults for cross-plane health scoring."""
    return {
        "policy_compliance_rate": 70.0,
        "trace_coverage_rate": 70.0,
        "evaluation_coverage_rate": 65.0,
        "workflow_success_rate": 70.0,
        "exception_escalation_precision": 70.0,
        "memory_grounding_score": 70.0,
        "memory_freshness_hours": 48.0,
        "incident_mtta_minutes": 120.0,
    }


def compute_cross_plane_health(health_signals: Mapping[str, float]) -> dict[str, Any]:
    """Compute health scores for control/intelligence/execution and reliability."""
    merged = {**default_health_signals(), **health_signals}
    policy = _bounded(merged["policy_compliance_rate"])
    trace = _bounded(merged["trace_coverage_rate"])
    eval_cov = _bounded(merged["evaluation_coverage_rate"])
    workflow_success = _bounded(merged["workflow_success_rate"])
    escalation_precision = _bounded(merged["exception_escalation_precision"])
    memory_grounding = _bounded(merged["memory_grounding_score"])

    freshness_hours = max(0.0, float(merged["memory_freshness_hours"]))
    freshness_score = _bounded(100.0 - min(100.0, (freshness_hours / 168.0) * 100.0))

    incident_mtta_minutes = max(0.0, float(merged["incident_mtta_minutes"]))
    incident_response_score = _bounded(
        100.0 - min(100.0, (incident_mtta_minutes / 720.0) * 100.0)
    )

    control_plane_health = round((policy + trace + eval_cov) / 3.0, 2)
    intelligence_plane_health = round((memory_grounding + freshness_score) / 2.0, 2)
    execution_plane_health = round((workflow_success + escalation_precision) / 2.0, 2)
    reliability_health = round((trace + incident_response_score + workflow_success) / 3.0, 2)

    overall = round(
        (
            control_plane_health * 0.35
            + intelligence_plane_health * 0.2
            + execution_plane_health * 0.25
            + reliability_health * 0.2
        ),
        2,
    )

    if overall >= 85:
        health_band = "resilient"
    elif overall >= 70:
        health_band = "stable"
    elif overall >= 55:
        health_band = "at_risk"
    else:
        health_band = "unstable"

    return {
        "overall_health_score": overall,
        "health_band": health_band,
        "control_plane_health": control_plane_health,
        "intelligence_plane_health": intelligence_plane_health,
        "execution_plane_health": execution_plane_health,
        "reliability_health": reliability_health,
        "derived_scores": {
            "memory_freshness_score": freshness_score,
            "incident_response_score": incident_response_score,
        },
    }


def compute_full_enterprise_assessment(
    *,
    system_scores: Mapping[str, float],
    implemented_system_ids: Iterable[str],
    health_signals: Mapping[str, float],
) -> dict[str, Any]:
    """Combine maturity scoring with layer validation and health."""
    maturity = compute_enterprise_nervous_system(system_scores)
    stack_validation = validate_layer_stack(implemented_system_ids)
    cross_plane_health = compute_cross_plane_health(health_signals)

    enterprise_ready = (
        maturity["ready_for_agentic_enterprise"]
        and stack_validation["can_run_governed_autonomy"]
        and not stack_validation["critical_blockers"]
        and cross_plane_health["overall_health_score"] >= 70
    )

    return {
        "enterprise_ready": enterprise_ready,
        "maturity": maturity,
        "stack_validation": stack_validation,
        "cross_plane_health": cross_plane_health,
    }


__all__ = [
    "LAYER_SYSTEM_CONTRACTS",
    "LayerSystemContract",
    "compute_cross_plane_health",
    "compute_full_enterprise_assessment",
    "default_health_signals",
    "dependency_graph_payload",
    "layer_contracts_payload",
    "validate_layer_stack",
]
