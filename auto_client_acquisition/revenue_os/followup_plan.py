"""Follow-up cadence labels for governed outreach (draft-only; no sends)."""

from __future__ import annotations


def default_follow_up_plan_bullets() -> list[str]:
    return ["D+3 check-in draft", "D+7 value recap", "D+14 proof review"]


__all__ = ["default_follow_up_plan_bullets"]
