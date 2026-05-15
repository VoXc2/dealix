"""Enterprise Nervous System assessment for agentic organizations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from auto_client_acquisition.enterprise_maturity_os.enterprise_maturity_model import (
    ReadinessBand,
    readiness_band,
)


class CoreSystem(IntEnum):
    AGENT_OPERATING_SYSTEM = 1
    WORKFLOW_ORCHESTRATION_SYSTEM = 2
    ORGANIZATIONAL_MEMORY_SYSTEM = 3
    GOVERNANCE_OPERATING_SYSTEM = 4
    EXECUTIVE_INTELLIGENCE_SYSTEM = 5
    ORGANIZATIONAL_GRAPH_SYSTEM = 6
    EXECUTION_SYSTEM = 7
    EVALUATION_SYSTEM = 8
    OBSERVABILITY_SYSTEM = 9
    TRANSFORMATION_SYSTEM = 10
    DIGITAL_WORKFORCE_SYSTEM = 11
    CONTINUOUS_EVOLUTION_SYSTEM = 12
    IDENTITY_ACCESS_SYSTEM = 13
    INTEGRATION_FABRIC_SYSTEM = 14
    APPROVAL_ESCALATION_SYSTEM = 15
    POLICY_RISK_COMPLIANCE_SYSTEM = 16
    KNOWLEDGE_RETRIEVAL_SYSTEM = 17
    VALUE_PROOF_SYSTEM = 18
    ADOPTION_ENABLEMENT_SYSTEM = 19
    ENTERPRISE_SCALING_SYSTEM = 20


CORE_SYSTEM_LABELS_AR: dict[CoreSystem, str] = {
    CoreSystem.AGENT_OPERATING_SYSTEM: "نظام تشغيل الوكلاء",
    CoreSystem.WORKFLOW_ORCHESTRATION_SYSTEM: "نظام أوركسترايشن سير العمل",
    CoreSystem.ORGANIZATIONAL_MEMORY_SYSTEM: "نظام الذاكرة التنظيمية",
    CoreSystem.GOVERNANCE_OPERATING_SYSTEM: "نظام الحوكمة التشغيلي",
    CoreSystem.EXECUTIVE_INTELLIGENCE_SYSTEM: "نظام الذكاء التنفيذي",
    CoreSystem.ORGANIZATIONAL_GRAPH_SYSTEM: "نظام الرسم التنظيمي",
    CoreSystem.EXECUTION_SYSTEM: "نظام التنفيذ التشغيلي",
    CoreSystem.EVALUATION_SYSTEM: "نظام التقييم",
    CoreSystem.OBSERVABILITY_SYSTEM: "نظام الرصد التشغيلي",
    CoreSystem.TRANSFORMATION_SYSTEM: "نظام التحول المؤسسي",
    CoreSystem.DIGITAL_WORKFORCE_SYSTEM: "نظام القوى العاملة الرقمية",
    CoreSystem.CONTINUOUS_EVOLUTION_SYSTEM: "نظام التطور المستمر",
    CoreSystem.IDENTITY_ACCESS_SYSTEM: "نظام الهوية والصلاحيات",
    CoreSystem.INTEGRATION_FABRIC_SYSTEM: "نظام نسيج التكامل",
    CoreSystem.APPROVAL_ESCALATION_SYSTEM: "نظام الموافقات والتصعيد",
    CoreSystem.POLICY_RISK_COMPLIANCE_SYSTEM: "نظام السياسات والمخاطر والامتثال",
    CoreSystem.KNOWLEDGE_RETRIEVAL_SYSTEM: "نظام استرجاع المعرفة",
    CoreSystem.VALUE_PROOF_SYSTEM: "نظام إثبات القيمة",
    CoreSystem.ADOPTION_ENABLEMENT_SYSTEM: "نظام التبني والتمكين",
    CoreSystem.ENTERPRISE_SCALING_SYSTEM: "نظام التوسع المؤسسي",
}


def _bounded_score(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return int(value)


def _mean(values: tuple[int, ...]) -> int:
    if not values:
        return 0
    return int(round(sum(values) / len(values)))


@dataclass(frozen=True, slots=True)
class CoreSystemsSnapshot:
    agent_operating_system: int
    workflow_orchestration_system: int
    organizational_memory_system: int
    governance_operating_system: int
    executive_intelligence_system: int
    organizational_graph_system: int
    execution_system: int
    evaluation_system: int
    observability_system: int
    transformation_system: int
    digital_workforce_system: int
    continuous_evolution_system: int
    identity_access_system: int
    integration_fabric_system: int
    approval_escalation_system: int
    policy_risk_compliance_system: int
    knowledge_retrieval_system: int
    value_proof_system: int
    adoption_enablement_system: int
    enterprise_scaling_system: int

    def score_by_system(self) -> dict[CoreSystem, int]:
        return {
            CoreSystem.AGENT_OPERATING_SYSTEM: _bounded_score(self.agent_operating_system),
            CoreSystem.WORKFLOW_ORCHESTRATION_SYSTEM: _bounded_score(self.workflow_orchestration_system),
            CoreSystem.ORGANIZATIONAL_MEMORY_SYSTEM: _bounded_score(self.organizational_memory_system),
            CoreSystem.GOVERNANCE_OPERATING_SYSTEM: _bounded_score(self.governance_operating_system),
            CoreSystem.EXECUTIVE_INTELLIGENCE_SYSTEM: _bounded_score(self.executive_intelligence_system),
            CoreSystem.ORGANIZATIONAL_GRAPH_SYSTEM: _bounded_score(self.organizational_graph_system),
            CoreSystem.EXECUTION_SYSTEM: _bounded_score(self.execution_system),
            CoreSystem.EVALUATION_SYSTEM: _bounded_score(self.evaluation_system),
            CoreSystem.OBSERVABILITY_SYSTEM: _bounded_score(self.observability_system),
            CoreSystem.TRANSFORMATION_SYSTEM: _bounded_score(self.transformation_system),
            CoreSystem.DIGITAL_WORKFORCE_SYSTEM: _bounded_score(self.digital_workforce_system),
            CoreSystem.CONTINUOUS_EVOLUTION_SYSTEM: _bounded_score(self.continuous_evolution_system),
            CoreSystem.IDENTITY_ACCESS_SYSTEM: _bounded_score(self.identity_access_system),
            CoreSystem.INTEGRATION_FABRIC_SYSTEM: _bounded_score(self.integration_fabric_system),
            CoreSystem.APPROVAL_ESCALATION_SYSTEM: _bounded_score(self.approval_escalation_system),
            CoreSystem.POLICY_RISK_COMPLIANCE_SYSTEM: _bounded_score(self.policy_risk_compliance_system),
            CoreSystem.KNOWLEDGE_RETRIEVAL_SYSTEM: _bounded_score(self.knowledge_retrieval_system),
            CoreSystem.VALUE_PROOF_SYSTEM: _bounded_score(self.value_proof_system),
            CoreSystem.ADOPTION_ENABLEMENT_SYSTEM: _bounded_score(self.adoption_enablement_system),
            CoreSystem.ENTERPRISE_SCALING_SYSTEM: _bounded_score(self.enterprise_scaling_system),
        }


@dataclass(frozen=True, slots=True)
class OrganizationalCapabilitySnapshot:
    workflow_redesign: int
    workflow_execution: int
    workflow_governance: int
    workflow_evaluation: int
    workflow_scaling: int
    agent_supervision: int
    digital_workforce_management: int
    executive_intelligence_generation: int
    operational_impact_measurement: int
    continuous_improvement: int

    def score_by_capability(self) -> dict[str, int]:
        return {
            "workflow_redesign": _bounded_score(self.workflow_redesign),
            "workflow_execution": _bounded_score(self.workflow_execution),
            "workflow_governance": _bounded_score(self.workflow_governance),
            "workflow_evaluation": _bounded_score(self.workflow_evaluation),
            "workflow_scaling": _bounded_score(self.workflow_scaling),
            "agent_supervision": _bounded_score(self.agent_supervision),
            "digital_workforce_management": _bounded_score(self.digital_workforce_management),
            "executive_intelligence_generation": _bounded_score(self.executive_intelligence_generation),
            "operational_impact_measurement": _bounded_score(self.operational_impact_measurement),
            "continuous_improvement": _bounded_score(self.continuous_improvement),
        }


@dataclass(frozen=True, slots=True)
class EnterpriseNervousSystemAssessment:
    overall_system_score: int
    overall_system_band: ReadinessBand
    organizational_capability_score: int
    organizational_capability_band: ReadinessBand
    combined_score: int
    combined_band: ReadinessBand
    system_scores: dict[CoreSystem, int]
    system_bands: dict[CoreSystem, ReadinessBand]
    capability_scores: dict[str, int]
    weak_systems: tuple[CoreSystem, ...]
    weak_capabilities: tuple[str, ...]
    is_agentic_enterprise_ready: bool
    is_mission_critical_ready: bool
    verdict_ar: str
    next_actions_ar: tuple[str, ...]


def _lowest_systems(system_scores: dict[CoreSystem, int], *, count: int = 5) -> tuple[CoreSystem, ...]:
    pairs = sorted(system_scores.items(), key=lambda item: item[1])
    return tuple(system for system, _ in pairs[:count])


def _weak_capabilities(scores: dict[str, int], *, threshold: int = 75) -> tuple[str, ...]:
    weak = [name for name, value in scores.items() if value < threshold]
    return tuple(sorted(weak))


def _actions_from_weak_areas(
    weak_systems: tuple[CoreSystem, ...],
    weak_capabilities: tuple[str, ...],
) -> tuple[str, ...]:
    actions: list[str] = []
    if CoreSystem.GOVERNANCE_OPERATING_SYSTEM in weak_systems:
        actions.append("ارفع نضج الحوكمة: policy engine + approvals + audit explainability.")
    if CoreSystem.WORKFLOW_ORCHESTRATION_SYSTEM in weak_systems:
        actions.append("ثبّت orchestration end-to-end مع retries وتصعيد واضح.")
    if CoreSystem.ORGANIZATIONAL_MEMORY_SYSTEM in weak_systems:
        actions.append("وحّد الذاكرة التنظيمية وربطها بالصلاحيات وسجل القرار.")
    if "workflow_execution" in weak_capabilities:
        actions.append("اربط الذكاء بالتنفيذ الفعلي لا بتوليد المحتوى فقط.")
    if "operational_impact_measurement" in weak_capabilities:
        actions.append("فعّل قياس الأثر التنفيذي (ROI/latency/adoption) لكل workflow.")
    if "continuous_improvement" in weak_capabilities:
        actions.append("أنشئ feedback loop أسبوعي لتحسين workflows والسياسات.")
    if not actions:
        actions.append("حافظ على وتيرة التحسين مع مراجعة شهرية لنضج الأنظمة العشرين.")
    return tuple(actions)


def assess_enterprise_nervous_system(
    systems: CoreSystemsSnapshot,
    capabilities: OrganizationalCapabilitySnapshot,
) -> EnterpriseNervousSystemAssessment:
    """Assess whether Dealix behaves like an Enterprise Nervous System."""
    system_scores = systems.score_by_system()
    system_bands = {name: readiness_band(score) for name, score in system_scores.items()}
    capability_scores = capabilities.score_by_capability()

    overall_system_score = _mean(tuple(system_scores.values()))
    organizational_capability_score = _mean(tuple(capability_scores.values()))
    combined_score = _mean((overall_system_score, organizational_capability_score))

    overall_system_band = readiness_band(overall_system_score)
    organizational_capability_band = readiness_band(organizational_capability_score)
    combined_band = readiness_band(combined_score)

    weak_systems = _lowest_systems(system_scores, count=5)
    weak_capabilities = _weak_capabilities(capability_scores, threshold=75)

    all_systems_enterprise_ready = all(score >= 85 for score in system_scores.values())
    all_caps_enterprise_ready = all(score >= 85 for score in capability_scores.values())
    all_systems_mission_critical = all(score >= 95 for score in system_scores.values())
    all_caps_mission_critical = all(score >= 95 for score in capability_scores.values())

    is_agentic_enterprise_ready = all_systems_enterprise_ready and all_caps_enterprise_ready
    is_mission_critical_ready = all_systems_mission_critical and all_caps_mission_critical

    if is_mission_critical_ready:
        verdict_ar = "Dealix يعمل كطبقة تشغيل مؤسسية حرجة (Mission-Critical Agentic Infrastructure)."
    elif is_agentic_enterprise_ready:
        verdict_ar = "Dealix وصل لمستوى بنية Agentic مؤسسية جاهزة للتشغيل الواسع."
    elif combined_score >= 75:
        verdict_ar = "Dealix في مستوى Client Pilot قوي لكنه يحتاج تقوية أنظمة أساسية قبل اعتماد مؤسسي كامل."
    else:
        verdict_ar = "Dealix ما زال في مرحلة انتقالية؛ التركيز يجب أن يكون على نضج الأنظمة التشغيلية لا زيادة features."

    next_actions = _actions_from_weak_areas(weak_systems, weak_capabilities)

    return EnterpriseNervousSystemAssessment(
        overall_system_score=overall_system_score,
        overall_system_band=overall_system_band,
        organizational_capability_score=organizational_capability_score,
        organizational_capability_band=organizational_capability_band,
        combined_score=combined_score,
        combined_band=combined_band,
        system_scores=system_scores,
        system_bands=system_bands,
        capability_scores=capability_scores,
        weak_systems=weak_systems,
        weak_capabilities=weak_capabilities,
        is_agentic_enterprise_ready=is_agentic_enterprise_ready,
        is_mission_critical_ready=is_mission_critical_ready,
        verdict_ar=verdict_ar,
        next_actions_ar=next_actions,
    )
