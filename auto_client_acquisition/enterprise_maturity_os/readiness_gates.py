"""Enterprise readiness gates — 10 gates, weighted criteria, 5 score bands.

Each gate scores 0–100 from boolean evidence. Bands follow the doctrine:
0–59 prototype, 60–74 internal beta, 75–84 client pilot,
85–94 enterprise-ready, 95+ mission-critical.
"""

from __future__ import annotations

from dataclasses import dataclass

# Per-gate criteria → weight. Each gate's weights sum to 100.
GATE_CRITERIA: dict[str, dict[str, int]] = {
    "architecture": {
        "multi_tenant_isolation": 25,
        "service_boundaries_defined": 20,
        "scalable_data_layer": 20,
        "documented_architecture": 15,
        "failure_modes_handled": 20,
    },
    "security": {
        "rbac_enforced": 25,
        "secrets_managed": 20,
        "audit_logging": 20,
        "vulnerability_scanning": 15,
        "data_classification": 20,
    },
    "governance": {
        "approvals_enforced": 25,
        "policy_registry": 20,
        "forbidden_actions_blocked": 20,
        "immutable_audit_trail": 20,
        "lawful_basis_tracked": 15,
    },
    "workflow": {
        "workflows_defined": 20,
        "workflow_execution_engine": 25,
        "retries_and_escalation": 20,
        "human_in_the_loop": 20,
        "edge_cases_tested": 15,
    },
    "evaluation": {
        "hallucination_checks": 20,
        "grounding_and_citations": 20,
        "workflow_quality_scored": 25,
        "agent_behavior_evaluated": 20,
        "business_impact_measured": 15,
    },
    "operational": {
        "observability_metrics": 25,
        "traces_and_logs": 20,
        "alerting": 20,
        "incident_runbooks": 20,
        "dead_letter_handling": 15,
    },
    "delivery": {
        "onboarding_kit": 20,
        "delivery_playbooks": 20,
        "qa_checklists": 20,
        "proof_pack_assembly": 25,
        "handoff_process": 15,
    },
    "transformation": {
        "maturity_model_published": 25,
        "operating_model_defined": 20,
        "adoption_framework": 20,
        "workflow_redesign_method": 15,
        "roi_framework": 20,
    },
    "executive": {
        "executive_dashboards": 25,
        "revenue_impact_proven": 25,
        "time_saved_proven": 20,
        "executive_briefs": 15,
        "strategic_intelligence": 15,
    },
    "scale": {
        "second_operator_can_deliver": 20,
        "templates_complete": 20,
        "semi_automated_reporting": 20,
        "stable_qa_at_volume": 25,
        "repeatable_proof_packs": 15,
    },
}

GATE_IDS: tuple[str, ...] = tuple(GATE_CRITERIA.keys())

# Band thresholds (inclusive lower bound) → band id.
_BANDS: tuple[tuple[int, str], ...] = (
    (95, "mission_critical"),
    (85, "enterprise_ready"),
    (75, "client_pilot"),
    (60, "internal_beta"),
    (0, "prototype"),
)


@dataclass(frozen=True, slots=True)
class GateScore:
    gate_id: str
    score: int
    band: str
    breakdown: dict[str, dict[str, object]]


def readiness_band(score: int) -> str:
    """Map a 0–100 score to one of the 5 doctrine bands."""
    for lower, band in _BANDS:
        if score >= lower:
            return band
    return "prototype"


def gate_criteria(gate_id: str) -> dict[str, int]:
    """Criteria → weight for `gate_id`. Raises KeyError for unknown gates."""
    return dict(GATE_CRITERIA[gate_id])


def score_gate(gate_id: str, evidence: dict[str, bool] | None = None) -> GateScore:
    """Score one gate 0–100 from boolean evidence; missing criteria score 0."""
    criteria = GATE_CRITERIA[gate_id]
    ev = evidence or {}
    breakdown: dict[str, dict[str, object]] = {}
    total = 0
    for key, weight in criteria.items():
        met = bool(ev.get(key, False))
        earned = weight if met else 0
        total += earned
        breakdown[key] = {"weight": weight, "met": met, "earned": earned}
    return GateScore(gate_id=gate_id, score=total, band=readiness_band(total), breakdown=breakdown)


__all__ = [
    "GATE_CRITERIA",
    "GATE_IDS",
    "GateScore",
    "gate_criteria",
    "readiness_band",
    "score_gate",
]
