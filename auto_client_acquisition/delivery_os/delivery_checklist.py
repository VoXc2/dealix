"""Delivery checklist materialized from canonical phases."""

from __future__ import annotations

from auto_client_acquisition.delivery_os.framework import (
    DEFAULT_PHASE_CHECKLISTS,
    DeliveryPhase,
    phases_in_order,
)


def delivery_checklist_flat() -> list[tuple[str, str]]:
    """(phase, item) pairs in stable order."""
    out: list[tuple[str, str]] = []
    for phase in phases_in_order():
        for item in DEFAULT_PHASE_CHECKLISTS.get(phase, []):
            out.append((phase.value, item))
    return out


def checklist_for_phase(phase: DeliveryPhase) -> list[str]:
    return list(DEFAULT_PHASE_CHECKLISTS.get(phase, []))
