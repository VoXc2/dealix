"""CommercialEngine — records validated CEL transitions as RevenueEvents.

The engine is the only writer of `commercial.*` events. Every transition is
validated by `validate_transition` before an event is appended; an illegal
transition raises `ValueError` and nothing is written.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.commercial_os.cel import STATE_TO_CEL
from auto_client_acquisition.commercial_os.projections import (
    current_commercial_state,
)
from auto_client_acquisition.commercial_os.transitions import (
    TransitionResult,
    validate_transition,
)
from auto_client_acquisition.revenue_memory.event_store import (
    EventStore,
    InMemoryEventStore,
)
from auto_client_acquisition.revenue_memory.events import RevenueEvent, make_event

# Commercial state -> the `commercial.*` event type that records reaching it.
_STATE_TO_EVENT_TYPE: dict[str, str] = {
    "prepared_not_sent": "commercial.prepared",
    "sent": "commercial.sent",
    "replied_interested": "commercial.reply_classified",
    "silent": "commercial.reply_classified",
    "not_interested": "commercial.reply_classified",
    "meeting_booked": "commercial.meeting_used",
    "used_in_meeting": "commercial.meeting_used",
    "scope_requested": "commercial.scope_requested",
    "pilot_intro_requested": "commercial.pilot_intro_requested",
    "invoice_sent": "commercial.invoice_sent",
    "invoice_paid": "commercial.invoice_paid",
}


def event_type_for_state(state: str) -> str:
    """Return the `commercial.*` event type that records reaching `state`."""
    if state not in _STATE_TO_EVENT_TYPE:
        raise ValueError(f"no event type for state: {state}")
    return _STATE_TO_EVENT_TYPE[state]


@dataclass(frozen=True)
class RecordedTransition:
    """Result of a successful `record_transition` call."""

    event: RevenueEvent
    state: str
    cel: str


class CommercialEngine:
    """Validates and records commercial state transitions.

    The engine is subject-scoped per call: `subject_id` identifies one
    commercial engagement (an account, deal, or campaign timeline).
    """

    def __init__(self, store: EventStore | None = None) -> None:
        self._store: EventStore = store if store is not None else InMemoryEventStore()

    @property
    def store(self) -> EventStore:
        """The injected (or default in-memory) event store."""
        return self._store

    def current_state(
        self, *, customer_id: str, subject_type: str, subject_id: str
    ) -> dict[str, str] | None:
        """Return `{state, cel}` for one engagement, or `None` if no events."""
        events = list(
            self._store.read_for_subject(
                subject_type, subject_id, customer_id=customer_id
            )
        )
        states = current_commercial_state(events)
        return states.get(subject_id)

    def record_transition(
        self,
        *,
        customer_id: str,
        subject_type: str,
        subject_id: str,
        next_state: str,
        founder_confirmed: bool = False,
        used_in_meeting: bool = False,
        scope_or_intro_requested: bool = False,
        invoice_paid: bool = False,
        actor: str = "system",
        payload: dict | None = None,
        correlation_id: str | None = None,
    ) -> RecordedTransition:
        """Validate a transition and append a `commercial.*` event on success.

        Raises:
            ValueError: if the transition is illegal (the `reason` from
                `validate_transition` is the message). Nothing is written.
        """
        current = self.current_state(
            customer_id=customer_id,
            subject_type=subject_type,
            subject_id=subject_id,
        )
        current_state = current["state"] if current is not None else None

        result: TransitionResult = validate_transition(
            current_state,
            next_state,
            founder_confirmed=founder_confirmed,
            used_in_meeting=used_in_meeting,
            scope_or_intro_requested=scope_or_intro_requested,
            invoice_paid=invoice_paid,
        )
        if not result.ok:
            raise ValueError(result.reason)

        cel = STATE_TO_CEL[next_state]
        event_payload: dict = dict(payload or {})
        event_payload.update(
            {
                "commercial_state": next_state,
                "cel": cel,
                "from_state": current_state,
            }
        )
        event = make_event(
            event_type=event_type_for_state(next_state),
            customer_id=customer_id,
            subject_type=subject_type,
            subject_id=subject_id,
            payload=event_payload,
            correlation_id=correlation_id,
            actor=actor,
        )
        self._store.append(event)
        return RecordedTransition(event=event, state=next_state, cel=cel)
