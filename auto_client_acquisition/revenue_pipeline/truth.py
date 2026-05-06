"""Stages and revenue truth — educational defaults for API snapshot."""

from __future__ import annotations

from typing import Any

STAGES: tuple[str, ...] = (
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
    "closed_won",
    "closed_lost",
)


def pipeline_summary() -> dict[str, Any]:
    return {
        "stages": list(STAGES),
        "revenue_truth": {
            "revenue_requires": "payment_received OR written_commitment_received (documented)",
            "not_revenue": ["diagnostic_delivered", "pilot_offered", "draft_invoice"],
        },
        "crm_v10": "POST /api/v1/crm-v10/score-deal for deal scoring; stages in crm_v10 schemas.",
    }
