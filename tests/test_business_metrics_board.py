"""Wave 13 Phase 11 — Business Metrics Board tests.

Asserts:
  - 12 metrics computable
  - confirmed_revenue_sar reads ONLY from payment_confirmed (Article 8)
  - invoice_intent_total_sar EXPLICITLY DROPPED — does NOT contribute
  - is_estimate flags correct (confirmed_revenue=False, mrr=True, etc.)
  - sprint_to_partner_conversion_pct correct math
  - gross_margin formula
  - portfolio aggregation correct
  - article_13 trigger fires at 3 paid + 1 partner
  - NPS handles None gracefully
  - tenant respected (one customer's metrics don't leak)

Sandbox-safe: direct module load.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load(rel: str, name: str):
    repo_root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(name, repo_root / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_SCH = _load("auto_client_acquisition/business_metrics_board/schemas.py",
             "_test_w13_p11_bmb_schemas")
sys.modules["auto_client_acquisition.business_metrics_board.schemas"] = _SCH

_COMP = _load("auto_client_acquisition/business_metrics_board/computer.py",
              "_test_w13_p11_bmb_computer")
_PORT = _load("auto_client_acquisition/business_metrics_board/portfolio_view.py",
              "_test_w13_p11_bmb_portfolio")

CustomerMetrics = _SCH.CustomerMetrics
PortfolioMetrics = _SCH.PortfolioMetrics
compute_customer_metrics = _COMP.compute_customer_metrics
compute_portfolio_metrics = _PORT.compute_portfolio_metrics


# ── Test 1 ────────────────────────────────────────────────────────────
def test_12_customer_metrics_present():
    cm = compute_customer_metrics(customer_handle="acme")
    d = cm.model_dump()
    expected_metrics = {
        "confirmed_revenue_sar",
        "mrr_run_rate_sar",
        "sprint_to_partner_conversion_pct",
        "gross_margin_estimate_pct",
        "founder_hours_per_customer_estimate",
        "churn_risk_count",
        "proof_events_total",
        "case_studies_published",
        "nps_average",
        "customer_active",
        "pipeline_value_estimate_sar",
        "zatca_invoices_drafted",
    }
    for m in expected_metrics:
        assert m in d, f"missing metric: {m}"


# ── Test 2 ────────────────────────────────────────────────────────────
def test_confirmed_revenue_only_from_payment_confirmed():
    """Article 8: confirmed_revenue reads ONLY from payment_confirmed."""
    cm = compute_customer_metrics(
        customer_handle="acme",
        payment_confirmed_total_sar=499.0,
        invoice_intent_total_sar=2999.0,  # NOT counted
    )
    assert cm.confirmed_revenue_sar == 499.0  # only confirmed
    # invoice_intent dropped completely
    d = cm.model_dump()
    assert "invoice_intent_total_sar" not in d


# ── Test 3 ────────────────────────────────────────────────────────────
def test_invoice_intent_zero_revenue():
    """Even with massive invoice_intent, confirmed_revenue stays 0 if no payment."""
    cm = compute_customer_metrics(
        customer_handle="acme",
        payment_confirmed_total_sar=0.0,
        invoice_intent_total_sar=100_000.0,  # invoice but no payment
    )
    assert cm.confirmed_revenue_sar == 0.0
    assert cm.gross_margin_estimate_pct == 0.0


# ── Test 4 ────────────────────────────────────────────────────────────
def test_estimate_flags_correct():
    """Article 8: confirmed_revenue=False (ground truth);
    mrr/conversion/margin/founder_hours/churn/nps/pipeline=True (estimates)."""
    cm = compute_customer_metrics(customer_handle="acme")
    flags = cm.estimate_flags
    # Ground truth (NOT estimate)
    assert flags["confirmed_revenue_sar"] is False
    assert flags["proof_events_total"] is False
    assert flags["case_studies_published"] is False
    assert flags["zatca_invoices_drafted"] is False
    # Estimates
    assert flags["mrr_run_rate_sar"] is True
    assert flags["sprint_to_partner_conversion_pct"] is True
    assert flags["gross_margin_estimate_pct"] is True
    assert flags["founder_hours_per_customer_estimate"] is True
    assert flags["churn_risk_count"] is True
    assert flags["nps_average"] is True
    assert flags["pipeline_value_estimate_sar"] is True


# ── Test 5 ────────────────────────────────────────────────────────────
def test_sprint_to_partner_conversion_pct():
    cm = compute_customer_metrics(
        customer_handle="acme",
        sprint_count=10,
        partner_conversions=8,
    )
    assert cm.sprint_to_partner_conversion_pct == 80.0

    # Edge: 0 sprints → 0%
    cm0 = compute_customer_metrics(customer_handle="x", sprint_count=0, partner_conversions=0)
    assert cm0.sprint_to_partner_conversion_pct == 0.0


# ── Test 6 ────────────────────────────────────────────────────────────
def test_gross_margin_formula():
    cm = compute_customer_metrics(
        customer_handle="acme",
        payment_confirmed_total_sar=1000.0,
        estimated_direct_cost_sar=300.0,
    )
    # (1000-300)/1000 = 70%
    assert cm.gross_margin_estimate_pct == 70.0


# ── Test 7 ────────────────────────────────────────────────────────────
def test_nps_handles_none():
    cm_no_nps = compute_customer_metrics(customer_handle="acme", nps_responses=None)
    assert cm_no_nps.nps_average is None
    cm_with_nps = compute_customer_metrics(customer_handle="acme", nps_responses=[8, 9, 7, 10])
    assert cm_with_nps.nps_average == 8.5


# ── Test 8 ────────────────────────────────────────────────────────────
def test_portfolio_aggregation():
    c1 = compute_customer_metrics(
        customer_handle="acme",
        payment_confirmed_total_sar=499.0,
        customer_active=True,
        proof_events_total=3,
    )
    c2 = compute_customer_metrics(
        customer_handle="bravo",
        payment_confirmed_total_sar=2999.0,
        customer_active=True,
        proof_events_total=5,
    )
    p = compute_portfolio_metrics([c1, c2])
    assert p.customer_count_active == 2
    assert p.total_confirmed_revenue_sar == 499.0 + 2999.0
    assert p.total_proof_events == 8


# ── Test 9 ────────────────────────────────────────────────────────────
def test_article_13_trigger_fires_at_3_paid_plus_1_partner():
    """Per plan §31.1: 3 paid Sprints + 1 Partner upsell + synthesis written."""
    p_not_yet = compute_portfolio_metrics(
        [], confirmed_paid_sprint_customers=2, portfolio_partner_conversions=0,
    )
    assert p_not_yet.article_13_trigger_status == "not_yet"

    p_partial = compute_portfolio_metrics(
        [], confirmed_paid_sprint_customers=3, portfolio_partner_conversions=0,
    )
    assert p_partial.article_13_trigger_status == "not_yet"  # missing partner

    p_fired = compute_portfolio_metrics(
        [], confirmed_paid_sprint_customers=3, portfolio_partner_conversions=1,
    )
    assert p_fired.article_13_trigger_status == "fired"


# ── Test 10 ───────────────────────────────────────────────────────────
def test_tenant_respected_in_per_customer():
    """Calling computer for one handle never returns another handle's data."""
    cm_a = compute_customer_metrics(
        customer_handle="acme", payment_confirmed_total_sar=499.0,
    )
    cm_b = compute_customer_metrics(
        customer_handle="bravo", payment_confirmed_total_sar=999.0,
    )
    assert cm_a.customer_handle == "acme"
    assert cm_a.confirmed_revenue_sar == 499.0
    assert cm_b.customer_handle == "bravo"
    assert cm_b.confirmed_revenue_sar == 999.0
    # No bleed-through
    assert cm_a.customer_handle != cm_b.customer_handle
