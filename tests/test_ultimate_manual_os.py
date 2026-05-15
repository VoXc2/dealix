"""Tests for ultimate_manual_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.ultimate_manual_os import (
    ProductizationGateInput,
    UltimateRetainerGate,
    productization_gate_passes,
    ultimate_decision_tier,
    ultimate_retainer_gate_passes,
)


def test_decision_tiers() -> None:
    assert ultimate_decision_tier(0) == "do_not"
    assert ultimate_decision_tier(3) == "cautious"
    assert ultimate_decision_tier(4) == "priority"
    assert ultimate_decision_tier(6) == "strategic_bet"


def test_decision_invalid() -> None:
    with pytest.raises(ValueError):
        ultimate_decision_tier(7)


def test_productization_gate() -> None:
    ok = ProductizationGateInput(
        manual_step_repeated=5,
        time_hours_per_project=3.0,
        linked_to_paid_offer=True,
        reduces_risk_or_improves_margin=True,
        testable=True,
        reusable=True,
    )
    assert productization_gate_passes(ok)
    bad = ProductizationGateInput(
        manual_step_repeated=2,
        time_hours_per_project=1.0,
        linked_to_paid_offer=True,
        reduces_risk_or_improves_margin=True,
        testable=True,
        reusable=True,
    )
    assert not productization_gate_passes(bad)


def test_retainer_gate() -> None:
    g = UltimateRetainerGate(
        proof_score=85,
        client_health=75,
        workflow_recurring=True,
        monthly_value_clear=True,
        stakeholder_engaged=True,
    )
    assert ultimate_retainer_gate_passes(g)
    assert not ultimate_retainer_gate_passes(
        UltimateRetainerGate(85, 75, True, True, False),
    )
