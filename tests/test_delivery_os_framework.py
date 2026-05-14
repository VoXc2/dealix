"""Delivery OS — phases and checklists."""

from __future__ import annotations

from auto_client_acquisition.delivery_os import (
    DEFAULT_PHASE_CHECKLISTS,
    DeliveryPhase,
    phases_in_order,
)


def test_eight_phases_in_order() -> None:
    phases = phases_in_order()
    assert len(phases) == 8
    assert phases[0] == DeliveryPhase.DISCOVER
    assert phases[-1] == DeliveryPhase.EXPAND


def test_each_phase_has_checklist() -> None:
    for p in phases_in_order():
        assert p in DEFAULT_PHASE_CHECKLISTS
        assert len(DEFAULT_PHASE_CHECKLISTS[p]) >= 1
