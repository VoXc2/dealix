"""Unified Value Plan snapshot — gates, Motion A, evidence, first paid, weekly KPIs."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_append import evening_reminder_ar, has_evidence_today
from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.motion_a_pipeline import build_motion_a_pipeline_plan
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT
from dealix.commercial_ops.targeting_csv import load_targets
from dealix.commercial_ops.weekly_scorecard_commercial import build_weekly_scorecard


def _brief_paths(day: str) -> dict[str, str | None]:
    d = FOUNDER_BRIEFS_DIR

    def _rel(p: Path) -> str | None:
        if not p.is_file():
            return None
        return str(p.relative_to(REPO_ROOT)).replace("\\", "/")

    return {
        "motion_a_md": _rel(d / f"motion_a_{day}.md"),
        "weekly_scorecard_md": _rel(d / f"weekly_scorecard_{day}.md"),
        "commercial_md": _rel(d / f"commercial_{day}.md"),
        "daily_pack_md": _rel(d / f"DAILY_PACK_{day}.md"),
        "value_plan_json": _rel(d / f"value_plan_{day}.json"),
        "value_plan_md": _rel(d / f"value_plan_{day}.md"),
    }


def _pack_status_for_day(day: str) -> dict[str, Any]:
    d = FOUNDER_BRIEFS_DIR
    pack_path = d / f"DAILY_PACK_{day}.md"
    try:
        pack_index = str(pack_path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        pack_index = str(pack_path)
    war_room = REPO_ROOT / "data/war_room_today.json"
    return {
        "date": day,
        "brief_exists": (d / f"brief_{day}.md").is_file(),
        "commercial_exists": (d / f"commercial_{day}.md").is_file(),
        "war_room_exists": war_room.is_file(),
        "pack_index": pack_index,
    }


def build_value_plan_snapshot(*, motion_top_n: int = 5) -> dict[str, Any]:
    """Single JSON for founder UI, API, and CI — no invented revenue."""
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    rows = load_evidence_rows()
    evidence = count_evidence_events(rows, exclude_placeholders=True)
    evidence_all = count_evidence_events(rows)
    evening = evening_reminder_ar(rows=rows)
    first_paid = analyze_first_paid_diagnostic()
    motion = build_motion_a_pipeline_plan(top_n=motion_top_n)
    weekly = build_weekly_scorecard()
    targets = load_targets()
    from dealix.commercial_ops.expansion_status import build_expansion_status
    from dealix.commercial_ops.founder_strongest_ops import build_strongest_ops_snapshot
    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot
    from dealix.commercial_ops.motion_pipelines import build_all_motions_summary

    gtm = build_gtm_stack_snapshot(abm_top_n=motion_top_n)
    expansion = build_expansion_status(abm_top_n=motion_top_n)
    motions = build_all_motions_summary(top_n=min(3, motion_top_n))
    strongest_ops = build_strongest_ops_snapshot(mode="morning", run_checks=False)

    gates = {
        "soft_launch_doc": "docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md",
        "verify_script": "scripts/verify_commercial_launch_ready.py",
        "go_live_script": "scripts/verify_dealix_commercial_go_live.ps1",
        "paid_after_soft_doc": "docs/commercial/PAID_LAUNCH_AFTER_SOFT_PASS_AR.md",
        "paid_readiness_script": "scripts/verify_paid_launch_readiness.py",
    }

    north_star = {
        "pilots_active_note_ar": "املأ يدوياً من التسليم الجارٍ",
        "proof_packs_week": (weekly.get("north_star") or {}).get("proof_packs_delivered_week", 0),
        "first_paid_verdict": first_paid["verdict"],
        "first_close_ready": first_paid["first_close_ready"],
    }

    scripts_ar = {
        "morning": "powershell -File scripts/founder_morning.ps1",
        "evening": "powershell -File scripts/founder_evening.ps1",
        "motion_a": "py -3 scripts/founder_motion_a_pipeline.py",
        "weekly": "py -3 scripts/founder_weekly_scorecard.py",
        "paid_gate": "py -3 scripts/founder_paid_launch_gate.py",
        "full_day": "powershell -File scripts/run_value_plan_day.ps1",
    }

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "date": day,
        "policy_ar": "لا توسعة منتج قبل أول Diagnostic مدفوع + Proof Pack — Motion A أولاً.",
        "north_star": north_star,
        "evidence": evidence,
        "evidence_all_rows": evidence_all,
        "evening": evening,
        "first_paid_diagnostic": first_paid,
        "motion_a": {
            "focus_ar": motion.get("focus_ar"),
            "targets": (motion.get("targets") or [])[:motion_top_n],
            "verdict": (motion.get("first_paid") or {}).get("verdict"),
        },
        "weekly_scorecard": {
            "week_end": weekly.get("week_end"),
            "kpi_week": weekly.get("kpi_week"),
            "conversion_demo_to_invoice": weekly.get("conversion_demo_to_invoice"),
        },
        "targeting": {
            "agency_pool_rows": len(targets),
            "min_rows_soft": 120,
            "min_rows_wave2": 150,
            "min_rows_wave3": 200,
            "social_posts_target": 140,
            "social_cycle_weeks": 28,
            "min_rows_wave4": 250,
        },
        "expansion_status": expansion,
        "pack_status": _pack_status_for_day(day),
        "brief_paths": _brief_paths(day),
        "gates": gates,
        "scripts": scripts_ar,
        "ops_ui": {
            "founder": "/ar/ops/founder",
            "war_room": "/ar/ops/war-room",
            "approvals": "/ar/ops/approvals",
            "marketing": "/ar/ops/marketing",
            "evidence": "/ar/ops/evidence",
            "business_now": "/ar/business-now",
            "risk_score": "/ar/risk-score",
            "diagnostic": "/ar/dealix-diagnostic",
            "proof_pack": "/ar/proof-pack",
            "home": "/ar",
        },
        "commercial_value_map": {
            "doc_path": "docs/commercial/COMMERCIAL_VALUE_MAP_AR.md",
            "quick_ref_path": "docs/commercial/COMMERCIAL_OPS_QUICK_REFERENCE_AR.md",
            "market_intel_index": "docs/commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md",
            "api_path": "/api/v1/ops-autopilot/founder/commercial-value-map",
            "status_script": "scripts/commercial_value_map_status.py",
            "value_plan_day_script": "scripts/run_value_plan_day.ps1",
        },
        "gtm_stack": gtm,
        "motions_pipeline": motions,
        "strongest_ops": {
            "verdict": strongest_ops.get("verdict"),
            "tasks_today_count": strongest_ops.get("tasks_today_count"),
            "brief_paths": {
                "json": f"data/founder_briefs/strongest_ops_{day}.json",
                "markdown": f"data/founder_briefs/strongest_ops_{day}.md",
            },
            "api_path": "/api/v1/ops-autopilot/founder/strongest-ops",
            "runner": "scripts/run_founder_strongest_ops.py",
        },
        "warnings_ar": _build_warnings(
            first_paid, evidence, evening, targets, gtm, expansion, strongest_ops
        ),
    }


def _build_warnings(
    first_paid: dict[str, Any],
    evidence: dict[str, Any],
    evening: dict[str, Any],
    targets: list[dict[str, str]],
    gtm: dict[str, Any] | None = None,
    expansion: dict[str, Any] | None = None,
    strongest_ops: dict[str, Any] | None = None,
) -> list[str]:
    out: list[str] = []
    if strongest_ops and strongest_ops.get("verdict") == "FAIL_WIRING":
        out.append("أقوى خطة: مسارات ناقصة — py -3 scripts/founder_strongest_plan_status.py")
    if first_paid["verdict"] == "PIPELINE_OPEN":
        out.append("بوابة القيمة مفتوحة: أغلق Diagnostic واحد (دفع + Proof) لشركة حقيقية.")
    if int(evidence.get("today_total") or 0) < 1:
        out.append("سجّل حدث أدلة واحد اليوم (مساءً: founder_evening.ps1).")
    if not evening.get("logged_today"):
        out.append(evening.get("reminder_ar") or "")
    if len(targets) < 80:
        out.append(f"استهداف: {len(targets)} صف — Soft ≥80 · wave2 ≥150.")
    elif len(targets) < 150:
        out.append(
            f"استهداف: {len(targets)} صف — للموجة 2: py -3 scripts/expand_agency_targets_seed.py --wave2"
        )
    soc = (expansion or {}).get("social") or {}
    if soc and not soc.get("queue_ready_28w"):
        out.append(
            f"سوشال: {soc.get('posts', 0)} منشور / {soc.get('cycle_weeks', 0)} أسبوع — "
            "هدف 28: expand_social_queue_12w.py --cycle-weeks 28"
        )
    abm = (gtm or {}).get("abm_wave1") or {}
    if abm and not abm.get("wave1_ready"):
        out.append(
            f"موجة ABM 1: {abm.get('active_rows', 0)}/{abm.get('min_required', 30)} "
            "صف فعّال — راجع ABM_WAVE1_ICP_AR.md."
        )
    dual = (gtm or {}).get("dual_track") or {}
    if dual.get("recommended_track") == "A" and (dual.get("high_priority_stale") or 0) > 0:
        out.append(f"مسار A: {dual['high_priority_stale']} هدف high بلا تاريخ متابعة.")
    return [w for w in out if w]


def render_value_plan_markdown(snapshot: dict[str, Any]) -> str:
    fp = snapshot.get("first_paid_diagnostic") or {}
    ev = snapshot.get("evidence") or {}
    lines = [
        f"# Value Plan Snapshot · {snapshot.get('date')}",
        "",
        f"_{snapshot.get('policy_ar')}_",
        "",
        "## North Star",
        f"- Proof packs هذا الأسبوع: **{(snapshot.get('north_star') or {}).get('proof_packs_week', 0)}**",
        f"- First paid verdict: `{fp.get('verdict')}`",
        "",
        "## Evidence",
        f"- اليوم: **{ev.get('today_total', 0)}** · الأسبوع: **{ev.get('week_total', 0)}**",
        "",
        "## Motion A (أعلى P0)",
        "",
    ]
    for t in (snapshot.get("motion_a") or {}).get("targets") or []:
        lines.append(
            f"- **{t.get('company')}** · `{t.get('status')}` → {t.get('next_action_ar')}"
        )
    exp = snapshot.get("expansion_status") or {}
    tgt = exp.get("targeting") or {}
    soc = exp.get("social") or {}
    lines.extend(
        [
            "",
            "## Expansion",
            f"- Targeting pool: **{tgt.get('pool_rows', 0)}** · wave2: `{tgt.get('wave2_ready')}`",
            f"- Social: **{soc.get('posts', 0)}** posts / **{soc.get('cycle_weeks', 0)}**w",
            "",
        ]
    )
    for w in snapshot.get("warnings_ar") or []:
        lines.append("")
        lines.append(f"> ⚠️ {w}")
    lines.append("")
    lines.append(f"_Generated: {snapshot.get('generated_at')}_")
    return "\n".join(lines)
