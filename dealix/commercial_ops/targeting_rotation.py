"""Daily P0 target rotation from agency seed CSV — no scraping."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

import yaml

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV, ICP_AGENCY_YAML

CLOSED = {"closed_lost", "closed_won", "archived"}
STATUS_RANK = {
    "not_contacted": 5,
    "replied": 4,
    "message_drafted": 3,
    "approved_to_send": 3,
    "sent_manual": 2,
    "meeting_booked": 1,
    "scope_requested": 1,
}


def _parse_date(raw: str) -> date | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def _priority_rank(raw: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get((raw or "medium").strip().lower(), 2)


def _load_icp_defaults() -> dict[str, Any]:
    if not ICP_AGENCY_YAML.is_file():
        return {}
    data = yaml.safe_load(ICP_AGENCY_YAML.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def enrich_row(row: dict[str, str], icp: dict[str, Any]) -> dict[str, str]:
    out = dict(row)
    if not (out.get("pain_hypothesis") or "").strip() and icp.get("core_message_ar"):
        out["pain_hypothesis"] = str(icp["core_message_ar"]).strip().replace("\n", " ")[:200]
    if not (out.get("next_action") or "").strip():
        out["next_action"] = "مسودة لمسة أولى — وكالة wedge (P0)"
    if not (out.get("motion") or "").strip():
        out["motion"] = str(icp.get("motion") or "A")
    return out


def select_daily_p0_targets(
    rows: list[dict[str, str]] | None = None,
    *,
    top_n: int = 10,
    cooldown_days: int = 3,
    on_date: date | None = None,
) -> list[dict[str, str]]:
    """Pick today's P0 accounts: priority, status, cooldown since last touch."""
    from dealix.commercial_ops.targeting_csv import load_targets

    pool = rows if rows is not None else load_targets(AGENCY_TARGETS_CSV)
    today = on_date or datetime.now(UTC).date()
    cutoff = today - timedelta(days=cooldown_days)
    icp = _load_icp_defaults()

    eligible: list[dict[str, str]] = []
    for row in pool:
        st = (row.get("status") or "not_contacted").strip().lower()
        if st in CLOSED:
            continue
        seg = (row.get("segment") or "").strip().lower()
        if seg and seg not in ("agency_wedge", "agency", ""):
            pr = (row.get("priority") or "").strip().lower()
            if pr != "high":
                continue
        last = _parse_date(row.get("next_action_date") or "")
        if last is not None and last >= cutoff and st not in ("replied", "meeting_booked"):
            continue
        eligible.append(enrich_row(row, icp))

    def sort_key(r: dict[str, str]) -> tuple[int, int, str]:
        st = (r.get("status") or "not_contacted").strip().lower()
        return (
            _priority_rank(r.get("priority") or "medium"),
            STATUS_RANK.get(st, 0),
            r.get("company") or "",
        )

    eligible.sort(key=sort_key, reverse=True)
    return eligible[:top_n]


def preview_next_targets(
    rows: list[dict[str, str]] | None = None,
    *,
    top_n: int = 3,
    on_date: date | None = None,
) -> list[dict[str, str]]:
    """Preview likely P0 picks for the next calendar day (rotation planning)."""
    today = on_date or datetime.now(UTC).date()
    tomorrow = today + timedelta(days=1)
    return select_daily_p0_targets(rows, top_n=top_n, on_date=tomorrow)


def apply_rotation_touch_dates(
    rows: list[dict[str, str]],
    selected: list[dict[str, str]],
    *,
    on_date: date | None = None,
) -> list[dict[str, str]]:
    """Mark selected rows with next_action_date = today (for CSV write-back)."""
    today = (on_date or datetime.now(UTC).date()).isoformat()
    selected_keys = {(r.get("company") or "", r.get("contact") or "") for r in selected}
    out: list[dict[str, str]] = []
    for row in rows:
        key = (row.get("company") or "", row.get("contact") or "")
        if key in selected_keys:
            updated = dict(row)
            updated["next_action_date"] = today
            if (updated.get("status") or "") == "not_contacted":
                updated["status"] = "message_drafted"
            out.append(updated)
        else:
            out.append(dict(row))
    return out
