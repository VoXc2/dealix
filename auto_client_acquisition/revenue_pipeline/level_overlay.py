"""Revenue Pipeline — L2-L7 evidence-level labeling overlay.

This module does NOT introduce a second state machine. It is a thin
*labeling overlay* on top of the canonical pipeline machine in
``stage_policy.py``: it maps each existing ``PipelineStage`` to the
strategy's evidence/deal level (L2-L7) and to a strategy event label.

The strategy's transition rules are already enforced by the existing
machine and are NOT re-implemented here:

- "no 'sent' without founder confirmation" — the ``founder_sent_manually``
  stage is only reachable through ``advance_stage`` (founder action).
- "no revenue counted before invoice paid" — ``is_l7_confirmed`` delegates
  to ``counts_as_revenue`` (single source of truth, Constitution Art. VI).

Strategy reference: docs/02_strategy/GOVERNED_REVENUE_AI_OPERATIONS.md §7.
Pure-local. NO DB. NO external call. NO LLM.
"""

from __future__ import annotations

from typing import Literal

from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    counts_as_commitment,
    counts_as_revenue,
)

# The strategy's evidence/deal levels. L0/L3 are intentionally unused —
# the strategy jumps L2 → L4 (a draft that has not been sent carries no
# external evidence; sending it is the first external evidence event).
EvidenceStateLevel = Literal[
    "L1",
    "L2",
    "L4",
    "L5",
    "L6",
    "L7_candidate",
    "L7_confirmed",
]

# Ordering rank — higher means more deal evidence accrued.
LEVEL_RANK: dict[EvidenceStateLevel, int] = {
    "L1": 1,
    "L2": 2,
    "L4": 4,
    "L5": 5,
    "L6": 6,
    "L7_candidate": 7,
    "L7_confirmed": 8,
}

# Every canonical PipelineStage → its evidence level.
LEVEL_FOR_STAGE: dict[PipelineStage, EvidenceStateLevel] = {
    "warm_intro_selected": "L1",
    "message_drafted": "L2",          # prepared_not_sent
    "founder_sent_manually": "L4",    # sent
    "replied": "L4",                  # replied_interested
    "diagnostic_requested": "L4",     # meeting_booked
    "diagnostic_delivered": "L5",     # used_in_meeting
    "pilot_offered": "L6",            # scope_requested
    "commitment_received": "L7_candidate",  # invoice_sent
    "payment_received": "L7_confirmed",     # invoice_paid
    "delivery_started": "L7_confirmed",
    "delivered": "L7_confirmed",
    "proof_pack_delivered": "L7_confirmed",
    "upsell_offered": "L7_confirmed",
    "closed_won": "L7_confirmed",
    "closed_lost": "L1",              # off-path terminal — no evidence retained
}

# Every canonical PipelineStage → the strategy's event label.
STAGE_EVENT_LABEL: dict[PipelineStage, str] = {
    "warm_intro_selected": "warm_intro_selected",
    "message_drafted": "prepared_not_sent",
    "founder_sent_manually": "sent",
    "replied": "replied_interested",
    "diagnostic_requested": "meeting_booked",
    "diagnostic_delivered": "used_in_meeting",
    "pilot_offered": "scope_requested",
    "commitment_received": "invoice_sent",
    "payment_received": "invoice_paid",
    "delivery_started": "delivery_started",
    "delivered": "delivered",
    "proof_pack_delivered": "proof_pack_delivered",
    "upsell_offered": "upsell_offered",
    "closed_won": "closed_won",
    "closed_lost": "closed_lost",
}


def level_for_stage(stage: PipelineStage) -> EvidenceStateLevel:
    """Return the evidence level (L2-L7) for a pipeline stage."""
    return LEVEL_FOR_STAGE[stage]


def event_label_for_stage(stage: PipelineStage) -> str:
    """Return the strategy event label for a pipeline stage."""
    return STAGE_EVENT_LABEL[stage]


def level_rank(level: EvidenceStateLevel) -> int:
    """Numeric rank for a level (used to compare evidence depth)."""
    return LEVEL_RANK[level]


def is_l7_confirmed(stage: PipelineStage) -> bool:
    """L7 confirmed = real money landed. Delegates to ``counts_as_revenue``."""
    return counts_as_revenue(stage)


def is_l7_candidate(stage: PipelineStage) -> bool:
    """L7 candidate = a written commitment exists but payment has not landed."""
    return counts_as_commitment(stage) and not counts_as_revenue(stage)
