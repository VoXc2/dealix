"""Full autonomous commercial ops — governed morning pipeline + unified snapshot.

Autonomous = run all deterministic steps (War Room, packs, drafts, metrics).
Human-only = approve external send, CRM truth, close deals (2026 B2B best practice).
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT, WAR_ROOM_TODAY_JSON

# External GTM research alignment (2025–2026) — not performance claims for Dealix.
RESEARCH_ALIGNMENT_AR = {
    "external_consensus": [
        "4–6 طبقات مدمجة أفضل من 15+ أداة منفصلة",
        "Human-in-the-loop: AI يمسود، المؤسس يوافق ويرسل (Agentic + HITL 2026)",
        "حوكمة الإجراءات الذاتية أهم من تسريع النشاط — accountability + سلامة التوقعات",
        "لا إغلاق صفقات أو تفاوض سعر بالذكاء الاصطناعي",
        "ABM + enrichment + sequences بمسودات معتمدة",
        "قياس TTV والاحتفاظ لا vanity metrics",
        "GTM كنظام تشغيل أسبوعي بأدلة — ليس PDF ثابت",
    ],
    "dealix_choice_ar": [
        "Revenue OS بحوكمة — لا cold WhatsApp/LinkedIn تلقائي",
        "موجات ABM warm فقط + Proof Stack قبل ديمو طويل",
        "مسار A/B يومي + لوب debrief + ترميز 10 صفقات",
        "أتمتة صباحية كاملة حتى حد الموافقة الخارجية",
    ],
    "verdict_ar": (
        "Dealix أصرّ من المتوسط السوقي على الامتثال — "
        "هذا أفضل مسار لـ founder-led B2B في السعودية، وليس «إرسالاً تلقائياً كاملاً»."
    ),
    "sources_2026": [
        "https://salespipe.co/blog/founder-led-outbound-with-ai-gtm-playbook",
        "https://productquant.dev/blog/complete-gtm-strategy-guide/",
        "https://formanorden.com/blog/gtm-engineering-complete-guide",
        "https://wyzard.ai/blog/autonomous-vs-assisted-gtm-agentic-ai-hitl/",
        "https://www.fullcast.com/content/autonomous-revenue-operations/",
    ],
}


def _run_script(rel: str, *args: str, timeout_s: int = 90) -> dict[str, Any]:
    cmd = [sys.executable, str(REPO_ROOT / rel), *args]
    try:
        proc = subprocess.run(  # noqa: S603 — sys.executable; controlled script path
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
        )
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-800:],
            "stderr_tail": (proc.stderr or "")[-400:],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "exit_code": -1, "error": "timeout"}
    except OSError as exc:
        return {"ok": False, "exit_code": -1, "error": str(exc)}


def _step_war_room(*, top_n: int) -> dict[str, Any]:
    from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
    from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    pool = select_daily_p0_targets(load_targets(), top_n=top_n)
    payload = attach_outreach_drafts(build_war_room_today(pool, top_n=top_n))
    WAR_ROOM_TODAY_JSON.parent.mkdir(parents=True, exist_ok=True)
    WAR_ROOM_TODAY_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "targets": len((payload.get("targets") or {}).get("items") or []),
        "path": str(WAR_ROOM_TODAY_JSON.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def _step_daily_pack() -> dict[str, Any]:
    from dealix.commercial_ops.daily_pack import write_daily_pack_index

    path = write_daily_pack_index()
    return {"ok": True, "pack_md": str(path.relative_to(REPO_ROOT)).replace("\\", "/")}


def _step_value_plan_export(*, top_n: int) -> dict[str, Any]:
    from dealix.commercial_ops.value_plan import (
        build_value_plan_snapshot,
        render_value_plan_markdown,
    )

    snap = build_value_plan_snapshot(motion_top_n=top_n)
    day = snap.get("date") or datetime.now(UTC).strftime("%Y-%m-%d")
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = FOUNDER_BRIEFS_DIR / f"value_plan_{day}.md"
    json_path = FOUNDER_BRIEFS_DIR / f"value_plan_{day}.json"
    md_path.write_text(render_value_plan_markdown(snap) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "json": str(json_path.relative_to(REPO_ROOT)).replace("\\", "/")}


def _step_dogfooding(*, top_n: int = 10) -> dict[str, Any]:
    from dealix.commercial_ops.dogfooding_war_room import build_dogfooding_payload
    from dealix.commercial_ops.paths import DEALIX_DOGFOODING_WAR_ROOM_JSON

    payload = build_dogfooding_payload(top_n=top_n)
    DEALIX_DOGFOODING_WAR_ROOM_JSON.parent.mkdir(parents=True, exist_ok=True)
    DEALIX_DOGFOODING_WAR_ROOM_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    n = len((payload.get("targets") or {}).get("items") or [])
    return {
        "ok": True,
        "targets": n,
        "path": str(DEALIX_DOGFOODING_WAR_ROOM_JSON.relative_to(REPO_ROOT)).replace(
            "\\", "/"
        ),
    }


def _step_motion_pipelines(*, top_n: int) -> dict[str, Any]:
    from dealix.commercial_ops.motion_a_pipeline import build_motion_a_pipeline_plan

    plan = build_motion_a_pipeline_plan(top_n=top_n)
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    path = FOUNDER_BRIEFS_DIR / f"motion_a_{day}.md"
    lines = [f"# Motion A · {day}", ""]
    for t in plan.get("targets") or []:
        lines.append(f"- **{t.get('company')}** · `{t.get('status')}` → {t.get('next_action_ar')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"ok": True, "targets": len(plan.get("targets") or [])}


MORNING_CORE_STEPS: list[tuple[str, str, Callable[..., dict[str, Any]]]] = [
    ("war_room", "مزامنة War Room + مسودات لمسة", _step_war_room),
    ("dogfooding", "War Room داخلي Dealix", _step_dogfooding),
    ("daily_pack", "فهرس حزمة اليوم", _step_daily_pack),
    ("value_plan", "لقطة Value Plan", _step_value_plan_export),
    ("motion_a", "خط Motion A", _step_motion_pipelines),
]

OPTIONAL_SCRIPT_STEPS: list[tuple[str, str, str, list[str]]] = [
    ("expand_daily", "توسعة wave2+20w", "scripts/expand_commercial_operating_stack.py", ["--daily"]),
    ("gtm_verify", "تحقق GTM", "scripts/verify_gtm_stack.py", []),
    ("gtm_status", "لقطة GTM", "scripts/founder_gtm_status.py", ["--json"]),
    ("comprehensive", "خطة شاملة", "scripts/founder_comprehensive_plan_status.py", ["--json"]),
    ("first_paid", "تتبع أول دفع", "scripts/verify_first_paid_diagnostic_tracker.py", []),
    ("strongest_plan", "أقوى خطة", "scripts/founder_strongest_plan_status.py", []),
    ("value_map", "خريطة القيمة", "scripts/commercial_value_map_status.py", []),
    ("autopilot_brief", "موجز Autopilot", "scripts/run_founder_full_autopilot.py", []),
    ("strongest_ops", "Strongest Ops صباح", "scripts/run_founder_strongest_ops.py", ["--morning"]),
]


def _step_commercial_digest() -> dict[str, Any]:
    from dealix.commercial_ops.digest import build_commercial_digest

    digest = build_commercial_digest(skip_no_build=True)
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    path = FOUNDER_BRIEFS_DIR / f"commercial_{day}.md"
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [f"# Commercial digest · {day}", ""]
    for line in digest.get("today_focus_ar") or []:
        lines.append(f"- {line}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "focus_count": len(digest.get("today_focus_ar") or []),
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def _step_autopilot_brief() -> dict[str, Any]:
    from dealix.commercial_ops.founder_full_autopilot import (
        build_autopilot_snapshot,
        render_autopilot_brief_markdown,
    )

    day = datetime.now(UTC).strftime("%Y-%m-%d")
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    path = FOUNDER_BRIEFS_DIR / f"autopilot_{day}.md"
    snap = build_autopilot_snapshot()
    path.write_text(render_autopilot_brief_markdown(snap) + "\n", encoding="utf-8")
    return {"ok": True, "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/")}


MORNING_EXTENDED_STEPS: list[tuple[str, str, Callable[..., dict[str, Any]]]] = [
    ("digest", "موجز تجاري يومي", _step_commercial_digest),
    ("autopilot_brief", "موجز Full Autopilot", _step_autopilot_brief),
]


def run_morning_core(
    *,
    top_n: int = 15,
    run_optional_scripts: bool = True,
) -> dict[str, Any]:
    """Execute in-repo autonomous morning (no external send)."""
    steps: list[dict[str, Any]] = []
    all_core = [*MORNING_CORE_STEPS, *MORNING_EXTENDED_STEPS]
    for sid, label_ar, fn in all_core:
        try:
            if fn in (_step_war_room, _step_dogfooding, _step_value_plan_export, _step_motion_pipelines):
                result = fn(top_n=top_n)
            else:
                result = fn()
            steps.append({"id": sid, "label_ar": label_ar, **result})
        except Exception as exc:
            steps.append({"id": sid, "label_ar": label_ar, "ok": False, "error": str(exc)})

    if run_optional_scripts:
        for sid, label_ar, script, args in OPTIONAL_SCRIPT_STEPS:
            r = _run_script(script, *args)
            steps.append({"id": sid, "label_ar": label_ar, **r})

    core_ids = {x[0] for x in MORNING_CORE_STEPS}
    core_ok = all(s.get("ok") for s in steps if s["id"] in core_ids)
    all_ok = all(s.get("ok") for s in steps)
    return {
        "ran_at": datetime.now(UTC).isoformat(),
        "verdict": "PASS" if all_ok else ("PARTIAL" if core_ok else "FAIL"),
        "steps": steps,
        "policy_ar": "أتمتة كاملة حتى الموافقة الخارجية — لا إرسال بارد.",
    }


def build_value_plan_hint(*, top_n: int = 15) -> dict[str, Any]:
    """Fast value-plan slice for packs/API (full plan: build_value_plan_snapshot)."""
    return _lightweight_value_plan_hint(top_n=top_n)


def _lightweight_value_plan_hint(*, top_n: int = 15) -> dict[str, Any]:
    """Fast value-plan slice for snapshots (full plan via include_value_plan=True)."""
    from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic

    paid = analyze_first_paid_diagnostic()
    warnings: list[str] = []
    if paid.get("verdict") == "PIPELINE_OPEN":
        warnings.append("بوابة 0–1: أغلق أول Diagnostic مدفوع + Proof Pack")
    return {
        "lightweight": True,
        "motion_top_n": top_n,
        "first_paid_diagnostic": paid,
        "warnings_ar": warnings,
    }


def build_full_autonomous_ops_snapshot(
    *,
    top_n: int = 15,
    include_nested: bool = True,
    include_value_plan: bool = False,
) -> dict[str, Any]:
    from dealix.commercial_ops.expansion_status import build_expansion_status
    from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

    gtm = build_gtm_stack_snapshot(abm_top_n=top_n)
    expansion = build_expansion_status(abm_top_n=top_n)
    comprehensive = build_comprehensive_status()
    if include_value_plan:
        from dealix.commercial_ops.value_plan import build_value_plan_snapshot

        value_plan: dict[str, Any] = build_value_plan_snapshot(motion_top_n=top_n)
    else:
        value_plan = build_value_plan_hint(top_n=top_n)
    strongest_ops: dict[str, Any] | None = None
    plan_wiring: dict[str, Any] | None = None
    if include_nested:
        from dealix.commercial_ops.founder_strongest_ops import build_strongest_ops_snapshot
        from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status

        strongest_ops = build_strongest_ops_snapshot(mode="morning", run_checks=False)
        plan_wiring = strongest_plan_status()

    founder_only = _founder_only_actions(gtm, comprehensive, value_plan)
    auto_ready = _automation_readiness(gtm, comprehensive, value_plan)

    from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot

    founder_autopilot = build_autopilot_snapshot()
    for item in (founder_autopilot.get("queue") or [])[:3]:
        title = item.get("title_ar")
        if title and title not in founder_only:
            founder_only.append(str(title))

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "schema_version": "1.1",
        "research_alignment": RESEARCH_ALIGNMENT_AR,
        "automation_readiness": auto_ready,
        "founder_only_actions_ar": founder_only,
        "founder_autopilot": {
            "verdict": founder_autopilot.get("verdict"),
            "queue": founder_autopilot.get("queue"),
            "customer_stage": founder_autopilot.get("customer_stage"),
            "pls_readiness": founder_autopilot.get("pls_readiness"),
            "benchmark_ar": founder_autopilot.get("benchmark_ar"),
        },
        "gtm_stack": gtm,
        "expansion": expansion,
        "comprehensive_plan": comprehensive,
        "value_plan": value_plan,
        "strongest_ops": strongest_ops,
        "strongest_plan_wiring": plan_wiring,
        "commands": {
            "unified_day": "py -3 scripts/run_dealix_unified_founder_day.py",
            "morning_full": "bash scripts/run_founder_commercial_day.sh",
            "morning_core": "py -3 scripts/run_full_commercial_ops_autopilot.py --execute",
            "complete_day": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "full_autonomous": "py -3 scripts/run_dealix_full_autonomous_ops.py",
            "strongest_ops": "py -3 scripts/run_founder_strongest_ops.py --morning",
            "evening": "py -3 scripts/founder_evening_evidence.py",
            "cadence": "bash scripts/founder_cadence.sh",
            "dogfooding": "py -3 scripts/founder_dogfooding_war_room_sync.py",
            "api_snapshot": "/api/v1/ops-autopilot/founder/full-autonomous-ops",
            "strongest_ops_api": "/api/v1/ops-autopilot/founder/strongest-ops",
        },
        "doc_path": "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
    }


def _automation_readiness(
    gtm: dict[str, Any],
    comprehensive: dict[str, Any],
    value_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dual = gtm.get("dual_track") or {}
    cadence = comprehensive.get("daily_cadence") or {}
    phase = comprehensive.get("phase_0_1_gate") or {}
    blockers: list[str] = []

    if dual.get("recommended_track") == "A" and (dual.get("high_priority_stale") or 0) > 0:
        blockers.append("أهداف high بلا تاريخ — War Room")
    if not cadence.get("evidence_logged_today"):
        blockers.append("سجّل حدث أدلة اليوم (مساءً)")
    if value_plan:
        for w in value_plan.get("warnings_ar") or []:
            if w and w not in blockers:
                blockers.append(str(w))

    if blockers:
        verdict = "NEEDS_FOUNDER"
    elif phase.get("verdict") == "BLOCKED":
        verdict = "BLOCKED"
    else:
        verdict = "AUTONOMOUS_READY"

    return {
        "verdict": verdict,
        "blockers_ar": blockers[:6],
        "automated_layers_ar": [
            "War Room + مسودات لمسة",
            "حزمة يومية + Value Plan + GTM",
            "سوشال مسودة + AEO",
            "توسيع targeting/social (idempotent)",
        ],
        "human_layers_ar": [
            "موافقة LinkedIn/Gmail",
            "إرسال يدوي message_sent_manual",
            "Discovery/Demo حي",
            "CRM → KPI import",
        ],
    }


def _founder_only_actions(
    gtm: dict[str, Any],
    comprehensive: dict[str, Any],
    value_plan: dict[str, Any] | None = None,
) -> list[str]:
    out: list[str] = []
    dual = gtm.get("dual_track") or {}
    out.append(dual.get("reason_ar") or "راجع مسار A/B")
    for t in (gtm.get("abm_wave1") or {}).get("top_targets") or []:
        if (t.get("priority") or "").lower() == "high" and t.get("status") in {
            "not_contacted",
            "message_drafted",
        }:
            out.append(f"لمسة معتمدة: {t.get('company')}")
            if len(out) >= 4:
                break
    cadence = comprehensive.get("daily_cadence") or {}
    if not cadence.get("evidence_logged_today"):
        out.append("مساءً: founder_evening_evidence.py --append")
    if cadence.get("is_friday_run_scorecard"):
        out.append("جمعة: founder_weekly_scorecard.py")
    if value_plan and not value_plan.get("lightweight"):
        for w in (value_plan.get("warnings_ar") or [])[:2]:
            out.append(w)
    return out[:8]
