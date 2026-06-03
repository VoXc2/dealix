"""Retainer gate — proof, health, recurrence, value, stakeholder (Ultimate Manual §16)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UltimateRetainerGate:
    proof_score: int
    client_health: int
    workflow_recurring: bool
    monthly_value_clear: bool
    stakeholder_engaged: bool


def ultimate_retainer_gate_passes(g: UltimateRetainerGate) -> bool:
    return (
        g.proof_score >= 80
        and g.client_health >= 70
        and g.workflow_recurring
        and g.monthly_value_clear
        and g.stakeholder_engaged
    )
