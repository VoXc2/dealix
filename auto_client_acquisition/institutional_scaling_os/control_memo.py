"""Monthly institutional control memo — section completeness."""

from __future__ import annotations

from collections.abc import Mapping

CONTROL_MEMO_SECTIONS: tuple[str, ...] = (
    "revenue",
    "proof",
    "trust",
    "productization",
    "capital",
    "clients",
    "units",
    "market",
    "stop_list",
    "strategic_bet",
)


def control_memo_complete(content_by_section: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k for k in CONTROL_MEMO_SECTIONS if not (content_by_section.get(k) or "").strip()
    ]
    return not missing, tuple(missing)


def build_control_memo_markdown_skeleton(*, title: str = "Dealix Institutional Control Memo") -> str:
    """Monthly board-level memo — empty sections for founder/CEO fill-in."""
    lines = [
        f"# {title}",
        "",
        "## 1. Revenue",
        "What did we sell? What is recurring?",
        "",
        "## 2. Proof",
        "What did we prove? Which proof can support sales?",
        "",
        "## 3. Trust",
        "What risks did we block? Any incidents?",
        "",
        "## 4. Productization",
        "What repeated enough to become a tool?",
        "",
        "## 5. Capital",
        "What assets did we create?",
        "",
        "## 6. Clients",
        "Who is expansion-ready? Who is risky?",
        "",
        "## 7. Units",
        "Which business unit is maturing?",
        "",
        "## 8. Market",
        "What language is the market adopting?",
        "",
        "## 9. Stop List",
        "What should we stop selling, building, or supporting?",
        "",
        "## 10. Strategic Bet",
        "What is the next high-leverage move?",
        "",
    ]
    return "\n".join(lines)
