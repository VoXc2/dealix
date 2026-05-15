"""Tool boundary vocabulary for governed agents (MVP deny-list)."""

from __future__ import annotations

from collections.abc import Iterable

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
    *,
    allowed_tools: Iterable[str] | None = None,
) -> tuple[bool, str]:
    """Resolve whether a tool may run.

    The forbidden MVP deny-list always wins, even if a caller lists the
    tool in ``allowed_tools``. When ``allowed_tools`` is provided, the tool
    must also be present in that per-agent grant.
    """
    t = tool.strip().lower()
    if t in FORBIDDEN_TOOLS_MVP:
        return False, f"tool '{t}' is hard-blocked in the MVP deny-list"
    if allowed_tools is not None:
        grant = {x.strip().lower() for x in allowed_tools}
        if t not in grant:
            return False, f"tool '{t}' not in this agent's allowed_tools"
        return True, "ok"
    if t in ALLOWED_TOOLS_MVP:
        return True, "ok"
    return False, f"tool '{t}' not in the MVP allow-list"


__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "is_tool_allowed",
    "tool_allowed_mvp",
]
