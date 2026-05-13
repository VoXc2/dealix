"""Kill System — when and why to stop.

See ``docs/endgame/KILL_SYSTEM.md``. Kill is preferred to drift.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class KillTarget(str, Enum):
    SERVICE = "service"
    FEATURE = "feature"
    MARKET = "market"
    VENTURE = "venture"


class KillDecision(str, Enum):
    KILL = "kill"
    PAUSE = "pause"
    RECOMMIT = "recommit"


@dataclass(frozen=True)
class KillCriteria:
    """The objective signals that trigger a kill review.

    Producers fill the fields that apply to the target type. Fields left
    at their defaults do not contribute to a kill score.
    """

    target_type: KillTarget

    # Service signals
    low_win_rate: bool = False
    low_margin: bool = False
    high_scope_creep: bool = False
    weak_proof: bool = False
    no_retainer_path: bool = False
    high_governance_risk: bool = False
    not_repeatable: bool = False

    # Feature signals
    not_reused: bool = False
    not_tied_to_revenue_proof_or_governance: bool = False
    maintenance_exceeds_value: bool = False
    does_not_reduce_delivery_effort: bool = False

    # Market signals
    buyer_unclear: bool = False
    weak_budget: bool = False
    too_long_sales_cycle: bool = False
    data_risk_too_high: bool = False
    no_proof_path: bool = False

    # Venture signals
    missed_milestones: bool = False
    forks_core_os: bool = False
    no_retainers_in_stage: bool = False
    consumes_operator_time_without_capital_return: bool = False


# A KILL is recommended when at least this many target-relevant signals
# are present. PAUSE is the fallback when at least one signal is present
# but the threshold is not met.
_KILL_THRESHOLD: dict[KillTarget, int] = {
    KillTarget.SERVICE: 3,
    KillTarget.FEATURE: 2,
    KillTarget.MARKET: 3,
    KillTarget.VENTURE: 2,
}


def _service_signals(c: KillCriteria) -> int:
    return sum(
        (
            c.low_win_rate,
            c.low_margin,
            c.high_scope_creep,
            c.weak_proof,
            c.no_retainer_path,
            c.high_governance_risk,
            c.not_repeatable,
        )
    )


def _feature_signals(c: KillCriteria) -> int:
    return sum(
        (
            c.not_reused,
            c.not_tied_to_revenue_proof_or_governance,
            c.maintenance_exceeds_value,
            c.does_not_reduce_delivery_effort,
        )
    )


def _market_signals(c: KillCriteria) -> int:
    return sum(
        (
            c.buyer_unclear,
            c.weak_budget,
            c.too_long_sales_cycle,
            c.data_risk_too_high,
            c.no_proof_path,
        )
    )


def _venture_signals(c: KillCriteria) -> int:
    return sum(
        (
            c.missed_milestones,
            c.forks_core_os,
            c.no_retainers_in_stage,
            c.consumes_operator_time_without_capital_return,
        )
    )


_COUNTERS = {
    KillTarget.SERVICE: _service_signals,
    KillTarget.FEATURE: _feature_signals,
    KillTarget.MARKET: _market_signals,
    KillTarget.VENTURE: _venture_signals,
}


def evaluate_kill(criteria: KillCriteria) -> KillDecision:
    """Return the kill decision implied by the criteria.

    A venture that forks the Core OS is killed unconditionally — that
    behavior is constitutional under the doctrine.
    """

    if (
        criteria.target_type is KillTarget.VENTURE
        and criteria.forks_core_os
    ):
        return KillDecision.KILL

    signals = _COUNTERS[criteria.target_type](criteria)
    threshold = _KILL_THRESHOLD[criteria.target_type]

    if signals >= threshold:
        return KillDecision.KILL
    if signals >= 1:
        return KillDecision.PAUSE
    return KillDecision.RECOMMIT
