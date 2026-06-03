"""Productization gate from Ultimate Manual §18."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProductizationGateInput:
    manual_step_repeated: int
    time_hours_per_project: float
    linked_to_paid_offer: bool
    reduces_risk_or_improves_margin: bool
    testable: bool
    reusable: bool


def productization_gate_passes(p: ProductizationGateInput) -> bool:
    return (
        p.manual_step_repeated >= 3
        and p.time_hours_per_project >= 2.0
        and p.linked_to_paid_offer
        and p.reduces_risk_or_improves_margin
        and p.testable
        and p.reusable
    )
