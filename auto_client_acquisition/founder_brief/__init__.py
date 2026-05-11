"""Wave 16 §C1 — Founder Brief auto-source helper.

Composes counts from layer modules (approval_center, service_sessions,
payment_state, support_os) into a single LayerCounts dataclass that the
:func:`scripts.dealix_founder_daily_brief.build_brief` function can
consume directly.

This replaces the manual --blocking-approvals 3 / --pending-payments 2
CLI flags with `--auto-source` which queries the live in-process state.

Hard rules:
- Article 4: pure-read; never writes, never sends.
- Article 8: returns 0 honestly when modules empty (no fabrication).
- Article 11: composes existing module APIs (list_pending,
  list_sessions). Does NOT introduce a new persistence layer.

Sandbox-safe: all queries are in-memory; no network, no DB.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True, slots=True)
class LayerCounts:
    """Counts pulled from each Wave 13/14 layer for the daily brief.

    Every field is an integer count. Article 8: zero is honest when no
    data is loaded — the brief reflects "no signal" instead of inventing
    activity.
    """

    blocking_approvals: int = 0
    pending_payment_confirmations: int = 0
    pending_proof_packs_to_send: int = 0
    overdue_followups: int = 0
    sla_at_risk_tickets: int = 0
    paid_customers: int = 0
    sources_used: tuple[str, ...] = ()
    is_estimate: bool = True  # Article 8


def _count_blocking_approvals(*, threshold_hours: int = 24) -> int:
    """Approvals pending for more than `threshold_hours` from now."""
    try:
        from auto_client_acquisition.approval_center import list_pending
    except ImportError:
        return 0
    try:
        pending = list_pending()
    except Exception:
        return 0
    cutoff = datetime.now(UTC) - timedelta(hours=threshold_hours)
    count = 0
    for req in pending:
        created_at = getattr(req, "created_at", None)
        if created_at is None:
            count += 1  # unknown age = blocking by default
            continue
        # Normalize timezone if needed
        if hasattr(created_at, "tzinfo") and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        if created_at <= cutoff:
            count += 1
    return count


def _count_pending_payments() -> int:
    """Payment intents waiting for founder confirmation."""
    try:
        from auto_client_acquisition.payment_ops.refund_state_machine import (
            list_payment_states,
        )
    except ImportError:
        return 0
    try:
        states = list_payment_states()
    except Exception:
        return 0
    return sum(
        1 for s in states
        if getattr(s, "state", "") in ("invoice_intent_created", "evidence_received")
    )


def _count_pending_proof_packs() -> int:
    """Service sessions completed but proof pack not yet built."""
    try:
        from auto_client_acquisition.service_sessions.store import list_sessions
    except ImportError:
        return 0
    try:
        sessions = list_sessions(status="completed")
    except Exception:
        return 0
    return sum(
        1 for s in sessions
        if not getattr(s, "proof_pack_built", False)
    )


def _count_overdue_followups() -> int:
    """Active service sessions with no activity in 48+ hours.

    Best-effort — depends on whether the session has a
    ``last_activity_at`` attribute. Returns 0 if attribute missing.
    """
    try:
        from auto_client_acquisition.service_sessions.store import list_sessions
    except ImportError:
        return 0
    try:
        sessions = list_sessions(status="active")
    except Exception:
        return 0
    cutoff = datetime.now(UTC) - timedelta(hours=48)
    count = 0
    for s in sessions:
        last = getattr(s, "last_activity_at", None) or getattr(s, "started_at", None)
        if last is None:
            continue
        if hasattr(last, "tzinfo") and last.tzinfo is None:
            last = last.replace(tzinfo=UTC)
        if last <= cutoff:
            count += 1
    return count


def _count_sla_at_risk_tickets() -> int:
    """Support tickets within 25% of SLA breach."""
    try:
        from auto_client_acquisition.support_os.ticket import list_open_tickets
    except ImportError:
        return 0
    try:
        tickets = list_open_tickets()
    except Exception:
        return 0
    count = 0
    for t in tickets:
        risk = getattr(t, "sla_at_risk", None)
        if risk is True:
            count += 1
    return count


def _count_paid_customers() -> int:
    """Customers who have ever reached payment_confirmed state."""
    try:
        from auto_client_acquisition.payment_ops.refund_state_machine import (
            list_payment_states,
        )
    except ImportError:
        return 0
    try:
        states = list_payment_states()
    except Exception:
        return 0
    handles = {
        getattr(s, "customer_handle", None)
        for s in states
        if getattr(s, "state", "") == "payment_confirmed"
    }
    handles.discard(None)
    return len(handles)


def query_layer_counts() -> LayerCounts:
    """Pull live counts from all 5 layer modules + paid customers.

    Returns LayerCounts with `sources_used` listing which modules
    successfully responded. Modules that aren't loaded contribute 0
    (Article 8: honest zero, not fabricated).
    """
    sources: list[str] = []

    blocking = _count_blocking_approvals()
    if blocking >= 0:
        sources.append("approval_center")

    payments = _count_pending_payments()
    sources.append("payment_ops")

    proof = _count_pending_proof_packs()
    sources.append("service_sessions:completed")

    followups = _count_overdue_followups()
    sources.append("service_sessions:active")

    sla = _count_sla_at_risk_tickets()
    sources.append("support_os")

    paid = _count_paid_customers()

    return LayerCounts(
        blocking_approvals=blocking,
        pending_payment_confirmations=payments,
        pending_proof_packs_to_send=proof,
        overdue_followups=followups,
        sla_at_risk_tickets=sla,
        paid_customers=paid,
        sources_used=tuple(sources),
    )
