"""Pipeline aggregate view for RevOps (uses default in-memory pipeline)."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    counts_as_commitment,
    counts_as_revenue,
)


def pipeline_aggregate() -> dict[str, Any]:
    """Counts leads by coarse buckets for finance/margin estimates."""
    pipe = get_default_pipeline()
    leads = pipe.list_all()
    by_stage: dict[str, int] = {}
    for lead in leads:
        st = str(lead.stage)
        by_stage[st] = by_stage.get(st, 0) + 1

    commitment_like = sum(1 for L in leads if counts_as_commitment(L.stage))
    revenue_like = sum(1 for L in leads if counts_as_revenue(L.stage))

    return {
        "schema_version": 1,
        "total_leads": len(leads),
        "stages": by_stage,
        "commitment_like_count": commitment_like,
        "revenue_like_count": revenue_like,
        "terminal_stages": ["closed_won", "closed_lost"],
    }


def list_open_stages() -> list[PipelineStage]:
    """Stages considered 'open' before closed_won/lost (for ops dashboards)."""
    return [
        "warm_intro_selected",
        "message_drafted",
        "founder_sent_manually",
        "replied",
        "diagnostic_requested",
        "diagnostic_delivered",
        "pilot_offered",
        "commitment_received",
        "payment_received",
        "delivery_started",
        "delivered",
        "proof_pack_delivered",
        "upsell_offered",
    ]
