"""Strategic bets — one-to-three monthly bets taxonomy."""

from __future__ import annotations

STRATEGIC_BET_TYPES: tuple[str, ...] = (
    "revenue_bet",
    "product_bet",
    "trust_bet",
    "distribution_bet",
    "enterprise_bet",
    "venture_bet",
)


def strategic_bet_type_valid(bet_type: str) -> bool:
    return bet_type in STRATEGIC_BET_TYPES
