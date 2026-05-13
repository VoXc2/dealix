"""Strategic bets — bounded monthly bets with validation."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import StrategicBetsInput


class StrategicBetsError(ValueError):
    pass


def validate_monthly_bets(inp: StrategicBetsInput, *, max_bets: int = 3) -> StrategicBetsInput:
    if len(inp.bets) > max_bets:
        raise StrategicBetsError(f"At most {max_bets} bets per month; got {len(inp.bets)}")
    if len(inp.bets) == 0:
        raise StrategicBetsError("Provide at least one bet for the month")
    return inp
