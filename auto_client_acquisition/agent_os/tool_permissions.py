"""Tool permissions — hard-blocked + allowed lists for MVP agents.

These are non-negotiable. Even if an agent card lists a forbidden tool
in `allowed_tools`, `is_tool_allowed()` returns False.
"""
from __future__ import annotations

ALLOWED_MVP_TOOLS = frozenset({
    "read",
    "analyze",
    "draft",
    "recommend",
    "queue_for_approval",
    "search_internal",
    "compute_score",
    "render_markdown",
    "validate_schema",
})

FORBIDDEN_MVP_TOOLS = frozenset({
    "send_email",
    "send_whatsapp",
    "send_sms",
    "linkedin_post",
    "linkedin_message",
    "scrape_web",
    "scrape_linkedin",
    "scrape_email",
    "export_pii",
    "purchase_data",
    "bulk_blast",
    "auto_charge_payment",
})


def is_tool_allowed(tool_name: str, *, allowed_tools: list[str] | None = None) -> tuple[bool, str]:
    """Hard rule:
       - If tool in FORBIDDEN list → (False, "hard-blocked tool in MVP").
       - Else if `allowed_tools` provided and tool not in it → (False, "not in agent's allowed_tools").
       - Else if tool in ALLOWED_MVP_TOOLS → (True, "").
       - Else → (False, "tool not in MVP allowlist").
    """
    name = tool_name.strip().lower()
    if name in FORBIDDEN_MVP_TOOLS:
        return False, f"tool {name!r} is hard-blocked in MVP (Dealix non-negotiable)"
    if allowed_tools is not None and name not in {t.lower() for t in allowed_tools}:
        return False, f"tool {name!r} not in agent's allowed_tools"
    if name in ALLOWED_MVP_TOOLS:
        return True, ""
    return False, f"tool {name!r} not in MVP allowlist {sorted(ALLOWED_MVP_TOOLS)}"


__all__ = ["ALLOWED_MVP_TOOLS", "FORBIDDEN_MVP_TOOLS", "is_tool_allowed"]
