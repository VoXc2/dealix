"""Market-proof lifecycle state machine (L2 to L7).

Tracks how a warm contact progresses from a prepared (not sent) outreach
message to confirmed revenue. The system prepares, suggests, logs and
verifies; the founder approves every external action.

There is intentionally NO function in this module that sends a message or
executes an external action. Every transition is routed through
``enforce_doctrine_non_negotiables`` so any caller that requests an
autonomous external send trips a doctrine breach (ValueError).
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.safe_send_gateway.doctrine import (
    enforce_doctrine_non_negotiables,
)

# ── States and their proof levels ──────────────────────────────────
STATE_TO_LEVEL: dict[str, str] = {
    "prepared_not_sent": "L2",
    "sent": "L4",
    "replied_interested": "L4",
    "meeting_booked": "L4",
    "used_in_meeting": "L5",
    "scope_requested": "L6",
    "pilot_intro_requested": "L6",
    "invoice_sent": "L7_candidate",
    "invoice_paid": "L7_confirmed",
}

# Terminal states a contact can drop into instead of progressing.
TERMINAL_STATES: tuple[str, ...] = ("no_reply", "not_interested")

LIFECYCLE_STATES: tuple[str, ...] = tuple(STATE_TO_LEVEL) + TERMINAL_STATES

# ── Allowed transitions (forward-only DAG) ─────────────────────────
ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "prepared_not_sent": ("sent",),
    "sent": ("replied_interested", "meeting_booked", "no_reply", "not_interested"),
    "replied_interested": ("meeting_booked", "not_interested"),
    "meeting_booked": ("used_in_meeting",),
    "used_in_meeting": ("scope_requested", "pilot_intro_requested"),
    "scope_requested": ("invoice_sent",),
    "pilot_intro_requested": ("invoice_sent",),
    "invoice_sent": ("invoice_paid",),
    "invoice_paid": (),
    "no_reply": (),
    "not_interested": (),
}

# States that count as "revenue confirmed".
_REVENUE_CONFIRMED_STATE = "invoice_paid"

# ── In-memory append-only ledger (mirrors friction_log style) ──────
_LEDGER: dict[str, list[dict[str, Any]]] = {}
_lock = threading.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clear_for_test() -> None:
    """Reset the in-memory ledger. Test-only helper."""
    with _lock:
        _LEDGER.clear()


def state_machine_definition() -> dict[str, Any]:
    """Return the full state machine definition (states, levels, transitions)."""
    return {
        "states": list(LIFECYCLE_STATES),
        "terminal_states": list(TERMINAL_STATES),
        "state_to_level": dict(STATE_TO_LEVEL),
        "allowed_transitions": {k: list(v) for k, v in ALLOWED_TRANSITIONS.items()},
        "revenue_confirmed_state": _REVENUE_CONFIRMED_STATE,
    }


def _check_guards(
    *,
    to_state: str,
    founder_confirmed: bool,
    payment_confirmed: bool,
    scope_or_intro_request: str | None,
    history_states: list[str],
) -> None:
    """Raise ValueError if a transition guard rule is violated."""
    if to_state == "sent" and not founder_confirmed:
        raise ValueError(
            "Cannot enter 'sent' without founder_confirmed=True — "
            "the founder must approve the manual send. "
            "لا يمكن الدخول إلى حالة 'مرسل' دون موافقة المؤسس على الإرسال اليدوي."
        )
    if to_state == "used_in_meeting" and "meeting_booked" not in history_states:
        raise ValueError(
            "Cannot enter 'used_in_meeting' (L5) — the contact must have "
            "passed through 'meeting_booked'. "
            "لا يمكن الدخول إلى L5 قبل المرور بحالة 'تم حجز اجتماع'."
        )
    if to_state in ("scope_requested", "pilot_intro_requested") and not scope_or_intro_request:
        raise ValueError(
            f"Cannot enter '{to_state}' (L6) without a recorded scope or "
            "intro request (scope_or_intro_request). "
            "لا يمكن الدخول إلى L6 دون تسجيل طلب نطاق أو طلب تعريف."
        )
    if to_state == "invoice_paid" and not payment_confirmed:
        raise ValueError(
            "Cannot enter 'invoice_paid' (L7_confirmed) without "
            "payment_confirmed=True. Revenue is never counted before "
            "payment is confirmed. "
            "لا يمكن تأكيد الإيراد قبل تأكيد الدفع."
        )


def record_transition(
    contact_id: str,
    from_state: str,
    to_state: str,
    *,
    founder_confirmed: bool = False,
    payment_confirmed: bool = False,
    scope_or_intro_request: str | None = None,
    evidence_ref: str | None = None,
    doctrine_flags: dict[str, bool] | None = None,
) -> dict[str, Any]:
    """Record a single lifecycle transition and return the transition record.

    Raises ValueError on an invalid transition, a guard-rule violation, or a
    doctrine non-negotiable breach. The router maps ValueError to HTTP 403.
    """
    if not contact_id:
        raise ValueError("contact_id is required")
    if from_state not in LIFECYCLE_STATES:
        raise ValueError(f"unknown from_state: {from_state!r}")
    if to_state not in LIFECYCLE_STATES:
        raise ValueError(f"unknown to_state: {to_state!r}")

    # Doctrine non-negotiables — wire every flag the caller passed through.
    flags = dict(doctrine_flags or {})
    enforce_doctrine_non_negotiables(
        request_cold_whatsapp=bool(flags.get("request_cold_whatsapp", False)),
        request_linkedin_automation=bool(flags.get("request_linkedin_automation", False)),
        request_scraping=bool(flags.get("request_scraping", False)),
        request_bulk_outreach=bool(flags.get("request_bulk_outreach", False)),
        request_guaranteed_sales_claim=bool(flags.get("request_guaranteed_sales_claim", False)),
        request_fake_proof=bool(flags.get("request_fake_proof", False)),
        request_external_send_without_approval=bool(
            flags.get("request_external_send_without_approval", False)
        ),
    )

    allowed = ALLOWED_TRANSITIONS.get(from_state, ())
    if to_state not in allowed:
        raise ValueError(
            f"invalid transition {from_state!r} -> {to_state!r}; "
            f"allowed from {from_state!r}: {list(allowed)}"
        )

    with _lock:
        history = _LEDGER.get(contact_id, [])
        history_states = [from_state] + [r["to_state"] for r in history]

        # A contact's recorded from_state must match its current state.
        if history:
            current = history[-1]["to_state"]
            if current != from_state:
                raise ValueError(
                    f"from_state {from_state!r} does not match the contact's "
                    f"current state {current!r}"
                )

        _check_guards(
            to_state=to_state,
            founder_confirmed=founder_confirmed,
            payment_confirmed=payment_confirmed,
            scope_or_intro_request=scope_or_intro_request,
            history_states=history_states,
        )

        record: dict[str, Any] = {
            "contact_id": contact_id,
            "from_state": from_state,
            "to_state": to_state,
            "from_level": STATE_TO_LEVEL.get(from_state),
            "to_level": STATE_TO_LEVEL.get(to_state),
            "founder_confirmed": bool(founder_confirmed),
            "payment_confirmed": bool(payment_confirmed),
            "scope_or_intro_request": scope_or_intro_request,
            "evidence_ref": evidence_ref,
            "revenue_counted": to_state == _REVENUE_CONFIRMED_STATE,
            "recorded_at": _now_iso(),
        }
        _LEDGER.setdefault(contact_id, []).append(record)
    return record


def ledger() -> dict[str, list[dict[str, Any]]]:
    """Return a copy of the full append-only transition ledger."""
    with _lock:
        return {cid: [dict(r) for r in recs] for cid, recs in _LEDGER.items()}


def current_state(contact_id: str) -> str | None:
    """Return the current state of a contact, or None if it has no history."""
    with _lock:
        history = _LEDGER.get(contact_id, [])
        return history[-1]["to_state"] if history else None


def snapshot() -> dict[str, Any]:
    """Compute a command-center snapshot of the lifecycle.

    Revenue stays 0 until at least one contact reaches ``invoice_paid``.
    """
    with _lock:
        history_by_contact = {
            cid: [dict(r) for r in recs] for cid, recs in _LEDGER.items()
        }

    level_counts: dict[str, int] = {"L4": 0, "L5": 0, "L6": 0, "L7": 0}
    current_by_contact: dict[str, str] = {}
    contacts_paid = 0

    for contact_id, recs in history_by_contact.items():
        if not recs:
            continue
        cur = recs[-1]["to_state"]
        current_by_contact[contact_id] = cur
        level = STATE_TO_LEVEL.get(cur, "")
        if level == "L4":
            level_counts["L4"] += 1
        elif level == "L5":
            level_counts["L5"] += 1
        elif level == "L6":
            level_counts["L6"] += 1
        elif level in ("L7_candidate", "L7_confirmed"):
            level_counts["L7"] += 1
        if cur == _REVENUE_CONFIRMED_STATE:
            contacts_paid += 1

    return {
        "level_counts": level_counts,
        "current_state_by_contact": current_by_contact,
        "blocked_items": list_blocked(),
        "contacts_with_confirmed_revenue": contacts_paid,
        "revenue_confirmed": contacts_paid > 0,
    }


# ── Blocked-item tracking ──────────────────────────────────────────
_BLOCKED: list[dict[str, Any]] = []


def record_blocked(
    contact_id: str,
    from_state: str,
    to_state: str,
    reason: str,
) -> dict[str, Any]:
    """Log a contact that could not progress because a guard failed."""
    item = {
        "contact_id": contact_id,
        "from_state": from_state,
        "to_state": to_state,
        "reason": reason,
        "recorded_at": _now_iso(),
    }
    with _lock:
        _BLOCKED.append(item)
    return item


def list_blocked() -> list[dict[str, Any]]:
    """Return contacts stuck because a guard rule failed."""
    with _lock:
        return [dict(b) for b in _BLOCKED]


def clear_blocked_for_test() -> None:
    """Reset the in-memory blocked-items list. Test-only helper."""
    with _lock:
        _BLOCKED.clear()


__all__ = [
    "ALLOWED_TRANSITIONS",
    "LIFECYCLE_STATES",
    "STATE_TO_LEVEL",
    "TERMINAL_STATES",
    "clear_blocked_for_test",
    "clear_for_test",
    "current_state",
    "ledger",
    "list_blocked",
    "record_blocked",
    "record_transition",
    "snapshot",
    "state_machine_definition",
]
