"""Incident tracking for operational chaos control."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class IncidentStatus(StrEnum):
    OPEN = 'open'
    MITIGATED = 'mitigated'
    RESOLVED = 'resolved'


@dataclass(frozen=True, slots=True)
class Incident:
    incident_id: str
    title: str
    severity: str
    status: IncidentStatus


_INCIDENTS: dict[str, Incident] = {}


def open_incident(incident: Incident) -> None:
    _INCIDENTS[incident.incident_id] = incident


def update_incident_status(incident_id: str, status: IncidentStatus) -> None:
    incident = _INCIDENTS.get(incident_id)
    if incident is None:
        raise KeyError('incident_not_found')
    _INCIDENTS[incident_id] = replace(incident, status=status)


def list_incidents() -> tuple[Incident, ...]:
    return tuple(_INCIDENTS.values())


def clear_incidents_for_tests() -> None:
    _INCIDENTS.clear()


__all__ = [
    'Incident',
    'IncidentStatus',
    'clear_incidents_for_tests',
    'list_incidents',
    'open_incident',
    'update_incident_status',
]
