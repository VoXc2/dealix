"""Infer strongest-plan task completion from evidence, cadence, and repo signals."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_daily_cadence,
    analyze_weekly_one_decision,
)
from dealix.commercial_ops.founder_strongest_plan import load_strongest_plan_checklist
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT, WAR_ROOM_TODAY_JSON

CompletionStatus = str  # done | due_today | open | blocked

RuleFn = Callable[[dict[str, Any]], bool]


def _brief_exists_today(prefix: str) -> bool:
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    return (FOUNDER_BRIEFS_DIR / f"{prefix}_{day}.md").is_file()


def build_completion_context() -> dict[str, Any]:
    """Signals used to mark checklist tasks done / due (no invented CRM numbers)."""
    rows = load_evidence_rows()
    evidence = count_evidence_events(rows, exclude_placeholders=True)
    cadence = analyze_daily_cadence()
    weekly = analyze_weekly_one_decision()
    today = datetime.now(UTC).date()
    war_room_mtime_ok = False
    if WAR_ROOM_TODAY_JSON.is_file():
        mtime = datetime.fromtimestamp(
            WAR_ROOM_TODAY_JSON.stat().st_mtime, tz=UTC
        ).date()
        war_room_mtime_ok = mtime == today

    return {
        "date": today.isoformat(),
        "weekday": today.weekday(),
        "is_friday": today.weekday() == 4,
        "evidence_today": int(evidence.get("today_total") or 0),
        "evidence_logged_today": bool(cadence.get("evidence_logged_today")),
        "weekly_decision_ok": weekly.get("verdict") not in ("MISSING", "STALE"),
        "war_room_today": war_room_mtime_ok,
        "strongest_ops_brief_today": _brief_exists_today("strongest_ops"),
        "autopilot_brief_today": _brief_exists_today("autopilot"),
        "value_plan_brief_today": _brief_exists_today("value_plan"),
        "pack_index_today": (
            FOUNDER_BRIEFS_DIR / f"DAILY_PACK_{datetime.now(UTC).strftime('%Y-%m-%d')}.md"
        ).is_file(),
    }


def _rules() -> dict[str, RuleFn]:
    ctx_default: dict[str, Any] = {}

    def c(ctx: dict[str, Any] | None = None) -> dict[str, Any]:
        return ctx if ctx is not None else ctx_default

    return {
        "t01": lambda ctx: bool(ctx.get("weekly_decision_ok")),
        "t05": lambda ctx: bool(ctx.get("strongest_ops_brief_today") or ctx.get("pack_index_today")),
        "t07": lambda ctx: bool(ctx.get("war_room_today")),
        "t08": lambda ctx: bool(ctx.get("evidence_logged_today")),
        "t09": lambda ctx: bool(ctx.get("evidence_today") >= 1),
        "t10": lambda ctx: bool(ctx.get("is_friday") and ctx.get("strongest_ops_brief_today")),
        "t11": lambda ctx: bool(ctx.get("strongest_ops_brief_today")),
        "t52": lambda ctx: bool(ctx.get("weekly_decision_ok")),
        "t55": lambda ctx: bool(ctx.get("strongest_ops_brief_today")),
        "t56": lambda ctx: bool(ctx.get("evidence_logged_today")),
        "t58": lambda ctx: bool(ctx.get("evidence_logged_today")),
        "t59": lambda ctx: bool(ctx.get("autopilot_brief_today") or ctx.get("value_plan_brief_today")),
        "t68": lambda ctx: bool(ctx.get("pack_index_today")),
        "t94": lambda ctx: bool(ctx.get("war_room_today")),
        "t109": lambda ctx: bool(ctx.get("war_room_today") and ctx.get("value_plan_brief_today")),
        "t110": lambda ctx: bool(ctx.get("autopilot_brief_today")),
        "t111": lambda ctx: bool(ctx.get("strongest_ops_brief_today")),
        "t117": lambda ctx: True,  # wiring checked separately in summary
        "t121": lambda ctx: bool(ctx.get("pack_index_today")),
    }


_DAILY_SECTIONS = frozenset({"daily", "motion_a", "content"})
_WEEKLY_SECTIONS = frozenset({"weekly", "week0", "research", "autonomous_ops"})


def infer_task_completion(
    task: dict[str, Any],
    ctx: dict[str, Any],
    *,
    wiring_ok: bool = True,
) -> dict[str, Any]:
    """Per-task completion for UI and briefs."""
    tid = str(task.get("id") or "")
    rules = _rules()
    if tid == "t117":
        done = wiring_ok
    elif tid in rules:
        done = rules[tid](ctx)
    else:
        done = False

    section = str(task.get("section") or "")
    if done:
        status: CompletionStatus = "done"
        reason_ar = "إشارة تشغيل أو أدلة اليوم"
    elif section in _DAILY_SECTIONS:
        status = "due_today"
        reason_ar = "مطلوب في إيقاع اليوم"
    elif section in _WEEKLY_SECTIONS and ctx.get("weekday") in (6, 0):
        status = "due_today"
        reason_ar = "مراجعة أسبوعية (أحد/اثنين)"
    elif section in _WEEKLY_SECTIONS and ctx.get("is_friday"):
        status = "due_today"
        reason_ar = "جمعة — scorecard/ريترو"
    else:
        status = "open"
        reason_ar = "عند الحاجة أو مرحلة نشطة"

    return {
        "status": status,
        "done": done,
        "reason_ar": reason_ar,
    }


def enrich_checklist_with_completion(
    *,
    wiring_ok: bool | None = None,
) -> dict[str, Any]:
    """Attach completion to all checklist tasks + rollup."""
    from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status

    st = strongest_plan_status()
    ok = wiring_ok if wiring_ok is not None else bool(st.get("ok"))
    ctx = build_completion_context()
    checklist = load_strongest_plan_checklist()
    tasks_out: list[dict[str, Any]] = []

    for task in checklist.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        comp = infer_task_completion(task, ctx, wiring_ok=ok)
        tasks_out.append({**task, "completion": comp})

    done_n = sum(1 for t in tasks_out if (t.get("completion") or {}).get("done"))
    due_n = sum(
        1
        for t in tasks_out
        if (t.get("completion") or {}).get("status") == "due_today"
        and not (t.get("completion") or {}).get("done")
    )
    open_n = len(tasks_out) - done_n - due_n

    return {
        "context": ctx,
        "tasks": tasks_out,
        "summary": {
            "total": len(tasks_out),
            "done": done_n,
            "due_today": due_n,
            "open": open_n,
            "percent_done": round(100.0 * done_n / len(tasks_out), 1) if tasks_out else 0.0,
            "percent_due_or_done": round(100.0 * (done_n + due_n) / len(tasks_out), 1)
            if tasks_out
            else 0.0,
        },
        "policy_ar": (
            "«منجز» = إشارة أدلة/تشغيل حقيقية — لا يعني إرسالاً خارجياً أو إغلاق صفقة."
        ),
    }
