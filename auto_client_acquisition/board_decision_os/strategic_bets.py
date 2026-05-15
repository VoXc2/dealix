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


class StrategicBetsError(ValueError):
    """Raised when monthly strategic bet constraints are violated."""


def validate_monthly_bets(inp: "StrategicBetsInput", *, max_bets: int = 3) -> "StrategicBetsInput":
    from auto_client_acquisition.board_decision_os.schemas import StrategicBetsInput

    if len(inp.bets) > max_bets:
        raise StrategicBetsError(f"At most {max_bets} bets per month; got {len(inp.bets)}")
    if len(inp.bets) == 0:
        raise StrategicBetsError("Provide at least one bet for the month")
    return inp
