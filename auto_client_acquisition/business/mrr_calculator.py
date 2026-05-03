"""
MRR (Monthly Recurring Revenue) calculator.

Aggregates active subscriptions to compute MRR per partner / globally / per
sector. Pure data — no I/O. Pass in a list of SubscriptionRecord-like
objects (anything with .status, .mrr_sar, .partner_id).

Usage:
    rows = [...]  # list of SubscriptionRecord
    total = total_mrr(rows)                # SAR
    per_partner = mrr_by_partner(rows)     # {partner_id: SAR}
    arr = annualize(total)                 # ARR = MRR * 12
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Protocol


class _SubscriptionLike(Protocol):
    status: str
    mrr_sar: float
    partner_id: str | None


# Statuses that count toward MRR. "trialing" is borderline — we exclude
# it from MRR but include in pipeline forecasts elsewhere.
ACTIVE_STATUSES: frozenset[str] = frozenset({"active", "past_due"})


def total_mrr(subscriptions: Iterable[_SubscriptionLike]) -> float:
    """Sum mrr_sar across all active subscriptions."""
    return round(
        sum(float(s.mrr_sar or 0.0) for s in subscriptions if s.status in ACTIVE_STATUSES),
        2,
    )


def mrr_by_partner(subscriptions: Iterable[_SubscriptionLike]) -> dict[str, float]:
    """Return {partner_id: mrr_sar}. Subscriptions without partner are bucketed under '_direct'."""
    out: dict[str, float] = defaultdict(float)
    for s in subscriptions:
        if s.status not in ACTIVE_STATUSES:
            continue
        key = s.partner_id or "_direct"
        out[key] += float(s.mrr_sar or 0.0)
    return {k: round(v, 2) for k, v in out.items()}


def active_count(subscriptions: Iterable[_SubscriptionLike]) -> int:
    return sum(1 for s in subscriptions if s.status in ACTIVE_STATUSES)


def annualize(mrr_sar: float) -> float:
    """Return ARR = MRR × 12."""
    return round(mrr_sar * 12.0, 2)


def churn_rate(
    subscriptions: Iterable[_SubscriptionLike],
    *,
    canceled_in_period: int,
    period_active_at_start: int,
) -> float:
    """Return fractional churn for the period (0.0 to 1.0).

    Pure formula: canceled / active_at_start. `subscriptions` is unused here
    but kept for future per-partner churn extension.
    """
    _ = list(subscriptions)  # silence unused
    if period_active_at_start <= 0:
        return 0.0
    return round(canceled_in_period / period_active_at_start, 4)
