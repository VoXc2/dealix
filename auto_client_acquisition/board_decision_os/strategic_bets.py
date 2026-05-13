"""Strategic Bets — 1..3 per month across six bet kinds."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StrategicBetKind(str, Enum):
    REVENUE = "revenue"
    PRODUCT = "product"
    TRUST = "trust"
    DISTRIBUTION = "distribution"
    ENTERPRISE = "enterprise"
    VENTURE = "venture"


STRATEGIC_BET_KINDS: tuple[StrategicBetKind, ...] = tuple(StrategicBetKind)


@dataclass(frozen=True)
class StrategicBet:
    period: str
    kind: StrategicBetKind
    description: str
    owner: str


def validate_bet_count(bets: tuple[StrategicBet, ...]) -> tuple[bool, str | None]:
    """Doctrine: 1..3 bets per period; more is dilution."""

    if not 1 <= len(bets) <= 3:
        return (False, f"bet_count_out_of_range:{len(bets)}")
    periods = {b.period for b in bets}
    if len(periods) != 1:
        return (False, "bets_must_share_one_period")
    return (True, None)
