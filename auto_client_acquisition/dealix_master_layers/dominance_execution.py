"""Execution contracts for Organizational Intelligence Dominance."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.dealix_master_layers.registry import OI_DOMINANCE_LAYERS


@dataclass(frozen=True)
class CapabilityContract:
    """One capability contract that must exist for an OI dominance layer."""

    contract_id: str
    layer_slug: str
    capability_name: str
    trigger_event: str
    actor_identity: str
    policy_fence: tuple[str, ...]
    approval_path: tuple[str, ...]
    execution_guarantees: tuple[str, ...]
    evidence_outputs: tuple[str, ...]
    success_kpis: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class GateMilestone:
    """One gate in the dominance execution model."""

    gate_id: str
    title: str
    description: str
    priorities: tuple[str, ...]
    completion_checks: tuple[str, ...]


CAPABILITY_CONTRACTS: tuple[CapabilityContract, ...] = (
    CapabilityContract(
        contract_id="L1-operating-fabric-context",
        layer_slug="enterprise_operating_fabric",
        capability_name="Organizational Context Resolution",
        trigger_event="workflow_started",
        actor_identity="workflow_orchestrator",
        policy_fence=("org_context_required", "state_lineage_required"),
        approval_path=("A0-runtime",),
        execution_guarantees=("deterministic_context_load", "state_transition_traceable"),
        evidence_outputs=("context_resolution_audit_event",),
        success_kpis=("context_resolution_success_rate", "state_lineage_coverage"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L2-digital-workforce-lifecycle",
        layer_slug="digital_workforce_infrastructure",
        capability_name="Agent Lifecycle Governance",
        trigger_event="agent_onboarded_or_offboarded",
        actor_identity="agent_supervisor",
        policy_fence=("agent_identity_required", "permission_scope_required"),
        approval_path=("A1-manager-approval",),
        execution_guarantees=("lifecycle_state_recorded", "policy_boundary_enforced"),
        evidence_outputs=("agent_lifecycle_event", "agent_policy_snapshot"),
        success_kpis=("agent_registry_completeness", "unauthorized_agent_action_rate"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L3-agentic-bpm-routing",
        layer_slug="agentic_bpm_engine",
        capability_name="Adaptive Process Routing",
        trigger_event="process_state_changed",
        actor_identity="process_router",
        policy_fence=("approval_checkpoint_required", "business_boundary_enforced"),
        approval_path=("A1-manager-approval", "A2-risk-approval"),
        execution_guarantees=("routing_replayable", "transition_idempotent"),
        evidence_outputs=("process_transition_event", "governance_route_decision"),
        success_kpis=("routing_success_rate", "policy_breach_rate"),
        status="planned",
    ),
    CapabilityContract(
        contract_id="L4-memory-fabric-lineage",
        layer_slug="organizational_memory_fabric",
        capability_name="Decision Lineage and Citation",
        trigger_event="decision_output_created",
        actor_identity="memory_fabric_runtime",
        policy_fence=("citation_required", "lineage_required"),
        approval_path=("A0-runtime",),
        execution_guarantees=("citation_persisted", "lineage_queryable"),
        evidence_outputs=("decision_lineage_record", "citation_bundle"),
        success_kpis=("lineage_completeness_ratio", "citation_coverage_ratio"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L5-governed-autonomy-runtime",
        layer_slug="governed_autonomy_engine",
        capability_name="Runtime Tool Fencing and Approval",
        trigger_event="external_action_requested",
        actor_identity="governance_runtime",
        policy_fence=("tool_fence_required", "draft_first_required"),
        approval_path=("A2-governance-approval", "A3-executive-approval"),
        execution_guarantees=("action_traceable", "action_reversible_or_compensated"),
        evidence_outputs=("governance_decision_log", "approval_audit_log"),
        success_kpis=("approved_action_ratio", "reversal_success_rate"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L6-execution-dominance-recovery",
        layer_slug="execution_dominance_engine",
        capability_name="Workflow Recovery and Compensation",
        trigger_event="workflow_step_failed",
        actor_identity="execution_recovery_engine",
        policy_fence=("retry_budget_enforced", "compensation_required_for_irreversible"),
        approval_path=("A1-ops-approval",),
        execution_guarantees=("retry_safe", "idempotent_mutations", "compensation_supported"),
        evidence_outputs=("recovery_event", "compensation_event"),
        success_kpis=("recovery_mttr", "failed_workflow_recovery_rate"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L7-executive-intelligence-pack",
        layer_slug="executive_intelligence_engine",
        capability_name="Executive Insight Synthesis",
        trigger_event="weekly_exec_pack_generated",
        actor_identity="executive_reporting_runtime",
        policy_fence=("evidence_backed_insights", "confidence_disclosed"),
        approval_path=("A1-founder-review",),
        execution_guarantees=("insight_generation_reproducible",),
        evidence_outputs=("executive_brief", "forecast_confidence_report"),
        success_kpis=("exec_brief_adoption_rate", "forecast_confidence_accuracy"),
        status="planned",
    ),
    CapabilityContract(
        contract_id="L8-trust-explainability-audit",
        layer_slug="trust_and_explainability_engine",
        capability_name="Decision Explainability and Audit",
        trigger_event="high_impact_decision_finalized",
        actor_identity="trust_engine",
        policy_fence=("explainability_payload_required", "audit_event_required"),
        approval_path=("A2-risk-approval",),
        execution_guarantees=("decision_explainable", "audit_reconstructable"),
        evidence_outputs=("explainability_payload", "auditability_record"),
        success_kpis=("explainability_completeness", "audit_reconstruction_success"),
        status="in_progress",
    ),
    CapabilityContract(
        contract_id="L9-evaluation-dominance-gates",
        layer_slug="evaluation_dominance",
        capability_name="Release Evaluation Gate",
        trigger_event="release_candidate_created",
        actor_identity="release_gate_engine",
        policy_fence=("governance_eval_required", "business_impact_eval_required"),
        approval_path=("A2-quality-gate", "A3-release-gate"),
        execution_guarantees=("failed_gate_blocks_release",),
        evidence_outputs=("evaluation_gate_report",),
        success_kpis=("release_gate_pass_rate", "post_release_incident_rate"),
        status="planned",
    ),
    CapabilityContract(
        contract_id="L10-self-evolving-safe-loop",
        layer_slug="self_evolving_enterprise_engine",
        capability_name="Safe Optimization Loop",
        trigger_event="optimization_candidate_proposed",
        actor_identity="learning_system_runtime",
        policy_fence=("expected_impact_required", "rollback_plan_required"),
        approval_path=("A1-owner-approval", "A2-governance-approval"),
        execution_guarantees=("optimization_staged", "promotion_reversible"),
        evidence_outputs=("optimization_decision_record", "post_optimization_impact_report"),
        success_kpis=("optimization_win_rate", "rollback_incident_rate"),
        status="planned",
    ),
)


DOMINANCE_GATES: tuple[GateMilestone, ...] = (
    GateMilestone(
        gate_id="A",
        title="Governed Actions Foundation",
        description="Identity, policy fences, approvals, and reversibility baseline.",
        priorities=(
            "agent_identity_contract",
            "runtime_governance_contract",
            "reversibility_baseline",
        ),
        completion_checks=(
            "Every production action has policy fence and approval class.",
            "Every mutation path has rollback or compensation record.",
        ),
    ),
    GateMilestone(
        gate_id="B",
        title="Execution Dominance",
        description="Reliable orchestration with retries, idempotency, and recovery.",
        priorities=(
            "workflow_reliability_contract",
            "cross_workflow_observability",
        ),
        completion_checks=(
            "Critical workflows satisfy idempotency and recovery contracts.",
            "DLQ and retry diagnostics are visible to operators.",
        ),
    ),
    GateMilestone(
        gate_id="C",
        title="Memory and Executive Intelligence",
        description="Decision lineage, citations, and executive insight artifacts.",
        priorities=(
            "decision_lineage_standard",
            "executive_intelligence_pack",
        ),
        completion_checks=(
            "Executive decisions carry citation bundle and confidence metadata.",
            "Leadership reports expose ROI, bottlenecks, and forecast posture.",
        ),
    ),
    GateMilestone(
        gate_id="D",
        title="Evaluation Dominance and Self-Evolution",
        description="Release gates and safe optimization loops.",
        priorities=(
            "release_evaluation_gates",
            "safe_learning_loop",
        ),
        completion_checks=(
            "Release candidates fail closed when eval gates fail.",
            "Optimizations require staged rollout and rollback plan.",
        ),
    ),
)


def contracts_by_layer_slug() -> dict[str, tuple[CapabilityContract, ...]]:
    grouped: dict[str, list[CapabilityContract]] = {}
    for contract in CAPABILITY_CONTRACTS:
        grouped.setdefault(contract.layer_slug, []).append(contract)
    return {slug: tuple(contracts) for slug, contracts in grouped.items()}


def missing_contract_layer_slugs() -> tuple[str, ...]:
    grouped = contracts_by_layer_slug()
    missing = [
        layer.slug for layer in OI_DOMINANCE_LAYERS if not grouped.get(layer.slug, ())
    ]
    return tuple(missing)


def dominance_readiness_snapshot() -> dict[str, object]:
    grouped = contracts_by_layer_slug()
    by_status: dict[str, int] = {"planned": 0, "in_progress": 0, "operational": 0}
    for contract in CAPABILITY_CONTRACTS:
        by_status.setdefault(contract.status, 0)
        by_status[contract.status] += 1

    layer_readiness: list[dict[str, object]] = []
    for layer in OI_DOMINANCE_LAYERS:
        contracts = grouped.get(layer.slug, ())
        layer_readiness.append(
            {
                "layer_id": layer.layer_id,
                "slug": layer.slug,
                "title": layer.title,
                "contract_count": len(contracts),
                "statuses": sorted({contract.status for contract in contracts}),
            }
        )

    return {
        "layer_count": len(OI_DOMINANCE_LAYERS),
        "contract_count": len(CAPABILITY_CONTRACTS),
        "status_counts": by_status,
        "missing_layer_contracts": list(missing_contract_layer_slugs()),
        "gates": [gate.gate_id for gate in DOMINANCE_GATES],
        "layer_readiness": layer_readiness,
    }


__all__ = [
    "CAPABILITY_CONTRACTS",
    "DOMINANCE_GATES",
    "CapabilityContract",
    "GateMilestone",
    "contracts_by_layer_slug",
    "dominance_readiness_snapshot",
    "missing_contract_layer_slugs",
]
