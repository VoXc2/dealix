"""Wave 13 Phase 11 — Business Metrics Board HTTP surface.

- GET /api/v1/metrics/status
- POST /api/v1/metrics/customer/{customer_handle}  → 12 metrics
- POST /api/v1/metrics/portfolio                    → aggregated

Both endpoints accept inputs as POST body (so caller composes from
their CRM/payment_ops/proof_ledger before passing to us).

Article 4: read-only; tenant-isolated for {customer_handle}.
Article 8: every numeric is_estimate=True except confirmed_revenue
(ground truth from payment_confirmed).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.business_metrics_board import (
    compute_customer_metrics,
    compute_portfolio_metrics,
)
from auto_client_acquisition.business_metrics_board.schemas import CustomerMetrics

router = APIRouter(prefix="/api/v1/metrics", tags=["Business Metrics Board"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "confirmed_revenue_only_from_payment_confirmed": True,
    "every_numeric_is_estimate_except_confirmed_revenue": True,
}


class CustomerMetricsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    payment_confirmed_total_sar: float = Field(0.0, ge=0.0)
    invoice_intent_total_sar: float = Field(0.0, ge=0.0)
    monthly_recurring_estimate_sar: float = Field(0.0, ge=0.0)
    sprint_count: int = Field(0, ge=0)
    partner_conversions: int = Field(0, ge=0)
    estimated_founder_hours: float = Field(0.0, ge=0.0)
    estimated_direct_cost_sar: float = Field(0.0, ge=0.0)
    churn_risk_count: int = Field(0, ge=0)
    proof_events_total: int = Field(0, ge=0)
    case_studies_published: int = Field(0, ge=0)
    nps_responses: list[int] | None = None
    customer_active: bool = False
    pipeline_estimate_sar: float = Field(0.0, ge=0.0)
    zatca_invoices_drafted: int = Field(0, ge=0)


class PortfolioMetricsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customers: list[CustomerMetrics] = Field(default_factory=list)
    confirmed_paid_sprint_customers: int = Field(0, ge=0)
    portfolio_partner_conversions: int = Field(0, ge=0)


@router.get("/status")
async def metrics_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "wave": "wave13_phase_11_business_metrics_board",
        "metrics_count": 12,
        "hard_gates": _HARD_GATES,
    }


@router.post("/customer/{customer_handle}")
async def customer_metrics_endpoint(
    customer_handle: str,
    req: CustomerMetricsRequest,
) -> dict[str, Any]:
    metrics = compute_customer_metrics(
        customer_handle=customer_handle,
        payment_confirmed_total_sar=req.payment_confirmed_total_sar,
        invoice_intent_total_sar=req.invoice_intent_total_sar,
        monthly_recurring_estimate_sar=req.monthly_recurring_estimate_sar,
        sprint_count=req.sprint_count,
        partner_conversions=req.partner_conversions,
        estimated_founder_hours=req.estimated_founder_hours,
        estimated_direct_cost_sar=req.estimated_direct_cost_sar,
        churn_risk_count=req.churn_risk_count,
        proof_events_total=req.proof_events_total,
        case_studies_published=req.case_studies_published,
        nps_responses=req.nps_responses,
        customer_active=req.customer_active,
        pipeline_estimate_sar=req.pipeline_estimate_sar,
        zatca_invoices_drafted=req.zatca_invoices_drafted,
    )
    return {
        "metrics": metrics.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/portfolio")
async def portfolio_metrics_endpoint(req: PortfolioMetricsRequest) -> dict[str, Any]:
    portfolio = compute_portfolio_metrics(
        req.customers,
        confirmed_paid_sprint_customers=req.confirmed_paid_sprint_customers,
        portfolio_partner_conversions=req.portfolio_partner_conversions,
    )
    return {
        "portfolio": portfolio.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }
