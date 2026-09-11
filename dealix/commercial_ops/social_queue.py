"""Social content queue — current Dealix corporate drafts only (no auto-publish)."""

from __future__ import annotations

import os
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.doctrine import SOAEN_CHECKLIST_AR
from dealix.commercial_ops.paths import SOCIAL_QUEUE_YAML

CURRENT_LAUNCH_AUTHORITY = "corporate_brand_gtm_v1"

# Historical content remains in YAML/Git history as an audit trail, but it must
# never become today's draft after the parent-company GTM authority changed.
_RETIRED_COMMERCIAL_TOKENS = (
    "4,999",
    "15,000",
    "1,500",
    "2,999",
    "499 ر.س",
    "499 sar",
    "sprint 499",
    "data pack 1500",
    "growth 2999",
    "risk score",
    "أول diagnostic مدفوع",
    "first-paid-diagnostic",
    "diagnostic → sprint",
    "diagnostic + proof",
    "10-lead-audit",
    "10 leads",
    "/ar/risk-score",
    "/ar/proof-pack",
)


def _post_text(post: dict[str, Any]) -> str:
    return "\n".join(
        str(post.get(key) or "")
        for key in ("title_ar", "body_ar", "cta_ar", "cta", "aeo_slug")
    ).casefold()


def is_current_launch_safe_post(post: dict[str, Any]) -> bool:
    """Return False when a draft carries a retired offer/price/funnel token."""
    text = _post_text(post)
    return not any(token.casefold() in text for token in _RETIRED_COMMERCIAL_TOKENS)


def _is_selectable_post(post: dict[str, Any]) -> bool:
    """Only exact current-authority, not-yet-published rows can become today's draft."""
    return (
        str(post.get("launch_authority") or "") == CURRENT_LAUNCH_AUTHORITY
        and is_current_launch_safe_post(post)
        and (post.get("status") or "draft") != "published"
    )


def load_social_queue(path: Path | None = None) -> dict[str, Any]:
    p = path or SOCIAL_QUEUE_YAML
    if not p.is_file():
        return {"posts": []}
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {"posts": []}
    if not isinstance(data, dict):
        raise ValueError("social content queue root must be a mapping")
    posts = data.get("posts") or []
    if not isinstance(posts, list):
        raise ValueError("social content queue posts must be a list")
    return data


def get_post_for_date(
    on_date: date | None = None,
    *,
    queue: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Pick a current-authority draft by anchor week + weekday (Sun=0 .. Sat=6).

    Legacy authority, unsafe historical or already-published posts are excluded
    even when they match today's slot. If no current corporate draft remains,
    return ``None`` rather than resurrecting stale content.
    """
    data = queue if queue is not None else load_social_queue()
    posts: list[dict[str, Any]] = [
        dict(post)
        for post in (data.get("posts") or [])
        if isinstance(post, dict) and _is_selectable_post(post)
    ]
    if not posts:
        return None

    d = on_date or datetime.now(UTC).date()
    anchor_raw = str(data.get("anchor_date") or "2026-09-13").strip()
    try:
        anchor = date.fromisoformat(anchor_raw[:10])
    except ValueError:
        anchor = date(2026, 9, 13)
    num_weeks = max(1, int(data.get("cycle_weeks") or 8))
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
            return {
                **post,
                "calendar_date": d.isoformat(),
                "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
            }
    return {
        **posts[0],
        "calendar_date": d.isoformat(),
        "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
    }


def format_linkedin_draft(post: dict[str, Any]) -> str:
    """Format a safe internal draft; never format legacy authority or retired copy."""
    if str(post.get("launch_authority") or "") != CURRENT_LAUNCH_AUTHORITY:
        raise ValueError("refusing to format social draft with legacy launch authority")
    if not is_current_launch_safe_post(post):
        raise ValueError("refusing to format social draft with retired commercial authority")
    title = post.get("title_ar") or ""
    body = post.get("body_ar") or ""
    cta = post.get("cta_ar") or post.get("cta") or ""
    lines = [
        title,
        "",
        body,
        "",
        f"➡️ {cta}",
        "",
        "— Dealix · Strategy + Systems + Intelligence + Products · Revenue + Proof + Command",
        "(مسودة داخلية — Approval-first، راجع SOAEN قبل أي نشر)",
    ]
    return "\n".join(lines)


def _atomic_dump_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write YAML atomically so parallel readers never observe a partial file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)

        with temp_path.open(encoding="utf-8") as handle:
            validated = yaml.safe_load(handle)
        if not isinstance(validated, dict) or not isinstance(validated.get("posts"), list):
            raise ValueError("refusing to replace social queue with invalid YAML")

        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def mark_post_status(
    *,
    week: int,
    day: int,
    status: str,
    path: Path | None = None,
) -> dict[str, Any]:
    """Update a current-authority queue row atomically. This never publishes externally."""
    allowed = {"draft", "approved", "published"}
    if status not in allowed:
        raise ValueError(f"status must be one of {allowed}")
    p = path or SOCIAL_QUEUE_YAML
    data = load_social_queue(p)
    posts: list[dict[str, Any]] = list(data.get("posts") or [])

    matching_indexes = [
        idx
        for idx, post in enumerate(posts)
        if int(post.get("week", 0)) == week and int(post.get("day", -1)) == day
    ]
    if not matching_indexes:
        raise KeyError(f"no post for week={week} day={day}")

    editable_index = next(
        (
            idx
            for idx in matching_indexes
            if str(posts[idx].get("launch_authority") or "") == CURRENT_LAUNCH_AUTHORITY
            and is_current_launch_safe_post(posts[idx])
            and (posts[idx].get("status") or "draft") != "published"
        ),
        None,
    )
    if editable_index is None:
        raise ValueError(
            "refusing to approve/publish: no safe unpublished current-authority row"
        )

    posts[editable_index]["status"] = status
    data["posts"] = posts
    _atomic_dump_yaml(p, data)
    return {"week": week, "day": day, "status": status, "updated": True}
