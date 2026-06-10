"""Monthly board memo — section completeness."""

from __future__ import annotations

from collections.abc import Mapping

BOARD_MEMO_SECTIONS: tuple[str, ...] = (
    "executive_summary",
    "revenue",
    "retainers",
    "proof",
    "governance",
    "capital_creation",
    "productization",
    "delivery",
    "market",
    "business_units",
    "stop_list",
    "next_strategic_bet",
)


def board_memo_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k for k in BOARD_MEMO_SECTIONS if not (content_by_section.get(k) or "").strip()
    ]
    return not missing, tuple(missing)


def build_board_memo_markdown_skeleton(*, title: str = "Dealix Board Memo") -> str:
    """Twelve-section monthly memo — empty prompts for leadership fill-in."""
    lines = [
        f"# {title}",
        "",
        "## 1. Executive Summary",
        "What moved the company forward this month?",
        "",
        "## 2. Revenue",
        "What sold? What did not sell? What has pricing power?",
        "",
        "## 3. Retainers",
        "Which clients are ready to continue or expand?",
        "",
        "## 4. Proof",
        "What did we prove? Which Proof Packs can support sales?",
        "",
        "## 5. Governance",
        "What risks were blocked? Any incidents? Any new rules?",
        "",
        "## 6. Capital Creation",
        "What assets were created? What can be reused?",
        "",
        "## 7. Productization",
        "What repeated enough to become a tool or feature?",
        "",
        "## 8. Delivery",
        "Where did QA succeed or fail? Where did scope creep appear?",
        "",
        "## 9. Market",
        "What language are clients using? Any inbound signals?",
        "",
        "## 10. Business Units",
        "Which unit is maturing: Revenue, Brain, Governance, Operations?",
        "",
        "## 11. Stop List",
        "What should we stop selling, building, or supporting?",
        "",
        "## 12. Next Strategic Bet",
        "What is the highest-leverage move next?",
        "",
    ]
    return "\n".join(lines)
