"""Weekly content calendar — typed shell, every post is approval_required."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.growth_v10.schemas import WeeklyContentCalendar


def build_calendar(week_label: str, planned_posts: list[dict[str, Any]] | None = None) -> WeeklyContentCalendar:
    """Build a WeeklyContentCalendar; every post is forced approval_required."""
    posts: list[dict[str, Any]] = []
    for raw in (planned_posts or []):
        item = dict(raw)
        item["approval_required"] = True  # platform-level — cannot be overridden
        posts.append(item)
    return WeeklyContentCalendar(
        week_label=week_label,
        planned_posts=posts,
        approval_required=True,
    )
