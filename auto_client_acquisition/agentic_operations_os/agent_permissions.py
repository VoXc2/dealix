"""Agent permissions — least privilege, MVP tool classes."""

from __future__ import annotations

from enum import StrEnum


class ToolClass(StrEnum):
    READ_ONLY = "A"
    ANALYSIS = "B"
    DRAFT = "C"
    INTERNAL_WRITE = "D"
    EXTERNAL_ACTION = "E"
    HIGH_RISK = "F"


FORBIDDEN_TOOL_SLUGS: frozenset[str] = frozenset(
    {
        "send_email",
        "send_whatsapp",
        "scrape_web",
        "linkedin_automation",
        "export_pii",
        "bulk_outreach",
    }
)


def tool_class_allowed_in_mvp(
    tool_class: ToolClass,
    *,
    internal_write_approved: bool,
) -> bool:
    """MVP: A/B/C allowed; D only with approval; E/F blocked."""
    if tool_class in (ToolClass.READ_ONLY, ToolClass.ANALYSIS, ToolClass.DRAFT):
        return True
    if tool_class == ToolClass.INTERNAL_WRITE:
        return internal_write_approved
    return False


def agent_tool_forbidden(tool_slug: str) -> bool:
    return tool_slug.lower() in {s.lower() for s in FORBIDDEN_TOOL_SLUGS}


def permission_change_requires_audit(_old: frozenset[str], _new: frozenset[str]) -> bool:
    """Any permission delta must be audited (contract flag for callers)."""
    return True
