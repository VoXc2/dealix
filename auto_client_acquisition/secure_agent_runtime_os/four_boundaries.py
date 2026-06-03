"""Four boundary protection for agent runtime.

Prompts, tools, data, and context must each pass an integrity check
before an agent action is permitted. Pure functions.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class BoundaryCheck:
    boundary: str  # prompt | tool | data | context
    allowed: bool
    reason: str = ""


# Prompt injection heuristics.
_PROMPT_INJECTION_PATTERNS = (
    r"ignore (?:all )?previous instructions",
    r"disregard (?:the )?system prompt",
    r"override.*safety",
    r"reveal.*system prompt",
    r"تجاهل (?:كل )?التعليمات",
    r"اعمل.*خارج.*الحدود",
)


def check_prompt_integrity(text: str) -> BoundaryCheck:
    if not text:
        return BoundaryCheck(boundary="prompt", allowed=True)
    low = text.lower()
    for pat in _PROMPT_INJECTION_PATTERNS:
        if re.search(pat, low):
            return BoundaryCheck(
                boundary="prompt",
                allowed=False,
                reason=f"prompt_injection_pattern:{pat}",
            )
    return BoundaryCheck(boundary="prompt", allowed=True)


def check_tool_boundary(
    *,
    tool_name: str,
    allowed_tools: list[str] | None = None,
) -> BoundaryCheck:
    from auto_client_acquisition.agent_os.tool_permissions import is_tool_allowed
    ok, reason = is_tool_allowed(tool_name, allowed_tools=allowed_tools)
    return BoundaryCheck(boundary="tool", allowed=ok, reason=reason)


def check_data_boundary(
    *,
    source_passport_present: bool,
    contains_pii: bool,
    external_use: bool,
) -> BoundaryCheck:
    """Block data flowing externally without a passport or with un-approved PII."""
    if external_use and not source_passport_present:
        return BoundaryCheck(
            boundary="data",
            allowed=False,
            reason="external_use_without_source_passport",
        )
    if external_use and contains_pii:
        return BoundaryCheck(
            boundary="data",
            allowed=False,
            reason="external_pii_requires_approval",
        )
    return BoundaryCheck(boundary="data", allowed=True)


def check_context_boundary(
    *,
    cross_customer: bool,
    session_scope: str = "",
) -> BoundaryCheck:
    """Prevent context contamination across customer tenants."""
    if cross_customer:
        return BoundaryCheck(
            boundary="context",
            allowed=False,
            reason="cross_customer_context_contamination",
        )
    if not session_scope:
        return BoundaryCheck(
            boundary="context",
            allowed=False,
            reason="missing_session_scope",
        )
    return BoundaryCheck(boundary="context", allowed=True)


def check_all_boundaries(
    *,
    prompt_text: str = "",
    tool_name: str = "",
    allowed_tools: list[str] | None = None,
    source_passport_present: bool = True,
    contains_pii: bool = False,
    external_use: bool = False,
    cross_customer: bool = False,
    session_scope: str = "default",
) -> dict[str, BoundaryCheck]:
    return {
        "prompt": check_prompt_integrity(prompt_text),
        "tool": check_tool_boundary(tool_name=tool_name, allowed_tools=allowed_tools),
        "data": check_data_boundary(
            source_passport_present=source_passport_present,
            contains_pii=contains_pii,
            external_use=external_use,
        ),
        "context": check_context_boundary(
            cross_customer=cross_customer, session_scope=session_scope
        ),
    }


def all_passed(checks: dict[str, BoundaryCheck]) -> bool:
    return all(c.allowed for c in checks.values())


__all__ = [
    "BoundaryCheck",
    "all_passed",
    "check_all_boundaries",
    "check_context_boundary",
    "check_data_boundary",
    "check_prompt_integrity",
    "check_tool_boundary",
]
