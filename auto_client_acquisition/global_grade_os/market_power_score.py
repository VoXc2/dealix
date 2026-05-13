"""Market Power Score — composite + sustained-quarter rule.

See ``docs/global_grade/MARKET_POWER_SCORE.md``. Builds on the endgame
layer ``market_power.py`` indicators.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.market_power import (
    MARKET_POWER_INDICATORS,
    MarketPowerIndicator,
    MarketPowerReading,
    MIN_SUSTAINED_INDICATORS,
    MIN_SUSTAINED_QUARTERS,
)


@dataclass(frozen=True)
class MarketPowerScoreReading:
    """A composite reading derived from a list of quarterly readings."""

    quarter: str
    sustained_count: int
    sustained: frozenset[MarketPowerIndicator]
    escalation_recommended: bool


@dataclass(frozen=True)
class MarketPowerScore:
    """Multi-quarter market power state."""

    history: tuple[MarketPowerScoreReading, ...]

    def latest(self) -> MarketPowerScoreReading | None:
        return self.history[-1] if self.history else None

    def is_escalation_recommended(self) -> bool:
        latest = self.latest()
        return bool(latest and latest.escalation_recommended)


def compute_market_power_score(
    readings: tuple[MarketPowerReading, ...],
) -> MarketPowerScore:
    """Compute the score across the provided quarterly readings."""

    history: list[MarketPowerScoreReading] = []
    for idx, reading in enumerate(readings):
        tail = readings[max(0, idx - MIN_SUSTAINED_QUARTERS + 1) : idx + 1]
        if len(tail) < MIN_SUSTAINED_QUARTERS:
            sustained = frozenset()
        else:
            common = set(tail[0].sustained)
            for prior in tail[1:]:
                common &= prior.sustained
            sustained = frozenset(common)
        escalation = len(sustained) >= MIN_SUSTAINED_INDICATORS
        history.append(
            MarketPowerScoreReading(
                quarter=reading.quarter,
                sustained_count=len(sustained),
                sustained=sustained,
                escalation_recommended=escalation,
            )
        )
    return MarketPowerScore(history=tuple(history))


__all__ = [
    "MarketPowerScore",
    "MarketPowerScoreReading",
    "compute_market_power_score",
    "MARKET_POWER_INDICATORS",
]
