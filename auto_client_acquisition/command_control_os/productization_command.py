"""Productization Command — gate + path from manual to SaaS module.

See ``docs/command_control/PRODUCTIZATION_COMMAND.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ProductizationStep(IntEnum):
    MANUAL = 0
    TEMPLATE = 1
    SCRIPT = 2
    INTERNAL_TOOL = 3
    CLIENT_FEATURE = 4
    SAAS_MODULE = 5


@dataclass(frozen=True)
class ProductizationCandidate:
    name: str
    current_step: ProductizationStep
    manual_step_repeated: int
    time_cost_hours_per_project: float
    linked_to_paid_offer: bool
    reduces_risk_or_improves_margin: bool
    testable: bool
    reusable: bool


@dataclass(frozen=True)
class ProductizationGate:
    passes: bool
    failed_checks: tuple[str, ...]
    next_step: ProductizationStep | None


_MIN_REPEATED: int = 3
_MIN_TIME_HOURS: float = 2.0


def evaluate_productization(candidate: ProductizationCandidate) -> ProductizationGate:
    failures: list[str] = []
    if candidate.manual_step_repeated < _MIN_REPEATED:
        failures.append("manual_step_repeated_below_threshold")
    if candidate.time_cost_hours_per_project < _MIN_TIME_HOURS:
        failures.append("time_cost_below_threshold")
    if not candidate.linked_to_paid_offer:
        failures.append("not_linked_to_paid_offer")
    if not candidate.reduces_risk_or_improves_margin:
        failures.append("no_risk_or_margin_improvement")
    if not candidate.testable:
        failures.append("not_testable")
    if not candidate.reusable:
        failures.append("not_reusable")

    if failures or candidate.current_step is ProductizationStep.SAAS_MODULE:
        return ProductizationGate(
            passes=not failures,
            failed_checks=tuple(failures),
            next_step=None if failures else None,
        )

    next_step = ProductizationStep(candidate.current_step + 1)
    return ProductizationGate(
        passes=True,
        failed_checks=(),
        next_step=next_step,
    )
