"""Board Memo v12 — 12-section monthly board memo."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BoardMemoV12Section(str, Enum):
    EXECUTIVE_SUMMARY = "executive_summary"
    REVENUE = "revenue"
    RETAINERS = "retainers"
    PROOF = "proof"
    GOVERNANCE = "governance"
    CAPITAL_CREATION = "capital_creation"
    PRODUCTIZATION = "productization"
    DELIVERY = "delivery"
    MARKET = "market"
    BUSINESS_UNITS = "business_units"
    STOP_LIST = "stop_list"
    NEXT_STRATEGIC_BET = "next_strategic_bet"


BOARD_MEMO_V12_SECTIONS: tuple[BoardMemoV12Section, ...] = tuple(BoardMemoV12Section)

_TITLES: dict[BoardMemoV12Section, str] = {
    s: f"{i+1}. {s.value.replace('_', ' ').title()}"
    for i, s in enumerate(BOARD_MEMO_V12_SECTIONS)
}


@dataclass(frozen=True)
class BoardMemoV12:
    period: str
    author: str
    sections: dict[BoardMemoV12Section, str]

    def __post_init__(self) -> None:
        missing = set(BOARD_MEMO_V12_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_board_memo_v12_sections:"
                + ",".join(sorted(s.value for s in missing))
            )


def render_board_memo_v12(memo: BoardMemoV12) -> str:
    parts = [f"# Dealix Board Memo — {memo.period}", "", f"Author: {memo.author}", ""]
    for s in BOARD_MEMO_V12_SECTIONS:
        parts.append(f"## {_TITLES[s]}")
        parts.append("")
        parts.append(memo.sections[s].strip() or "none")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
