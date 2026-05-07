"""Revenue Profitability + Gross Margin Radar (Phase 6 Wave 5).

Reads payment_ops + service_sessions to compute per-service gross
margin estimates. Every margin field is marked is_estimate=True
(Article 8 — no fake revenue).

Hard rule:
  invoice_intent          ≠ revenue
  invoice_sent_manual     ≠ revenue
  payment_evidence_uploaded → possible revenue (not yet)
  payment_confirmed       = revenue
"""
from auto_client_acquisition.revenue_profitability.gross_margin import (
    compute_gross_margin,
)
from auto_client_acquisition.revenue_profitability.finance_radar import (
    finance_radar_summary,
)
from auto_client_acquisition.revenue_profitability.revenue_truth import (
    is_revenue,
    revenue_summary,
)
from auto_client_acquisition.revenue_profitability.service_cost import (
    estimate_service_cost,
)

__all__ = [
    "compute_gross_margin",
    "estimate_service_cost",
    "finance_radar_summary",
    "is_revenue",
    "revenue_summary",
]
