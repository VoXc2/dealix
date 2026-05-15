"""Wave 12.5 §33.2.4 — Refund State Machine v2.

Adds 3-state refund path on top of the existing single-state ``refunded``:

    payment_confirmed
        ↓ (founder initiates)
    refund_requested
        ↓ (founder uploads evidence — bank reversal screenshot)
    refund_evidence_uploaded
        ↓ (founder confirms ledger entry)
    refund_completed

Hard rule (Article 4 + Article 8):
- Refund is ALWAYS founder-initiated; no automatic refund path
- Each transition requires explicit evidence
- ``refund_completed`` flips ``is_revenue=False`` on the original
  payment record (revenue rolled back)

Reuses ``dealix_payment_confirmation_stub.py`` payment state lexicon.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any, Literal

RefundState = Literal[
    "not_requested",                  # initial (no refund in progress)
    "refund_requested",                # founder initiated
    "refund_evidence_uploaded",        # bank reversal evidence on file
    "refund_completed",                # ledger entry made; is_revenue → False
    "refund_voided",                   # founder cancelled mid-process
]


_REFUND_TRANSITIONS: dict[RefundState, set[RefundState]] = {
    "not_requested": {"refund_requested"},
    "refund_requested": {"refund_evidence_uploaded", "refund_voided"},
    "refund_evidence_uploaded": {"refund_completed", "refund_voided"},
    "refund_completed": set(),  # terminal
    "refund_voided": set(),     # terminal
}


@dataclass(frozen=True, slots=True)
class RefundEvent:
    """A single refund-state transition (append-only audit)."""

    timestamp: str
    from_state: RefundState
    to_state: RefundState
    actor: str         # who initiated (founder / csm / system)
    note: str          # short explanation
    evidence_ref: str = ""  # bank reversal ID, screenshot path, etc.


@dataclass(frozen=True, slots=True)
class RefundRecord:
    """Refund state for a single payment.

    Article 8 invariant: when ``state=refund_completed``, the related
    payment's ``is_revenue`` MUST flip to False (caller's responsibility
    to update the payment record).
    """

    customer_handle: str
    payment_id: str
    state: RefundState
    amount_sar: float
    history: tuple[RefundEvent, ...] = field(default_factory=tuple)


class RefundTransitionError(ValueError):
    """Raised when an invalid refund-state transition is attempted."""


def can_transition(current: RefundState, target: RefundState) -> bool:
    """Check whether the transition is allowed by the state machine."""
    return target in _REFUND_TRANSITIONS.get(current, set())


def request_refund(
    record: RefundRecord,
    *,
    actor: str = "founder",
    note: str = "",
    now: datetime | None = None,
) -> RefundRecord:
    """Initiate a refund: not_requested → refund_requested.

    Args:
        record: Current refund record (must be in not_requested state).
        actor: Who initiated. Article 4: must be founder/csm/admin —
            never "system" (no auto-refunds).
        note: Reason / summary (≤200 chars).
        now: Override timestamp (for tests).

    Returns:
        New RefundRecord (frozen — original unchanged).

    Raises:
        RefundTransitionError: if record is not in not_requested state
            OR actor is not human.
    """
    if not can_transition(record.state, "refund_requested"):
        raise RefundTransitionError(
            f"cannot refund from state {record.state!r}; must be not_requested"
        )
    if actor in ("system", "auto"):
        raise RefundTransitionError(
            f"refund actor {actor!r} is not human — Article 4 requires founder/csm/admin"
        )
    ts = (now or datetime.now(UTC)).isoformat()
    event = RefundEvent(
        timestamp=ts,
        from_state=record.state,
        to_state="refund_requested",
        actor=actor,
        note=(note or "")[:200],
    )
    return RefundRecord(
        customer_handle=record.customer_handle,
        payment_id=record.payment_id,
        amount_sar=record.amount_sar,
        state="refund_requested",
        history=(*record.history, event),
    )


def upload_refund_evidence(
    record: RefundRecord,
    *,
    actor: str = "founder",
    evidence_ref: str,
    note: str = "",
    now: datetime | None = None,
) -> RefundRecord:
    """Attach bank-reversal evidence: refund_requested → refund_evidence_uploaded.

    Args:
        evidence_ref: Bank reversal transaction ID OR uploaded
            screenshot path. Required (≥3 chars).

    Raises:
        RefundTransitionError: invalid state OR missing evidence_ref.
    """
    if not can_transition(record.state, "refund_evidence_uploaded"):
        raise RefundTransitionError(
            f"cannot upload evidence from state {record.state!r}; "
            f"must be refund_requested"
        )
    if not evidence_ref or len(evidence_ref.strip()) < 3:
        raise RefundTransitionError(
            "evidence_ref required (≥3 chars) — Article 8: no fake refund completion"
        )
    ts = (now or datetime.now(UTC)).isoformat()
    event = RefundEvent(
        timestamp=ts,
        from_state=record.state,
        to_state="refund_evidence_uploaded",
        actor=actor,
        note=(note or "")[:200],
        evidence_ref=evidence_ref.strip(),
    )
    return RefundRecord(
        customer_handle=record.customer_handle,
        payment_id=record.payment_id,
        amount_sar=record.amount_sar,
        state="refund_evidence_uploaded",
        history=(*record.history, event),
    )


def complete_refund(
    record: RefundRecord,
    *,
    actor: str = "founder",
    ledger_entry_id: str,
    note: str = "",
    now: datetime | None = None,
) -> RefundRecord:
    """Confirm refund + roll back revenue: refund_evidence_uploaded → refund_completed.

    The caller MUST also update the original payment record's
    ``is_revenue`` to False — this function only records the refund-
    side event.

    Args:
        ledger_entry_id: Accounting ledger reference for the rollback.
            Required (≥3 chars).

    Raises:
        RefundTransitionError: invalid state OR missing ledger_entry_id.
    """
    if not can_transition(record.state, "refund_completed"):
        raise RefundTransitionError(
            f"cannot complete from state {record.state!r}; "
            f"must be refund_evidence_uploaded"
        )
    if not ledger_entry_id or len(ledger_entry_id.strip()) < 3:
        raise RefundTransitionError(
            "ledger_entry_id required (≥3 chars) — Article 8: no completion without trail"
        )
    ts = (now or datetime.now(UTC)).isoformat()
    event = RefundEvent(
        timestamp=ts,
        from_state=record.state,
        to_state="refund_completed",
        actor=actor,
        note=(note or "")[:200],
        evidence_ref=ledger_entry_id.strip(),
    )
    return RefundRecord(
        customer_handle=record.customer_handle,
        payment_id=record.payment_id,
        amount_sar=record.amount_sar,
        state="refund_completed",
        history=(*record.history, event),
    )


def void_refund(
    record: RefundRecord,
    *,
    actor: str = "founder",
    note: str = "",
    now: datetime | None = None,
) -> RefundRecord:
    """Cancel a refund mid-process: refund_requested OR refund_evidence_uploaded → refund_voided.

    Useful when founder realizes the refund shouldn't proceed.
    Original payment stays as revenue.
    """
    if not can_transition(record.state, "refund_voided"):
        raise RefundTransitionError(
            f"cannot void from state {record.state!r}"
        )
    ts = (now or datetime.now(UTC)).isoformat()
    event = RefundEvent(
        timestamp=ts,
        from_state=record.state,
        to_state="refund_voided",
        actor=actor,
        note=(note or "")[:200],
    )
    return RefundRecord(
        customer_handle=record.customer_handle,
        payment_id=record.payment_id,
        amount_sar=record.amount_sar,
        state="refund_voided",
        history=(*record.history, event),
    )


def is_revenue_after_refund(record: RefundRecord) -> bool:
    """Returns False ONLY when refund completed; True otherwise.

    Article 8: this is the canonical helper for downstream code that
    asks "should this payment count as revenue right now?".
    """
    return record.state != "refund_completed"


# ─────────────────────────────────────────────────────────────────────
# ZATCA auto-draft helper (Wave 12.5 §33.2.4)
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ZATCADraftRequest:
    """Idempotent ZATCA invoice draft request.

    NEVER auto-submits to Fatoora — only drafts. Founder explicitly
    calls submit endpoint.

    Article 4 (NO_LIVE_CHARGE / no auto-submit): ``would_submit``
    is always False — Wave 12.5 wires draft creation only.
    """

    payment_id: str
    customer_handle: str
    amount_sar: float
    idempotency_key: str
    requested_at: str
    would_submit: bool = False


def request_zatca_draft_on_payment_confirmed(
    *,
    payment_id: str,
    customer_handle: str,
    amount_sar: float,
    payment_state: str,
    now: datetime | None = None,
) -> ZATCADraftRequest | None:
    """Build a ZATCA draft request when payment_confirmed.

    Returns None when payment_state != "payment_confirmed" — never
    drafts for invoice_intent / payment_pending / evidence_received
    (Article 8 revenue truth).

    Idempotency key = ``zatca_draft:{payment_id}`` — caller's job to
    reject duplicate calls; this function just produces the request
    deterministically.

    Args:
        payment_id: The payment record ID.
        customer_handle: Tenant scope.
        amount_sar: Confirmed amount.
        payment_state: Current state (must be "payment_confirmed").
        now: Override timestamp.

    Returns:
        ZATCADraftRequest when state qualifies; None otherwise.
    """
    if payment_state != "payment_confirmed":
        return None
    ts = (now or datetime.now(UTC)).isoformat()
    return ZATCADraftRequest(
        payment_id=payment_id,
        customer_handle=customer_handle,
        amount_sar=amount_sar,
        idempotency_key=f"zatca_draft:{payment_id}",
        requested_at=ts,
        would_submit=False,  # Article 4: NEVER auto-submits
    )


def is_in_zatca_wave_24_bracket(turnover_sar: float) -> bool:
    """ZATCA Phase 2 Wave 24 (June 30, 2026 deadline) applies to
    businesses with VAT-registered turnover > SAR 375,000 in any of
    2022, 2023, or 2024.

    Returns True when this customer falls in the Wave 24 bracket
    (most relevant for Dealix's SMB segment).

    Source: https://zatca.gov.sa/en/E-Invoicing/Introduction/Pages/Roll-out-phases.aspx
    """
    return turnover_sar > 375_000.0
