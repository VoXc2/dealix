"""Autonomous founder strongest-plan ops — daily/weekly briefs, task selection, cadence hooks."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_daily_cadence,
    analyze_weekly_one_decision,
    build_comprehensive_status,
    init_weekly_decision,
)
from dealix.commercial_ops.founder_strongest_plan import (
    load_strongest_plan_checklist,
    strongest_plan_snapshot,
    strongest_plan_status,
    tasks_by_section,
)
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT

CadenceMode = Literal["morning", "evening", "weekly", "full"]

# Sections surfaced per cadence (subset of checklist — full list in YAML).
_CADENCE_SECTIONS: dict[CadenceMode, list[str]] = {
    "morning": [
        "week0",
        "daily",
        "motion_a",
        "content",
        "phase_01",
        "governance",
        "integrations",
        "finance_unit",
    ],
    "evening": ["daily", "governance", "kpi", "trust_security"],
    "weekly": [
        "week0",
        "weekly",
        "motion_a",
        "phase_01",
        "phase_24",
        "governance",
        "kpi",
        "research",
        "customer_success",
        "autonomous_ops",
    ],
    "full": [
        "week0",
        "daily",
        "weekly",
        "motion_a",
        "content",
        "phase_01",
        "phase_24",
        "governance",
        "kpi",
        "optional",
        "presentations",
        "public_gtm",
        "dogfood",
        "engineering_fe",
        "engineering_be",
        "value_delivery",
        "autonomous_ops",
        "integrations",
        "finance_unit",
        "customer_success",
        "trust_security",
        "research",
    ],
}

# External benchmarks (founder-led B2B rhythm — not legal advice).
RESEARCH_BENCHMARKS_AR: list[dict[str, str]] = [
    {
        "source": "Founder weekly operating review (evidence-first)",
        "dealix_alignment_ar": "قرار أسبوعي + حزمة أدلة آلية (CSV/API) بدل لقطات يدوية",
    },
    {
        "source": "Pipeline inspection 30–45m (late-stage + blockers log)",
        "dealix_alignment_ar": "War Room + scorecard جمعة + SOAEN على كل touchpoint",
    },
    {
        "source": "Sales operating rhythm vs tracking tools",
        "dealix_alignment_ar": "أمر صباحي ثابت + مسودات/موافقة — الأداة لا تستبدل الإيقاع",
    },
    {
        "source": "Saudi PDPL as procurement trust",
        "dealix_alignment_ar": "طبقة امتثال + anti-waste قبل إرسال خارجي",
    },
    {
        "source": "GTM as operating system (ProductQuant 2026)",
        "dealix_alignment_ar": "134 مهمة آلية + حلقة أدلة أسبوعية — ليس مستنداً ساكناً",
    },
    {
        "source": "Weekly pipeline inspection → forecast accuracy",
        "dealix_alignment_ar": "scorecard من evidence CSV · لا أرقام CRM مخترعة",
    },
    {
        "source": "Founder weekly review with evidence chain (Athenic-style)",
        "dealix_alignment_ar": "قرار واحد + strongest_ops brief يومي/أسبوعي",
    },
]


def _today() -> datetime:
    return datetime.now(UTC)


def _ensure_weekly_decision_file() -> dict[str, Any]:
    weekly = analyze_weekly_one_decision()
    created: str | None = None
    if weekly.get("verdict") in ("MISSING", "STALE"):
        try:
            path = init_weekly_decision()
            created = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            weekly = analyze_weekly_one_decision()
        except (FileNotFoundError, ValueError, OSError) as exc:
            return {"weekly": weekly, "init_error": str(exc), "created_path": None}
    return {"weekly": weekly, "created_path": created}


def select_tasks_for_mode(
    mode: CadenceMode,
    *,
    comprehensive: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Pick checklist tasks for today based on cadence + active MASTER phase."""
    grouped = tasks_by_section()
    sections = set(_CADENCE_SECTIONS.get(mode, _CADENCE_SECTIONS["morning"]))
    today = _today().date()
    weekday = today.weekday()

    if weekday == 6:  # Sunday
        sections.update({"week0"})
    if weekday == 4:  # Friday
        sections.update({"weekly"})

    comp = comprehensive or build_comprehensive_status()
    phase = (comp.get("master_execution_phase") or {}).get("active_phase", 1)
    if phase <= 1:
        sections.update({"phase_01"})
    elif phase <= 4:
        sections.update({"phase_24", "motion_a"})
    else:
        sections.update({"optional", "engineering_be", "value_delivery"})

    out: list[dict[str, Any]] = []
    for sid in sorted(sections):
        for task in grouped.get(sid, []):
            if isinstance(task, dict):
                out.append({**task, "section": sid})
    out.sort(key=lambda t: (t.get("section", ""), t.get("n") or 0))
    return out


def _run_script(rel: str, *extra: str) -> dict[str, Any]:
    path = REPO_ROOT / rel.replace("/", "\\") if "\\" in rel else REPO_ROOT / rel
    if not path.is_file():
        return {"script": rel, "ok": False, "skipped": True, "reason": "missing"}
    cmd = [sys.executable, str(path), *extra]
    try:
        proc = subprocess.run(  # noqa: S603 — sys.executable; controlled script path
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        return {
            "script": rel,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-500:],
            "stderr_tail": (proc.stderr or "")[-300:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"script": rel, "ok": False, "error": str(exc)}


def build_strongest_ops_snapshot(
    *,
    mode: CadenceMode = "morning",
    run_checks: bool = False,
) -> dict[str, Any]:
    """Unified autonomous ops payload for API, UI, and brief writers."""
    day = _today().strftime("%Y-%m-%d")
    rows = load_evidence_rows()
    evidence = count_evidence_events(rows, exclude_placeholders=True)
    cadence = analyze_daily_cadence()
    weekly_init = _ensure_weekly_decision_file()
    comprehensive = build_comprehensive_status()
    plan = strongest_plan_snapshot()
    tasks_today = select_tasks_for_mode(mode, comprehensive=comprehensive)

    full_ops_bridge = plan.get("full_ops_bridge") if mode in ("morning", "full", "weekly") else None

    checks: dict[str, Any] = {}
    if run_checks:
        checks = {
            "strongest_plan_status": _run_script(
                "scripts/founder_strongest_plan_status.py"
            ),
            "comprehensive_plan_status": _run_script(
                "scripts/founder_comprehensive_plan_status.py", "--json"
            ),
        }
        if mode in ("weekly", "full"):
            checks["weekly_scorecard"] = _run_script(
                "scripts/founder_weekly_scorecard.py"
            )
        if mode == "full":
            checks["full_autonomous_morning"] = _run_script(
                "scripts/run_full_commercial_ops_autopilot.py", "--execute"
            )

    warnings_ar: list[str] = []
    if not cadence.get("evidence_logged_today") and mode == "evening":
        warnings_ar.append("لم يُسجَّل حدث أدلة اليوم — أضف سطراً في evidence_events_tracker.csv")
    wk = weekly_init.get("weekly") or {}
    if wk.get("verdict") in ("MISSING", "STALE"):
        warnings_ar.append("قرار الأسبوع ناقص أو قديم — املأ data/founder_weekly/decision_*.yaml")
    phase_gate = comprehensive.get("phase_0_1_gate") or {}
    if phase_gate.get("verdict") == "BLOCKED" and phase_gate.get("blockers_ar"):
        warnings_ar.extend(list(phase_gate["blockers_ar"])[:2])

    return {
        "schema_version": "1.0",
        "generated_at": _today().isoformat(),
        "date": day,
        "mode": mode,
        "policy_ar": plan.get("policy_ar"),
        "no_build_rule_ar": plan.get("no_build_rule_ar"),
        "strongest_plan": plan,
        "comprehensive": comprehensive,
        "weekly_decision_init": weekly_init,
        "evidence_today": evidence.get("today_total", 0),
        "cadence": cadence,
        "tasks_today": tasks_today,
        "tasks_today_count": len(tasks_today),
        "research_benchmarks_ar": RESEARCH_BENCHMARKS_AR,
        "automation": {
            "morning": "py -3 scripts/run_founder_strongest_ops.py --morning",
            "evening": "py -3 scripts/run_founder_strongest_ops.py --evening",
            "weekly": "py -3 scripts/run_founder_strongest_ops.py --weekly",
            "full": "py -3 scripts/run_founder_strongest_ops.py --full",
            "complete_day": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "cadence_ps1": "powershell -File scripts/founder_cadence.ps1",
            "cadence_sh": "bash scripts/founder_cadence.sh",
            "cadence_complete": "powershell -File scripts/founder_cadence.ps1 -Complete",
        },
        "full_ops_bridge": full_ops_bridge,
        "checks": checks,
        "warnings_ar": warnings_ar,
        "verdict": _ops_verdict(mode, plan, comprehensive, cadence, warnings_ar),
    }


def _ops_verdict(
    mode: CadenceMode,
    plan: dict[str, Any],
    comprehensive: dict[str, Any],
    cadence: dict[str, Any],
    warnings: list[str],
) -> str:
    plan_ok = (plan.get("status") or {}).get("ok") is True
    phase = (comprehensive.get("phase_0_1_gate") or {}).get("verdict")
    if not plan_ok:
        return "FAIL_WIRING"
    if len(warnings) > 2:
        return "ATTENTION"
    if phase == "BLOCKED":
        return "FOCUS_PHASE_01"
    if mode == "evening" and not cadence.get("evidence_logged_today"):
        return "LOG_EVIDENCE"
    return "OK"


def run_strongest_ops(
    *,
    mode: CadenceMode = "morning",
    run_checks: bool = False,
    write_brief: bool = True,
) -> dict[str, Any]:
    """Execute strongest ops: optional checks, brief files, return snapshot."""
    brief_paths: dict[str, str] = {}
    if write_brief:
        brief_paths = write_strongest_ops_brief(mode=mode, run_checks=run_checks)
    snap = build_strongest_ops_snapshot(mode=mode, run_checks=run_checks)
    if brief_paths:
        snap["brief_paths"] = brief_paths
    return snap


def write_strongest_ops_brief(
    *,
    mode: CadenceMode = "morning",
    run_checks: bool = False,
) -> dict[str, str]:
    """Write data/founder_briefs/strongest_ops_{date}.md and .json."""
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    snap = build_strongest_ops_snapshot(mode=mode, run_checks=run_checks)
    day = snap["date"]
    json_path = FOUNDER_BRIEFS_DIR / f"strongest_ops_{day}.json"
    md_path = FOUNDER_BRIEFS_DIR / f"strongest_ops_{day}.md"
    json_path.write_text(
        json.dumps(snap, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(_render_brief_md(snap), encoding="utf-8")
    return {
        "json": str(json_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "markdown": str(md_path.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def _render_brief_md(snap: dict[str, Any]) -> str:
    lines = [
        f"# Strongest Ops — {snap.get('date')} ({snap.get('mode')})",
        "",
        f"**Verdict:** `{snap.get('verdict')}`",
        "",
        snap.get("no_build_rule_ar") or "",
        "",
        "## مهام اليوم (مختارة آلياً)",
        "",
    ]
    for t in snap.get("tasks_today") or []:
        lines.append(f"- [{t.get('section')}] **{t.get('n')}.** {t.get('title_ar')}")
    if snap.get("warnings_ar"):
        lines.extend(["", "## تنبيهات", ""])
        for w in snap["warnings_ar"]:
            lines.append(f"- {w}")
    lines.extend(["", "## مرجع", "", "[FOUNDER_STRONGEST_PLAN_AR.md](../docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md)"])
    return "\n".join(lines)
