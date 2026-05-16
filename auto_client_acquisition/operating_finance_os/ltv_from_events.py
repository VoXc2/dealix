"""LTV estimate from value ledger events (offline, source-backed)."""

from __future__ import annotations

from auto_client_acquisition.value_os.value_ledger import list_events, summarize


def estimate_ltv_sar(*, customer_id: str, period_days: int = 365) -> dict[str, float]:
    """Sum verified+ client_confirmed tiers as LTV proxy."""
    summary = summarize(customer_id=customer_id, period_days=period_days)
    ltv = float(summary.get("verified", 0)) + float(summary.get("client_confirmed", 0))
    observed = float(summary.get("observed", 0))
    return {
        "ltv_sar": ltv,
        "observed_sar": observed,
        "event_count": float(len(list_events(customer_id=customer_id, since_days=period_days))),
    }
