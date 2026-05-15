"""Tool boundary vocabulary for governed agents (MVP deny-list).

Doctrine: forbidden tools are hard-blocked regardless of autonomy level —
no scraping, no cold WhatsApp, no LinkedIn automation, no bulk PII export,
no live external send.
"""

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


def _norm(tool: str) -> str:
    return tool.strip().lower()


def is_tool_allowed(
    tool: str,
    allowed_tools: Iterable[str] | None = None,
) -> tuple[bool, str]:
    """Decide whether a tool may be used.

    Returns ``(allowed, reason)``. Forbidden tools are hard-blocked. When an
    ``allowed_tools`` list is supplied the tool must appear in it; otherwise
    the tool must be part of the MVP allow-vocabulary.
    """
    t = _norm(tool)
    if t in FORBIDDEN_TOOLS_MVP:
        return False, f"hard-blocked: {t} is a forbidden tool"
    if allowed_tools is not None:
        permitted = {_norm(a) for a in allowed_tools}
        if t not in permitted:
            return False, f"not-permitted: {t} not in agent allowed_tools"
        return True, "ok"
    if t in ALLOWED_TOOLS_MVP:
        return True, "ok"
    return False, f"not-permitted: {t} not in MVP tool vocabulary"


def tool_allowed_mvp(tool: str) -> bool:
    """Legacy boolean gate — preserved for secure_agent_runtime_os callers."""
    return is_tool_allowed(tool)[0]


def forbidden_tools_in(tools: Iterable[str]) -> list[str]:
    """Return the subset of ``tools`` that are on the forbidden deny-list."""
    return sorted({_norm(t) for t in tools} & FORBIDDEN_TOOLS_MVP)


__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "forbidden_tools_in",
    "is_tool_allowed",
    "tool_allowed_mvp",
]
