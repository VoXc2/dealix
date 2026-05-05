"""In-process append-only incident buffer."""
from __future__ import annotations

import threading
from typing import Optional

from auto_client_acquisition.observability_v6.schemas import (
    Incident,
    IncidentSeverity,
)

_INCIDENT_BUFFER: list[Incident] = []
_INCIDENT_LOCK = threading.Lock()


def record_incident(incident: Incident) -> Incident:
    """Append ``incident`` to the buffer (append-only)."""
    with _INCIDENT_LOCK:
        _INCIDENT_BUFFER.append(incident)
    return incident


def list_incidents(
    severity_filter: Optional[IncidentSeverity] = None,
) -> list[Incident]:
    """Return all incidents, optionally filtered to a severity tier."""
    with _INCIDENT_LOCK:
        snapshot = list(_INCIDENT_BUFFER)
    if severity_filter is None:
        return snapshot
    return [inc for inc in snapshot if inc.severity == severity_filter]


def _reset_incident_buffer() -> None:
    """Test-only helper — clears the in-process buffer."""
    with _INCIDENT_LOCK:
        _INCIDENT_BUFFER.clear()
