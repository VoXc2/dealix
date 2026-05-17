"""Commission clawback — Full Ops spec §8.

"clawback if refund within 30 days" — if a deal invoice is refunded
inside the clawback window, an already-computed commission is reversed.
Pure logic; no I/O.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timezone

from auto_client_acquisition.affiliate_os.commission import (
    Commission,
    CommissionStatus,
)

CLAWBACK_WINDOW_DAYS = 30


def _parse(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def should_clawback(
    *,
    invoice_status: str,
    paid_at: str = "",
    refunded_at: str = "",
    window_days: int = CLAWBACK_WINDOW_DAYS,
) -> bool:
    """Decide whether a commission must be clawed back.

    Clawback applies when the invoice is ``refunded`` and the refund
    happened within ``window_days`` of payment. If either timestamp is
    missing we clawback conservatively (a refund did occur).
    """
    if invoice_status != "refunded":
        return False
    paid = _parse(paid_at)
    refunded = _parse(refunded_at)
    if paid is None or refunded is None:
        return True
    return (refunded - paid).days <= window_days


def apply_clawback(commission: Commission) -> Commission:
    """Return a copy of the commission flipped to ``CLAWED_BACK``."""
    return replace(
        commission,
        status=CommissionStatus.CLAWED_BACK.value,
        updated_at=datetime.now(UTC).isoformat(),
    )


__all__ = ["CLAWBACK_WINDOW_DAYS", "apply_clawback", "should_clawback"]
