"""Compute customer health from observable, PII-free signals."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Iterable

from auto_client_acquisition.crm_v10.schemas import (
    Account,
    CustomerHealth,
    Deal,
    ProofEventRef,
    ServiceSession,
    SupportTicket,
)


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def compute_health(
    account: Account,
    deals: Iterable[Deal],
    service_sessions: Iterable[ServiceSession],
    proof_events: Iterable[ProofEventRef],
    support_tickets: Iterable[SupportTicket],
) -> CustomerHealth:
    """Return a deterministic ``CustomerHealth`` for the given account."""
    deals = [d for d in deals if d.account_id == account.id]
    sessions = [s for s in service_sessions if s.account_id == account.id]
    proofs = [p for p in proof_events if p.account_id == account.id]
    tickets = [t for t in support_tickets if t.account_id == account.id]

    # Delivery consistency: completed sessions / total scheduled+completed.
    relevant_sessions = [
        s for s in sessions if s.status in ("scheduled", "in_progress", "completed")
    ]
    if relevant_sessions:
        delivery_consistency = sum(
            1 for s in relevant_sessions if s.status == "completed"
        ) / len(relevant_sessions)
    else:
        delivery_consistency = 0.0

    # Support load — more open / blocked tickets = lower health.
    open_tickets = sum(
        1 for t in tickets if t.status in ("open", "in_progress")
    )
    blocked_tickets = sum(1 for t in tickets if t.priority == "blocked")
    support_load = _clamp01(1.0 - 0.1 * open_tickets - 0.2 * blocked_tickets)

    # Recent proof — having ≥1 proof event in any recent window improves
    # the score. We use a coarse "any proof within 30 days" check.
    now = datetime.now(UTC)
    recent_proof = 0.0
    if proofs:
        for p in proofs:
            age_days = (now - p.created_at).days
            if 0 <= age_days <= 30:
                recent_proof = 1.0
                break
        if recent_proof == 0.0:
            recent_proof = 0.5  # has proofs but all are stale

    # Deal momentum — won deals push up, lost deals push down.
    if deals:
        won = sum(1 for d in deals if d.stage == "won")
        lost = sum(1 for d in deals if d.stage == "lost")
        denom = max(1, won + lost)
        deal_momentum = _clamp01(0.5 + 0.5 * (won - lost) / denom)
    else:
        deal_momentum = 0.5

    factors = {
        "delivery_consistency": round(delivery_consistency, 4),
        "support_load": round(support_load, 4),
        "recent_proof": round(recent_proof, 4),
        "deal_momentum": round(deal_momentum, 4),
    }

    # Equal-weighted aggregate, clamped.
    score = _clamp01(sum(factors.values()) / len(factors))

    return CustomerHealth(
        account_id=account.id,
        score=round(score, 4),
        factors=factors,
        last_updated=now,
    )


__all__ = ["compute_health"]
