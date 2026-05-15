"""Value ledger events.

Two layers live here:

1. ``ValueLedgerEvent`` — the auditable per-engagement value record
   (re-exported from ``proof_architecture_os`` for the stable
   ``value_os`` import path used across the codebase).

2. ``ValueEvent`` — the tiered, source-disciplined value ledger that the
   Value OS router (``/api/v1/value``) and the Monthly Value Report
   build on. Tier discipline is the enterprise guarantee: a ``verified``
   (measured) value event is rejected unless it carries a ``source_ref``;
   ``client_confirmed`` requires both a ``source_ref`` and a
   ``confirmation_ref``. Estimated value can never silently become a
   verified claim.

The store is in-memory/process-scoped — the same stopgap pattern the rest
of the control plane uses before a persistent backend ships. Every
operational object carries a ``tenant_id`` (``"default"`` in dev/test;
production callers pass a real tenant).
"""

from __future__ import annotations

import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

# ── Tier vocabulary ──────────────────────────────────────────────────
# estimated  → modelled range; never claimable externally
# observed   → seen in-workflow; not independently sourced
# verified   → measured against a real source (source_ref REQUIRED)
# client_confirmed → verified AND confirmed by the client (both refs)
VALUE_TIERS: frozenset[str] = frozenset(
    {"estimated", "observed", "verified", "client_confirmed"},
)

# Tiers that represent a *measured* claim — these carry source discipline.
MEASURED_TIERS: frozenset[str] = frozenset({"verified", "client_confirmed"})


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier/source discipline."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    """One tiered value event for a customer."""

    value_event_id: str
    tenant_id: str
    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    occurred_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @property
    def is_measured(self) -> bool:
        """A measured event is one in a measured tier with a source_ref."""
        return self.tier in MEASURED_TIERS and bool(self.source_ref.strip())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_value_event(
    *,
    tier: str,
    source_ref: str,
    confirmation_ref: str = "",
) -> None:
    """Enforce tier/source discipline. Raises ``ValueDisciplineError``.

    The enterprise rule: a measured (``verified``) metric without a
    ``source_ref`` is not admissible; ``client_confirmed`` additionally
    requires a ``confirmation_ref``.
    """
    if tier not in VALUE_TIERS:
        raise ValueDisciplineError(
            f"unknown_value_tier:{tier} (expected one of {sorted(VALUE_TIERS)})",
        )
    if tier in MEASURED_TIERS and not source_ref.strip():
        raise ValueDisciplineError(f"{tier}_value_requires_source_ref")
    if tier == "client_confirmed" and not confirmation_ref.strip():
        raise ValueDisciplineError("client_confirmed_value_requires_confirmation_ref")


# ── In-memory tenant-scoped store ────────────────────────────────────
_LOCK = threading.Lock()
_EVENTS: list[ValueEvent] = []


def add_event(
    *,
    customer_id: str,
    kind: str,
    tier: str,
    amount: float = 0.0,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
    tenant_id: str = "default",
) -> ValueEvent:
    """Record a value event after enforcing tier/source discipline."""
    if not customer_id.strip():
        raise ValueDisciplineError("customer_id_required")
    if not kind.strip():
        raise ValueDisciplineError("kind_required")
    validate_value_event(
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
    )
    event = ValueEvent(
        value_event_id=f"val_{uuid4().hex[:12]}",
        tenant_id=tenant_id or "default",
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    with _LOCK:
        _EVENTS.append(event)
    return event


def list_events(
    *,
    customer_id: str | None = None,
    tenant_id: str | None = None,
) -> list[ValueEvent]:
    """Return value events, optionally filtered by customer and/or tenant."""
    with _LOCK:
        rows = list(_EVENTS)
    if tenant_id is not None:
        rows = [e for e in rows if e.tenant_id == tenant_id]
    if customer_id is not None:
        rows = [e for e in rows if e.customer_id == customer_id]
    return rows


def clear_value_ledger_for_tests() -> None:
    with _LOCK:
        _EVENTS.clear()


__all__ = [
    "MEASURED_TIERS",
    "VALUE_TIERS",
    "ValueDisciplineError",
    "ValueEvent",
    "ValueLedgerEvent",
    "add_event",
    "clear_value_ledger_for_tests",
    "list_events",
    "validate_value_event",
    "value_ledger_event_valid",
]
