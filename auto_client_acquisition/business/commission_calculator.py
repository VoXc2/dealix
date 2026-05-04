"""
Commission calculator for partners.

Two commission models supported:

1. **Recurring (mrr_share_pct)** — partner earns X% of customer's MRR
   every month while subscription is active. Default model.

2. **One-time (setup_fee_sar)** — partner earns a fixed SAR amount at
   activation. Stacks with recurring.

Inputs:
    - PartnerRecord-like (with mrr_share_pct, setup_fee_sar)
    - SubscriptionRecord-like rows attributed to that partner
    - Optionally PaymentRecord-like rows for actual paid commissions

Outputs are pure data (no I/O).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol


class _PartnerLike(Protocol):
    id: str
    mrr_share_pct: float
    setup_fee_sar: float


class _SubscriptionLike(Protocol):
    id: str
    status: str
    mrr_sar: float
    partner_id: str | None


class _PaymentLike(Protocol):
    amount_sar: float
    status: str
    partner_id: str | None
    subscription_id: str | None


# Commission only earned while subscription is in good standing.
COMMISSIONABLE_STATUSES: frozenset[str] = frozenset({"active"})

# Payments that count toward commission ledger (not refunds).
COMMISSIONABLE_PAYMENT_STATUSES: frozenset[str] = frozenset({"paid"})


def expected_monthly_commission(
    partner: _PartnerLike,
    subscriptions: Iterable[_SubscriptionLike],
) -> float:
    """Return SAR expected per month from active referrals.

    expected = sum(mrr_sar) * (mrr_share_pct / 100)
    """
    pct = float(partner.mrr_share_pct or 0.0) / 100.0
    if pct <= 0.0:
        return 0.0
    eligible = [
        s for s in subscriptions
        if (s.partner_id == partner.id and s.status in COMMISSIONABLE_STATUSES)
    ]
    base = sum(float(s.mrr_sar or 0.0) for s in eligible)
    return round(base * pct, 2)


def commission_from_payments(
    partner: _PartnerLike,
    payments: Iterable[_PaymentLike],
) -> float:
    """Return SAR earned to-date from actual paid invoices for this partner."""
    pct = float(partner.mrr_share_pct or 0.0) / 100.0
    if pct <= 0.0:
        return 0.0
    eligible = [
        p for p in payments
        if (p.partner_id == partner.id and p.status in COMMISSIONABLE_PAYMENT_STATUSES)
    ]
    base = sum(float(p.amount_sar or 0.0) for p in eligible)
    return round(base * pct, 2)


def setup_bonus(
    partner: _PartnerLike,
    new_subscription_count: int,
) -> float:
    """Return total setup-fee bonuses for newly-activated subs in a period."""
    fee = float(partner.setup_fee_sar or 0.0)
    if fee <= 0.0 or new_subscription_count <= 0:
        return 0.0
    return round(fee * new_subscription_count, 2)


def partner_scorecard(
    partner: _PartnerLike,
    subscriptions: Iterable[_SubscriptionLike],
    payments: Iterable[_PaymentLike],
    *,
    new_subs_this_month: int = 0,
) -> dict[str, float | int | str]:
    """Return a complete commission snapshot for the partner dashboard."""
    subs = list(subscriptions)
    pays = list(payments)
    eligible_subs = [s for s in subs if s.partner_id == partner.id]
    active_subs = [s for s in eligible_subs if s.status in COMMISSIONABLE_STATUSES]
    return {
        "partner_id": partner.id,
        "mrr_share_pct": float(partner.mrr_share_pct or 0.0),
        "setup_fee_sar": float(partner.setup_fee_sar or 0.0),
        "active_referrals": len(active_subs),
        "total_referrals": len(eligible_subs),
        "expected_monthly_commission_sar": expected_monthly_commission(partner, active_subs),
        "earned_to_date_sar": commission_from_payments(partner, pays),
        "setup_bonus_this_month_sar": setup_bonus(partner, new_subs_this_month),
    }
