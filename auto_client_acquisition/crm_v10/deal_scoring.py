"""Deterministic deal scoring — win probability + risk flags."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.crm_v10.schemas import Account, Deal


# Stage → base win probability before adjustments. Mirrors the value-ladder
# stages: pilot offered → paid → in delivery → won/lost.
STAGE_BASE_WIN_PROB: dict[str, float] = {
    "pilot_offered": 0.20,
    "payment_pending": 0.45,
    "paid_or_committed": 0.65,
    "in_delivery": 0.80,
    "won": 1.0,
    "lost": 0.0,
}


def _days_in_stage(deal: Deal) -> int:
    """Crude proxy: days since deal expected_close_date is None means we
    use the absence as zero. We cannot infer per-stage age without an
    audit trail, so this returns 0 for now and is wired here for the
    future Twenty CRM real adapter to fill in.
    """
    if deal.expected_close_date is None:
        return 0
    today = datetime.now(UTC).date()
    delta = (deal.expected_close_date - today).days
    return max(0, -delta)  # 0 if close-date is in the future


def score_deal(
    deal: Deal,
    account: Account,
    proof_events_count: int,
) -> dict[str, Any]:
    """Return ``{win_probability, days_in_stage, risk_flags}``."""
    base = STAGE_BASE_WIN_PROB.get(deal.stage, 0.0)

    # Account health bumps probability slightly.
    health_bump = max(0.0, min(0.15, account.customer_health_score * 0.15))
    proof_bump = min(0.10, 0.02 * max(0, int(proof_events_count)))

    win_probability = max(0.0, min(1.0, base + health_bump + proof_bump))
    days_in_stage = _days_in_stage(deal)

    risk_flags: list[str] = []
    if deal.amount_sar < 0:
        risk_flags.append("negative_amount")
    if deal.amount_sar == 0 and deal.stage in (
        "paid_or_committed", "in_delivery", "won",
    ):
        risk_flags.append("zero_amount_in_committed_stage")
    if deal.stage == "payment_pending" and proof_events_count == 0:
        risk_flags.append("payment_pending_without_proof")
    if days_in_stage > 14:
        risk_flags.append("stale_close_date")
    if account.customer_health_score < 0.3 and deal.stage in (
        "payment_pending", "paid_or_committed", "in_delivery",
    ):
        risk_flags.append("low_account_health")

    return {
        "win_probability": win_probability,
        "days_in_stage": days_in_stage,
        "risk_flags": risk_flags,
    }


__all__ = ["STAGE_BASE_WIN_PROB", "score_deal"]
