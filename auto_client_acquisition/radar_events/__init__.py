"""Radar Event Backbone (Phase 9).

Event taxonomy + thread-safe append-only store with PII redaction
on insert. No external analytics dependency. File + in-memory.
"""
from auto_client_acquisition.radar_events.event_store import (
    list_recent,
    record_event,
    summary_metrics,
)
from auto_client_acquisition.radar_events.taxonomy import (
    EVENT_TYPES,
    is_known_event_type,
)

__all__ = [
    "EVENT_TYPES",
    "is_known_event_type",
    "list_recent",
    "record_event",
    "summary_metrics",
]
