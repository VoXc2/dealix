"""Business Metrics Board schemas — Pydantic v2."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


class CustomerMetrics(BaseModel):
    """12 metrics per customer (Article 8: every numeric is_estimate=True).

    `confirmed_revenue_sar` reads from payment_state=payment_confirmed ONLY.
    """

    model_config = ConfigDict(extra="forbid")

    customer_handle: str = Field(..., min_length=1, max_length=64)

    # 12 canonical metrics
    confirmed_revenue_sar: float = Field(default=0.0, ge=0.0)  # ONLY payment_confirmed
    mrr_run_rate_sar: float = Field(default=0.0, ge=0.0)  # estimate
    sprint_to_partner_conversion_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    gross_margin_estimate_pct: float = Field(default=0.0, ge=-100.0, le=100.0)
    founder_hours_per_customer_estimate: float = Field(default=0.0, ge=0.0)
    churn_risk_count: int = Field(default=0, ge=0)
    proof_events_total: int = Field(default=0, ge=0)
    case_studies_published: int = Field(default=0, ge=0)
    nps_average: float | None = None  # null when insufficient data
    customer_active: bool = False
    pipeline_value_estimate_sar: float = Field(default=0.0, ge=0.0)
    zatca_invoices_drafted: int = Field(default=0, ge=0)  # NEVER auto-submitted

    # Article 8: every metric is_estimate=True except confirmed_revenue_sar
    # (which is ground truth from payment_confirmed events)
    estimate_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "confirmed_revenue_sar": False,  # ground truth
            "mrr_run_rate_sar": True,
            "sprint_to_partner_conversion_pct": True,
            "gross_margin_estimate_pct": True,
            "founder_hours_per_customer_estimate": True,
            "churn_risk_count": True,
            "proof_events_total": False,  # counted from proof_ledger
            "case_studies_published": False,
            "nps_average": True,
            "pipeline_value_estimate_sar": True,
            "zatca_invoices_drafted": False,
        }
    )
    computed_at: datetime = Field(default_factory=_now)


class PortfolioMetrics(BaseModel):
    """Aggregated metrics across all customers (founder dashboard).

    Article 8: every numeric is an aggregate of customer-level estimates.
    """

    model_config = ConfigDict(extra="forbid")

    customer_count_active: int = Field(default=0, ge=0)
    total_confirmed_revenue_sar: float = Field(default=0.0, ge=0.0)
    total_mrr_run_rate_sar: float = Field(default=0.0, ge=0.0)
    avg_gross_margin_pct: float = Field(default=0.0, ge=-100.0, le=100.0)
    total_founder_hours_estimate: float = Field(default=0.0, ge=0.0)
    portfolio_churn_risk_count: int = Field(default=0, ge=0)
    total_proof_events: int = Field(default=0, ge=0)
    total_case_studies_published: int = Field(default=0, ge=0)
    portfolio_nps_average: float | None = None
    total_pipeline_value_estimate_sar: float = Field(default=0.0, ge=0.0)
    total_zatca_invoices_drafted: int = Field(default=0, ge=0)
    article_13_trigger_status: str = "not_yet"  # 'fired' when ≥3 paid Sprints
    is_estimate: bool = True
    computed_at: datetime = Field(default_factory=_now)
