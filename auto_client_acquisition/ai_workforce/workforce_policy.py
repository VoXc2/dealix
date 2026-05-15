"""Hard-rule policy enforcement on every AgentTask.

Two checks run after each agent body returns:
  1. Tool veto — if any forbidden_tools appear referenced in the
     task's output as an ACTION (a value the agent intends to USE),
     the task is flipped to ``action_mode=blocked``.
  2. Forbidden marketing tokens — ``نضمن`` / ``guaranteed`` / ``blast``
     / ``scrape`` in any rendered string flips the task to blocked.

The tool scan deliberately skips fields whose KEY identifies the
value as something explicitly LISTED-as-blocked (``blocked_channels``,
``vetoed_tools``, ``forbidden_*``, ``excludes``). These fields surface
the exact tokens to communicate that they are off-limits — penalising
that would block legitimate, defensive output.

This is the last line of defense before ComplianceGuardAgent runs.
"""
from __future__ import annotations

import json
import re
from typing import Any

from auto_client_acquisition.ai_workforce.schemas import AgentTask, RiskLevel

# Hard-rule tool tokens that NO task may carry as a live action.
HARD_RULE_TOOLS: tuple[str, ...] = (
    "cold_whatsapp",
    "linkedin_automation",
    "scrape_web",
    "send_email_live",
    "send_whatsapp_live",
    "charge_payment_live",
)


# Keys whose values are EXPECTED to enumerate forbidden tokens (as a
# safety policy declaration). Tokens here don't count as "used".
_BLOCKED_LIST_KEYS: frozenset[str] = frozenset({
    "blocked_channels",
    "blocked_tools",
    "vetoed_tools",
    "forbidden_tools",
    "forbidden_channels",
    "excludes",
    "blocked",
})


# Forbidden marketing claim tokens.
_FORBIDDEN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"نضمن"),
    re.compile(r"\bguaranteed\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\bscrape\b", re.IGNORECASE),
)


def _stringify(value: Any) -> str:
    """Best-effort stringify for scanning."""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        return str(value)


def _scan_for_active_tool_token(value: Any, parent_key: str | None = None) -> str | None:
    """Recursive scan that ignores values nested under a blocked-list key.

    Returns the first hard-rule token found in an ACTIVE (non-listing)
    position, or None.
    """
    if parent_key is not None and parent_key in _BLOCKED_LIST_KEYS:
        return None

    if isinstance(value, dict):
        for k, v in value.items():
            hit = _scan_for_active_tool_token(v, parent_key=str(k))
            if hit is not None:
                return hit
        return None

    if isinstance(value, (list, tuple, set)):
        for item in value:
            hit = _scan_for_active_tool_token(item, parent_key=parent_key)
            if hit is not None:
                return hit
        return None

    text = value if isinstance(value, str) else _stringify(value)
    for token in HARD_RULE_TOOLS:
        if token in text:
            return token
    return None


def _has_forbidden_marketing(task: AgentTask) -> str | None:
    fields = (
        task.action_summary_ar,
        task.action_summary_en,
        _stringify(task.output),
    )
    for field in fields:
        if not field:
            continue
        for pat in _FORBIDDEN_PATTERNS:
            if pat.search(field):
                return pat.pattern
    return None


def apply_policy(task: AgentTask) -> AgentTask:
    """Veto a task if it references a forbidden tool or marketing claim.

    The ComplianceGuardAgent legitimately exposes the technical veto
    list (it IS the policy declaration), so it is exempt from BOTH the
    tool-token scan and any nested-value heuristics.
    """
    if task.agent_id == "ComplianceGuardAgent":
        return task

    bad_tool = _scan_for_active_tool_token(task.output)
    if bad_tool is not None:
        return task.model_copy(update={
            "action_mode": "blocked",
            "approval_status": "blocked",
            "risk_level": RiskLevel.BLOCKED.value,
            "action_summary_en": (
                f"blocked by policy: forbidden tool token '{bad_tool}' present"
            ),
        })

    bad_token = _has_forbidden_marketing(task)
    if bad_token is not None:
        return task.model_copy(update={
            "action_mode": "blocked",
            "approval_status": "blocked",
            "risk_level": RiskLevel.BLOCKED.value,
            "action_summary_en": (
                f"blocked by policy: forbidden marketing token '{bad_token}'"
            ),
        })

    return task
