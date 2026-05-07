"""Revenue Profitability HTTP surface (Phase 6 Wave 5).

  GET  /api/v1/revenue-profitability/status
  POST /api/v1/revenue-profitability/estimate-service-margin
  GET  /api/v1/revenue-profitability/radar
  GET  /api/v1/revenue-profitability/revenue-summary
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.revenue_profitability import (
    compute_gross_margin,
    estimate_service_cost,
    finance_radar_summary,
    revenue_summary,
)

router = APIRouter(
    prefix="/api/v1/revenue-profitability",
    tags=["revenue-profitability"],
)

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "no_fake_forecast": True,
    "every_margin_is_estimate": True,
    "only_payment_confirmed_counts_as_revenue": True,
    "read_only": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "revenue_profitability",
        "version": "1.0.0",
        "supported_service_types": [
            "diagnostic", "leadops_sprint", "growth_proof_sprint",
            "support_ops_setup", "customer_portal_setup",
            "executive_pack", "proof_pack", "agency_partner_pack",
        ],
        "revenue_rule": "only_payment_confirmed_counts",
        "hard_gates": _HARD_GATES,
    }


@router.post("/estimate-service-margin")
async def estimate_margin(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    service_type = payload.get("service_type")
    revenue_sar = payload.get("revenue_sar")
    if not service_type or revenue_sar is None:
        raise HTTPException(
            status_code=422,
            detail="service_type + revenue_sar required",
        )
    try:
        revenue_float = float(revenue_sar)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="revenue_sar must be numeric")
    margin = compute_gross_margin(
        service_type=service_type, revenue_sar=revenue_float,
    )
    return {**margin, "hard_gates": _HARD_GATES}


@router.get("/radar")
async def radar() -> dict[str, Any]:
    summary = finance_radar_summary()
    return {**summary, "hard_gates": _HARD_GATES}


@router.get("/revenue-summary")
async def revenue_summary_endpoint(customer_handle: str | None = None) -> dict[str, Any]:
    summary = revenue_summary(customer_handle=customer_handle)
    return {**summary, "hard_gates": _HARD_GATES}
