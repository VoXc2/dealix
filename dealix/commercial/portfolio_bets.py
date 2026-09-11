"""Portfolio of Bets — exploration vs exploitation, DeepWIP 3."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from dealix.commercial.probability_engine import EconomicBet, BetState, ProbBand

class PortfolioBets(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bets: list[EconomicBet] = []
    exploration_budget_pct: int = 15  # 10-20% for cheap experiments

    def add(self, bet: EconomicBet) -> None:
        self.bets.append(bet)

    def active_deep(self) -> list[EconomicBet]:
        return [b for b in self.bets if b.state == BetState.ACTIVE_DEEP]

    def can_promote_to_deep(self) -> bool:
        return len(self.active_deep()) < 3

    def rank(self) -> list[EconomicBet]:
        # Rank by expected_chain_value / (cost+time+founder) with exploration bonus for cheap tests
        def score(b: EconomicBet) -> float:
            chain = b.expected_chain_value()
            cost = b.cost_to_test_sar + b.delivery_cost_sar + b.founder_minutes*5 + b.time_to_cash_days*10
            base = chain / max(1, cost)
            # exploration bonus for CHEAP_TEST
            if b.state == BetState.CHEAP_TEST:
                base *= 1.2
            return base
        return sorted(self.bets, key=lambda b: score(b), reverse=True)

    def top3(self) -> list[EconomicBet]:
        return self.rank()[:3]

    def kill_zombies(self) -> list[str]:
        killed = []
        for b in self.bets:
            if b.state not in (BetState.KILLED, BetState.SCALING) and b.next_review < datetime.now(UTC).isoformat() and not b.expected_value_sar:
                b.state = BetState.KILLED
                killed.append(b.bet_id)
        return killed

    def to_dict(self) -> dict[str, Any]:
        return {"total": len(self.bets), "active_deep": len(self.active_deep()), "ranked": [b.bet_id for b in self.rank()]}

__all__ = ["PortfolioBets", "EconomicBet", "BetState"]
