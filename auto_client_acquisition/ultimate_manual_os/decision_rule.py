"""Six-question decision rule — how many «yes» answers dictate the tier."""

from __future__ import annotations

from typing import Literal

DealixDecisionTier = Literal["do_not", "cautious", "priority", "strategic_bet"]


def ultimate_decision_tier(yes_count: int) -> DealixDecisionTier:
    """Maps count of affirmative answers (0–6) to tier."""
    if yes_count < 0 or yes_count > 6:
        msg = f"yes_count must be 0..6, got {yes_count}"
        raise ValueError(msg)
    if yes_count <= 2:
        return "do_not"
    if yes_count == 3:
        return "cautious"
    if yes_count == 4:
        return "priority"
    return "strategic_bet"
