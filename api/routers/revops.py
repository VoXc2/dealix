"""RevOps API — finance brief + revenue truth (read-only)."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.revops import (
    MarginInputs,
    build_finance_brief,
    build_revops_truth_snapshot,
    estimate_margin,
)
from auto_client_acquisition.revops.pipeline import pipeline_aggregate
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline

router = APIRouter(prefix="/api/v1/revops", tags=["revops"])

_HARD_GATES = {
    "no_live_charge": True,
    "draft_invoice_not_revenue": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def revops_status() -> dict[str, Any]:
    return {
        "service": "revops",
        "module": "revops",
        "status": "operational",
        "version": "v12_5",
        "hard_gates": _HARD_GATES,
        "next_action_ar": "افتح finance-brief للملخص اليومي",
        "next_action_en": "Open finance-brief for the daily snapshot.",
    }


@router.get("/finance-brief")
async def finance_brief(
    delivery_hours_month: float = 0.0,
    support_hours_month: float = 0.0,
    refund_risk_factor: float = 0.0,
) -> dict[str, Any]:
    brief = build_finance_brief(
        delivery_hours_month=delivery_hours_month,
        support_hours_month=support_hours_month,
        refund_risk_factor=refund_risk_factor,
    )
    brief["hard_gates"] = {**brief.get("hard_gates", {}), **_HARD_GATES}
    return brief


@router.get("/truth")
async def revops_truth() -> dict[str, Any]:
    pipe = get_default_pipeline()
    snap = build_revops_truth_snapshot(pipe.summary())
    return {"schema_version": 1, "revops_truth": snap, "hard_gates": _HARD_GATES}


@router.get("/pipeline-aggregate")
async def revops_pipeline() -> dict[str, Any]:
    return pipeline_aggregate()


@router.get("/margin-estimate")
async def margin_estimate(
    revenue_sar: int = 0,
    delivery_hours: float = 0.0,
    support_hours: float = 0.0,
    refund_risk_factor: float = 0.0,
) -> dict[str, Any]:
    return estimate_margin(
        MarginInputs(
            revenue_sar=revenue_sar,
            delivery_hours=delivery_hours,
            support_hours=support_hours,
            refund_risk_factor=refund_risk_factor,
        )
    )
