"""Per-tool permission matrix.

Tools that need explicit gates:
  - moyasar_charge_live   → requires DEALIX_MOYASAR_MODE=live
  - whatsapp_send_live    → BLOCKED (NO_LIVE_SEND)
  - linkedin_automate     → BLOCKED (NO_LINKEDIN_AUTO)
  - email_send_live       → requires gate + approval
  - scrape_external       → BLOCKED (NO_SCRAPING)
  - public_post           → requires approval
"""
from __future__ import annotations

import os
from typing import Any

# Tool registry — what each tool needs to be permitted
_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "moyasar_charge_live": {
        "permitted": False,  # default
        "requires_env": ["DEALIX_MOYASAR_MODE=live"],
        "blocked_unless_env": True,
    },
    "moyasar_charge_test": {
        "permitted": True,
        "requires_env": [],
        "blocked_unless_env": False,
    },
    "whatsapp_send_live": {
        "permitted": False,
        "requires_env": [],
        "always_blocked": True,
        "block_reason": "NO_LIVE_SEND constitutional gate",
    },
    "whatsapp_template_internal": {
        "permitted": True,
        "requires_env": [],
        "blocked_unless_env": False,
    },
    "linkedin_automate": {
        "permitted": False,
        "requires_env": [],
        "always_blocked": True,
        "block_reason": "NO_LINKEDIN_AUTO constitutional gate",
    },
    "email_send_live": {
        "permitted": False,
        "requires_env": [],
        "requires_approval": True,
    },
    "scrape_external": {
        "permitted": False,
        "requires_env": [],
        "always_blocked": True,
        "block_reason": "NO_SCRAPING constitutional gate",
    },
    "public_post": {
        "permitted": False,
        "requires_env": [],
        "requires_approval": True,
    },
    "internal_brief": {
        "permitted": True,
        "requires_env": [],
        "blocked_unless_env": False,
    },
}


def check_tool_permission(
    *,
    tool_name: str,
    has_human_approval: bool = False,
) -> dict[str, Any]:
    """Returns {permitted, reason, action_mode}."""
    tool = _TOOL_REGISTRY.get(tool_name)
    if tool is None:
        return {
            "permitted": False,
            "reason": f"unknown_tool:{tool_name}",
            "action_mode": "blocked",
        }

    if tool.get("always_blocked"):
        return {
            "permitted": False,
            "reason": tool.get("block_reason", "always_blocked"),
            "action_mode": "blocked",
        }

    if tool.get("blocked_unless_env"):
        env_required = tool.get("requires_env", [])
        for var_spec in env_required:
            if "=" in var_spec:
                var, expected = var_spec.split("=", 1)
                if os.environ.get(var) != expected:
                    return {
                        "permitted": False,
                        "reason": f"env_required:{var_spec}",
                        "action_mode": "blocked",
                    }

    if tool.get("requires_approval"):
        if not has_human_approval:
            return {
                "permitted": False,
                "reason": "human_approval_required",
                "action_mode": "approval_required",
            }
        # Has explicit human approval → permitted as approved_manual
        return {
            "permitted": True,
            "reason": "approved_with_human_approval",
            "action_mode": "approved_manual",
        }

    if tool.get("permitted"):
        return {
            "permitted": True,
            "reason": "tool_in_allowed_set",
            "action_mode": "draft_only",
        }

    return {
        "permitted": False,
        "reason": "tool_not_permitted_by_default",
        "action_mode": "blocked",
    }
