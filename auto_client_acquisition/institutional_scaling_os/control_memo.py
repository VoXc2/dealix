"""Monthly Institutional Control Memo — 10 sections."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class InstitutionalControlMemoSection(str, Enum):
    REVENUE = "revenue"
    PROOF = "proof"
    TRUST = "trust"
    PRODUCTIZATION = "productization"
    CAPITAL = "capital"
    CLIENTS = "clients"
    UNITS = "units"
    MARKET = "market"
    STOP_LIST = "stop_list"
    STRATEGIC_BET = "strategic_bet"


CONTROL_MEMO_SECTIONS: tuple[InstitutionalControlMemoSection, ...] = tuple(
    InstitutionalControlMemoSection
)


_TITLES: dict[InstitutionalControlMemoSection, str] = {
    InstitutionalControlMemoSection.REVENUE: "1. Revenue",
    InstitutionalControlMemoSection.PROOF: "2. Proof",
    InstitutionalControlMemoSection.TRUST: "3. Trust",
    InstitutionalControlMemoSection.PRODUCTIZATION: "4. Productization",
    InstitutionalControlMemoSection.CAPITAL: "5. Capital",
    InstitutionalControlMemoSection.CLIENTS: "6. Clients",
    InstitutionalControlMemoSection.UNITS: "7. Units",
    InstitutionalControlMemoSection.MARKET: "8. Market",
    InstitutionalControlMemoSection.STOP_LIST: "9. Stop List",
    InstitutionalControlMemoSection.STRATEGIC_BET: "10. Strategic Bet",
}


@dataclass(frozen=True)
class InstitutionalControlMemo:
    period: str
    author: str
    sections: dict[InstitutionalControlMemoSection, str]

    def __post_init__(self) -> None:
        missing = set(CONTROL_MEMO_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_control_memo_sections:"
                + ",".join(sorted(s.value for s in missing))
            )


def render_control_memo(memo: InstitutionalControlMemo) -> str:
    parts = [
        f"# Dealix Institutional Control Memo — {memo.period}",
        "",
        f"Author: {memo.author}",
        "",
    ]
    for section in CONTROL_MEMO_SECTIONS:
        parts.append(f"## {_TITLES[section]}")
        parts.append("")
        parts.append(memo.sections[section].strip() or "none")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
