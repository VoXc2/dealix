"""Enterprise Nervous System maturity model for agentic organizations.

This module turns strategic language into deterministic capability scoring:
- Assess 12 core systems (phase 1 of a 20-system target architecture).
- Compute a weighted organizational capability score (0..100).
- Enforce governed-autonomy readiness gates.
- Return actionable next moves in Arabic for operator execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

TARGET_SYSTEMS_COUNT_DEFAULT = 20
ASSESSMENT_SYSTEMS_COUNT = 12
DEFAULT_TARGET_SCORE = 85.0


@dataclass(frozen=True, slots=True)
class CoreSystemDefinition:
    system_id: str
    name_en: str
    name_ar: str
    intent_en: str
    weight: float


CORE_SYSTEMS: tuple[CoreSystemDefinition, ...] = (
    CoreSystemDefinition(
        system_id="agent_operating_system",
        name_en="Agent Operating System",
        name_ar="نظام تشغيل الوكلاء",
        intent_en="Manage AI workers, roles, permissions, memory, and KPIs.",
        weight=0.12,
    ),
    CoreSystemDefinition(
        system_id="workflow_orchestration_system",
        name_en="Workflow Orchestration System",
        name_ar="نظام تنسيق سير العمل",
        intent_en="Route events into governed workflow execution paths.",
        weight=0.12,
    ),
    CoreSystemDefinition(
        system_id="organizational_memory_system",
        name_en="Organizational Memory System",
        name_ar="نظام الذاكرة المؤسسية",
        intent_en="Persist operational memory as reusable institutional intelligence.",
        weight=0.10,
    ),
    CoreSystemDefinition(
        system_id="governance_operating_system",
        name_en="Governance Operating System",
        name_ar="نظام الحوكمة التشغيلية",
        intent_en="Apply policy, approvals, auditability, explainability, and risk control.",
        weight=0.12,
    ),
    CoreSystemDefinition(
        system_id="executive_intelligence_system",
        name_en="Executive Intelligence System",
        name_ar="نظام الذكاء التنفيذي",
        intent_en="Continuously surface bottlenecks, risks, and strategic opportunities.",
        weight=0.08,
    ),
    CoreSystemDefinition(
        system_id="organizational_graph_system",
        name_en="Organizational Graph System",
        name_ar="نظام الرسم البياني المؤسسي",
        intent_en="Model relationships across people, decisions, workflows, and risk.",
        weight=0.07,
    ),
    CoreSystemDefinition(
        system_id="execution_system",
        name_en="Execution System",
        name_ar="نظام التنفيذ",
        intent_en="Execute operations safely across CRM, proposals, approvals, and workflows.",
        weight=0.10,
    ),
    CoreSystemDefinition(
        system_id="evaluation_system",
        name_en="Evaluation System",
        name_ar="نظام التقييم",
        intent_en="Measure hallucination risk, policy compliance, and business outcomes.",
        weight=0.09,
    ),
    CoreSystemDefinition(
        system_id="observability_system",
        name_en="Observability System",
        name_ar="نظام المراقبة",
        intent_en="Track traces, retries, failures, latency, and agent health.",
        weight=0.08,
    ),
    CoreSystemDefinition(
        system_id="transformation_system",
        name_en="Transformation System",
        name_ar="نظام التحول المؤسسي",
        intent_en="Run maturity-led operating model redesign, not feature delivery only.",
        weight=0.05,
    ),
    CoreSystemDefinition(
        system_id="digital_workforce_system",
        name_en="Digital Workforce System",
        name_ar="نظام القوى العاملة الرقمية",
        intent_en="Operate AI org charts, supervision, and digital labor performance.",
        weight=0.04,
    ),
    CoreSystemDefinition(
        system_id="continuous_evolution_system",
        name_en="Continuous Evolution System",
        name_ar="نظام التطور المستمر",
        intent_en="Improve workflows through closed-loop feedback and learning.",
        weight=0.03,
    ),
)

CORE_SYSTEM_IDS: frozenset[str] = frozenset(x.system_id for x in CORE_SYSTEMS)
CORE_SYSTEM_WEIGHTS: dict[str, float] = {x.system_id: x.weight for x in CORE_SYSTEMS}

CRITICAL_GOVERNANCE_SYSTEMS: frozenset[str] = frozenset(
    {
        "agent_operating_system",
        "governance_operating_system",
        "evaluation_system",
        "observability_system",
    }
)

NEXT_MOVE_AR: dict[str, str] = {
    "agent_operating_system": "وحّد بطاقة الهوية لكل Agent (الدور، الصلاحيات، KPI، مستوى المخاطر) قبل أي توسع.",
    "workflow_orchestration_system": "ابنِ Orchestration قياسي: event → reasoning → approval → execution → retry → monitoring.",
    "organizational_memory_system": "فعّل سجل ذاكرة مؤسسية موحد لكل قرار وتشغيل وربطه بنتائج الأعمال.",
    "governance_operating_system": "ثبّت policy engine + approval matrix + audit trail لكل إجراء خارجي.",
    "executive_intelligence_system": "أطلق موجز تنفيذي أسبوعي آلي يغطي الاختناقات، التسربات، والمخاطر التشغيلية.",
    "organizational_graph_system": "ابنِ graph علاقات يربط العملاء والقرارات والموافقات والمشاريع والمخاطر.",
    "execution_system": "حوّل المخرجات من نصوص إلى إجراءات محكومة عبر connectors مع بوابات موافقة إلزامية.",
    "evaluation_system": "اعتمد evals تشغيلية إلزامية: دقة التنفيذ، الالتزام بالسياسات، وقياس الأثر التجاري.",
    "observability_system": "فعّل telemetry موحد (trace_id, retries, failures, latency) لكل Agent وworkflow.",
    "transformation_system": "حوّل البيع من features إلى خارطة تحول مؤسسي مبنية على مستويات نضج واضحة.",
    "digital_workforce_system": "عرّف هيكل القوى العاملة الرقمية (فرق، إشراف، مراجعة أداء، تصعيدات).",
    "continuous_evolution_system": "أغلق حلقة التعلم: feedback → تحليل → تحسين workflows → إعادة تقييم.",
}


@dataclass(frozen=True, slots=True)
class SystemScore:
    system_id: str
    name_en: str
    name_ar: str
    score: float
    weight: float
    weighted_score: float
    level: str
    gap_to_target: float
    next_move_ar: str


@dataclass(frozen=True, slots=True)
class EnterpriseNervousAssessment:
    overall_score: float
    maturity_band: str
    governed_autonomy_ready: bool
    target_score: float
    assessed_systems_count: int
    target_systems_count: int
    architecture_coverage_percent: float
    weakest_systems: tuple[str, ...]
    prioritized_next_moves_ar: tuple[str, ...]
    systems: tuple[SystemScore, ...]


def _clamp(score: float) -> float:
    return max(0.0, min(100.0, float(score)))


def _level(score: float) -> str:
    if score >= 85:
        return "optimized"
    if score >= 70:
        return "scaled"
    if score >= 50:
        return "developing"
    return "nascent"


def _maturity_band(overall_score: float) -> str:
    if overall_score >= 90:
        return "enterprise_nervous_system_ready"
    if overall_score >= 75:
        return "agentic_operator"
    if overall_score >= 55:
        return "system_led"
    if overall_score >= 35:
        return "workflow_enabled"
    return "feature_led"


def framework_catalog() -> tuple[CoreSystemDefinition, ...]:
    """Return immutable catalog of phase-1 core systems."""
    return CORE_SYSTEMS


def unknown_system_ids(system_scores: Mapping[str, float]) -> tuple[str, ...]:
    """Return unknown incoming system IDs to prevent silent scoring mistakes."""
    unknown = sorted(set(system_scores.keys()) - CORE_SYSTEM_IDS)
    return tuple(unknown)


def assess_enterprise_nervous_system(
    *,
    system_scores: Mapping[str, float],
    target_score: float = DEFAULT_TARGET_SCORE,
    target_systems_count: int = TARGET_SYSTEMS_COUNT_DEFAULT,
) -> EnterpriseNervousAssessment:
    """Compute organizational capability for the Enterprise Nervous System model."""
    normalized_target = _clamp(target_score)
    entries: list[SystemScore] = []
    weighted_total = 0.0
    critical_scores: list[float] = []

    for system in CORE_SYSTEMS:
        raw_score = _clamp(system_scores.get(system.system_id, 0.0))
        weighted = round(raw_score * system.weight, 3)
        weighted_total += weighted
        if system.system_id in CRITICAL_GOVERNANCE_SYSTEMS:
            critical_scores.append(raw_score)
        entries.append(
            SystemScore(
                system_id=system.system_id,
                name_en=system.name_en,
                name_ar=system.name_ar,
                score=round(raw_score, 2),
                weight=system.weight,
                weighted_score=weighted,
                level=_level(raw_score),
                gap_to_target=round(max(0.0, normalized_target - raw_score), 2),
                next_move_ar=NEXT_MOVE_AR[system.system_id],
            )
        )

    overall = round(_clamp(weighted_total), 2)
    weakest = tuple(x.system_id for x in sorted(entries, key=lambda s: s.score)[:5])
    next_moves = tuple(NEXT_MOVE_AR[sid] for sid in weakest)

    governed_ready = (
        overall >= 70.0
        and len(critical_scores) == len(CRITICAL_GOVERNANCE_SYSTEMS)
        and min(critical_scores) >= 65.0
    )

    coverage = round((ASSESSMENT_SYSTEMS_COUNT / float(max(1, target_systems_count))) * 100.0, 2)

    return EnterpriseNervousAssessment(
        overall_score=overall,
        maturity_band=_maturity_band(overall),
        governed_autonomy_ready=governed_ready,
        target_score=normalized_target,
        assessed_systems_count=ASSESSMENT_SYSTEMS_COUNT,
        target_systems_count=target_systems_count,
        architecture_coverage_percent=coverage,
        weakest_systems=weakest,
        prioritized_next_moves_ar=next_moves,
        systems=tuple(entries),
    )
