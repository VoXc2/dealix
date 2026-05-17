"""No-Build Gate — do not build a feature unless it earns the right.

Build is permitted only when at least one condition holds:
  - a customer asked for it
  - a workflow repeated >= 3 times
  - it reduces a real risk
  - it speeds up paid delivery
  - it opens a retainer

Otherwise: sell, deliver, measure, learn. Do not build.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

WORKFLOW_REPEAT_THRESHOLD = 3


class BuildReason(StrEnum):
    CUSTOMER_REQUESTED = "customer_requested"
    WORKFLOW_REPEATED = "workflow_repeated_3x"
    REDUCES_REAL_RISK = "reduces_real_risk"
    SPEEDS_PAID_DELIVERY = "speeds_paid_delivery"
    OPENS_RETAINER = "opens_retainer"


@dataclass(frozen=True, slots=True)
class NoBuildDecision:
    should_build: bool
    directive: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def no_build_decision(
    *,
    customer_requested: bool = False,
    workflow_repeat_count: int = 0,
    reduces_real_risk: bool = False,
    speeds_paid_delivery: bool = False,
    opens_retainer: bool = False,
) -> NoBuildDecision:
    """Evaluate whether a proposed build is justified."""
    reasons: list[str] = []
    if customer_requested:
        reasons.append(BuildReason.CUSTOMER_REQUESTED.value)
    if workflow_repeat_count >= WORKFLOW_REPEAT_THRESHOLD:
        reasons.append(BuildReason.WORKFLOW_REPEATED.value)
    if reduces_real_risk:
        reasons.append(BuildReason.REDUCES_REAL_RISK.value)
    if speeds_paid_delivery:
        reasons.append(BuildReason.SPEEDS_PAID_DELIVERY.value)
    if opens_retainer:
        reasons.append(BuildReason.OPENS_RETAINER.value)

    should_build = bool(reasons)
    directive = "BUILD" if should_build else "SELL_DELIVER_MEASURE_LEARN"
    return NoBuildDecision(
        should_build=should_build,
        directive=directive,
        reasons=tuple(reasons),
    )


__all__ = [
    "WORKFLOW_REPEAT_THRESHOLD",
    "BuildReason",
    "NoBuildDecision",
    "no_build_decision",
]
