"""Dealix Revenue Pipeline — lightweight truth tracker.

Distinct from ``customer_loop`` (which tracks 12-state journey) and
from ``crm_v10`` (which scores leads/deals). This module enforces ONE
thing: **revenue truth labels** that cannot be silently flipped.

Canonical rule:

    REVENUE_LIVE = no_until_real_money_or_signed_commitment

A pipeline stage advances ONLY on real evidence:

- A draft Moyasar invoice is NOT revenue.
- A pilot offered is NOT revenue.
- A verbal "yes" is NOT a commitment.
- Only ``payment_received`` (Moyasar dashboard / bank statement) OR
  ``commitment_received`` (signed/written email) advances the truth.

Pure-local. NO DB. NO external call. NO LLM.
"""
from auto_client_acquisition.revenue_pipeline.revenue_truth import (
    RevenueTruthSnapshot,
    is_v12_1_unlocked,
    snapshot_revenue_truth,
)
from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    advance_stage,
    counts_as_commitment,
    counts_as_revenue,
    valid_transitions,
)

__all__ = [
    "PipelineStage",
    "RevenueTruthSnapshot",
    "advance_stage",
    "counts_as_commitment",
    "counts_as_revenue",
    "is_v12_1_unlocked",
    "snapshot_revenue_truth",
    "valid_transitions",
]
