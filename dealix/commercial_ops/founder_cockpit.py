"""Unified founder cockpit — one read model for full autonomous self-serve ops."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.autonomous_ops import (
    BENCHMARK_COMPARISON_AR,
    build_autonomous_ops_status,
    load_last_autonomous_run,
)
from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot
from dealix.commercial_ops.founder_max_ops_backlog import summarize_backlog
from dealix.commercial_ops.founder_strongest_ops import build_strongest_ops_snapshot
from dealix.commercial_ops.full_ops_autopilot import (
    RESEARCH_ALIGNMENT_AR,
    build_full_autonomous_ops_snapshot,
    run_morning_core,
)
from dealix.commercial_ops.paths import REPO_ROOT

# HITL spectrum — external GTM consensus 2026 (not legal advice).
HITL_RESEARCH_2026_AR: list[dict[str, str]] = [
    {
        "level": "AI يقترح — المؤسس ينفّذ",
        "when_ar": "تجريب قناة جديدة",
        "dealix": "War Room + مسودات لمسة",
    },
    {
        "level": "AI يمسود — المؤسس يوافق (موصى به)",
        "when_ar": "LinkedIn · Gmail · واتساب warm",
        "dealix": "/ops/approvals + message_sent_manual",
    },
    {
        "level": "AI ينفّذ — المؤسس يراجع عينة",
        "when_ar": "بعد 10+ صفقات مُرمّزة",
        "dealix": "توسيع targeting/social idempotent فقط",
    },
    {
        "level": "AI مستقل كامل",
        "when_ar": "غير مناسب لـ B2B سعودي مبكر",
        "dealix": "ممنوع — لا cold WhatsApp/LinkedIn",
    },
]


def build_founder_cockpit(
    *,
    top_n: int = 15,
    strongest_ops_mode: str = "morning",
) -> dict[str, Any]:
    """Single Ops UI payload — compare benchmarks, run morning, see blockers."""
    n = max(1, min(top_n, 30))
    mode = strongest_ops_mode if strongest_ops_mode in ("morning", "evening", "weekly", "full") else "morning"
    strongest = build_strongest_ops_snapshot(mode=mode, run_checks=False)  # type: ignore[arg-type]
    full_ops = build_full_autonomous_ops_snapshot(
        top_n=n,
        include_nested=False,
        include_value_plan=False,
    )
    autonomous = build_autonomous_ops_status(abm_top_n=n)
    autopilot = build_autopilot_snapshot()
    backlog = summarize_backlog()

    readiness = _cockpit_verdict(strongest, full_ops, autopilot, autonomous, backlog)
    cadence = (autopilot.get("comprehensive_plan") or strongest.get("comprehensive") or {}).get(
        "daily_cadence"
    )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "schema_version": "1.0",
        "cockpit_verdict": readiness["verdict"],
        "cockpit_summary_ar": readiness["summary_ar"],
        "next_actions_ar": readiness["next_actions_ar"][:12],
        "founder_only_actions_ar": full_ops.get("founder_only_actions_ar"),
        "automation_readiness": full_ops.get("automation_readiness"),
        "comprehensive_plan": full_ops.get("comprehensive_plan"),
        "gtm_stack": full_ops.get("gtm_stack"),
        "research_alignment": RESEARCH_ALIGNMENT_AR,
        "benchmark_rows": autonomous.get("benchmark_comparison_ar") or BENCHMARK_COMPARISON_AR,
        "comparison_note_ar": autonomous.get("comparison_note_ar"),
        "technical_expansion_ready": autonomous.get("technical_expansion_ready"),
        "hitl_spectrum_2026_ar": HITL_RESEARCH_2026_AR,
        "human_only_ar": autonomous.get("human_only_ar"),
        "daily_cadence": cadence,
        "last_unified_day": _load_last_artifact("unified_founder_day_"),
        "last_autonomous_run": load_last_autonomous_run(),
        "strongest_ops": strongest,
        "full_autonomous_ops": full_ops,
        "governed_autopilot": autopilot,
        "max_ops_backlog": backlog,
        "autonomous_last_run": autonomous.get("last_run"),
        "commands": {
            **(full_ops.get("commands") or {}),
            "unified_day": "py -3 scripts/run_dealix_unified_founder_day.py",
            "strongest_ops_morning": "py -3 scripts/run_founder_strongest_ops.py --morning",
            "strongest_ops_full": "py -3 scripts/run_founder_strongest_ops.py --full --run-checks",
            "dealix_full_autonomous": "py -3 scripts/run_dealix_full_autonomous_ops.py",
            "complete_autonomous_day": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "complete_autonomous_api": "POST /api/v1/ops-autopilot/founder/complete-autonomous-day/run",
            "cockpit_api": "GET /api/v1/ops-autopilot/founder/cockpit",
            "run_morning_api": "POST /api/v1/ops-autopilot/founder/cockpit/run-morning",
            "run_unified_api": "POST /api/v1/ops-autopilot/founder/cockpit/run-unified-day",
            "run_evening_api": "POST /api/v1/ops-autopilot/founder/cockpit/run-evening",
            "run_weekly_api": "POST /api/v1/ops-autopilot/founder/cockpit/run-weekly",
            "complete_day_cli": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "one_command": "bash scripts/founder_one_command.sh",
            "verify_stack": "py -3 scripts/verify_full_autonomous_ops_stack.py",
        },
        "policy_ar": strongest.get("policy_ar"),
        "docs": [
            "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
            "docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md",
            "docs/commercial/GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md",
        ],
    }


def run_cockpit_morning(
    *,
    top_n: int = 15,
    run_optional_scripts: bool = True,
) -> dict[str, Any]:
    """Execute governed morning core + refresh cockpit snapshot."""
    morning = run_morning_core(top_n=top_n, run_optional_scripts=run_optional_scripts)
    cockpit = build_founder_cockpit(top_n=top_n, strongest_ops_mode="morning")
    cockpit["morning_run"] = morning
    cockpit["cockpit_verdict"] = _morning_cockpit_verdict(morning.get("verdict"))
    return cockpit


def _load_last_artifact(prefix: str) -> dict[str, Any] | None:
    from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR

    if not FOUNDER_BRIEFS_DIR.is_dir():
        return None
    files = sorted(FOUNDER_BRIEFS_DIR.glob(f"{prefix}*.json"), reverse=True)
    if not files:
        return None
    try:
        import json

        return json.loads(files[0].read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def run_cockpit_evening(*, top_n: int = 15) -> dict[str, Any]:
    """Evening cadence — reminder + strongest ops evening brief (no external send)."""
    from dealix.commercial_ops.evidence_append import evening_reminder_ar
    from dealix.commercial_ops.founder_strongest_ops import (
        build_strongest_ops_snapshot,
        write_strongest_ops_brief,
    )

    paths = write_strongest_ops_brief(mode="evening", run_checks=False)
    snap = build_strongest_ops_snapshot(mode="evening", run_checks=False)
    cockpit = build_founder_cockpit(top_n=top_n, strongest_ops_mode="evening")
    cockpit["evening_run"] = {
        "verdict": snap.get("verdict"),
        "reminder_ar": evening_reminder_ar(),
        "brief_paths": paths,
    }
    if not (snap.get("cadence") or {}).get("evidence_logged_today"):
        cockpit["cockpit_verdict"] = "NEEDS_FOUNDER"
        cockpit["cockpit_summary_ar"] = (
            cockpit.get("cockpit_summary_ar") or ""
        ) + " · سجّل أدلة اليوم."
    return cockpit


def run_cockpit_weekly(
    *,
    top_n: int = 15,
    run_optional_scripts: bool = True,
) -> dict[str, Any]:
    """Weekly cadence — strongest ops weekly + optional scorecard script."""
    import sys

    from dealix.commercial_ops.founder_strongest_ops import (
        build_strongest_ops_snapshot,
        write_strongest_ops_brief,
    )

    paths = write_strongest_ops_brief(mode="weekly", run_checks=run_optional_scripts)
    snap = build_strongest_ops_snapshot(mode="weekly", run_checks=run_optional_scripts)
    scorecard: dict[str, Any] = {"skipped": True}
    if run_optional_scripts:
        from dealix.commercial_ops.full_ops_autopilot import _run_script

        scorecard = _run_script("scripts/founder_weekly_scorecard.py")

    weekly_loop: dict[str, Any] = {"skipped": True}
    if run_optional_scripts:
        from dealix.commercial_ops.full_ops_autopilot import _run_script
        from dealix.commercial_ops.paths import REPO_ROOT

        if sys.platform == "win32":
            weekly_loop = (
                _run_script("scripts/founder_weekly_loop.ps1")
                if (REPO_ROOT / "scripts/founder_weekly_loop.ps1").is_file()
                else {"skipped": True}
            )
        elif (REPO_ROOT / "scripts/founder_weekly_loop.sh").is_file():
            weekly_loop = _run_script("scripts/founder_weekly_loop.sh")

    cockpit = build_founder_cockpit(top_n=top_n, strongest_ops_mode="weekly")
    cockpit["weekly_run"] = {
        "verdict": snap.get("verdict"),
        "brief_paths": paths,
        "scorecard": scorecard,
        "weekly_loop": weekly_loop,
    }
    return cockpit


def run_cockpit_unified_day(
    *,
    top_n: int = 15,
    quick: bool = False,
    run_optional_scripts: bool = True,
) -> dict[str, Any]:
    """Full unified founder day (in-process) + refreshed cockpit."""
    from dealix.commercial_ops.unified_founder_day import run_unified_founder_day

    unified = run_unified_founder_day(
        quick=quick,
        top_n=top_n,
        run_commercial_subprocess=not quick,
        run_optional_scripts=run_optional_scripts,
    )
    cockpit = build_founder_cockpit(top_n=top_n, strongest_ops_mode="morning")
    cockpit["unified_day_run"] = unified
    cockpit["morning_run"] = next(
        (p.get("detail") for p in unified.get("phases") or [] if "Morning core" in str(p.get("label"))),
        None,
    )
    cockpit["cockpit_verdict"] = _morning_cockpit_verdict(unified.get("verdict"))
    cockpit["comprehensive_plan"] = unified.get("comprehensive_plan")
    return cockpit


def run_cockpit_complete_autonomous_day(
    *,
    top_n: int = 15,
    weekly: bool = False,
    evening: bool = False,
    skip_commercial_day: bool = False,
    use_unified_in_process: bool = True,
) -> dict[str, Any]:
    """Maximum governed day (subprocess + in-process) + refreshed cockpit."""
    from dealix.commercial_ops.complete_autonomous_day import run_complete_autonomous_day

    payload = run_complete_autonomous_day(
        weekly=weekly,
        evening=evening,
        skip_commercial_day=skip_commercial_day,
        use_unified_in_process=use_unified_in_process,
        top_n=top_n,
    )
    mode = "full" if weekly else "morning"
    cockpit = build_founder_cockpit(top_n=top_n, strongest_ops_mode=mode)
    cockpit["complete_autonomous_day"] = payload
    v = payload.get("verdict")
    if v == "PASS":
        cockpit["cockpit_verdict"] = "AUTONOMOUS_READY"
    elif v == "DEGRADED":
        cockpit["cockpit_verdict"] = "AUTONOMOUS_PARTIAL"
    else:
        cockpit["cockpit_verdict"] = "NEEDS_FOUNDER"
    cockpit["cockpit_summary_ar"] = (
        (cockpit.get("cockpit_summary_ar") or "")
        + f" · يوم ذاتي كامل: {v}"
    ).strip()
    return cockpit


def _morning_cockpit_verdict(run_verdict: str | None) -> str:
    if run_verdict == "PASS":
        return "AUTONOMOUS_READY"
    if run_verdict in ("PARTIAL", "DEGRADED"):
        return "AUTONOMOUS_PARTIAL"
    return "NEEDS_FOUNDER"


def _cockpit_verdict(
    strongest: dict[str, Any],
    full_ops: dict[str, Any],
    autopilot: dict[str, Any],
    autonomous: dict[str, Any],
    backlog: dict[str, Any],
) -> dict[str, Any]:
    actions: list[str] = []
    blockers = 0

    plan_st = (strongest.get("strongest_plan") or {}).get("status") or {}
    if not plan_st.get("ok"):
        blockers += 1
        actions.append("أصلح wiring أقوى خطة: founder_strongest_plan_status.py")

    av = (autopilot.get("verdict") or {}).get("level")
    if av == "RED":
        blockers += 2
    elif av == "YELLOW":
        blockers += 1
    for item in (autopilot.get("queue") or [])[:4]:
        t = item.get("title_ar")
        if t:
            actions.append(t)

    for line in full_ops.get("founder_only_actions_ar") or []:
        if line and line not in actions:
            actions.append(line)

    for w in strongest.get("warnings_ar") or []:
        if w not in actions:
            actions.append(w)

    if blockers >= 2:
        verdict = "NEEDS_FOUNDER"
        summary = "أوقف التوسع — أغلق البوابة والأدلة أولاً"
    elif blockers == 1 or backlog.get("verdict") == "OPEN":
        verdict = "AUTONOMOUS_PARTIAL"
        summary = (
            "أقصى أتمتة ممكنة للتحضير (War Room · مسودات · أدلة) — "
            "الإرسال والإغلاق لك فقط"
        )
    else:
        verdict = "AUTONOMOUS_READY"
        summary = RESEARCH_ALIGNMENT_AR.get("verdict_ar") or "جاهز للتشغيل الذاتي بحوكمة"

    return {
        "verdict": verdict,
        "summary_ar": summary,
        "next_actions_ar": [a for a in actions if a][:12],
    }
