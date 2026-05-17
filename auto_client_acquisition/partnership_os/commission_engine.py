"""Commission calculation + clawback — the affiliate machine money core.

Hard money doctrine (playbook section B.1), enforced here so no caller
can bypass it:

  - a commission line is created ONLY after the deal invoice is paid;
  - clawback applies if the customer is refunded within 30 days of the
    invoice being paid;
  - no commission on self-referrals, unqualified, duplicate,
    out-of-ICP or consent-less referrals.

Pure functions over plain dicts/dataclasses — the router persists the
result. No I/O here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from auto_client_acquisition.partnership_os.tiers import get_tier

CLAWBACK_WINDOW_DAYS = 30


class CommissionRefused(Exception):
    """Raised when a commission cannot be created under doctrine."""


@dataclass(slots=True)
class CommissionLine:
    """A calculated commission line, ready to persist."""

    id: str = field(default_factory=lambda: f"cmn_{uuid4().hex[:12]}")
    partner_id: str = ""
    referral_id: str = ""
    deal_id: str = ""
    tier: str = ""
    basis_amount_sar: float = 0.0
    rate: float = 0.0
    amount_sar: float = 0.0
    status: str = "eligible"
    invoice_paid_at: str = ""
    calculated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "partner_id": self.partner_id,
            "referral_id": self.referral_id,
            "deal_id": self.deal_id,
            "tier": self.tier,
            "basis_amount_sar": self.basis_amount_sar,
            "rate": self.rate,
            "amount_sar": self.amount_sar,
            "status": self.status,
            "invoice_paid_at": self.invoice_paid_at,
            "calculated_at": self.calculated_at,
        }


def _parse_dt(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str) and value.strip():
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return None


def calculate(referral: dict[str, Any], deal: dict[str, Any]) -> CommissionLine:
    """Calculate a commission line for a paid deal attributed to a referral.

    ``referral`` keys: ``id``, ``partner_id``, ``qualified``, ``stage``,
    optionally ``tier``.
    ``deal`` keys: ``id``, ``invoice_paid`` (bool), ``invoice_paid_at``,
    ``amount_sar``, optionally ``tier``, ``in_icp``, ``duplicate``.

    Raises ``CommissionRefused`` when any hard money rule fails.
    """
    if not bool(deal.get("invoice_paid")):
        raise CommissionRefused(
            "commission cannot be created before the deal invoice is paid"
        )

    if str(referral.get("stage") or "") == "rejected":
        raise CommissionRefused("referral was rejected — no commission")

    if bool(referral.get("self_referral")):
        raise CommissionRefused("self-referral — no commission")

    if bool(deal.get("duplicate")) or bool(referral.get("duplicate")):
        raise CommissionRefused("duplicate referral — no commission")

    if deal.get("in_icp") is False or referral.get("in_icp") is False:
        raise CommissionRefused("out-of-ICP lead — no commission")

    if referral.get("consent") is False:
        raise CommissionRefused("consent-less lead — no commission")

    tier_key = str(deal.get("tier") or referral.get("tier") or "")
    if not tier_key:
        raise CommissionRefused("no tier on the referral or deal")

    # Tiers 1-2 require a qualified referral; tier 1 is the lead rung and
    # also benefits from qualification, but only tier 2+ strictly demand it.
    try:
        tier = get_tier(tier_key)
    except ValueError as exc:
        raise CommissionRefused(str(exc)) from exc
    if tier.rank >= 2 and not bool(referral.get("qualified")):
        raise CommissionRefused(
            f"tier {tier.key} requires a qualified referral"
        )

    basis = float(deal.get("amount_sar") or 0.0)
    if basis <= 0:
        raise CommissionRefused("deal has no positive basis amount")

    amount = round(basis * tier.rate, 2)
    paid_at = _parse_dt(deal.get("invoice_paid_at"))

    return CommissionLine(
        partner_id=str(referral.get("partner_id") or deal.get("partner_id") or ""),
        referral_id=str(referral.get("id") or ""),
        deal_id=str(deal.get("id") or ""),
        tier=tier.key,
        basis_amount_sar=basis,
        rate=tier.rate,
        amount_sar=amount,
        status="eligible",
        invoice_paid_at=paid_at.isoformat() if paid_at else "",
    )


def within_clawback_window(
    invoice_paid_at: Any, refund_date: Any
) -> bool:
    """True when ``refund_date`` is within ``CLAWBACK_WINDOW_DAYS`` of payment."""
    paid = _parse_dt(invoice_paid_at)
    refunded = _parse_dt(refund_date)
    if paid is None or refunded is None:
        return False
    return paid <= refunded <= paid + timedelta(days=CLAWBACK_WINDOW_DAYS)


def clawback(commission: dict[str, Any], refund_date: Any) -> dict[str, Any]:
    """Apply a refund clawback to a commission record.

    Returns a patch dict for the commission. If the refund falls within
    the clawback window the commission is voided (``clawed_back``,
    amount zeroed); otherwise the commission stands.
    """
    paid_at = commission.get("invoice_paid_at")
    if within_clawback_window(paid_at, refund_date):
        return {
            "status": "clawed_back",
            "amount_sar": 0.0,
            "clawed_back": True,
            "reason": f"refund within {CLAWBACK_WINDOW_DAYS}-day window",
        }
    return {
        "status": commission.get("status", "eligible"),
        "amount_sar": float(commission.get("amount_sar") or 0.0),
        "clawed_back": False,
        "reason": f"refund outside {CLAWBACK_WINDOW_DAYS}-day window — commission stands",
    }


__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "CommissionLine",
    "CommissionRefused",
    "calculate",
    "clawback",
    "within_clawback_window",
]
