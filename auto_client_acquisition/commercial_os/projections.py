"""Projections over the commercial event stream.

`current_commercial_state` folds a stream of `commercial.*` RevenueEvents into
the latest `{state, cel}` per engagement subject. Pure: no I/O.
"""

from __future__ import annotations

from collections.abc import Iterable

from auto_client_acquisition.commercial_os.cel import STATE_TO_CEL
from auto_client_acquisition.revenue_memory.events import RevenueEvent

_COMMERCIAL_EVENT_TYPES: frozenset[str] = frozenset(
    {
        "commercial.prepared",
        "commercial.sent",
        "commercial.reply_classified",
        "commercial.meeting_used",
        "commercial.scope_requested",
        "commercial.pilot_intro_requested",
        "commercial.invoice_sent",
        "commercial.invoice_paid",
    }
)


def current_commercial_state(
    events: Iterable[RevenueEvent],
) -> dict[str, dict[str, str]]:
    """Fold a commercial event stream into the latest state per subject.

    Args:
        events: any iterable of RevenueEvents (non-commercial events ignored).

    Returns:
        `{subject_id: {"state": <state>, "cel": <cel>}}`. The latest event
        wins, ordered by `(occurred_at, event_id)`.
    """
    commercial = [
        e for e in events if e.event_type in _COMMERCIAL_EVENT_TYPES
    ]
    commercial.sort(key=lambda e: (e.occurred_at, e.event_id))

    latest: dict[str, dict[str, str]] = {}
    for e in commercial:
        state = e.payload.get("commercial_state")
        if not isinstance(state, str) or state not in STATE_TO_CEL:
            continue
        latest[e.subject_id] = {"state": state, "cel": STATE_TO_CEL[state]}
    return latest
