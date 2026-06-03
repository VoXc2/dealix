"""Business Metrics Board — per-customer metrics composer.

Pure-fn (deterministic). Inputs come from the caller (router pulls
real data from payment_ops / proof_ledger / customer_success / etc.) —
keeps this module Article 11 thin and testable.

Hard rule (Article 8):
  - confirmed_revenue_sar reads ONLY from payment_confirmed state
  - invoice_intent_state DOES NOT count as revenue
"""

from __future__ import annotations

from auto_client_acquisition.business_metrics_board.schemas import (
    CustomerMetrics,
)


def compute_customer_metrics(
    *,
    customer_handle: str,
    payment_confirmed_total_sar: float = 0.0,  # GROUND TRUTH
    invoice_intent_total_sar: float = 0.0,  # NOT revenue
    monthly_recurring_estimate_sar: float = 0.0,
    sprint_count: int = 0,
    partner_conversions: int = 0,
    estimated_founder_hours: float = 0.0,
    estimated_direct_cost_sar: float = 0.0,
    churn_risk_count: int = 0,
    proof_events_total: int = 0,
    case_studies_published: int = 0,
    nps_responses: list[int] | None = None,
    customer_active: bool = False,
    pipeline_estimate_sar: float = 0.0,
    zatca_invoices_drafted: int = 0,
) -> CustomerMetrics:
    """Compose 12 metrics for one customer.

    Article 8 invariants:
      - confirmed_revenue_sar = payment_confirmed_total_sar ONLY
      - invoice_intent_total_sar EXPLICITLY DROPPED — does not contribute
      - gross_margin = (revenue - direct_cost) / revenue (0 if no revenue)
      - sprint_to_partner_conversion = partner_conversions / sprint_count
    """
    # Sprint-to-partner conversion %
    if sprint_count > 0:
        conv_pct = min(100.0, (partner_conversions / sprint_count) * 100.0)
    else:
        conv_pct = 0.0

    # Gross margin estimate (only meaningful if revenue exists)
    if payment_confirmed_total_sar > 0:
        margin_pct = (
            (payment_confirmed_total_sar - estimated_direct_cost_sar)
            / payment_confirmed_total_sar
        ) * 100.0
        margin_pct = max(-100.0, min(100.0, margin_pct))
    else:
        margin_pct = 0.0

    # NPS average (None when insufficient data)
    nps_avg: float | None = None
    if nps_responses and len(nps_responses) >= 1:
        nps_avg = sum(nps_responses) / len(nps_responses)

    return CustomerMetrics(
        customer_handle=customer_handle,
        confirmed_revenue_sar=float(payment_confirmed_total_sar),  # ground truth
        mrr_run_rate_sar=float(monthly_recurring_estimate_sar),
        sprint_to_partner_conversion_pct=float(conv_pct),
        gross_margin_estimate_pct=float(margin_pct),
        founder_hours_per_customer_estimate=float(estimated_founder_hours),
        churn_risk_count=int(churn_risk_count),
        proof_events_total=int(proof_events_total),
        case_studies_published=int(case_studies_published),
        nps_average=nps_avg,
        customer_active=bool(customer_active),
        pipeline_value_estimate_sar=float(pipeline_estimate_sar),
        zatca_invoices_drafted=int(zatca_invoices_drafted),
    )
