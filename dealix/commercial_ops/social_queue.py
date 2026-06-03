"""Social content queue — today's draft post (no auto-publish)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.doctrine import SOAEN_CHECKLIST_AR
from dealix.commercial_ops.paths import SOCIAL_QUEUE_YAML


def load_social_queue(path: Path | None = None) -> dict[str, Any]:
    p = path or SOCIAL_QUEUE_YAML
    if not p.is_file():
        return {"posts": []}
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {"posts": []}


def get_post_for_date(
    on_date: date | None = None,
    *,
    queue: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Pick post by anchor week + weekday (Sun=0 .. Sat=6)."""
    data = queue if queue is not None else load_social_queue()
    posts: list[dict[str, Any]] = list(data.get("posts") or [])
    if not posts:
        return None

    d = on_date or datetime.now(UTC).date()
    anchor_raw = (data.get("anchor_date") or "2026-05-17").strip()
    try:
        anchor = date.fromisoformat(anchor_raw[:10])
    except ValueError:
        anchor = date(2026, 5, 17)
    num_weeks = max(1, int(data.get("cycle_weeks") or 4))
    week_num = ((d - anchor).days // 7) % num_weeks + 1
    day_index = (d.weekday() + 1) % 7  # Sun=0

    for post in posts:
        if int(post.get("week", 0)) == week_num and int(post.get("day", -1)) == day_index:
            return {
                **post,
                "calendar_date": d.isoformat(),
                "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
            }

    for post in posts:
        if (post.get("status") or "draft") == "draft":
            return {**post, "calendar_date": d.isoformat(), "soaen_checklist_ar": SOAEN_CHECKLIST_AR}
    return {**posts[0], "calendar_date": d.isoformat(), "soaen_checklist_ar": SOAEN_CHECKLIST_AR}


def format_linkedin_draft(post: dict[str, Any]) -> str:
    title = post.get("title_ar") or ""
    body = post.get("body_ar") or ""
    cta = post.get("cta_ar") or post.get("cta") or ""
    lines = [title, "", body, "", f"➡️ {cta}", "", "— Dealix · Post-Lead Revenue Ops (مسودة — راجع SOAEN قبل النشر)"]
    return "\n".join(lines)


def mark_post_status(
    *,
    week: int,
    day: int,
    status: str,
    path: Path | None = None,
) -> dict[str, Any]:
    """Update queue YAML status (draft | approved | published). Does not publish externally."""
    allowed = {"draft", "approved", "published"}
    if status not in allowed:
        raise ValueError(f"status must be one of {allowed}")
    p = path or SOCIAL_QUEUE_YAML
    data = load_social_queue(p)
    posts: list[dict[str, Any]] = list(data.get("posts") or [])
    hit = False
    for post in posts:
        if int(post.get("week", 0)) == week and int(post.get("day", -1)) == day:
            post["status"] = status
            hit = True
            break
    if not hit:
        raise KeyError(f"no post for week={week} day={day}")
    data["posts"] = posts
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    return {"week": week, "day": day, "status": status, "updated": True}
