"""Canonical Friction Log — every place a client gets stuck becomes a
trackable event. Aggregated into a learning_debt signal that drives the
weekly capital review.
"""
from auto_client_acquisition.friction_log.aggregator import (
    FrictionAggregate,
    aggregate,
)
from auto_client_acquisition.friction_log.sanitizer import sanitize_notes
from auto_client_acquisition.friction_log.schemas import (
    FrictionEvent,
    FrictionKind,
    FrictionSeverity,
)
from auto_client_acquisition.friction_log.store import (
    clear_for_test,
    emit,
    list_events,
)

__all__ = [
    "FrictionAggregate",
    "FrictionEvent",
    "FrictionKind",
    "FrictionSeverity",
    "aggregate",
    "clear_for_test",
    "emit",
    "list_events",
    "sanitize_notes",
]
