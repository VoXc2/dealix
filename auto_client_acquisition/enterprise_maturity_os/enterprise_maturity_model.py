"""Enterprise maturity model for Agentic Enterprise Infrastructure."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum


class ReadinessBand(StrEnum):
    PROTOTYPE = "prototype"
    INTERNAL_BETA = "internal_beta"
    CLIENT_PILOT = "client_pilot"
    ENTERPRISE_READY = "enterprise_ready"
    MISSION_CRITICAL = "mission_critical"


class EnterpriseMaturityStage(IntEnum):
    AI_TOOL = 1
    AI_SAAS_PLATFORM = 2
    ENTERPRISE_AI_PLATFORM = 3
    AGENTIC_OPERATING_PLATFORM = 4
    AGENTIC_ENTERPRISE_INFRASTRUCTURE = 5
    ENTERPRISE_READY_INFRASTRUCTURE = 6
    MISSION_CRITICAL_OPERATING_LAYER = 7


READINESS_GATES: tuple[str, ...] = (
    "architecture_readiness",
    "security_readiness",
    "governance_readiness",
    "workflow_readiness",
    "evaluation_readiness",
    "operational_readiness",
    "delivery_readiness",
    "transformation_readiness",
    "executive_readiness",
    "scale_readiness",
)

STAGE_EN_LABELS: dict[EnterpriseMaturityStage, str] = {
    EnterpriseMaturityStage.AI_TOOL: "AI Tool",
    EnterpriseMaturityStage.AI_SAAS_PLATFORM: "AI SaaS Platform",
    EnterpriseMaturityStage.ENTERPRISE_AI_PLATFORM: "Enterprise AI Platform",
    EnterpriseMaturityStage.AGENTIC_OPERATING_PLATFORM: "Agentic Operating Platform",
    EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE: "Agentic Enterprise Infrastructure",
    EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE: "Enterprise-Ready Infrastructure",
    EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER: "Mission-Critical Operating Layer",
}

STAGE_AR_LABELS: dict[EnterpriseMaturityStage, str] = {
    EnterpriseMaturityStage.AI_TOOL: "أداة AI",
    EnterpriseMaturityStage.AI_SAAS_PLATFORM: "منصة SaaS للذكاء الاصطناعي",
    EnterpriseMaturityStage.ENTERPRISE_AI_PLATFORM: "منصة AI مؤسسية",
    EnterpriseMaturityStage.AGENTIC_OPERATING_PLATFORM: "منصة تشغيل Agentic",
    EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE: "بنية مؤسسية Agentic",
    EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE: "بنية جاهزة للمؤسسات",
    EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER: "طبقة تشغيلية حرجة للمؤسسة",
}

_CAPABILITY_LABELS: dict[str, str] = {
    "response_generation": "AI response generation",
    "api_and_tooling": "API and tool surface",
    "simple_workflows": "basic workflows",
    "auth_identity": "auth and identity",
    "dashboard_onboarding": "dashboard and onboarding",
    "billing_usage": "billing and usage tracking",
    "multi_user_workspaces": "multi-user workspaces",
    "tenant_isolation": "tenant isolation",
    "rbac_controls": "RBAC controls",
    "governance_audit_policies": "governance, approvals, and audit",
    "knowledge_layer": "permission-aware knowledge layer",
    "workflow_execution": "workflow execution runtime",
    "operational_evaluations": "operational evaluations",
    "agent_lifecycle_management": "agent lifecycle management",
    "workflow_orchestration": "workflow orchestration",
    "human_approval_routing": "human approval routing",
    "organizational_memory": "organizational memory",
    "operational_intelligence": "operational intelligence metrics",
    "distributed_execution": "distributed execution",
    "multi_agent_coordination": "multi-agent coordination",
    "governed_autonomy": "governed autonomy",
    "digital_workforce_management": "digital workforce management",
    "strategic_intelligence": "strategic intelligence",
    "continuous_learning_loop": "continuous learning",
    "autonomous_supervision": "autonomous supervision",
    "simulation_engine": "simulation engine",
    "executive_reasoning": "executive reasoning",
}

_STAGE_CAPABILITIES: dict[EnterpriseMaturityStage, tuple[str, ...]] = {
    EnterpriseMaturityStage.AI_TOOL: (
        "response_generation",
        "api_and_tooling",
        "simple_workflows",
    ),
    EnterpriseMaturityStage.AI_SAAS_PLATFORM: (
        "auth_identity",
        "dashboard_onboarding",
        "billing_usage",
        "multi_user_workspaces",
    ),
    EnterpriseMaturityStage.ENTERPRISE_AI_PLATFORM: (
        "tenant_isolation",
        "rbac_controls",
        "governance_audit_policies",
        "knowledge_layer",
        "workflow_execution",
        "operational_evaluations",
    ),
    EnterpriseMaturityStage.AGENTIC_OPERATING_PLATFORM: (
        "agent_lifecycle_management",
        "workflow_orchestration",
        "human_approval_routing",
        "organizational_memory",
        "operational_intelligence",
    ),
    EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE: (
        "distributed_execution",
        "multi_agent_coordination",
        "governed_autonomy",
        "digital_workforce_management",
        "strategic_intelligence",
    ),
    EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE: (
        "continuous_learning_loop",
        "autonomous_supervision",
    ),
    EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER: (
        "simulation_engine",
        "executive_reasoning",
    ),
}


def _bounded_score(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return int(value)


def _mean(*values: int) -> int:
    if not values:
        return 0
    return int(round(sum(values) / len(values)))


def readiness_band(score: int) -> ReadinessBand:
    bounded = _bounded_score(score)
    if bounded <= 59:
        return ReadinessBand.PROTOTYPE
    if bounded <= 74:
        return ReadinessBand.INTERNAL_BETA
    if bounded <= 84:
        return ReadinessBand.CLIENT_PILOT
    if bounded <= 94:
        return ReadinessBand.ENTERPRISE_READY
    return ReadinessBand.MISSION_CRITICAL


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    response_generation: bool = False
    api_and_tooling: bool = False
    simple_workflows: bool = False
    auth_identity: bool = False
    dashboard_onboarding: bool = False
    billing_usage: bool = False
    multi_user_workspaces: bool = False
    tenant_isolation: bool = False
    rbac_controls: bool = False
    governance_audit_policies: bool = False
    knowledge_layer: bool = False
    workflow_execution: bool = False
    operational_evaluations: bool = False
    agent_lifecycle_management: bool = False
    workflow_orchestration: bool = False
    human_approval_routing: bool = False
    organizational_memory: bool = False
    operational_intelligence: bool = False
    distributed_execution: bool = False
    multi_agent_coordination: bool = False
    governed_autonomy: bool = False
    digital_workforce_management: bool = False
    strategic_intelligence: bool = False
    continuous_learning_loop: bool = False
    autonomous_supervision: bool = False
    simulation_engine: bool = False
    executive_reasoning: bool = False


@dataclass(frozen=True, slots=True)
class WorkflowTestingMetrics:
    workflows_end_to_end: int
    approvals_covered: int
    failures_retries_covered: int
    escalations_covered: int
    edge_cases_covered: int

    def score(self) -> int:
        return _mean(
            _bounded_score(self.workflows_end_to_end),
            _bounded_score(self.approvals_covered),
            _bounded_score(self.failures_retries_covered),
            _bounded_score(self.escalations_covered),
            _bounded_score(self.edge_cases_covered),
        )


@dataclass(frozen=True, slots=True)
class GovernanceValidationMetrics:
    approvals_enforced: int
    permissions_correct: int
    audit_completeness: int
    policies_respected: int
    boundaries_respected: int

    def score(self) -> int:
        return _mean(
            _bounded_score(self.approvals_enforced),
            _bounded_score(self.permissions_correct),
            _bounded_score(self.audit_completeness),
            _bounded_score(self.policies_respected),
            _bounded_score(self.boundaries_respected),
        )


@dataclass(frozen=True, slots=True)
class OperationalEvaluationMetrics:
    hallucination_control: int
    grounding_accuracy: int
    task_success: int
    workflow_quality: int
    business_roi: int
    adoption_strength: int

    def score(self) -> int:
        return _mean(
            _bounded_score(self.hallucination_control),
            _bounded_score(self.grounding_accuracy),
            _bounded_score(self.task_success),
            _bounded_score(self.workflow_quality),
            _bounded_score(self.business_roi),
            _bounded_score(self.adoption_strength),
        )


@dataclass(frozen=True, slots=True)
class ExecutiveProofMetrics:
    revenue_growth_proof: int
    time_reduction_proof: int
    operations_efficiency_proof: int
    approval_speed_proof: int
    productivity_proof: int
    organizational_leverage_proof: int

    def score(self) -> int:
        return _mean(
            _bounded_score(self.revenue_growth_proof),
            _bounded_score(self.time_reduction_proof),
            _bounded_score(self.operations_efficiency_proof),
            _bounded_score(self.approval_speed_proof),
            _bounded_score(self.productivity_proof),
            _bounded_score(self.organizational_leverage_proof),
        )


@dataclass(frozen=True, slots=True)
class ReadinessGateMetrics:
    architecture_readiness: int
    security_readiness: int
    governance_readiness: int
    workflow_readiness: int
    evaluation_readiness: int
    operational_readiness: int
    delivery_readiness: int
    transformation_readiness: int
    executive_readiness: int
    scale_readiness: int

    def score_by_gate(self) -> dict[str, int]:
        return {
            "architecture_readiness": _bounded_score(self.architecture_readiness),
            "security_readiness": _bounded_score(self.security_readiness),
            "governance_readiness": _bounded_score(self.governance_readiness),
            "workflow_readiness": _bounded_score(self.workflow_readiness),
            "evaluation_readiness": _bounded_score(self.evaluation_readiness),
            "operational_readiness": _bounded_score(self.operational_readiness),
            "delivery_readiness": _bounded_score(self.delivery_readiness),
            "transformation_readiness": _bounded_score(self.transformation_readiness),
            "executive_readiness": _bounded_score(self.executive_readiness),
            "scale_readiness": _bounded_score(self.scale_readiness),
        }

    def overall_score(self) -> int:
        scores = self.score_by_gate()
        return _mean(*tuple(scores[name] for name in READINESS_GATES))


@dataclass(frozen=True, slots=True)
class VerificationInput:
    workflow_testing: WorkflowTestingMetrics
    governance_validation: GovernanceValidationMetrics
    operational_evaluations: OperationalEvaluationMetrics
    enterprise_readiness_gates: ReadinessGateMetrics
    executive_proof: ExecutiveProofMetrics


@dataclass(frozen=True, slots=True)
class VerificationSystemResult:
    system: str
    score: int
    band: ReadinessBand


@dataclass(frozen=True, slots=True)
class EnterpriseMaturityAssessment:
    stage: EnterpriseMaturityStage
    stage_name_en: str
    stage_name_ar: str
    overall_score: int
    verification_results: tuple[VerificationSystemResult, ...]
    gate_scores: dict[str, int]
    gate_bands: dict[str, ReadinessBand]
    missing_for_next_stage: tuple[str, ...]


def _stage_capabilities_met(stage: EnterpriseMaturityStage, caps: CapabilitySnapshot) -> bool:
    required = _STAGE_CAPABILITIES[stage]
    return all(bool(getattr(caps, k, False)) for k in required)


def _missing_capability_labels(stage: EnterpriseMaturityStage, caps: CapabilitySnapshot) -> tuple[str, ...]:
    required = _STAGE_CAPABILITIES[stage]
    missing = [k for k in required if not bool(getattr(caps, k, False))]
    return tuple(_CAPABILITY_LABELS.get(k, k) for k in missing)


def _verification_results(v: VerificationInput) -> tuple[VerificationSystemResult, ...]:
    workflow_score = v.workflow_testing.score()
    governance_score = v.governance_validation.score()
    operational_score = v.operational_evaluations.score()
    readiness_score = v.enterprise_readiness_gates.overall_score()
    executive_score = v.executive_proof.score()
    return (
        VerificationSystemResult(
            system="real_workflow_testing",
            score=workflow_score,
            band=readiness_band(workflow_score),
        ),
        VerificationSystemResult(
            system="governance_validation",
            score=governance_score,
            band=readiness_band(governance_score),
        ),
        VerificationSystemResult(
            system="operational_evaluations",
            score=operational_score,
            band=readiness_band(operational_score),
        ),
        VerificationSystemResult(
            system="enterprise_readiness_gates",
            score=readiness_score,
            band=readiness_band(readiness_score),
        ),
        VerificationSystemResult(
            system="executive_proof_system",
            score=executive_score,
            band=readiness_band(executive_score),
        ),
    )


def _all_systems_at_least(results: tuple[VerificationSystemResult, ...], threshold: int) -> bool:
    return all(r.score >= threshold for r in results)


def _all_gates_at_least(gate_scores: dict[str, int], threshold: int) -> bool:
    return all(gate_scores.get(name, 0) >= threshold for name in READINESS_GATES)


def assess_enterprise_maturity(
    capabilities: CapabilitySnapshot,
    verification: VerificationInput,
) -> EnterpriseMaturityAssessment:
    """Assess current maturity stage using capabilities + verification signals."""
    results = _verification_results(verification)
    gate_scores = verification.enterprise_readiness_gates.score_by_gate()
    gate_bands = {name: readiness_band(score) for name, score in gate_scores.items()}
    overall_score = _mean(*tuple(r.score for r in results))
    enterprise_ready_validated = _all_systems_at_least(results, 85) and _all_gates_at_least(gate_scores, 85)
    mission_critical_validated = _all_systems_at_least(results, 95) and _all_gates_at_least(gate_scores, 95)

    stage = EnterpriseMaturityStage.AI_TOOL
    for candidate in (
        EnterpriseMaturityStage.AI_SAAS_PLATFORM,
        EnterpriseMaturityStage.ENTERPRISE_AI_PLATFORM,
        EnterpriseMaturityStage.AGENTIC_OPERATING_PLATFORM,
        EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE,
    ):
        if _stage_capabilities_met(candidate, capabilities):
            stage = candidate
        else:
            break

    if (
        stage >= EnterpriseMaturityStage.AGENTIC_ENTERPRISE_INFRASTRUCTURE
        and _stage_capabilities_met(EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE, capabilities)
        and enterprise_ready_validated
    ):
        stage = EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE

    if (
        stage >= EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE
        and _stage_capabilities_met(EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER, capabilities)
        and mission_critical_validated
    ):
        stage = EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER

    if stage == EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER:
        missing_for_next = ()
    else:
        next_stage = EnterpriseMaturityStage(int(stage) + 1)
        missing_items: list[str] = list(_missing_capability_labels(next_stage, capabilities))
        if next_stage == EnterpriseMaturityStage.ENTERPRISE_READY_INFRASTRUCTURE and not enterprise_ready_validated:
            missing_items.append("all verification systems >=85")
            missing_items.append("all readiness gates >=85")
        if (
            next_stage == EnterpriseMaturityStage.MISSION_CRITICAL_OPERATING_LAYER
            and not mission_critical_validated
        ):
            missing_items.append("all verification systems >=95")
            missing_items.append("all readiness gates >=95")
        missing_for_next = tuple(dict.fromkeys(missing_items))

    return EnterpriseMaturityAssessment(
        stage=stage,
        stage_name_en=STAGE_EN_LABELS[stage],
        stage_name_ar=STAGE_AR_LABELS[stage],
        overall_score=overall_score,
        verification_results=results,
        gate_scores=gate_scores,
        gate_bands=gate_bands,
        missing_for_next_stage=missing_for_next,
    )
