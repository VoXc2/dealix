"""Attribution — last-touch + first-touch + simple multi-touch decay."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.growth_v10.schemas import EventRecord


def _name(ev: EventRecord) -> str:
    return ev.name.value if hasattr(ev.name, "value") else str(ev.name)


def attribute_revenue(
    revenue_event: EventRecord | dict[str, Any],
    prior_events: list[EventRecord],
) -> dict:
    """Return first-touch + last-touch + multi-touch attribution.

    multi_touch is a uniform decay (linear, descending) across the
    prior events, weights summing to ~1.0.
    """
    if isinstance(revenue_event, EventRecord):
        rev_name = _name(revenue_event)
    else:
        rev_name = str(revenue_event.get("name", "unknown"))

    if not prior_events:
        return {
            "first_touch": None,
            "last_touch": None,
            "multi_touch": {},
            "revenue_event": rev_name,
        }

    # Sort prior events by created_at ascending.
    ordered = sorted(prior_events, key=lambda e: e.created_at)
    first = _name(ordered[0])
    last = _name(ordered[-1])

    n = len(ordered)
    # Linear decay, oldest gets smallest, newest gets biggest.
    raw_weights = [i + 1 for i in range(n)]
    total = sum(raw_weights)
    multi_touch: dict[str, float] = {}
    for ev, w in zip(ordered, raw_weights, strict=True):
        nm = _name(ev)
        multi_touch[nm] = round(multi_touch.get(nm, 0.0) + (w / total), 6)

    return {
        "first_touch": first,
        "last_touch": last,
        "multi_touch": multi_touch,
        "revenue_event": rev_name,
    }
