"""Economic Dispatcher — explainable scoring and evidence-weighted ranking.

Evaluates candidate opportunities using an explainable framework:
ECONOMIC_PRIORITY = EXPECTED_VALUE × EVIDENCE_STRENGTH × DELIVERY_CONFIDENCE
                    × STRATEGIC_REUSE × REVERSIBILITY_FACTOR
                    - TOTAL_EXPECTED_COST - RISK_PENALTY
                    - FOUNDER_ATTENTION_PENALTY - PROCUREMENT_FRICTION
                    - COMPLEXITY_DEBT

Supports qualitative scoring, confidence ranges, evidence classes, conservative estimates.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import (
    EconomicCell,
    EvidenceLevel,
    KillTrigger,
    LifecycleState,
    MonetizationRail,
    PromotionGate,
    Sector,
    UNKNOWN,
)


# ─── Scoring Enums & Constants ─────────────────────────────────────────


class ConfidenceLevel(StrEnum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class EvidenceClass(StrEnum):
    ANECDOTAL = "anecdotal"
    PUBLIC_SOURCE = "public_source"
    THIRD_PARTY = "third_party"
    DIRECT_INTERACTION = "direct_interaction"
    CONTRACTUAL = "contractual"
    CUSTOMER_VALIDATED = "customer_validated"


EVIDENCE_WEIGHTS = {
    EvidenceClass.ANECDOTAL: 0.1,
    EvidenceClass.PUBLIC_SOURCE: 0.25,
    EvidenceClass.THIRD_PARTY: 0.4,
    EvidenceClass.DIRECT_INTERACTION: 0.6,
    EvidenceClass.CONTRACTUAL: 0.8,
    EvidenceClass.CUSTOMER_VALIDATED: 1.0,
}


SECTOR_STRATEGIC_FIT = {
    Sector.GOVERNMENT_B2G: "high",
    Sector.CONSTRUCTION_EPC: "high",
    Sector.INDUSTRIAL_MANUFACTURING: "medium_high",
    Sector.LOGISTICS_SUPPLY_CHAIN: "medium_high",
    Sector.ENERGY_UTILITIES_OIL_GAS: "high",
    Sector.FINANCE_FINTECH_INSURANCE: "high",
    Sector.TECHNOLOGY_SAAS_SI: "medium",
    Sector.EXPORT_IMPORT_RHQ: "very_high",
    Sector.HEALTHCARE: "medium",
    Sector.REAL_ESTATE_PROPTECH: "medium",
}


MONETIZATION_MARGIN = {
    MonetizationRail.FREE_DIAGNOSTIC: "none",
    MonetizationRail.PAID_DIAGNOSTIC: "medium",
    MonetizationRail.PAID_SPRINT: "medium_high",
    MonetizationRail.CUSTOMER_PILOT: "medium",
    MonetizationRail.FIXED_SCOPE_IMPLEMENTATION: "high",
    MonetizationRail.MANAGED_SERVICE: "high",
    MonetizationRail.MONTHLY_RETAINER: "high",
    MonetizationRail.SAAS_SUBSCRIPTION: "very_high",
    MonetizationRail.SEAT_BASED: "high",
    MonetizationRail.USAGE_BASED_API: "high",
    MonetizationRail.ENTERPRISE_LICENSE: "high",
    MonetizationRail.WHITE_LABEL: "medium_high",
    MonetizationRail.CO_DELIVERY_REVENUE_SHARE: "medium",
    MonetizationRail.CLOUD_MARKETPLACE: "medium_high",
}


# ─── Input Models ──────────────────────────────────────────────────────


class ScoringInput(BaseModel):
    """Input for economic scoring — all fields explicit, no inference."""

    model_config = ConfigDict(extra="forbid")

    cell_id: str
    # Positive factors
    near_term_cash_ev: str = UNKNOWN
    recurring_revenue_potential: str = UNKNOWN
    gross_margin_potential: str = UNKNOWN
    evidence_strength: EvidenceClass = EvidenceClass.ANECDOTAL
    buyer_access: str = UNKNOWN
    relationship_strength: str = UNKNOWN
    urgency: str = UNKNOWN
    time_to_cash: str = UNKNOWN
    delivery_confidence: str = UNKNOWN
    repeatability: str = UNKNOWN
    reusable_capability_value: str = UNKNOWN
    proof_creation_value: str = UNKNOWN
    strategic_option_value: str = UNKNOWN
    founder_minutes_saved: str = UNKNOWN
    operational_leverage: str = UNKNOWN
    learning_voi: str = UNKNOWN
    saudi_strategic_fit: str = UNKNOWN

    # Negative factors
    acquisition_cost: str = UNKNOWN
    implementation_cost: str = UNKNOWN
    compute_cost: str = UNKNOWN
    founder_attention: str = UNKNOWN
    delivery_burden: str = UNKNOWN
    maintenance_burden: str = UNKNOWN
    procurement_friction: str = UNKNOWN
    regulatory_exposure: str = UNKNOWN
    privacy_risk: str = UNKNOWN
    cybersecurity_risk: str = UNKNOWN
    dependency_risk: str = UNKNOWN
    irreversibility: str = UNKNOWN
    uncertainty: str = UNKNOWN
    weak_evidence: str = UNKNOWN
    complexity_debt: str = UNKNOWN
    opportunity_cost: str = UNKNOWN


class ScoringBreakdown(BaseModel):
    """Explainable score breakdown."""

    model_config = ConfigDict(extra="forbid")

    # Positive components
    expected_value: float = 0.0
    evidence_strength: float = 0.0
    delivery_confidence: float = 0.0
    strategic_reuse: float = 0.0
    reversibility_factor: float = 0.0

    # Negative components
    total_expected_cost: float = 0.0
    risk_penalty: float = 0.0
    founder_attention_penalty: float = 0.0
    procurement_friction: float = 0.0
    complexity_debt: float = 0.0

    # Final
    economic_priority: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    evidence_class: EvidenceClass = EvidenceClass.ANECDOTAL

    # Explanation
    positive_factors: list[str] = Field(default_factory=list)
    negative_factors: list[str] = Field(default_factory=list)
    unknown_inputs: list[str] = Field(default_factory=list)
    conservative_assumptions: list[str] = Field(default_factory=list)


class DispatchDecision(BaseModel):
    """Dispatcher output for one cell."""

    model_config = ConfigDict(extra="forbid")

    cell_id: str
    score: ScoringBreakdown
    recommended_action: str
    next_evidence_needed: list[str] = Field(default_factory=list)
    voi_experiment: str | None = None
    voi_cost: str = UNKNOWN
    voi_value: str = UNKNOWN
    decided_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    decision_id: str = ""

    def __post_init__(self) -> None:
        if not self.decision_id:
            payload = self.model_dump(mode="json", exclude={"decision_id", "decided_at"})
            self.decision_id = hashlib.sha256(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()[:16]


# ─── Scoring Engine ────────────────────────────────────────────────────


class EconomicDispatcher:
    """Calculate explainable economic priority for cells."""

    def __init__(self) -> None:
        pass

    def score(self, cell: EconomicCell, input_: ScoringInput | None = None) -> DispatchDecision:
        """Score a cell with explainable breakdown."""
        if input_ is None:
            input_ = self._extract_from_cell(cell)

        breakdown = self._calculate_breakdown(cell, input_)
        decision = self._make_decision(cell, input_, breakdown)
        return decision

    def _extract_from_cell(self, cell: EconomicCell) -> ScoringInput:
        """Extract scoring inputs from cell (conservative, explicit)."""
        return ScoringInput(
            cell_id=cell.identity.cell_id,
            near_term_cash_ev=cell.economics.time_to_cash,
            recurring_revenue_potential=cell.economics.recurring_value_potential,
            gross_margin_potential=cell.economics.gross_margin_hypothesis,
            evidence_strength=self._evidence_level_to_class(cell.evidence.evidence_level),
            buyer_access=cell.buyer.economic_buyer or UNKNOWN,
            relationship_strength=cell.evidence.relationship_evidence,
            urgency=cell.problem.urgency,
            time_to_cash=cell.economics.time_to_cash,
            delivery_confidence=self._infer_delivery_confidence(cell),
            repeatability="high" if cell.execution.reusable_factory_dependencies else UNKNOWN,
            reusable_capability_value="high" if cell.execution.reusable_factory_dependencies else UNKNOWN,
            proof_creation_value="high" if cell.proof.proof_strength != UNKNOWN else UNKNOWN,
            strategic_option_value=SECTOR_STRATEGIC_FIT.get(cell.market.sector, "medium"),
            founder_minutes_saved=cell.value.founder_minutes_saved,
            operational_leverage=cell.value.decision_latency_reduction,
            learning_voi="medium",
            saudi_strategic_fit=SECTOR_STRATEGIC_FIT.get(cell.market.sector, "medium"),
            acquisition_cost=cell.distribution.acquisition_cost_evidence,
            implementation_cost=cell.economics.cost_to_deliver,
            compute_cost=cell.economics.compute_cost,
            founder_attention=cell.execution.founder_dependency,
            delivery_burden=cell.execution.delivery_complexity,
            maintenance_burden=cell.economics.maintenance_cost,
            procurement_friction=cell.procurement.procurement_friction,
            regulatory_exposure=cell.risk.regulatory_risk,
            privacy_risk=cell.risk.privacy_risk,
            cybersecurity_risk=cell.risk.cybersecurity_risk,
            dependency_risk=cell.risk.dependency_risk,
            irreversibility=cell.risk.irreversibility,
            uncertainty="high" if cell.evidence.evidence_level in {EvidenceLevel.L0_ANECDOTAL, EvidenceLevel.L1_PUBLIC_SOURCE} else "medium",
            weak_evidence="yes" if cell.evidence.evidence_level == EvidenceLevel.L0_ANECDOTAL else "no",
            complexity_debt="high" if len(cell.execution.integration_dependencies) > 3 else "low",
            opportunity_cost=UNKNOWN,
        )

    def _evidence_level_to_class(self, level: EvidenceLevel) -> EvidenceClass:
        mapping = {
            EvidenceLevel.L0_ANECDOTAL: EvidenceClass.ANECDOTAL,
            EvidenceLevel.L1_PUBLIC_SOURCE: EvidenceClass.PUBLIC_SOURCE,
            EvidenceLevel.L2_THIRD_PARTY: EvidenceClass.THIRD_PARTY,
            EvidenceLevel.L3_DIRECT_INTERACTION: EvidenceClass.DIRECT_INTERACTION,
            EvidenceLevel.L4_CONTRACTUAL: EvidenceClass.CONTRACTUAL,
            EvidenceLevel.L5_CUSTOMER_VALIDATED: EvidenceClass.CUSTOMER_VALIDATED,
        }
        return mapping.get(level, EvidenceClass.ANECDOTAL)

    def _infer_delivery_confidence(self, cell: EconomicCell) -> str:
        deps = len(cell.execution.capability_dependencies) + len(cell.execution.integration_dependencies)
        if deps == 0:
            return "high"
        elif deps <= 2:
            return "medium"
        else:
            return "low"

    def _calculate_breakdown(self, cell: EconomicCell, input_: ScoringInput) -> ScoringBreakdown:
        """Calculate detailed breakdown with conservative estimates."""
        b = ScoringBreakdown()
        b.evidence_class = input_.evidence_strength
        b.evidence_strength = EVIDENCE_WEIGHTS.get(input_.evidence_strength, 0.1)

        # Expected Value (conservative)
        ev_components = []
        for field_name in ["near_term_cash_ev", "recurring_revenue_potential", "gross_margin_potential"]:
            val = getattr(input_, field_name)
            if val != UNKNOWN:
                try:
                    ev_components.append(float(val))
                except ValueError:
                    b.unknown_inputs.append(field_name)
                    b.conservative_assumptions.append(f"assumed 0 for {field_name}")
        b.expected_value = sum(ev_components) if ev_components else 0.0
        if ev_components:
            b.positive_factors.append(f"EV components: {ev_components}")

        # Delivery Confidence
        conf_map = {"high": 0.8, "medium": 0.5, "low": 0.2}
        b.delivery_confidence = conf_map.get(input_.delivery_confidence, 0.3)

        # Strategic Reuse
        strategic_map = {"very_high": 0.9, "high": 0.7, "medium_high": 0.6, "medium": 0.5, "low": 0.3}
        b.strategic_reuse = strategic_map.get(input_.strategic_option_value, 0.5)

        # Reversibility Factor (lower irreversibility = higher factor)
        irrev_map = {"low": 0.9, "medium": 0.6, "high": 0.2, "unknown": 0.4}
        b.reversibility_factor = irrev_map.get(input_.irreversibility, 0.4)

        # Total Expected Cost
        cost_components = []
        for field_name in ["acquisition_cost", "implementation_cost", "compute_cost", "maintenance_burden"]:
            val = getattr(input_, field_name)
            if val != UNKNOWN:
                try:
                    cost_components.append(float(val))
                except ValueError:
                    b.unknown_inputs.append(field_name)
        b.total_expected_cost = sum(cost_components) if cost_components else 0.0

        # Risk Penalty
        risk_fields = ["regulatory_exposure", "privacy_risk", "cybersecurity_risk", "dependency_risk"]
        risk_count = sum(1 for f in risk_fields if getattr(input_, f) not in {UNKNOWN, "low"})
        b.risk_penalty = risk_count * 0.15
        if risk_count:
            b.negative_factors.append(f"{risk_count} elevated risk factors")

        # Founder Attention Penalty
        att_map = {"low": 0.05, "medium": 0.15, "high": 0.3, "unknown": 0.2}
        b.founder_attention_penalty = att_map.get(input_.founder_attention, 0.2)

        # Procurement Friction
        proc_map = {"low": 0.05, "medium": 0.15, "high": 0.3, "unknown": 0.2}
        b.procurement_friction = proc_map.get(input_.procurement_friction, 0.15)

        # Complexity Debt
        comp_map = {"low": 0.05, "medium": 0.15, "high": 0.25}
        b.complexity_debt = comp_map.get(input_.complexity_debt, 0.1)

        # Final Score
        positive = (
            b.expected_value
            * b.evidence_strength
            * b.delivery_confidence
            * b.strategic_reuse
            * b.reversibility_factor
        )
        negative = (
            b.total_expected_cost
            + b.risk_penalty
            + b.founder_attention_penalty
            + b.procurement_friction
            + b.complexity_debt
        )
        b.economic_priority = max(0.0, positive - negative)

        # Confidence
        if b.evidence_strength >= 0.6 and len(b.unknown_inputs) == 0:
            b.confidence = ConfidenceLevel.HIGH
        elif b.evidence_strength >= 0.4 and len(b.unknown_inputs) <= 2:
            b.confidence = ConfidenceLevel.MEDIUM
        elif b.evidence_strength >= 0.25:
            b.confidence = ConfidenceLevel.LOW
        else:
            b.confidence = ConfidenceLevel.VERY_LOW

        return b

    def _make_decision(
        self, cell: EconomicCell, input_: ScoringInput, breakdown: ScoringBreakdown
    ) -> DispatchDecision:
        """Generate dispatch decision with VOI analysis."""
        # Determine recommended action based on state and score
        if cell.portfolio.lifecycle_state == LifecycleState.DISCOVERED:
            action = "INITIATE_RESEARCH"
        elif cell.portfolio.lifecycle_state == LifecycleState.WATCH:
            action = "MONITOR_SIGNALS"
        elif cell.portfolio.lifecycle_state == LifecycleState.RESEARCH:
            action = "GATHER_EVIDENCE"
        elif cell.portfolio.lifecycle_state == LifecycleState.VALIDATE:
            if breakdown.economic_priority > 0.5:
                action = "PROMOTE_TO_QUALIFIED"
            else:
                action = "CONTINUE_VALIDATION"
        elif cell.portfolio.lifecycle_state == LifecycleState.QUALIFIED:
            if breakdown.economic_priority > 0.7 and breakdown.confidence in {ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH}:
                action = "PROMOTE_TO_CANDIDATE_DEEP"
            else:
                action = "RUN_VALIDATION_EXPERIMENT"
        elif cell.portfolio.lifecycle_state == LifecycleState.ACTIVE_LIGHT:
            action = "EXECUTE_LIGHT_WORK"
        elif cell.portfolio.lifecycle_state == LifecycleState.CANDIDATE_DEEP:
            if cell.portfolio.deep_wip_slot:
                action = "EXECUTE_DEEP_WORK"
            else:
                action = "REQUEST_DEEP_WIP_SLOT"
        elif cell.portfolio.lifecycle_state == LifecycleState.ACTIVE_DEEP:
            action = "CONTINUE_DEEP_EXECUTION"
        elif cell.portfolio.lifecycle_state == LifecycleState.DELIVERING:
            action = "DELIVER_AND_CAPTURE_PROOF"
        elif cell.portfolio.lifecycle_state == LifecycleState.PROVEN:
            action = "EVALUATE_PRODUCTIZATION"
        elif cell.portfolio.lifecycle_state in {LifecycleState.BLOCKED, LifecycleState.PAUSED}:
            action = "RESOLVE_BLOCKER_OR_KILL"
        else:
            action = "REVIEW_STATE"

        # VOI Experiment
        voi_experiment = None
        if breakdown.confidence in {ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW} and breakdown.economic_priority > 0.3:
            voi_experiment = f"Cheap validation experiment for {cell.identity.cell_id}: {cell.problem.problem_class.value}"

        # Next evidence needed
        next_evidence = list(cell.portfolio.next_evidence_needed)
        if input_.evidence_strength == EvidenceClass.ANECDOTAL:
            next_evidence.append("direct_interaction_evidence")
        if cell.buyer.economic_buyer == "":
            next_evidence.append("identify_economic_buyer")
        if cell.problem.measurable_loss_type == UNKNOWN:
            next_evidence.append("quantify_economic_pain")

        return DispatchDecision(
            cell_id=cell.identity.cell_id,
            score=breakdown,
            recommended_action=action,
            next_evidence_needed=next_evidence,
            voi_experiment=voi_experiment,
            voi_cost="low" if voi_experiment else UNKNOWN,
            voi_value="high" if voi_experiment else UNKNOWN,
        )

    def rank_cells(self, cells: list[EconomicCell]) -> list[DispatchDecision]:
        """Rank multiple cells by economic priority."""
        decisions = [self.score(cell) for cell in cells]
        return sorted(decisions, key=lambda d: (-d.score.economic_priority, -d.score.confidence.value))


# ─── Batch Scoring for Registry ────────────────────────────────────────


class BatchDispatcher:
    """Score all cells in registry and produce ranked portfolio view."""

    def __init__(self, dispatcher: EconomicDispatcher | None = None) -> None:
        self.dispatcher = dispatcher or EconomicDispatcher()

    def rank_registry(self, registry) -> list[DispatchDecision]:
        """Score all cells, return ranked list."""
        cells = registry.list_all()
        return self.dispatcher.rank_cells(cells)

    def top_n(self, registry, n: int = 10) -> list[DispatchDecision]:
        ranked = self.rank_registry(registry)
        return ranked[:n]

    def top_3_deep_candidates(self, registry) -> list[DispatchDecision]:
        """Get top 3 candidates ready for ACTIVE_DEEP."""
        ranked = self.rank_registry(registry)
        candidates = [
            d for d in ranked
            if d.score.confidence in {ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH}
            and d.recommended_action in {"PROMOTE_TO_CANDIDATE_DEEP", "REQUEST_DEEP_WIP_SLOT", "EXECUTE_DEEP_WORK"}
        ]
        return candidates[:3]

    def portfolio_snapshot(self, registry) -> dict[str, Any]:
        """Generate portfolio snapshot for President Command."""
        ranked = self.rank_registry(registry)
        active_deep = registry.list_active_deep()

        return {
            "total_cells": len(ranked),
            "active_deep_count": len(active_deep),
            "active_deep_cells": [c.identity.cell_id for c in active_deep],
            "top_10": [
                {
                    "cell_id": d.cell_id,
                    "score": d.score.economic_priority,
                    "confidence": d.score.confidence.value,
                    "action": d.recommended_action,
                    "evidence_class": d.score.evidence_class.value,
                }
                for d in ranked[:10]
            ],
            "top_3_deep_ready": [
                {
                    "cell_id": d.cell_id,
                    "score": d.score.economic_priority,
                    "confidence": d.score.confidence.value,
                    "action": d.recommended_action,
                }
                for d in self.top_3_deep_candidates(registry)
            ],
            "killed_count": len(registry.list_by_state(LifecycleState.KILLED)),
            "blocked_count": len(registry.list_by_state(LifecycleState.BLOCKED)),
            "generated_at": datetime.now(UTC).isoformat(),
        }


__all__ = [
    "ConfidenceLevel",
    "EvidenceClass",
    "EVIDENCE_WEIGHTS",
    "SECTOR_STRATEGIC_FIT",
    "MONETIZATION_MARGIN",
    "ScoringInput",
    "ScoringBreakdown",
    "DispatchDecision",
    "EconomicDispatcher",
    "BatchDispatcher",
]
