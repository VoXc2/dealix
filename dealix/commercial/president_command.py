"""President Command — daily economic allocator.

Connects: truth, portfolio, opportunities, proof, actions, approvals,
relationships, production, economics.

Generates daily Top 3 with evidence and reasoning.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import (
    EconomicCell,
    LifecycleState,
    PromotionGate,
    UNKNOWN,
)
from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.economic_dispatcher import (
    BatchDispatcher,
    ConfidenceLevel,
    DispatchDecision,
    ScoringInput,
)
from dealix.commercial.portfolio_state_machine import (
    KillGateEvaluator,
    PortfolioStateMachine,
    TransitionReason,
)
from dealix.commercial.deep_wip_enforcer import (
    DeepWipEnforcer,
    DeepWipPolicy,
    PresidentWipController,
    get_enforcer,
)
from dealix.commercial.truth_types import TruthClass
from dealix.commercial.agent_work_packets import AgentPacketBuilder
from dealix.president_approval_digest import (
    PresidentDigest,
    WorkItem,
    WorkStatus,
    build_president_digest,
)


# ─── Input Models ───────────────────────────────────────────────────────


class Top3Selection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rank: int
    cell_id: str
    canonical_name: str
    economic_score: float
    confidence: ConfidenceLevel
    evidence_class: str
    why_selected: str
    evidence_refs: list[str]
    economic_hypothesis: str
    expected_movement: str
    next_measurable_event: str
    owner: str
    resource_budget: str
    stop_loss: str
    why_not_competitors: list[str]


class PresidentCommandOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command_id: str
    cycle_date: str
    generated_at: str
    top_3: list[Top3Selection]
    portfolio_snapshot: dict[str, Any]
    production_trust_status: str
    active_deep_count: int
    approvals_pending: int
    money_now_candidates: list[dict[str, Any]]
    risks: list[dict[str, Any]]
    decisions_needed: list[dict[str, Any]]


# ─── President Command Engine ─────────────────────────────────────────


@dataclass
class PresidentCommand:
    """Daily economic allocation engine."""

    registry: EconomicCellRegistry
    state_machine: PortfolioStateMachine = field(default_factory=PortfolioStateMachine)
    dispatcher: BatchDispatcher = field(default_factory=BatchDispatcher)
    wip_enforcer: DeepWipEnforcer = field(default_factory=lambda: get_enforcer())
    wip_controller: PresidentWipController = field(default_factory=lambda: PresidentWipController(get_enforcer()))
    kill_evaluator: KillGateEvaluator = field(default_factory=KillGateEvaluator)
    packet_builder: AgentPacketBuilder = field(default_factory=AgentPacketBuilder)

    def run_daily_cycle(
        self,
        *,
        evidence_updates: dict[str, dict[str, Any]] | None = None,
        production_trust_status: str = "UNKNOWN",
        approvals_pending: int = 0,
    ) -> PresidentCommandOutput:
        """Execute one daily allocation cycle."""

        evidence_updates = evidence_updates or {}

        # 1. Read live Company Truth (registry state)
        # 2. Inspect production trust
        # 3. Read Portfolio Registry
        # 4. Read Opportunity Graph (registry cells)
        # 5. Read Action Queue (pending work)
        # 6. Read Approval Queue
        # 7. Read Proof Ledger
        # 8. Read Relationship/Consent state
        # 9. Read customer/delivery evidence
        # 10. Read model/runtime cost evidence
        # 11. Detect material external changes
        # 12. Refresh stale high-value evidence
        # 13. Recalculate economic priorities
        ranked = self.dispatcher.rank_registry(self.registry)

        # 14. Evaluate promotion gates
        self._evaluate_promotions(ranked, evidence_updates)

        # 15. Evaluate kill gates
        self._evaluate_kills(evidence_updates)

        # 16. Enforce ACTIVE_DEEP ≤ 3
        self._enforce_deep_wip(ranked)

        # 17. Choose Top 3 deep priorities
        top_3 = self._select_top_3(ranked)

        # 18. Allocate work to five logical agents
        agent_packets = self._create_agent_packets(top_3)

        # 19. Generate bounded work packets
        # 20. Execute safe work (deferred to agents)
        # 21. Verify outputs (deferred)
        # 22. Record receipts (deferred)
        # 23. Update learning (deferred)
        # 24. Surface only founder decisions that truly require the founder

        output = PresidentCommandOutput(
            command_id=self._generate_command_id(),
            cycle_date=datetime.now(UTC).strftime("%Y-%m-%d"),
            generated_at=datetime.now(UTC).isoformat(),
            top_3=top_3,
            portfolio_snapshot=self.dispatcher.portfolio_snapshot(self.registry),
            production_trust_status=production_trust_status,
            active_deep_count=self.wip_enforcer.current_count(),
            approvals_pending=approvals_pending,
            money_now_candidates=self._identify_money_now(ranked),
            risks=self._identify_risks(),
            decisions_needed=self._identify_decisions(top_3),
        )

        return output

    def _create_agent_packets(self, top_3: list[Top3Selection]) -> dict[str, Any]:
        """Create work packets for all five agents."""
        cells = self.registry.list_all()
        return self.packet_builder.build_all_packets(top_3, cells, self.dispatcher.portfolio_snapshot(self.registry))

    def _evaluate_promotions(self, ranked: list[DispatchDecision], evidence_updates: dict[str, dict[str, Any]]) -> None:
        """Evaluate promotion gates for cells ready to advance."""
        for decision in ranked:
            cell = self.registry.get(decision.cell_id)
            if not cell:
                continue

            current = cell.portfolio.lifecycle_state
            next_state = self._next_lifecycle_state(current)
            if not next_state:
                continue

            gate = cell.portfolio.promotion_gate
            if not gate:
                # Assign first gate based on state
                gate = self._gate_for_state(current)
                if not gate:
                    continue

            evidence = evidence_updates.get(cell.identity.cell_id, {})
            passed, missing = self.state_machine.evaluate_promotion(cell, gate, evidence)

            if passed:
                # Promote
                updated = self.state_machine.transition(
                    cell,
                    next_state,
                    TransitionReason.PROMOTION_GATE_PASSED,
                    gate=gate,
                    evidence_refs=evidence.get("refs", []),
                    notes=f"Gate {gate.value} passed",
                )
                self.registry.update(updated)
            elif missing:
                # Record missing evidence for next cycle
                updated = cell.model_copy(update={
                    "portfolio": cell.portfolio.model_copy(update={
                        "next_evidence_needed": list(set(cell.portfolio.next_evidence_needed + missing)),
                    }),
                })
                self.registry.update(updated)

    def _evaluate_kills(self, evidence_updates: dict[str, dict[str, Any]]) -> None:
        """Evaluate kill gates for all cells."""
        for cell in self.registry.list_all():
            if cell.portfolio.lifecycle_state in {LifecycleState.KILLED, LifecycleState.RETIRED}:
                continue

            evidence = evidence_updates.get(cell.identity.cell_id, {})
            triggers = self.kill_evaluator.evaluate(cell, evidence)

            if triggers:
                primary = triggers[0]
                self.state_machine.transition(
                    cell,
                    LifecycleState.KILLED,
                    TransitionReason.KILL_GATE_TRIGGERED,
                    gate=primary,
                    evidence_refs=evidence.get("refs", []),
                    notes=f"Kill triggers: {[t.value for t in triggers]}",
                )

    def _enforce_deep_wip(self, ranked: list[DispatchDecision]) -> None:
        """Ensure ACTIVE_DEEP ≤ 3."""
        # Already enforced by registry, but double-check
        active = self.registry.list_active_deep()
        if len(active) > 3:
            # Force demote lowest priority
            active_ids = {c.identity.cell_id for c in active}
            ranked_active = [d for d in ranked if d.cell_id in active_ids]
            if ranked_active:
                victim = ranked_active[-1]
                victim_cell = self.registry.get(victim.cell_id)
                if victim_cell:
                    self.wip_enforcer.force_release_slot(victim_cell.identity.cell_id)
                    self.state_machine.transition(
                        victim_cell,
                        LifecycleState.CANDIDATE_DEEP,
                        TransitionReason.WIP_SLOT_RELEASED,
                        notes="Forced demotion: DEEP_WIP_MAX exceeded",
                    )

    def _select_top_3(self, ranked: list[DispatchDecision]) -> list[Top3Selection]:
        """Select top 3 with full reasoning."""
        # Filter to cells that are deep-ready or active deep
        deep_ready = [
            d for d in ranked
            if d.score.confidence in {ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH}
            and d.recommended_action in {
                "PROMOTE_TO_CANDIDATE_DEEP",
                "REQUEST_DEEP_WIP_SLOT",
                "EXECUTE_DEEP_WORK",
                "CONTINUE_DEEP_EXECUTION",
            }
        ]

        # Also consider high-score qualified cells
        qualified = [
            d for d in ranked
            if d.score.economic_priority > 0.5
            and d.recommended_action in {"PROMOTE_TO_CANDIDATE_DEEP", "RUN_VALIDATION_EXPERIMENT"}
        ]

        candidates = deep_ready + qualified
        seen = set()
        unique = []
        for c in candidates:
            if c.cell_id not in seen:
                seen.add(c.cell_id)
                unique.append(c)

        top_3 = []
        for i, decision in enumerate(unique[:3]):
            cell = self.registry.get(decision.cell_id)
            if not cell:
                continue

            # Build reasoning
            why_selected = self._build_selection_reasoning(cell, decision, ranked)
            why_not = self._build_competitor_reasoning(cell, decision, ranked[:10])

            top_3.append(Top3Selection(
                rank=i + 1,
                cell_id=cell.identity.cell_id,
                canonical_name=cell.identity.canonical_name,
                economic_score=decision.score.economic_priority,
                confidence=decision.score.confidence,
                evidence_class=decision.score.evidence_class.value,
                why_selected=why_selected,
                evidence_refs=cell.evidence.evidence_sources,
                economic_hypothesis=self._economic_hypothesis(cell),
                expected_movement=self._expected_movement(cell, decision),
                next_measurable_event=decision.next_evidence_needed[0] if decision.next_evidence_needed else "evidence_collection",
                owner=cell.portfolio.assigned_agent or self._default_owner(cell),
                resource_budget=self._estimate_budget(cell),
                stop_loss=cell.portfolio.stop_loss or "kill_gate_triggered",
                why_not_competitors=why_not,
            ))

        return top_3

    def _build_selection_reasoning(self, cell: EconomicCell, decision: DispatchDecision, ranked: list[DispatchDecision]) -> str:
        parts = [
            f"Score: {decision.score.economic_priority:.3f}",
            f"Confidence: {decision.score.confidence.value}",
            f"Evidence: {decision.score.evidence_class.value}",
            f"State: {cell.portfolio.lifecycle_state.value}",
        ]
        if decision.score.positive_factors:
            parts.append(f"Positive: {', '.join(decision.score.positive_factors[:3])}")
        return "; ".join(parts)

    def _build_competitor_reasoning(self, cell: EconomicCell, decision: DispatchDecision, top_10: list[DispatchDecision]) -> list[str]:
        reasons = []
        for other in top_10:
            if other.cell_id == cell.identity.cell_id:
                continue
            if other.score.economic_priority >= decision.score.economic_priority * 0.8:
                reasons.append(f"{other.cell_id}: similar score ({other.score.economic_priority:.3f}) but {other.score.confidence.value} confidence")
        return reasons[:3]

    def _economic_hypothesis(self, cell: EconomicCell) -> str:
        return (
            f"{cell.problem.problem_class.value} in {cell.market.sector.value} "
            f"for {cell.buyer.buyer_group.value} via {cell.monetization.monetization_rail.value} "
            f"→ {cell.economics.probability_adjusted_value or 'unknown'} EV"
        )

    def _expected_movement(self, cell: EconomicCell, decision: DispatchDecision) -> str:
        action_map = {
            "PROMOTE_TO_CANDIDATE_DEEP": "Enter deep execution with WIP slot",
            "REQUEST_DEEP_WIP_SLOT": "Claim deep WIP slot",
            "EXECUTE_DEEP_WORK": "Deliver pilot/proof",
            "CONTINUE_DEEP_EXECUTION": "Continue delivery, capture proof",
            "RUN_VALIDATION_EXPERIMENT": "Run cheap validation experiment",
        }
        return action_map.get(decision.recommended_action, decision.recommended_action)

    def _default_owner(self, cell: EconomicCell) -> str:
        sector = cell.market.sector
        if sector in {cell.market.sector.GOVERNMENT_B2G, cell.market.sector.EXPORT_IMPORT_RHQ}:
            return "dealix-sales"
        elif sector in {cell.market.sector.TECHNOLOGY_SAAS_SI, cell.market.sector.FINANCE_FINTECH_INSURANCE}:
            return "dealix-engineer"
        return "dealix-delivery"

    def _estimate_budget(self, cell: EconomicCell) -> str:
        costs = []
        for field_name in ["cost_to_validate", "cost_to_sell", "cost_to_deliver"]:
            val = getattr(cell.economics, field_name)
            if val != UNKNOWN:
                costs.append(val)
        return f"validate:{costs[0] if len(costs) > 0 else '?'} sell:{costs[1] if len(costs) > 1 else '?'} deliver:{costs[2] if len(costs) > 2 else '?'}"

    def _identify_money_now(self, ranked: list[DispatchDecision]) -> list[dict[str, Any]]:
        """Identify strongest Money-Now paths."""
        money_now = []
        for decision in ranked[:10]:
            cell = self.registry.get(decision.cell_id)
            if not cell:
                continue

            # Money-Now criteria
            has_relationship = cell.evidence.relationship_evidence != UNKNOWN
            has_problem = cell.problem.measurable_loss_type != UNKNOWN
            has_buyer = cell.buyer.economic_buyer or cell.buyer.champion_role
            short_path = cell.procurement.procurement_friction in {"low", "medium"}
            feasible_delivery = cell.execution.delivery_complexity in {"low", "medium"}
            measurable_criteria = cell.offer.acceptance_criteria != ""

            if has_relationship and has_problem and has_buyer and short_path and feasible_delivery and measurable_criteria:
                money_now.append({
                    "cell_id": cell.identity.cell_id,
                    "name": cell.identity.canonical_name,
                    "score": decision.score.economic_priority,
                    "score_truth": TruthClass.ESTIMATED.value,
                    "evidence": cell.evidence.evidence_level.value,
                    "next_step": decision.recommended_action,
                })

        return money_now[:5]

    def _identify_risks(self) -> list[dict[str, Any]]:
        risks = []
        active = self.registry.list_active_deep()
        if len(active) == 3:
            risks.append({"code": "DEEP_WIP_AT_MAX", "message": "All 3 deep WIP slots occupied"})

        blocked = self.registry.list_by_state(LifecycleState.BLOCKED)
        if blocked:
            risks.append({"code": "BLOCKED_CELLS", "count": len(blocked)})

        return risks

    def _identify_decisions(self, top_3: list[Top3Selection]) -> list[dict[str, Any]]:
        decisions = []
        for sel in top_3:
            if sel.confidence in {ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW}:
                decisions.append({
                    "type": "LOW_CONFIDENCE_DEEP_WORK",
                    "cell_id": sel.cell_id,
                    "message": f"Top-{sel.rank} has {sel.confidence.value} confidence. Consider validation experiment first.",
                })
        return decisions

    def _next_lifecycle_state(self, current: LifecycleState) -> LifecycleState | None:
        transitions = {
            LifecycleState.DISCOVERED: LifecycleState.WATCH,
            LifecycleState.WATCH: LifecycleState.RESEARCH,
            LifecycleState.RESEARCH: LifecycleState.VALIDATE,
            LifecycleState.VALIDATE: LifecycleState.QUALIFIED,
            LifecycleState.QUALIFIED: LifecycleState.ACTIVE_LIGHT,
            LifecycleState.ACTIVE_LIGHT: LifecycleState.CANDIDATE_DEEP,
            LifecycleState.CANDIDATE_DEEP: LifecycleState.ACTIVE_DEEP,
            LifecycleState.ACTIVE_DEEP: LifecycleState.DELIVERING,
            LifecycleState.DELIVERING: LifecycleState.PROVEN,
            LifecycleState.PROVEN: LifecycleState.PRODUCTIZE,
            LifecycleState.PRODUCTIZE: LifecycleState.SCALE,
        }
        return transitions.get(current)

    def _gate_for_state(self, state: LifecycleState):
        gate_map = {
            LifecycleState.DISCOVERED: PromotionGate.GATE_1_REAL_SIGNAL,
            LifecycleState.WATCH: PromotionGate.GATE_1_REAL_SIGNAL,
            LifecycleState.RESEARCH: PromotionGate.GATE_2_BUYER,
            LifecycleState.VALIDATE: PromotionGate.GATE_3_ECONOMIC_PAIN,
            LifecycleState.QUALIFIED: PromotionGate.GATE_4_ACCESS,
            LifecycleState.ACTIVE_LIGHT: PromotionGate.GATE_5_PROCUREMENT,
            LifecycleState.CANDIDATE_DEEP: PromotionGate.GATE_6_DELIVERY,
        }
        return gate_map.get(state)

    def _generate_command_id(self) -> str:
        payload = f"president_command_{datetime.now(UTC).isoformat()}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


__all__ = [
    "Top3Selection",
    "PresidentCommandOutput",
    "PresidentCommand",
]
