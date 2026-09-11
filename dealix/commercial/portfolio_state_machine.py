"""Portfolio State Machine — explicit lifecycle with promotion/kill gates.

State changes require evidence. Model enthusiasm is not evidence.
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
    PromotionGate,
    UNKNOWN,
)


# ─── Transition Records ────────────────────────────────────────────────


class TransitionReason(StrEnum):
    PROMOTION_GATE_PASSED = "promotion_gate_passed"
    KILL_GATE_TRIGGERED = "kill_gate_triggered"
    MANUAL_OVERRIDE = "manual_override"
    EVIDENCE_EXPIRED = "evidence_expired"
    EXTERNAL_CHANGE = "external_change"
    WIP_SLOT_CLAIMED = "wip_slot_claimed"
    WIP_SLOT_RELEASED = "wip_slot_released"


class StateTransition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    transition_id: str
    cell_id: str
    from_state: LifecycleState
    to_state: LifecycleState
    reason: TransitionReason
    gate: PromotionGate | KillTrigger | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    decided_by: str = "system"
    decided_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.transition_id:
            payload = self.model_dump(mode="json", exclude={"transition_id", "decided_at"})
            object.__setattr__(self, "transition_id", hashlib.sha256(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()[:16])


# ─── Promotion Gate Evaluators ────────────────────────────────────────


class PromotionGateEvaluator:
    """Evaluate the 10 promotion gates with explicit evidence."""

    GATE_DESCRIPTIONS = {
        PromotionGate.GATE_1_REAL_SIGNAL: "Is there evidence the problem exists?",
        PromotionGate.GATE_2_BUYER: "Is there an identifiable accountable buyer?",
        PromotionGate.GATE_3_ECONOMIC_PAIN: "Can the consequence be described economically?",
        PromotionGate.GATE_4_ACCESS: "Is there a viable distribution/relationship path?",
        PromotionGate.GATE_5_PROCUREMENT: "Is purchase/procurement practically possible?",
        PromotionGate.GATE_6_DELIVERY: "Can Dealix deliver with bounded risk?",
        PromotionGate.GATE_7_ECONOMICS: "Is expected value attractive relative to cost?",
        PromotionGate.GATE_8_PROOF: "Can success produce customer-validatable proof?",
        PromotionGate.GATE_9_REPEATABILITY: "Could this become reusable?",
        PromotionGate.GATE_10_RISK: "Are regulatory/security/privacy/reputation risks acceptable?",
    }

    def evaluate(self, cell: EconomicCell, gate: PromotionGate, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        """Returns (passed, missing_evidence)."""
        checks = {
            PromotionGate.GATE_1_REAL_SIGNAL: self._gate_1_real_signal,
            PromotionGate.GATE_2_BUYER: self._gate_2_buyer,
            PromotionGate.GATE_3_ECONOMIC_PAIN: self._gate_3_economic_pain,
            PromotionGate.GATE_4_ACCESS: self._gate_4_access,
            PromotionGate.GATE_5_PROCUREMENT: self._gate_5_procurement,
            PromotionGate.GATE_6_DELIVERY: self._gate_6_delivery,
            PromotionGate.GATE_7_ECONOMICS: self._gate_7_economics,
            PromotionGate.GATE_8_PROOF: self._gate_8_proof,
            PromotionGate.GATE_9_REPEATABILITY: self._gate_9_repeatability,
            PromotionGate.GATE_10_RISK: self._gate_10_risk,
        }
        checker = checks.get(gate)
        if not checker:
            return False, [f"unknown gate: {gate}"]
        return checker(cell, evidence)

    def _gate_1_real_signal(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if not evidence.get("problem_evidence"):
            missing.append("problem_evidence_ref")
        if cell.evidence.evidence_level == EvidenceLevel.L0_ANECDOTAL:
            missing.append("evidence_above_L0")
        return len(missing) == 0, missing

    def _gate_2_buyer(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if not cell.buyer.economic_buyer and not cell.buyer.champion_role:
            missing.append("economic_buyer_or_champion")
        if not evidence.get("buyer_verification"):
            missing.append("buyer_verification_ref")
        return len(missing) == 0, missing

    def _gate_3_economic_pain(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if cell.problem.measurable_loss_type == UNKNOWN:
            missing.append("measurable_loss_type")
        if not evidence.get("pain_quantification"):
            missing.append("pain_quantification_ref")
        return len(missing) == 0, missing

    def _gate_4_access(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if not cell.distribution.relationship_requirement and not evidence.get("warm_path"):
            missing.append("relationship_path_or_warm_intro")
        if cell.evidence.consent_requirement == "":
            missing.append("consent_state")
        return len(missing) == 0, missing

    def _gate_5_procurement(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if cell.procurement.procurement_rail in {cell.procurement.procurement_rail.TENDER, cell.procurement.procurement_rail.GOVERNMENT_PROCUREMENT}:
            if not evidence.get("vendor_registered"):
                missing.append("vendor_registration")
            if not evidence.get("framework_agreement"):
                missing.append("framework_agreement_ref")
        return len(missing) == 0, missing

    def _gate_6_delivery(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if not cell.execution.capability_dependencies:
            missing.append("capability_dependencies")
        if cell.execution.delivery_complexity in {"high", "unknown"}:
            missing.append("delivery_complexity_assessment")
        return len(missing) == 0, missing

    def _gate_7_economics(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if cell.economics.probability_adjusted_value == UNKNOWN:
            missing.append("probability_adjusted_value")
        if cell.economics.gross_margin_hypothesis == UNKNOWN:
            missing.append("gross_margin_hypothesis")
        return len(missing) == 0, missing

    def _gate_8_proof(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if cell.proof.proof_strength == UNKNOWN:
            missing.append("proof_method_design")
        if not evidence.get("proof_capture_plan"):
            missing.append("proof_capture_plan")
        return len(missing) == 0, missing

    def _gate_9_repeatability(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if not cell.execution.reusable_factory_dependencies:
            missing.append("reusable_factory_identification")
        return len(missing) == 0, missing

    def _gate_10_risk(self, cell: EconomicCell, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        missing = []
        if cell.risk.regulatory_risk in {"high", "unknown"}:
            missing.append("regulatory_risk_assessment")
        if cell.risk.cybersecurity_risk in {"high", "unknown"}:
            missing.append("cybersecurity_risk_assessment")
        if cell.risk.privacy_risk in {"high", "unknown"}:
            missing.append("privacy_risk_assessment")
        return len(missing) == 0, missing


# ─── Kill Gate Evaluators ─────────────────────────────────────────────


class KillGateEvaluator:
    """Evaluate the 14 kill triggers."""

    def evaluate(self, cell: EconomicCell, evidence: dict[str, Any]) -> list[KillTrigger]:
        """Return list of triggered kill gates."""
        triggers = []

        checks = {
            KillTrigger.NO_CUSTOMER_PROBLEM: lambda: cell.problem.pain_statement == "" and not evidence.get("problem_evidence"),
            KillTrigger.NO_BUYER: lambda: not cell.buyer.economic_buyer and not cell.buyer.champion_role and not evidence.get("buyer_verification"),
            KillTrigger.NO_ACQUISITION_PATH: lambda: not cell.distribution.relationship_requirement and not evidence.get("warm_path") and cell.evidence.consent_requirement in {"", UNKNOWN},
            KillTrigger.NO_PROCUREMENT_ROUTE: lambda: cell.procurement.procurement_rail in {cell.procurement.procurement_rail.TENDER, cell.procurement.procurement_rail.GOVERNMENT_PROCUREMENT} and not evidence.get("vendor_registered"),
            KillTrigger.NEGATIVE_ECONOMICS: lambda: cell.economics.probability_adjusted_value != UNKNOWN and self._is_negative(cell.economics.probability_adjusted_value),
            KillTrigger.UNACCEPTABLE_RISK: lambda: cell.risk.regulatory_risk == "high" or cell.risk.cybersecurity_risk == "high",
            KillTrigger.EXTREME_DELIVERY_BURDEN: lambda: cell.execution.delivery_complexity == "extreme",
            KillTrigger.EXCESSIVE_FOUNDER_DEPENDENCY: lambda: cell.execution.founder_dependency == "high",
            KillTrigger.NO_MEASURABLE_ACCEPTANCE: lambda: cell.offer.acceptance_criteria == "",
            KillTrigger.DUPLICATE_CAPABILITY: lambda: evidence.get("duplicate_of"),
            KillTrigger.NO_MOVEMENT_AFTER_EXPERIMENTS: lambda: evidence.get("experiments_run", 0) >= 3 and not evidence.get("movement"),
            KillTrigger.CUSTOMER_REJECTION: lambda: evidence.get("rejected", False),
            KillTrigger.STRONGER_SUBSTITUTE: lambda: evidence.get("stronger_substitute"),
            KillTrigger.TECHNICAL_IMPOSSIBILITY: lambda: evidence.get("technically_impossible", False),
            KillTrigger.COMPLIANCE_BARRIER: lambda: evidence.get("compliance_blocked", False),
            KillTrigger.EVIDENCE_DETERIORATION: lambda: evidence.get("evidence_stale", False),
        }

        for trigger, check in checks.items():
            try:
                if check():
                    triggers.append(trigger)
            except Exception:
                pass

        return triggers

    @staticmethod
    def _is_negative(value: str) -> bool:
        try:
            return float(value) < 0
        except ValueError:
            return False


# ─── State Machine ────────────────────────────────────────────────────


@dataclass
class PortfolioStateMachine:
    """Manages lifecycle transitions with evidence requirements."""

    promotion_evaluator: PromotionGateEvaluator = field(default_factory=PromotionGateEvaluator)
    kill_evaluator: KillGateEvaluator = field(default_factory=KillGateEvaluator)
    transitions: list[StateTransition] = field(default_factory=list)

    # Valid transitions
    VALID_TRANSITIONS: dict[LifecycleState, set[LifecycleState]] = field(default_factory=lambda: {
        LifecycleState.DISCOVERED: {LifecycleState.WATCH, LifecycleState.RESEARCH, LifecycleState.KILLED},
        LifecycleState.WATCH: {LifecycleState.RESEARCH, LifecycleState.DISCOVERED, LifecycleState.KILLED},
        LifecycleState.RESEARCH: {LifecycleState.VALIDATE, LifecycleState.WATCH, LifecycleState.KILLED},
        LifecycleState.VALIDATE: {LifecycleState.QUALIFIED, LifecycleState.RESEARCH, LifecycleState.KILLED, LifecycleState.BLOCKED},
        LifecycleState.QUALIFIED: {LifecycleState.ACTIVE_LIGHT, LifecycleState.CANDIDATE_DEEP, LifecycleState.VALIDATE, LifecycleState.KILLED, LifecycleState.PAUSED},
        LifecycleState.ACTIVE_LIGHT: {LifecycleState.CANDIDATE_DEEP, LifecycleState.QUALIFIED, LifecycleState.DELIVERING, LifecycleState.KILLED, LifecycleState.PAUSED},
        LifecycleState.CANDIDATE_DEEP: {LifecycleState.ACTIVE_DEEP, LifecycleState.ACTIVE_LIGHT, LifecycleState.KILLED, LifecycleState.PAUSED},
        LifecycleState.ACTIVE_DEEP: {LifecycleState.DELIVERING, LifecycleState.CANDIDATE_DEEP, LifecycleState.KILLED, LifecycleState.PAUSED},
        LifecycleState.DELIVERING: {LifecycleState.PROVEN, LifecycleState.ACTIVE_DEEP, LifecycleState.KILLED},
        LifecycleState.PROVEN: {LifecycleState.PRODUCTIZE, LifecycleState.SCALE, LifecycleState.DELIVERING, LifecycleState.RETIRED},
        LifecycleState.PRODUCTIZE: {LifecycleState.SCALE, LifecycleState.PROVEN, LifecycleState.RETIRED},
        LifecycleState.SCALE: {LifecycleState.RETIRED},
        LifecycleState.BLOCKED: {LifecycleState.VALIDATE, LifecycleState.QUALIFIED, LifecycleState.KILLED, LifecycleState.PAUSED},
        LifecycleState.PAUSED: {LifecycleState.QUALIFIED, LifecycleState.ACTIVE_LIGHT, LifecycleState.CANDIDATE_DEEP, LifecycleState.KILLED},
        LifecycleState.KILLED: {LifecycleState.RETIRED},
        LifecycleState.RETIRED: set(),
    })

    def can_transition(self, from_state: LifecycleState, to_state: LifecycleState) -> bool:
        return to_state in self.VALID_TRANSITIONS.get(from_state, set())

    def transition(
        self,
        cell: EconomicCell,
        to_state: LifecycleState,
        reason: TransitionReason,
        gate: PromotionGate | KillTrigger | None = None,
        evidence_refs: list[str] | None = None,
        decided_by: str = "system",
        notes: str = "",
    ) -> EconomicCell:
        """Execute state transition with validation."""
        from_state = cell.portfolio.lifecycle_state

        if not self.can_transition(from_state, to_state):
            raise ValueError(f"Invalid transition: {from_state} -> {to_state}")

        # Record transition
        transition = StateTransition(
            cell_id=cell.identity.cell_id,
            from_state=from_state,
            to_state=to_state,
            reason=reason,
            gate=gate,
            evidence_refs=evidence_refs or [],
            decided_by=decided_by,
            notes=notes,
        )
        self.transitions.append(transition)

        # Apply to cell
        return cell.model_copy(update={
            "portfolio": cell.portfolio.model_copy(update={
                "lifecycle_state": to_state,
            }),
            "identity": cell.identity.model_copy(update={
                "version": cell.identity.version + 1,
                "updated_at": datetime.now(UTC).isoformat(),
            }),
        })

    def evaluate_promotion(self, cell: EconomicCell, gate: PromotionGate, evidence: dict[str, Any]) -> tuple[bool, list[str]]:
        return self.promotion_evaluator.evaluate(cell, gate, evidence)

    def evaluate_kill_gates(self, cell: EconomicCell, evidence: dict[str, Any]) -> list[KillTrigger]:
        return self.kill_evaluator.evaluate(cell, evidence)

    def auto_evaluate(self, cell: EconomicCell, evidence: dict[str, Any]) -> list[EconomicCell]:
        """Auto-evaluate kill gates and return updated cell if killed."""
        triggers = self.evaluate_kill_gates(cell, evidence)
        if triggers:
            # Kill with highest severity trigger
            primary = triggers[0]
            return [self.transition(
                cell,
                LifecycleState.KILLED,
                TransitionReason.KILL_GATE_TRIGGERED,
                gate=primary,
                evidence_refs=evidence.get("refs", []),
                notes=f"Kill triggers: {[t.value for t in triggers]}",
            )]
        return []


# ─── Validation Experiments (Weak Gates) ───────────────────────────────


class ValidationExperiment(BaseModel):
    """Cheap experiment to reduce uncertainty when gate is weak."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    experiment_id: str
    cell_id: str
    target_gate: PromotionGate
    description: str
    estimated_cost: str
    estimated_duration_days: int
    success_criteria: str
    evidence_to_produce: list[str]
    voi_positive: bool = False

    @classmethod
    def create(cls, cell: EconomicCell, gate: PromotionGate, missing: list[str]) -> "ValidationExperiment":
        exp_id = f"exp_{cell.identity.cell_id}_{gate.value}_{hashlib.md5(str(missing).encode()).hexdigest()[:6]}"
        return cls(
            experiment_id=exp_id,
            cell_id=cell.identity.cell_id,
            target_gate=gate,
            description=f"Validate {gate.value}: {', '.join(missing)}",
            estimated_cost="low",
            estimated_duration_days=7,
            success_criteria=f"Produce evidence for: {', '.join(missing)}",
            evidence_to_produce=missing,
            voi_positive=True,
        )


__all__ = [
    "TransitionReason",
    "StateTransition",
    "PromotionGateEvaluator",
    "KillGateEvaluator",
    "PortfolioStateMachine",
    "ValidationExperiment",
]
