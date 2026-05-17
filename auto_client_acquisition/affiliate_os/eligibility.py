"""Commission eligibility gate — Full Ops spec §8 ("لا تدفع على").

A commission is payable ONLY when:
  1. the deal invoice status is ``paid`` (not draft/sent/voided/refunded), and
  2. the originating lead carries none of the disallowed flags.

This module is pure logic. The InvoiceStatus vocabulary mirrors
``auto_client_acquisition/revops/invoice_state.py``.
"""
from __future__ import annotations

from collections.abc import Iterable

# Lead flags that disqualify a commission outright (spec §8).
DISALLOWED_LEAD_FLAGS: frozenset[str] = frozenset(
    {
        "traffic_only",
        "unqualified",
        "duplicate",
        "student_or_job_seeker",
        "no_consent",
        "out_of_icp",
        "no_pain_or_budget",
        "self_referral",
    }
)


def commission_eligible(
    *,
    invoice_status: str,
    lead_flags: Iterable[str] = (),
) -> tuple[bool, tuple[str, ...]]:
    """Return ``(eligible, reasons)``.

    ``reasons`` is empty when eligible; otherwise it lists every blocker
    so the founder sees exactly why a payout cannot proceed.
    """
    reasons: list[str] = []
    if invoice_status != "paid":
        reasons.append(f"invoice_not_paid:{invoice_status or 'unknown'}")
    bad = sorted(set(lead_flags) & DISALLOWED_LEAD_FLAGS)
    reasons.extend(f"disallowed_lead:{flag}" for flag in bad)
    return (not reasons, tuple(reasons))


def is_disqualifying(lead_flags: Iterable[str]) -> bool:
    """True if the lead is permanently disqualified (not just unpaid)."""
    return bool(set(lead_flags) & DISALLOWED_LEAD_FLAGS)


__all__ = ["DISALLOWED_LEAD_FLAGS", "commission_eligible", "is_disqualifying"]
