"""Approval matrix — deterministic risk routing."""

from __future__ import annotations

from typing import Literal

Risk = Literal["low", "medium", "high"]


def approval_for_action(action: str) -> tuple[Risk, str]:
    a = action.lower().strip()
    if "whatsapp" in a or "cold_whatsapp" in a:
        return "high", "human+consent"
    if "linkedin" in a and "automation" in a:
        return "high", "blocked"
    if "send" in a and "email" in a:
        return "medium", "human"
    if "pii" in a or "personal" in a:
        return "high", "lawful_basis_required"
    if "publish" in a or "claim" in a:
        return "medium", "claim_qa"
    return "low", "auto"
