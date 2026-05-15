"""Schemas for ``org_consciousness_os`` — Systems 36-45.

All dataclasses are frozen and expose ``to_dict()``. The module persists
nothing: these are synthesis outputs derived from existing ledgers/stores.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ── System 36 — Organizational Consciousness ─────────────────────


@dataclass(frozen=True, slots=True)
class ExecutionHealthSignal:
    customer_id: str
    window_days: int
    friction_total: int
    friction_cost_minutes: int
    top_friction_kinds: tuple[tuple[str, int], ...]
    friction_wow_delta: int
    trace_count: int
    total_cost_usd: float
    avg_latency_ms: float
    congestion_events: dict[str, int]
    bottleneck: dict[str, Any]
    execution_health_score: int
    health_band: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "friction_total": self.friction_total,
            "friction_cost_minutes": self.friction_cost_minutes,
            "top_friction_kinds": [list(t) for t in self.top_friction_kinds],
            "friction_wow_delta": self.friction_wow_delta,
            "trace_count": self.trace_count,
            "total_cost_usd": self.total_cost_usd,
            "avg_latency_ms": self.avg_latency_ms,
            "congestion_events": dict(self.congestion_events),
            "bottleneck": dict(self.bottleneck),
            "execution_health_score": self.execution_health_score,
            "health_band": self.health_band,
        }


# ── System 37 — Causal Organizational Reasoning ──────────────────


@dataclass(frozen=True, slots=True)
class CausalLink:
    friction_event_id: str
    friction_kind: str
    workflow_id: str
    linked_task_ids: tuple[str, ...]
    hypothesis: str
    confidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "friction_event_id": self.friction_event_id,
            "friction_kind": self.friction_kind,
            "workflow_id": self.workflow_id,
            "linked_task_ids": list(self.linked_task_ids),
            "hypothesis": self.hypothesis,
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class CausalReasoningReport:
    customer_id: str
    window_days: int
    links: tuple[CausalLink, ...]
    top_root_causes: tuple[tuple[str, int], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "links": [link.to_dict() for link in self.links],
            "top_root_causes": [list(t) for t in self.top_root_causes],
        }


# ── System 38 — Digital Workforce Governance ─────────────────────


@dataclass(frozen=True, slots=True)
class AgentAccountabilityRecord:
    agent_id: str
    role_en: str
    owner: str
    autonomy_level: str
    risk_score: int
    risk_band: str
    lifecycle_stage: str
    deploy_ready: bool
    missing_prerequisites: tuple[str, ...]
    forbidden_tools: tuple[str, ...]
    auditability_card_valid: bool
    card_errors: tuple[str, ...]
    escalation_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role_en": self.role_en,
            "owner": self.owner,
            "autonomy_level": self.autonomy_level,
            "risk_score": self.risk_score,
            "risk_band": self.risk_band,
            "lifecycle_stage": self.lifecycle_stage,
            "deploy_ready": self.deploy_ready,
            "missing_prerequisites": list(self.missing_prerequisites),
            "forbidden_tools": list(self.forbidden_tools),
            "auditability_card_valid": self.auditability_card_valid,
            "card_errors": list(self.card_errors),
            "escalation_path": self.escalation_path,
        }


@dataclass(frozen=True, slots=True)
class WorkforceGovernanceReport:
    customer_id: str
    agents: tuple[AgentAccountabilityRecord, ...]
    agents_at_risk: int
    agents_not_deploy_ready: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "agents": [a.to_dict() for a in self.agents],
            "agents_at_risk": self.agents_at_risk,
            "agents_not_deploy_ready": self.agents_not_deploy_ready,
        }


# ── System 39 — Organizational Resilience ────────────────────────


@dataclass(frozen=True, slots=True)
class ResilienceSignal:
    customer_id: str
    window_days: int
    total_failures: int
    total_retries: int
    retry_exhausted: int
    executed: int
    circuit_state: str
    failover_recommended: bool
    by_action_type: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "total_failures": self.total_failures,
            "total_retries": self.total_retries,
            "retry_exhausted": self.retry_exhausted,
            "executed": self.executed,
            "circuit_state": self.circuit_state,
            "failover_recommended": self.failover_recommended,
            "by_action_type": dict(self.by_action_type),
        }


# ── System 40 — Trust Infrastructure ─────────────────────────────


@dataclass(frozen=True, slots=True)
class TrustSignal:
    customer_id: str
    explainability_score: int
    reversibility_score: int
    auditability_coverage: int
    pending_approvals: int
    governance_decision_sample: dict[str, Any]
    trust_index: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "explainability_score": self.explainability_score,
            "reversibility_score": self.reversibility_score,
            "auditability_coverage": self.auditability_coverage,
            "pending_approvals": self.pending_approvals,
            "governance_decision_sample": dict(self.governance_decision_sample),
            "trust_index": self.trust_index,
        }


# ── System 41 — Operational Value ────────────────────────────────


@dataclass(frozen=True, slots=True)
class OperationalValueSignal:
    customer_id: str
    value_events_count: int
    capital_events_count: int
    valid_value_events: int
    valid_capital_events: int
    value_metric_delta: int
    friction_cost_minutes: int
    roi_ratio: float
    impact_summary: str
    is_estimate: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "value_events_count": self.value_events_count,
            "capital_events_count": self.capital_events_count,
            "valid_value_events": self.valid_value_events,
            "valid_capital_events": self.valid_capital_events,
            "value_metric_delta": self.value_metric_delta,
            "friction_cost_minutes": self.friction_cost_minutes,
            "roi_ratio": self.roi_ratio,
            "impact_summary": self.impact_summary,
            "is_estimate": self.is_estimate,
        }


# ── System 42 — Organizational Learning Fabric ───────────────────


@dataclass(frozen=True, slots=True)
class LearningPattern:
    pattern_key: str
    occurrences: int
    windows_seen: int
    trend: str
    sample_workflows: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_key": self.pattern_key,
            "occurrences": self.occurrences,
            "windows_seen": self.windows_seen,
            "trend": self.trend,
            "sample_workflows": list(self.sample_workflows),
        }


@dataclass(frozen=True, slots=True)
class LearningFabricReport:
    customer_id: str
    lookback_windows: int
    window_days: int
    recurring_patterns: tuple[LearningPattern, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "lookback_windows": self.lookback_windows,
            "window_days": self.window_days,
            "recurring_patterns": [p.to_dict() for p in self.recurring_patterns],
        }


# ── System 43 — Meta-Orchestration ───────────────────────────────


@dataclass(frozen=True, slots=True)
class MetaOrchestrationRecommendation:
    customer_id: str
    workload_by_status: dict[str, int]
    imbalance_score: int
    recommendations: tuple[str, ...]
    is_recommendation_only: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "workload_by_status": dict(self.workload_by_status),
            "imbalance_score": self.imbalance_score,
            "recommendations": list(self.recommendations),
            "is_recommendation_only": self.is_recommendation_only,
        }


# ── System 44 — Strategic Organizational Intelligence ────────────


@dataclass(frozen=True, slots=True)
class StrategicBenchmark:
    metric: str
    customer_value: float
    cohort_median: float
    percentile: int
    direction: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "customer_value": self.customer_value,
            "cohort_median": self.cohort_median,
            "percentile": self.percentile,
            "direction": self.direction,
        }


@dataclass(frozen=True, slots=True)
class StrategicIntelligenceReport:
    customer_id: str
    cohort_size: int
    benchmarks: tuple[StrategicBenchmark, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "cohort_size": self.cohort_size,
            "benchmarks": [b.to_dict() for b in self.benchmarks],
        }


# ── System 45 — Self-Evolving Organizational Core ────────────────


@dataclass(frozen=True, slots=True)
class EvolutionProposal:
    proposal_id: str
    target: str
    change_summary: str
    rationale: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    status: str = "DRAFT"
    requires_human_approval: bool = True
    auto_apply: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "target": self.target,
            "change_summary": self.change_summary,
            "rationale": self.rationale,
            "evidence_refs": list(self.evidence_refs),
            "status": self.status,
            "requires_human_approval": self.requires_human_approval,
            "auto_apply": self.auto_apply,
        }


# ── Top-level synthesis ──────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class OrgConsciousnessSnapshot:
    customer_id: str
    generated_at: str
    window_days: int
    execution_health: ExecutionHealthSignal
    causal: CausalReasoningReport
    workforce_governance: WorkforceGovernanceReport
    resilience: ResilienceSignal
    trust: TrustSignal
    value: OperationalValueSignal
    learning: LearningFabricReport
    meta_orchestration: MetaOrchestrationRecommendation
    strategic: StrategicIntelligenceReport
    evolution_proposals: tuple[EvolutionProposal, ...]
    doctrine: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "generated_at": self.generated_at,
            "window_days": self.window_days,
            "execution_health": self.execution_health.to_dict(),
            "causal": self.causal.to_dict(),
            "workforce_governance": self.workforce_governance.to_dict(),
            "resilience": self.resilience.to_dict(),
            "trust": self.trust.to_dict(),
            "value": self.value.to_dict(),
            "learning": self.learning.to_dict(),
            "meta_orchestration": self.meta_orchestration.to_dict(),
            "strategic": self.strategic.to_dict(),
            "evolution_proposals": [p.to_dict() for p in self.evolution_proposals],
            "doctrine": dict(self.doctrine),
        }


# Doctrine posture of the whole module — read-only synthesis + draft proposals.
DOCTRINE_POSTURE: dict[str, bool] = {
    "read_only": True,
    "no_live_send": True,
    "no_live_charge": True,
    "no_external_execution": True,
    "proposals_draft_only": True,
}


__all__ = [
    "DOCTRINE_POSTURE",
    "AgentAccountabilityRecord",
    "CausalLink",
    "CausalReasoningReport",
    "EvolutionProposal",
    "ExecutionHealthSignal",
    "LearningFabricReport",
    "LearningPattern",
    "MetaOrchestrationRecommendation",
    "OperationalValueSignal",
    "OrgConsciousnessSnapshot",
    "ResilienceSignal",
    "StrategicBenchmark",
    "StrategicIntelligenceReport",
    "TrustSignal",
    "WorkforceGovernanceReport",
]
