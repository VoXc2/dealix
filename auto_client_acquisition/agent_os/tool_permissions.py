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
    *,
    allowed_tools: list[str] | None = None,
) -> tuple[bool, str]:
    """Check whether a tool may be used, returning ``(ok, reason)``.

    A tool on the MVP deny-list is always hard-blocked. Otherwise the tool
    must be in the MVP allow-list and, if an explicit ``allowed_tools``
    grant is provided, in that grant too.
    """
    t = tool.strip().lower()
    if t in FORBIDDEN_TOOLS_MVP:
        return False, f"tool '{t}' is hard-blocked by the MVP deny-list"
    if t not in ALLOWED_TOOLS_MVP:
        return False, f"tool '{t}' is not in the MVP allow-list"
    if allowed_tools is not None:
        grant = {x.strip().lower() for x in allowed_tools}
        if t not in grant:
            return False, f"tool '{t}' is not in this agent's allowed_tools"
    return True, "allowed"


__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "is_tool_allowed",
    "tool_allowed_mvp",
]
