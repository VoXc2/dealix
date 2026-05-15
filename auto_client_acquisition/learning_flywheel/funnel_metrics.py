"""Wave 12 §32.3.11 — Funnel Metrics Calculator.

Computes the 5-stage Dealix conversion funnel from recorded learning
events:

    signal → lead → decision_passport → approved_action → delivery → proof

Hard rule (Article 8): every ratio is honest — returns ``None`` when
denominator is zero. Never divides-by-fake.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

from auto_client_acquisition.learning_flywheel.aggregator import _read_events


@dataclass(frozen=True, slots=True)
class FunnelMetrics:
    """5-stage Dealix conversion funnel.

    Each ``*_to_*`` is the fraction (numerator / denominator) in [0, 1],
    or None when the denominator is zero (Article 8 — no fake math).
    """

    period_start: str
    period_end: str
    # Stage counts
    signals_count: int
    leads_count: int
    decision_passports_count: int
    approved_actions_count: int
    delivery_starts_count: int
    proof_events_count: int
    payments_confirmed_count: int
    # Conversion ratios (None when denominator=0)
    signal_to_lead: float | None
    lead_to_passport: float | None
    passport_to_approved_action: float | None
    approved_action_to_delivery: float | None
    delivery_to_proof: float | None
    proof_to_payment: float | None


def compute_funnel(
    *,
    period_end: datetime | None = None,
    period_days: int = 30,
    storage_path: Path | None = None,
) -> FunnelMetrics:
    """Compute the 30-day Dealix funnel from recorded learning events.

    Args:
        period_end: End of window (default: now UTC).
        period_days: Window size (default 30).
        storage_path: Override (for tests).

    Returns:
        FunnelMetrics with honest counts + ratios.
    """
    end = period_end or datetime.now(UTC)
    start = end - timedelta(days=period_days)
    all_events = _read_events(storage_path=storage_path)

    # Filter to window
    in_window = []
    for e in all_events:
        try:
            ts = datetime.fromisoformat(e.timestamp.replace("Z", "+00:00"))
            if start <= ts <= end:
                in_window.append(e)
        except (ValueError, AttributeError):
            continue

    # Count each stage
    signals = sum(1 for e in in_window if e.kind == "signal_created")
    leads = sum(1 for e in in_window if e.kind == "lead_created")
    passports = sum(1 for e in in_window if e.kind == "decision_passport_created")
    approved = sum(1 for e in in_window if e.kind == "action_approved")
    deliveries = sum(1 for e in in_window if e.kind == "delivery_started")
    proofs = sum(1 for e in in_window if e.kind == "proof_created")
    payments = sum(1 for e in in_window if e.kind == "payment_confirmed")

    return FunnelMetrics(
        period_start=start.date().isoformat(),
        period_end=end.date().isoformat(),
        signals_count=signals,
        leads_count=leads,
        decision_passports_count=passports,
        approved_actions_count=approved,
        delivery_starts_count=deliveries,
        proof_events_count=proofs,
        payments_confirmed_count=payments,
        signal_to_lead=_safe_ratio(leads, signals),
        lead_to_passport=_safe_ratio(passports, leads),
        passport_to_approved_action=_safe_ratio(approved, passports),
        approved_action_to_delivery=_safe_ratio(deliveries, approved),
        delivery_to_proof=_safe_ratio(proofs, deliveries),
        proof_to_payment=_safe_ratio(payments, proofs),
    )


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    """Return numerator/denominator or None when denominator is zero.

    Article 8 — never divides by zero / never returns 0.0 when there's
    no signal at all (caller should distinguish "0% conversion" from
    "no data yet").
    """
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)
