"""Business Metrics Board — portfolio-level aggregator.

Composes per-customer CustomerMetrics into one founder dashboard.
"""

from __future__ import annotations

from collections.abc import Iterable

from auto_client_acquisition.business_metrics_board.schemas import (
    CustomerMetrics,
    PortfolioMetrics,
)


def _article_13_status(
    *,
    confirmed_paid_sprint_customers: int,
    partner_conversions: int,
) -> str:
    """Return 'fired' when ≥3 paid sprints + ≥1 partner conversion (per plan §31.1)."""
    if confirmed_paid_sprint_customers >= 3 and partner_conversions >= 1:
        return "fired"
    return "not_yet"


def compute_portfolio_metrics(
    customers: Iterable[CustomerMetrics],
    *,
    confirmed_paid_sprint_customers: int = 0,
    portfolio_partner_conversions: int = 0,
) -> PortfolioMetrics:
    """Aggregate a list of CustomerMetrics into one PortfolioMetrics.

    Article 8: total_confirmed_revenue_sar reads ONLY confirmed customer
    revenue (which itself is gated on payment_confirmed in computer.py).
    """
    customer_list = list(customers)

    customer_count_active = sum(1 for c in customer_list if c.customer_active)
    total_revenue = sum(c.confirmed_revenue_sar for c in customer_list)
    total_mrr = sum(c.mrr_run_rate_sar for c in customer_list)

    # Average gross margin — only across customers with revenue
    margins = [c.gross_margin_estimate_pct for c in customer_list if c.confirmed_revenue_sar > 0]
    avg_margin = sum(margins) / len(margins) if margins else 0.0

    total_founder_hours = sum(c.founder_hours_per_customer_estimate for c in customer_list)
    total_churn_risk = sum(c.churn_risk_count for c in customer_list)
    total_proof = sum(c.proof_events_total for c in customer_list)
    total_case_studies = sum(c.case_studies_published for c in customer_list)
    total_pipeline = sum(c.pipeline_value_estimate_sar for c in customer_list)
    total_zatca = sum(c.zatca_invoices_drafted for c in customer_list)

    # Portfolio NPS — average of customer NPS where available
    nps_values = [c.nps_average for c in customer_list if c.nps_average is not None]
    portfolio_nps = sum(nps_values) / len(nps_values) if nps_values else None

    return PortfolioMetrics(
        customer_count_active=customer_count_active,
        total_confirmed_revenue_sar=total_revenue,
        total_mrr_run_rate_sar=total_mrr,
        avg_gross_margin_pct=avg_margin,
        total_founder_hours_estimate=total_founder_hours,
        portfolio_churn_risk_count=total_churn_risk,
        total_proof_events=total_proof,
        total_case_studies_published=total_case_studies,
        portfolio_nps_average=portfolio_nps,
        total_pipeline_value_estimate_sar=total_pipeline,
        total_zatca_invoices_drafted=total_zatca,
        article_13_trigger_status=_article_13_status(
            confirmed_paid_sprint_customers=confirmed_paid_sprint_customers,
            partner_conversions=portfolio_partner_conversions,
        ),
        is_estimate=True,
    )
