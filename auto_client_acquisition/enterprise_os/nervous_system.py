"""Enterprise Nervous System capability engine for agentic organizations.

Deterministic scoring helpers used by API + tests:
- Define 20 canonical systems (12 core + 8 scale/support systems)
- Compute weighted maturity score and capability gates
- Generate phase roadmap and executive scorecard template
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class NervousSystemDefinition:
    """Definition for one organizational capability system."""

    system_id: str
    name: str
    track: str
    weight: float
    description: str


CORE_SYSTEMS: tuple[NervousSystemDefinition, ...] = (
    NervousSystemDefinition(
        "agent_operating_system",
        "Agent Operating System",
        "control_plane",
        0.06,
        "Identity, role, scope, KPIs, and guardrails for AI workers.",
    ),
    NervousSystemDefinition(
        "workflow_orchestration_system",
        "Workflow Orchestration System",
        "control_plane",
        0.06,
        "Event-to-execution orchestration, retries, and approval routing.",
    ),
    NervousSystemDefinition(
        "organizational_memory_system",
        "Organizational Memory System",
        "intelligence_plane",
        0.06,
        "Unified operational memory across customer, policy, and workflows.",
    ),
    NervousSystemDefinition(
        "governance_operating_system",
        "Governance Operating System",
        "control_plane",
        0.06,
        "Policy, approval, audit, explainability, and compliance controls.",
    ),
    NervousSystemDefinition(
        "executive_intelligence_system",
        "Executive Intelligence System",
        "intelligence_plane",
        0.05,
        "Continuous executive briefs, strategic memos, and risk signals.",
    ),
    NervousSystemDefinition(
        "organizational_graph_system",
        "Organizational Graph System",
        "intelligence_plane",
        0.05,
        "Graph of people, workflows, risks, projects, and decisions.",
    ),
    NervousSystemDefinition(
        "execution_system",
        "Execution System",
        "execution_plane",
        0.06,
        "Safe execution of real business operations via governed actions.",
    ),
    NervousSystemDefinition(
        "evaluation_system",
        "Evaluation System",
        "control_plane",
        0.05,
        "Quality and policy evals for agentic workflow outcomes.",
    ),
    NervousSystemDefinition(
        "observability_system",
        "Observability System",
        "control_plane",
        0.05,
        "Traces, failures, retries, bottlenecks, and health visibility.",
    ),
    NervousSystemDefinition(
        "transformation_system",
        "Transformation System",
        "execution_plane",
        0.04,
        "Maturity models and redesign frameworks for client transformation.",
    ),
    NervousSystemDefinition(
        "digital_workforce_system",
        "Digital Workforce System",
        "execution_plane",
        0.05,
        "AI org-chart, supervision, and performance management.",
    ),
    NervousSystemDefinition(
        "continuous_evolution_system",
        "Continuous Evolution System",
        "execution_plane",
        0.04,
        "Feedback loops that continuously refine workflows and policies.",
    ),
    # Additional 8 systems required to operationalize enterprise-grade scale.
    NervousSystemDefinition(
        "policy_engine_system",
        "Policy Engine System",
        "control_plane",
        0.04,
        "Machine-readable policy rules with deterministic decisions.",
    ),
    NervousSystemDefinition(
        "approval_fabric_system",
        "Approval Fabric System",
        "control_plane",
        0.04,
        "Dynamic approval routing across human and agent reviewers.",
    ),
    NervousSystemDefinition(
        "audit_explainability_system",
        "Audit Explainability System",
        "control_plane",
        0.04,
        "Full traceability and explainability for all critical actions.",
    ),
    NervousSystemDefinition(
        "risk_resilience_system",
        "Risk Resilience System",
        "control_plane",
        0.04,
        "Risk modeling, incident runbooks, and resilience controls.",
    ),
    NervousSystemDefinition(
        "knowledge_quality_system",
        "Knowledge Quality System",
        "intelligence_plane",
        0.04,
        "Grounding quality, freshness, and source trust controls.",
    ),
    NervousSystemDefinition(
        "adoption_change_system",
        "Adoption Change System",
        "execution_plane",
        0.04,
        "Human enablement, operating rhythm, and behavior adoption.",
    ),
    NervousSystemDefinition(
        "value_realization_system",
        "Value Realization System",
        "execution_plane",
        0.04,
        "Business impact tracking across revenue, cost, and cycle time.",
    ),
    NervousSystemDefinition(
        "platform_reliability_system",
        "Platform Reliability System",
        "execution_plane",
        0.03,
        "SLOs, capacity controls, and reliability engineering maturity.",
    ),
)

SYSTEM_IDS = {system.system_id for system in CORE_SYSTEMS}
_SYSTEM_BY_ID = {system.system_id: system for system in CORE_SYSTEMS}


def _clamp_score(value: float) -> float:
    return max(0.0, min(100.0, round(float(value), 2)))


def default_system_scores() -> dict[str, float]:
    """Neutral baseline scorecard for all 20 systems."""
    return {system.system_id: 50.0 for system in CORE_SYSTEMS}


def normalize_scores(system_scores: Mapping[str, float]) -> dict[str, float]:
    """Return canonical 20-system score map with unknown keys ignored."""
    normalized: dict[str, float] = {k: 0.0 for k in SYSTEM_IDS}
    for key, raw in system_scores.items():
        if key in normalized:
            normalized[key] = _clamp_score(raw)
    return normalized


def _maturity_band(score: float) -> str:
    if score < 40:
        return "foundational"
    if score < 60:
        return "emerging"
    if score < 75:
        return "scaling"
    if score < 90:
        return "agentic_enterprise_ready"
    return "enterprise_nervous_system"


def _phase_status(avg_score: float) -> str:
    if avg_score >= 75:
        return "on_track"
    if avg_score >= 55:
        return "at_risk"
    return "blocked"


def capability_roadmap(system_scores: Mapping[str, float]) -> list[dict[str, Any]]:
    """Roadmap phased by platform architecture: control → intelligence → execution."""
    scores = normalize_scores(system_scores)
    phase_tracks = (
        ("phase_a_control_plane", "control_plane"),
        ("phase_b_intelligence_plane", "intelligence_plane"),
        ("phase_c_execution_scale_plane", "execution_plane"),
    )

    phases: list[dict[str, Any]] = []
    for phase_id, track in phase_tracks:
        phase_systems = [system for system in CORE_SYSTEMS if system.track == track]
        avg = round(
            sum(scores[system.system_id] for system in phase_systems) / max(len(phase_systems), 1),
            2,
        )
        phases.append(
            {
                "phase_id": phase_id,
                "track": track,
                "status": _phase_status(avg),
                "average_score": avg,
                "target_score": 75,
                "systems": [
                    {
                        "system_id": system.system_id,
                        "name": system.name,
                        "score": scores[system.system_id],
                    }
                    for system in phase_systems
                ],
            }
        )
    return phases


def executive_scorecard_template() -> list[dict[str, str]]:
    """Executive KPIs that measure organizational capability (not feature count)."""
    return [
        {
            "metric_id": "workflow_cycle_time_reduction",
            "name_ar": "خفض زمن دورة سير العمل",
            "target": ">= 30%",
            "cadence": "weekly",
        },
        {
            "metric_id": "governed_autonomy_rate",
            "name_ar": "نسبة الأتمتة ضمن الحوكمة",
            "target": ">= 70%",
            "cadence": "weekly",
        },
        {
            "metric_id": "exception_escalation_precision",
            "name_ar": "دقة تصعيد الاستثناءات",
            "target": ">= 90%",
            "cadence": "weekly",
        },
        {
            "metric_id": "policy_compliance_pass_rate",
            "name_ar": "معدل الالتزام بالسياسات",
            "target": ">= 98%",
            "cadence": "daily",
        },
        {
            "metric_id": "memory_grounding_score",
            "name_ar": "جودة الذاكرة المؤسسية والـ grounding",
            "target": ">= 85/100",
            "cadence": "weekly",
        },
        {
            "metric_id": "workflow_success_rate",
            "name_ar": "معدل نجاح سير العمل",
            "target": ">= 92%",
            "cadence": "daily",
        },
        {
            "metric_id": "executive_signal_latency_hours",
            "name_ar": "زمن وصول الإشارات التنفيذية (بالساعات)",
            "target": "<= 24h",
            "cadence": "weekly",
        },
        {
            "metric_id": "revenue_leakage_prevented_sar",
            "name_ar": "القيمة المحمية من تسرب الإيراد (SAR)",
            "target": "increasing",
            "cadence": "monthly",
        },
        {
            "metric_id": "digital_workforce_uptime",
            "name_ar": "جاهزية القوى العاملة الرقمية",
            "target": ">= 99%",
            "cadence": "daily",
        },
        {
            "metric_id": "continuous_improvement_velocity",
            "name_ar": "سرعة التحسين المستمر",
            "target": ">= 4 approved improvements/month",
            "cadence": "monthly",
        },
    ]


def compute_enterprise_nervous_system(
    system_scores: Mapping[str, float],
) -> dict[str, Any]:
    """Compute maturity, readiness gates, and prioritized improvement backlog."""
    scores = normalize_scores(system_scores)
    total_weight = sum(system.weight for system in CORE_SYSTEMS) or 1.0
    weighted_score = round(
        sum(scores[s.system_id] * s.weight for s in CORE_SYSTEMS) / total_weight,
        2,
    )
    provided_known = len([k for k in system_scores if k in SYSTEM_IDS])
    coverage = round((provided_known / len(CORE_SYSTEMS)) * 100.0, 2)

    readiness_gates = {
        "can_redesign_workflows": scores["workflow_orchestration_system"] >= 65,
        "can_execute_workflows": scores["execution_system"] >= 65,
        "can_govern_workflows": (
            scores["governance_operating_system"] >= 70
            and scores["policy_engine_system"] >= 65
            and scores["approval_fabric_system"] >= 65
        ),
        "can_evaluate_workflows": scores["evaluation_system"] >= 65,
        "can_scale_workflows": (
            scores["workflow_orchestration_system"] >= 70
            and scores["platform_reliability_system"] >= 70
        ),
        "can_supervise_agents": (
            scores["agent_operating_system"] >= 70
            and scores["observability_system"] >= 65
        ),
        "can_manage_digital_workforce": scores["digital_workforce_system"] >= 70,
        "can_generate_executive_intelligence": scores["executive_intelligence_system"] >= 70,
        "can_measure_operational_impact": scores["value_realization_system"] >= 65,
        "can_improve_continuously": scores["continuous_evolution_system"] >= 65,
    }

    improvement_backlog = sorted(
        (
            {
                "system_id": system.system_id,
                "name": system.name,
                "score": scores[system.system_id],
                "gap_to_target": round(max(0.0, 75.0 - scores[system.system_id]), 2),
                "priority_score": round((75.0 - scores[system.system_id]) * system.weight, 4),
                "track": system.track,
            }
            for system in CORE_SYSTEMS
        ),
        key=lambda item: item["priority_score"],
        reverse=True,
    )

    return {
        "overall_score": weighted_score,
        "maturity_band": _maturity_band(weighted_score),
        "capability_coverage_percent": coverage,
        "systems_total": len(CORE_SYSTEMS),
        "systems": [
            {
                "system_id": system.system_id,
                "name": system.name,
                "track": system.track,
                "weight": system.weight,
                "score": scores[system.system_id],
            }
            for system in CORE_SYSTEMS
        ],
        "readiness_gates": readiness_gates,
        "ready_for_agentic_enterprise": all(readiness_gates.values()),
        "top_priorities": improvement_backlog[:8],
        "roadmap": capability_roadmap(scores),
        "executive_scorecard": executive_scorecard_template(),
    }


def systems_blueprint() -> dict[str, Any]:
    """Return static architecture blueprint for docs/API."""
    tracks = ("control_plane", "intelligence_plane", "execution_plane")
    return {
        "vision": "dealix_as_enterprise_nervous_system",
        "systems_total": len(CORE_SYSTEMS),
        "tracks": [
            {
                "track": track,
                "systems": [
                    {
                        "system_id": system.system_id,
                        "name": system.name,
                        "description": system.description,
                    }
                    for system in CORE_SYSTEMS
                    if system.track == track
                ],
            }
            for track in tracks
        ],
    }


__all__ = [
    "CORE_SYSTEMS",
    "NervousSystemDefinition",
    "SYSTEM_IDS",
    "capability_roadmap",
    "compute_enterprise_nervous_system",
    "default_system_scores",
    "executive_scorecard_template",
    "normalize_scores",
    "systems_blueprint",
]
