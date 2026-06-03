"""Revenue truth: what counts as revenue, what doesn't.

Hard rule (Article 8 NO_FAKE_REVENUE):
  invoice_intent          ≠ revenue
  invoice_sent_manual     ≠ revenue
  payment_pending         ≠ revenue
  payment_evidence_uploaded → POSSIBLE revenue (not yet)
  payment_confirmed       = REVENUE
  delivery_kickoff        = revenue (downstream)
  refunded                = NEGATIVE revenue
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call

_REVENUE_STATUSES = {"payment_confirmed", "delivery_kickoff"}
_NEGATIVE_STATUSES = {"refunded"}


def is_revenue(payment_status: str) -> bool:
    """Returns True only if status is in the strict revenue set."""
    return payment_status in _REVENUE_STATUSES


def revenue_summary(*, customer_handle: str | None = None) -> dict[str, Any]:
    """Returns truthful revenue summary across all payments (or one customer)."""
    return safe_call(
        name="revenue_summary",
        fn=lambda: _compute_summary(customer_handle),
        fallback={
            "confirmed_revenue_sar": 0.0,
            "refunded_sar": 0.0,
            "net_revenue_sar": 0.0,
            "confirmed_count": 0,
            "is_estimate": False,
            "source": "insufficient_data",
        },
    )


def _compute_summary(customer_handle: str | None) -> dict[str, Any]:
    from auto_client_acquisition.payment_ops.orchestrator import _INDEX
    payments = list(_INDEX.values())
    if customer_handle:
        payments = [p for p in payments if p.customer_handle == customer_handle]

    confirmed = [p for p in payments if is_revenue(p.status)]
    refunded = [p for p in payments if p.status in _NEGATIVE_STATUSES]

    confirmed_total = sum(p.amount_sar for p in confirmed)
    refunded_total = sum(p.amount_sar for p in refunded)

    return {
        "confirmed_revenue_sar": round(confirmed_total, 2),
        "refunded_sar": round(refunded_total, 2),
        "net_revenue_sar": round(confirmed_total - refunded_total, 2),
        "confirmed_count": len(confirmed),
        "refunded_count": len(refunded),
        "by_status_count": _count_by_status(payments),
        "is_estimate": False,  # this is real ground truth
        "source": "payment_ops.orchestrator",
    }


def _count_by_status(payments: list[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in payments:
        counts[p.status] = counts.get(p.status, 0) + 1
    return counts
