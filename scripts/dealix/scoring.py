"""Deterministic scoring for account packs.

Final Account Score =
    Account Score        * 0.30
  + Need Fit Score       * 0.30
  + Cash Priority Score  * 0.25
  + Contact Confidence   * 0.15   (confidence mapped to 0..100)

All scores are deterministic functions of the inputs so packs are reproducible
and checks can re-derive and verify them.
"""
from __future__ import annotations

CONFIDENCE_TO_SCORE = {"low": 40, "medium": 70, "high": 95}

WEIGHTS = {
    "account": 0.30,
    "need_fit": 0.30,
    "cash": 0.25,
    "contact": 0.15,
}


def need_fit_score(need_confidence, signals_count):
    base = CONFIDENCE_TO_SCORE.get(need_confidence, 40)
    bonus = min(signals_count, 4) * 5
    return round(min(100, base + bonus), 1)


def cash_priority_score(urgency, ticket_potential, speed_to_cash):
    score = urgency * 0.4 + ticket_potential * 0.3 + speed_to_cash * 0.3
    return round(min(100, max(0, score)), 1)


def account_score(sector_weight, need_fit, has_public_channel):
    score = sector_weight * 0.5 + need_fit * 0.4 + (10 if has_public_channel else 0)
    return round(min(100, max(0, score)), 1)


def final_account_score(account, need_fit, cash, contact_confidence):
    contact = CONFIDENCE_TO_SCORE.get(contact_confidence, 40)
    final = (
        account * WEIGHTS["account"]
        + need_fit * WEIGHTS["need_fit"]
        + cash * WEIGHTS["cash"]
        + contact * WEIGHTS["contact"]
    )
    return round(min(100, max(0, final)), 1)


def verify_final(pack, tolerance=0.2):
    """Return error string if the stored final score is inconsistent, else None."""
    expected = final_account_score(
        pack["account_score"],
        pack["need_fit_score"],
        pack["cash_priority_score"],
        pack["contact_confidence"],
    )
    if abs(expected - pack["final_account_score"]) > tolerance:
        return (
            f"{pack['company_name']}: final_account_score {pack['final_account_score']} "
            f"!= recomputed {expected}"
        )
    return None
