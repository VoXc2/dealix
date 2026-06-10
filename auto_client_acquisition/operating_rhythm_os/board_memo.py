"""Monthly board memo — section slugs for rhythm template (12 sections)."""

from __future__ import annotations

from collections.abc import Mapping

MONTHLY_BOARD_MEMO_SECTIONS: tuple[str, ...] = (
    "executive_summary",
    "revenue_quality",
    "proof_and_value",
    "governance_and_incidents",
    "client_adoption",
    "productization",
    "capital_assets_created",
    "market_intelligence",
    "business_unit_maturity",
    "stop_kill_decisions",
    "capital_allocation",
    "next_strategic_bets",
)


def monthly_board_memo_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k for k in MONTHLY_BOARD_MEMO_SECTIONS if not (content_by_section.get(k) or "").strip()
    ]
    return not missing, tuple(missing)
