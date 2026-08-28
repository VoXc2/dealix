"""V18 Founder Portfolio Command (Workstream J / §22-23).

Compresses the whole portfolio into MONEY / TOP 5 / BUYABILITY / EVENT /
DISTRIBUTION / EXPERIMENTS / CAPACITY / APPROVAL / NEXT AUTONOMOUS ACTION.
Never more than 5 portfolio moves. The founder sees decisions, not noise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.portfolio_os.buyability import (
    BuyabilityAssessment,
    assess_buyability,
)
from auto_client_acquisition.portfolio_os.capacity import (
    AllocationResult,
    CapacityAllocation,
    CapacityBudget,
    allocate_capacity,
)
from auto_client_acquisition.portfolio_os.distribution import (
    DistributionEdge,
    ProofReuseAssessment,
)
from auto_client_acquisition.portfolio_os.events import OptimizedEventPlan
from auto_client_acquisition.portfolio_os.experiments import ExperimentRegistry
from auto_client_acquisition.portfolio_os.losses import LossEvent
from auto_client_acquisition.portfolio_os.portfolio import (
    PortfolioItem,
    PortfolioRanking,
    rank_portfolio,
)


@dataclass(frozen=True, slots=True)
class PortfolioCommand:
    generated_at: str
    north_star: str = "FIRST VERIFIED PAID PILOT"
    verified_revenue_sar: float = 0.0
    closest_verified_money_path: str = ""
    top_moves: tuple[PortfolioItem, ...] = ()
    top_buyability_gaps: list[str] = field(default_factory=list)
    top_decision_risks: list[str] = field(default_factory=list)
    next_event_priority: str = ""
    highest_value_distribution: str = ""
    experiments_scale: list[str] = field(default_factory=list)
    experiments_retest: list[str] = field(default_factory=list)
    experiments_stop: list[str] = field(default_factory=list)
    experiments_invalid: list[str] = field(default_factory=list)
    capacity_summary: str = ""
    approval_needed: list[str] = field(default_factory=list)
    next_autonomous_action: str = ""
    proof_notes: list[str] = field(default_factory=list)
    learning: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "north_star": self.north_star,
            "verified_revenue_sar": self.verified_revenue_sar,
            "closest_verified_money_path": self.closest_verified_money_path,
            "top_moves": [i.to_dict() for i in self.top_moves],
            "top_buyability_gaps": self.top_buyability_gaps,
            "top_decision_risks": self.top_decision_risks,
            "next_event_priority": self.next_event_priority,
            "highest_value_distribution": self.highest_value_distribution,
            "experiments_scale": self.experiments_scale,
            "experiments_retest": self.experiments_retest,
            "experiments_stop": self.experiments_stop,
            "experiments_invalid": self.experiments_invalid,
            "capacity_summary": self.capacity_summary,
            "approval_needed": self.approval_needed,
            "next_autonomous_action": self.next_autonomous_action,
            "proof_notes": self.proof_notes,
            "learning": self.learning,
        }


def build_portfolio_command(
    *,
    generated_at: str,
    items: list[PortfolioItem],
    verified_revenue_sar: float = 0.0,
    closest_verified_money_path: str = "",
    assessments: list[BuyabilityAssessment] | None = None,
    event_plan: OptimizedEventPlan | None = None,
    distribution_edges: list[DistributionEdge] | None = None,
    proof_reuse: list[ProofReuseAssessment] | None = None,
    experiments: ExperimentRegistry | None = None,
    losses: list[LossEvent] | None = None,
    capacity_budget: CapacityBudget | None = None,
    capacity_allocation: AllocationResult | None = None,
) -> PortfolioCommand:
    """Compress the full portfolio into the founder command. Top 5 max.

    This is pure synthesis of deterministic inputs — it never creates
    qualification evidence, never invents proof, and never relaxes gates.
    """
    ranking: PortfolioRanking = rank_portfolio(items)
    top_moves = ranking.top(5)

    buyability_gaps: list[str] = []
    decision_risks: list[str] = []
    for a in assessments or []:
        if a.top_hidden_buyer_gap:
            gap = f"{a.account_id}: {a.top_hidden_buyer_gap}"
            if gap not in buyability_gaps:
                buyability_gaps.append(gap)
        if a.top_decision_risk:
            risk = f"{a.account_id}: {a.top_decision_risk}"
            if risk not in decision_risks:
                decision_risks.append(risk)
    buyability_gaps = buyability_gaps[:5]
    decision_risks = decision_risks[:5]

    next_event_priority = ""
    if event_plan and event_plan.allocations:
        best = max(event_plan.allocations, key=lambda a: a.score())
        next_event_priority = (
            f"{best.event_name} {best.day} {best.start_hour}-{best.end_hour}"
            f" @ {best.venue}"
        )

    highest_value_distribution = ""
    if distribution_edges:
        # Highest-value = edge with a clear CTA + evidence + outcome.
        scored = [
            e
            for e in distribution_edges
            if e.cta and e.evidence and e.outcome
        ]
        if scored:
            best = scored[0]
            highest_value_distribution = (
                f"{best.asset} → {best.audience} ({best.channel}): {best.cta}"
            )

    exp_scale: list[str] = []
    exp_retest: list[str] = []
    exp_stop: list[str] = []
    exp_invalid: list[str] = []
    for e in (experiments.experiments if experiments else ()):
        if e.decision == "SCALE":
            exp_scale.append(e.experiment_id)
        elif e.decision == "RETEST":
            exp_retest.append(e.experiment_id)
        elif e.decision == "STOP":
            exp_stop.append(e.experiment_id)
        elif e.decision == "INVALID":
            exp_invalid.append(e.experiment_id)

    capacity_summary = ""
    if capacity_allocation is not None:
        if capacity_allocation.feasible:
            capacity_summary = (
                "capacity feasible: "
                + ", ".join(capacity_allocation.accepted_lanes)
            )
        else:
            capacity_summary = (
                "capacity OVERBOOKED: "
                + "; ".join(v.to_dict()["resource"] for v in capacity_allocation.violations)
            )

    proof_notes: list[str] = []
    for p in proof_reuse or []:
        if not p.reusable:
            proof_notes.append(f"{p.proof_id}: reuse blocked ({', '.join(p.reasons)})")
    for l in losses or []:
        proof_notes.append(
            f"loss {l.account_id}: {l.reason} — {l.root_cause_hypothesis or 'root cause pending'}"
        )

    # Closest money path defaults to the top-ranked item when not provided.
    money_path = closest_verified_money_path
    if not money_path and top_moves:
        top = top_moves[0]
        money_path = (
            f"Lane {top.lane}: {top.company or top.item_id} → "
            f"{top.expected_next_evidence or 'evidence capture'}"
        )

    next_autonomous_action = ""
    if top_moves:
        top = top_moves[0]
        next_autonomous_action = (
            f"{top.lane}: prepare {top.expected_next_evidence or 'evidence capture'}"
            f" for {top.company or top.item_id} (L0-L4 only, no external send)"
        )

    return PortfolioCommand(
        generated_at=generated_at,
        verified_revenue_sar=verified_revenue_sar,
        closest_verified_money_path=money_path,
        top_moves=tuple(top_moves),
        top_buyability_gaps=buyability_gaps,
        top_decision_risks=decision_risks,
        next_event_priority=next_event_priority,
        highest_value_distribution=highest_value_distribution,
        experiments_scale=exp_scale,
        experiments_retest=exp_retest,
        experiments_stop=exp_stop,
        experiments_invalid=exp_invalid,
        capacity_summary=capacity_summary,
        approval_needed=[],
        next_autonomous_action=next_autonomous_action,
        proof_notes=proof_notes,
        learning=[],
    )
