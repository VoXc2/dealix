"""Venture factory gate — no spinout without traction + Core OS."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VentureGateChecklist:
    paid_clients_5plus: bool
    retainers_2plus: bool
    repeatable_delivery: bool
    product_module_clear: bool
    playbook_maturity_80plus: bool
    owner_exists: bool
    healthy_margin: bool
    proof_library_exists: bool
    core_os_dependency_clear: bool


def venture_gate_passes(c: VentureGateChecklist) -> bool:
    return all(
        (
            c.paid_clients_5plus,
            c.retainers_2plus,
            c.repeatable_delivery,
            c.product_module_clear,
            c.playbook_maturity_80plus,
            c.owner_exists,
            c.healthy_margin,
            c.proof_library_exists,
            c.core_os_dependency_clear,
        ),
    )
