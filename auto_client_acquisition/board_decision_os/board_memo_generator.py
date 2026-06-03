"""Board memo — section taxonomy for monthly board narrative."""

from __future__ import annotations

BOARD_MEMO_SECTIONS: tuple[str, ...] = (
    "executive_summary",
    "revenue_quality",
    "proof_and_value",
    "retainer_opportunities",
    "governance_and_risk",
    "productization_queue",
    "client_health",
    "market_intelligence",
    "business_unit_maturity",
    "stop_kill_list",
    "capital_allocation",
    "next_strategic_bets",
)


def board_memo_sections_complete(sections_present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [s for s in BOARD_MEMO_SECTIONS if s not in sections_present]
    return not missing, tuple(missing)
