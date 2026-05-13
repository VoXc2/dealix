"""Board Memo — twelve-question monthly leadership memo.

See ``docs/strategic_control/BOARD_MEMO_TEMPLATE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BoardMemoSection(str, Enum):
    SOLD = "what_did_we_sell"
    DELIVERED = "what_did_we_deliver"
    PROVED = "what_did_we_prove"
    RISKS_BLOCKED = "what_risks_did_we_block"
    ASSETS_CREATED = "what_assets_did_we_create"
    PRODUCTIZATION_CANDIDATES = "what_repeated_enough_to_productize"
    RETAINER_READY = "which_client_is_ready_for_retainer"
    SHOULD_SCALE = "which_service_should_scale"
    SHOULD_STOP = "which_service_should_stop"
    MARKET_SIGNAL = "which_market_signal_matters"
    UNIT_MATURING = "which_unit_is_maturing"
    NEXT_STRATEGIC_BET = "what_is_the_next_strategic_bet"


BOARD_MEMO_SECTIONS: tuple[BoardMemoSection, ...] = tuple(BoardMemoSection)


_SECTION_TITLES: dict[BoardMemoSection, str] = {
    BoardMemoSection.SOLD: "1. What did we sell?",
    BoardMemoSection.DELIVERED: "2. What did we deliver?",
    BoardMemoSection.PROVED: "3. What did we prove?",
    BoardMemoSection.RISKS_BLOCKED: "4. What risks did we block?",
    BoardMemoSection.ASSETS_CREATED: "5. What assets did we create?",
    BoardMemoSection.PRODUCTIZATION_CANDIDATES: "6. What repeated enough to productize?",
    BoardMemoSection.RETAINER_READY: "7. Which client is ready for retainer?",
    BoardMemoSection.SHOULD_SCALE: "8. Which service should scale?",
    BoardMemoSection.SHOULD_STOP: "9. Which service should stop?",
    BoardMemoSection.MARKET_SIGNAL: "10. Which market signal matters?",
    BoardMemoSection.UNIT_MATURING: "11. Which unit is maturing?",
    BoardMemoSection.NEXT_STRATEGIC_BET: "12. What is the next strategic bet?",
}


@dataclass(frozen=True)
class BoardMemo:
    period: str  # e.g. "2026-05"
    author: str
    sections: dict[BoardMemoSection, str]

    def __post_init__(self) -> None:
        missing = set(BOARD_MEMO_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_board_memo_sections:"
                + ",".join(sorted(s.value for s in missing))
            )


def render_board_memo(memo: BoardMemo) -> str:
    """Render the memo to a stable Markdown string.

    The output format is fixed so the memo is comparable across months.
    """

    parts: list[str] = [f"# Dealix Board Memo — {memo.period}", "", f"Author: {memo.author}", ""]
    for section in BOARD_MEMO_SECTIONS:
        parts.append(f"## {_SECTION_TITLES[section]}")
        parts.append("")
        parts.append(memo.sections[section].strip() or "none")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
