"""Tool boundary vocabulary for governed agents (MVP deny-list)."""

from __future__ import annotations

FORBIDDEN_TOOLS_MVP: frozenset[str] = frozenset(
    {
        "send_email",
        "send_whatsapp",
        "web_scrape",
        "linkedin_automation",
        "export_pii_bulk",
    },
)

ALLOWED_TOOLS_MVP: frozenset[str] = frozenset(
    {
        "read",
        "analyze",
        "draft",
        "recommend",
        "queue_for_approval",
    },
)


def tool_allowed_mvp(tool: str) -> bool:
    t = tool.strip().lower()
    if t in FORBIDDEN_TOOLS_MVP:
        return False
    return t in ALLOWED_TOOLS_MVP


__all__ = ["ALLOWED_TOOLS_MVP", "FORBIDDEN_TOOLS_MVP", "tool_allowed_mvp"]
