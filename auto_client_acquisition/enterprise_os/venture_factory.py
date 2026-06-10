"""Venture Factory — hard gate checklist (counts and booleans)."""

from __future__ import annotations

from typing import NamedTuple


class VentureGateInputs(NamedTuple):
    paid_clients: int
    retainers: int
    delivery_repeatable: bool
    product_module_used: bool
    playbook_maturity: float
    owner_exists: bool
    gross_margin_healthy: bool
    proof_library_exists: bool


def meets_venture_gate(inputs: VentureGateInputs) -> bool:
    """Institutional venture gate — all conditions must hold."""
    return (
        inputs.paid_clients >= 5
        and inputs.retainers >= 2
        and inputs.delivery_repeatable
        and inputs.product_module_used
        and inputs.playbook_maturity >= 80.0
        and inputs.owner_exists
        and inputs.gross_margin_healthy
        and inputs.proof_library_exists
    )
