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


def is_tool_allowed(
    tool: str,
    allowed_tools: list[str] | None = None,
) -> tuple[bool, str]:
    """Resolve whether a tool may run.

    Forbidden tools are hard-blocked regardless of any per-agent allow-list.
    When ``allowed_tools`` is provided, the tool must also be listed there.
    """
    t = tool.strip().lower()
    if t in FORBIDDEN_TOOLS_MVP:
        return False, f"tool '{t}' is hard-blocked by MVP doctrine"
    if t not in ALLOWED_TOOLS_MVP:
        return False, f"tool '{t}' is not in the MVP allow-list"
    if allowed_tools is not None:
        normalized = {a.strip().lower() for a in allowed_tools}
        if t not in normalized:
            return False, f"tool '{t}' is not in this agent's allowed_tools"
    return True, "ok"


__all__ = ["ALLOWED_TOOLS_MVP", "FORBIDDEN_TOOLS_MVP", "is_tool_allowed", "tool_allowed_mvp"]
