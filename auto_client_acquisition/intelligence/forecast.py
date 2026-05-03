"""
Forecast — Phase 5 light: linear pipeline + MRR projection.

Pure-computation. No LLM. Inputs:
  - active_prospects: list of ProspectRecord-like (.expected_value_sar, .status)
  - past_30d_events: list of ProofEventRecord-like (for win-rate calculation)
  - active_subscriptions: list of SubscriptionRecord-like (.mrr_sar, .status)
  - horizon_days: int (default 30)

Output: dict with pipeline_value, expected_close_rate, projected_revenue,
current_mrr, projected_mrr_at_horizon, confidence_ar.
"""

from __future__ import annotations

from typing import Any


# Stages we treat as "active pipeline" — these contribute to the forecast.
_ACTIVE_STAGES = {
    "qualified", "messaged", "replied", "diagnostic_sent",
    "meeting_booked", "pilot_offered", "invoice_sent",
}

# Default close rate when sample too small. From real Saudi B2B benchmarks
# (LinkedIn warm reply 7-10% × meeting 30% × close 40% ≈ 1-1.2% lead-to-close).
_DEFAULT_CLOSE_RATE = 0.05  # conservative until real data accumulates


def _close_rate_from_events(events: list, *, min_sample: int = 30) -> tuple[float, str]:
    """Compute close rate from ProofEventRecord history.
    Returns (rate, confidence_ar).
    """
    rows = list(events or [])
    closed_won = sum(1 for e in rows if getattr(e, "unit_type", "") == "meeting_closed")
    invoiced = sum(1 for e in rows
                   if getattr(e, "unit_type", "") == "payment_link_drafted")
    if invoiced + closed_won < min_sample:
        return _DEFAULT_CLOSE_RATE, (
            f"low (sample {invoiced + closed_won} < {min_sample} — using "
            f"conservative default {_DEFAULT_CLOSE_RATE:.0%})"
        )
    rate = closed_won / max(1, invoiced + closed_won)
    if rate <= 0.0:
        rate = _DEFAULT_CLOSE_RATE
    confidence = "medium" if invoiced + closed_won < 100 else "high"
    return rate, f"{confidence} (sample n={invoiced + closed_won})"


def project(
    active_prospects: list | None = None,
    past_events: list | None = None,
    active_subscriptions: list | None = None,
    horizon_days: int = 30,
) -> dict[str, Any]:
    prospects = list(active_prospects or [])
    events = list(past_events or [])
    subs = list(active_subscriptions or [])

    pipeline_total = sum(
        float(getattr(p, "expected_value_sar", 0) or 0)
        for p in prospects
        if getattr(p, "status", None) in _ACTIVE_STAGES
    )
    pipeline_count = sum(
        1 for p in prospects
        if getattr(p, "status", None) in _ACTIVE_STAGES
    )

    rate, rate_conf = _close_rate_from_events(events)
    projected_revenue = round(pipeline_total * rate, 2)

    current_mrr = sum(
        float(getattr(s, "mrr_sar", 0) or 0)
        for s in subs
        if getattr(s, "status", "") == "active"
    )
    # Linear projection — extrapolate one-time pilot conversions to MRR
    # equivalents using the standard upgrade factor (30% of pilots → Growth OS
    # at 2999 SAR/month = ~6× the one-time pilot value over 6 months).
    upgrade_factor = 0.30
    avg_growth_os = 2999.0  # Saudi Growth OS price
    projected_new_mrr = projected_revenue * upgrade_factor * (avg_growth_os / 499.0) / 6.0
    projected_mrr_at_horizon = round(current_mrr + projected_new_mrr, 2)

    return {
        "as_of_horizon_days": horizon_days,
        "pipeline_count": pipeline_count,
        "pipeline_value_sar": round(pipeline_total, 2),
        "expected_close_rate": round(rate, 4),
        "expected_close_rate_confidence_ar": rate_conf,
        "projected_revenue_sar": projected_revenue,
        "current_mrr_sar": round(current_mrr, 2),
        "current_arr_sar": round(current_mrr * 12, 2),
        "projected_mrr_at_horizon_sar": projected_mrr_at_horizon,
        "projected_arr_at_horizon_sar": round(projected_mrr_at_horizon * 12, 2),
        "method": "linear_pipeline_projection_v1",
        "note_ar": (
            "ملاحظة: التوقع خطي بسيط. الدقة تتحسن بعد ٩٠ يوم بيانات. "
            "Phase 5 الكامل (Bayesian + sector benchmarks) يتفعّل عند ٥ retainers."
        ),
    }
