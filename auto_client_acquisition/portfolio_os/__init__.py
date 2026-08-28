"""V18 Revenue Portfolio Control Plane — meta-layer over #1273/#1274.

Pure deterministic logic + canonical config. Consumes V17 primitives
(AccountCase, DealDeskResult, capability catalog) and Founder OS queues.
Never a CRM, Opportunity Graph, Approval Center, Proof Ledger or scheduler.

Submodules:
- buyability: buying-group model + decision-defensibility assessment
- portfolio: portfolio graph, value scoring, ranking
- experiments: experiment registry with SCALE/RETEST/STOP/INVALID gates
- capacity: founder/agent/event attention allocator
- distribution: asset→audience→channel graph + proof reuse gates
- events: event portfolio optimizer (Big 5 / LEAP / DeepFest)
- partners: partner/referral compounding evaluation
- losses: no-decision / loss intelligence
- command: Founder Portfolio Command synthesis (TOP 5 only)
"""

from __future__ import annotations

from auto_client_acquisition.portfolio_os.buyability import (
    BuyabilityAssessment,
    BuyingGroup,
    BuyingGroupMember,
    BuyingRole,
    RoleConfidence,
    assess_buyability,
    default_buying_group,
)
from auto_client_acquisition.portfolio_os.capacity import (
    AllocationViolation,
    CapacityAllocation,
    CapacityBudget,
    allocate_capacity,
    default_capacity_budget,
)
from auto_client_acquisition.portfolio_os.command import (
    PortfolioCommand,
    build_portfolio_command,
)
from auto_client_acquisition.portfolio_os.distribution import (
    DistributionEdge,
    ProofReuseAssessment,
    build_distribution_edge,
    evaluate_proof_reuse,
)
from auto_client_acquisition.portfolio_os.events import (
    EventAllocation,
    EventConflict,
    EventWindow,
    OptimizedEventPlan,
    canonical_event_windows,
    optimize_event_plan,
)
from auto_client_acquisition.portfolio_os.experiments import (
    Experiment,
    ExperimentDecision,
    ExperimentRegistry,
    register_experiment,
)
from auto_client_acquisition.portfolio_os.losses import (
    LossEvent,
    LossReason,
    record_loss,
)
from auto_client_acquisition.portfolio_os.partners import (
    PartnerPath,
    PartnerPathAssessment,
    assess_partner_path,
)
from auto_client_acquisition.portfolio_os.portfolio import (
    PortfolioItem,
    PortfolioLane,
    PortfolioRanking,
    rank_portfolio,
    value_score,
)

__all__ = [
    "AllocationViolation",
    "BuyabilityAssessment",
    "BuyingGroup",
    "BuyingGroupMember",
    "BuyingRole",
    "CapacityAllocation",
    "CapacityBudget",
    "DistributionEdge",
    "EventAllocation",
    "EventConflict",
    "EventWindow",
    "Experiment",
    "ExperimentDecision",
    "ExperimentRegistry",
    "LossEvent",
    "LossReason",
    "OptimizedEventPlan",
    "PartnerPath",
    "PartnerPathAssessment",
    "PortfolioCommand",
    "PortfolioItem",
    "PortfolioLane",
    "PortfolioRanking",
    "ProofReuseAssessment",
    "RoleConfidence",
    "allocate_capacity",
    "assess_buyability",
    "assess_partner_path",
    "build_distribution_edge",
    "build_portfolio_command",
    "canonical_event_windows",
    "default_buying_group",
    "default_capacity_budget",
    "evaluate_proof_reuse",
    "optimize_event_plan",
    "rank_portfolio",
    "record_loss",
    "register_experiment",
    "value_score",
]
