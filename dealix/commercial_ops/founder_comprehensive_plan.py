"""Founder comprehensive plan — daily anchors, phase gate, GTM codification, PDPL pass, weekly decision."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.founder_debrief import list_debriefs
from dealix.commercial_ops.paths import (
    FOUNDER_GTM_CODIFICATION_REGISTRY,
    FOUNDER_PDPL_PASS_YAML,
    FOUNDER_WEEKLY_DECISION_DIR,
    FOUNDER_WEEKLY_DECISION_TEMPLATE,
    REPO_ROOT,
)

# --- Daily anchor docs (todo: anchor-docs) ---
DAILY_ANCHOR_DOCS: dict[str, str] = {
    "founder_operating_system": "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
    "master_commercial_plan": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
    "revenue_war_room": "docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md",
    "execution_hub": "docs/ops/FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md",
    "daily_anchor": "docs/ops/FOUNDER_DAILY_ANCHOR_AR.md",
}

PHASE_GATE_DOC = "docs/ops/FOUNDER_PHASE_0_1_GATE_AR.md"
GTM_CODIFICATION_DOC = "docs/commercial/operations/FOUNDER_GTM_CODIFICATION_AR.md"
WEEKLY_DECISION_DOC = "docs/ops/FOUNDER_WEEKLY_ONE_DECISION_AR.md"
PDPL_PASS_DOC = "docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md"

CODIFICATION_TARGET = 10

MASTER_EXECUTION_PHASES: list[dict[str, Any]] = [
    {
        "phase": 0,
        "label_ar": "آلة إغلاق + Discovery",
        "doc": "docs/commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md",
    },
    {
        "phase": 1,
        "label_ar": "أول payment_received + proof_pack_delivered",
        "doc": "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
    },
    {
        "phase": 2,
        "label_ar": "تكرار Motion A (وكالة)",
        "doc": "docs/commercial/operations/motion_a_agency/",
    },
    {
        "phase": 3,
        "label_ar": "شريك + إحالة",
        "doc": "docs/commercial/operations/PARTNER_ONBOARDING_KIT_AR.md",
    },
    {
        "phase": 4,
        "label_ar": "AEO + Objection Engine",
        "doc": "docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md",
    },
    {
        "phase": 5,
        "label_ar": "منصة — بعد تكرار الأدلة",
        "doc": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
    },
]


def daily_anchor_docs() -> dict[str, Any]:
    """Resolve the three canonical daily references + execution hub."""
    resolved: dict[str, dict[str, Any]] = {}
    for key, rel in DAILY_ANCHOR_DOCS.items():
        p = REPO_ROOT / rel
        resolved[key] = {
            "path": rel,
            "exists": p.is_file(),
        }
    return {
        "anchors": resolved,
        "morning_command_sh": "scripts/run_founder_commercial_day.sh",
        "morning_command_ps1": "scripts/run_founder_commercial_day.ps1",
        "cadence_sh": "scripts/founder_cadence.sh",
        "cadence_ps1": "scripts/founder_cadence.ps1",
    }


def analyze_phase_0_1_gate() -> dict[str, Any]:
    """Phase 0–1: first paid diagnostic + proof pack before build/team expansion."""
    paid = analyze_first_paid_diagnostic()
    gate_open = paid["verdict"] == "CLOSED"
    if gate_open:
        verdict = "PASS"
        blockers_ar: list[str] = []
    elif paid["verdict"] == "IN_PROGRESS":
        verdict = "IN_PROGRESS"
        blockers_ar = _phase_blockers(paid)
    else:
        verdict = "BLOCKED"
        blockers_ar = _phase_blockers(paid)

    return {
        "verdict": verdict,
        "gate_open": gate_open,
        "no_build_until_closed": not gate_open,
        "first_paid": paid,
        "dod_doc": paid.get("dod_doc"),
        "phase_doc": PHASE_GATE_DOC,
        "blockers_ar": blockers_ar,
    }


def _phase_blockers(paid: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if not paid.get("payment_received_real"):
        blockers.append("سجّل payment_received حقيقي في evidence_events_tracker.csv")
    if not paid.get("proof_pack_delivered_real"):
        blockers.append("سجّل proof_pack_delivered بعد التسليم")
    if paid.get("crm_kpi_pending"):
        blockers.append("املأ kpi_founder_commercial_import.yaml من CRM (لا أرقام مخترعة)")
    return blockers


def analyze_gtm_codification(*, target: int = CODIFICATION_TARGET) -> dict[str, Any]:
    """Progress toward codifying first ~10 deals from debriefs + registry."""
    debriefs = list_debriefs(limit=50)
    filled = [
        d
        for d in debriefs
        if (d.get("one_decision") or "").strip() or (d.get("next_action") or "").strip()
    ]
    registry = _load_registry()
    patterns = registry.get("patterns") or []
    pattern_count = len(patterns) if isinstance(patterns, list) else 0

    debrief_count = len(filled)
    combined = max(debrief_count, pattern_count)
    if combined >= target:
        verdict = "READY"
    elif combined >= max(1, target // 2):
        verdict = "IN_PROGRESS"
    else:
        verdict = "OPEN"

    return {
        "verdict": verdict,
        "target_deals": target,
        "debriefs_with_notes": debrief_count,
        "registry_patterns": pattern_count,
        "recent_debriefs": debriefs[:5],
        "registry_path": str(
            FOUNDER_GTM_CODIFICATION_REGISTRY.relative_to(REPO_ROOT)
        ).replace("\\", "/"),
        "doc": GTM_CODIFICATION_DOC,
        "init_debrief_cmd": "py -3 scripts/founder_meeting_debrief_init.py --company \"...\"",
    }


def _load_registry() -> dict[str, Any]:
    if not FOUNDER_GTM_CODIFICATION_REGISTRY.is_file():
        return {}
    data = yaml.safe_load(FOUNDER_GTM_CODIFICATION_REGISTRY.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def analyze_pdpl_compliance_pass() -> dict[str, Any]:
    """Founder PDPL pass checklist — operational items, not legal sign-off."""
    if not FOUNDER_PDPL_PASS_YAML.is_file():
        return {
            "verdict": "MISSING_CONFIG",
            "items": [],
            "doc": PDPL_PASS_DOC,
        }
    data = yaml.safe_load(FOUNDER_PDPL_PASS_YAML.read_text(encoding="utf-8"))
    items = data.get("items") if isinstance(data, dict) else []
    if not isinstance(items, list):
        items = []
    done = sum(1 for i in items if isinstance(i, dict) and i.get("done"))
    total = len(items)
    if total == 0:
        verdict = "EMPTY"
    elif done == total:
        verdict = "PASS"
    elif done > 0:
        verdict = "IN_PROGRESS"
    else:
        verdict = "OPEN"
    return {
        "verdict": verdict,
        "done": done,
        "total": total,
        "items": items,
        "doc": PDPL_PASS_DOC,
        "legal_review_required": True,
        "closure_checklist": "docs/ops/PDPL_CLOSURE_CHECKLIST_AR.md",
    }


def analyze_weekly_one_decision() -> dict[str, Any]:
    """Weekly founder decision — canonical config yaml, legacy data/founder_weekly fallback."""
    config_path = REPO_ROOT / "dealix/config/founder_weekly_one_decision.yaml"
    config_data = _load_registry() if False else {}  # noqa: placeholder removed below
    config_data = {}
    if config_path.is_file():
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            config_data = raw if isinstance(raw, dict) else {}
        except yaml.YAMLError:
            config_data = {}

    one_decision_ar = (config_data.get("one_decision_ar") or "").strip()
    if one_decision_ar:
        week_iso = (config_data.get("week_iso") or "").strip()
        week_id = datetime.now(UTC).strftime("%Y-W%V")
        latest = {
            "one_decision": one_decision_ar,
            "one_decision_ar": one_decision_ar,
            "supports_phase": config_data.get("active_phase"),
            "active_phase": config_data.get("active_phase"),
            "success_by_friday_ar": config_data.get("success_by_friday_ar"),
            "blocked_by": config_data.get("blocked_by"),
            "stop_list": config_data.get("evidence_events_to_log") or [],
            "source": "config_yaml",
        }
        verdict = "FILLED" if week_iso else "STALE"
        return {
            "verdict": verdict,
            "week_id": week_iso or week_id,
            "has_this_week": bool(week_iso),
            "latest_path": str(config_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "latest": latest,
            "template_path": str(
                FOUNDER_WEEKLY_DECISION_TEMPLATE.relative_to(REPO_ROOT)
            ).replace("\\", "/")
            if FOUNDER_WEEKLY_DECISION_TEMPLATE.is_file()
            else None,
            "doc": WEEKLY_DECISION_DOC,
        }

    FOUNDER_WEEKLY_DECISION_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(
        FOUNDER_WEEKLY_DECISION_DIR.glob("decision_*.yaml"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    latest: dict[str, Any] | None = None
    latest_path: str | None = None
    if files:
        latest_path = str(files[0].relative_to(REPO_ROOT)).replace("\\", "/")
        try:
            latest = yaml.safe_load(files[0].read_text(encoding="utf-8"))
        except yaml.YAMLError:
            latest = None

    week_id = datetime.now(UTC).strftime("%Y-W%V")
    has_this_week = any(week_id in f.name for f in files[:3])
    one_legacy = ""
    if isinstance(latest, dict):
        one_legacy = (latest.get("one_decision") or latest.get("one_decision_ar") or "").strip()
    if one_legacy:
        verdict = "FILLED" if has_this_week else "STALE"
    else:
        verdict = "MISSING"

    return {
        "verdict": verdict,
        "week_id": week_id,
        "has_this_week": has_this_week,
        "latest_path": latest_path,
        "latest": latest,
        "template_path": str(
            FOUNDER_WEEKLY_DECISION_TEMPLATE.relative_to(REPO_ROOT)
        ).replace("\\", "/")
        if FOUNDER_WEEKLY_DECISION_TEMPLATE.is_file()
        else None,
        "doc": WEEKLY_DECISION_DOC,
    }


def analyze_daily_cadence() -> dict[str, Any]:
    """Evidence today + evening reminder + Friday scorecard hint."""
    rows = load_evidence_rows()
    today = datetime.now(UTC).date()
    ev = count_evidence_events(rows, on_date=today, exclude_placeholders=True)
    weekday = today.weekday()  # Mon=0 .. Sun=6
    is_friday = weekday == 4
    return {
        "date": today.isoformat(),
        "evidence_logged_today": ev["today_total"] > 0,
        "evidence_today_total": ev["today_total"],
        "evening_script": "scripts/founder_evening_evidence.py",
        "weekly_scorecard_script": "scripts/founder_weekly_scorecard.py",
        "is_friday_run_scorecard": is_friday,
        "cadence_evening_flag": "--evening",
        "cadence_weekly_flag": "--weekly",
    }


def _parse_supports_phase(raw: Any) -> int | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    for ch in text.replace("–", "-").split("-"):
        ch = ch.strip()
        if ch.isdigit():
            return int(ch)
    if text.isdigit():
        return int(text)
    return None


def infer_master_execution_phase(
    *,
    phase_gate: dict[str, Any] | None = None,
    weekly: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Map MASTER plan phases 0–5 from gate + weekly decision supports_phase."""
    gate = phase_gate or analyze_phase_0_1_gate()
    wk = weekly or analyze_weekly_one_decision()
    latest = wk.get("latest") if isinstance(wk.get("latest"), dict) else {}
    supports = _parse_supports_phase(latest.get("supports_phase"))

    if not gate.get("gate_open"):
        active = 1 if gate.get("verdict") == "IN_PROGRESS" else 0
    elif supports is not None:
        active = max(0, min(5, supports))
    else:
        active = 2

    phases = []
    for p in MASTER_EXECUTION_PHASES:
        ph = int(p["phase"])
        phases.append(
            {
                **p,
                "is_active": ph == active,
                "is_complete": ph < active or (ph <= 1 and gate.get("gate_open")),
            }
        )
    active_meta = next((p for p in phases if p["is_active"]), phases[0])
    return {
        "active_phase": active,
        "active_label_ar": active_meta.get("label_ar"),
        "active_doc": active_meta.get("doc"),
        "master_plan_doc": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
        "phases": phases,
        "supports_phase_raw": latest.get("supports_phase"),
    }


def build_comprehensive_status() -> dict[str, Any]:
    """Single snapshot for founder_comprehensive_plan_status.py and APIs."""
    phase_gate = analyze_phase_0_1_gate()
    weekly = analyze_weekly_one_decision()
    from dealix.commercial_ops.founder_max_ops_backlog import summarize_backlog
    from dealix.commercial_ops.paths import DEALIX_DOGFOODING_WAR_ROOM_JSON

    dogfooding_file = DEALIX_DOGFOODING_WAR_ROOM_JSON.is_file()

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "daily_anchors": daily_anchor_docs(),
        "daily_cadence": analyze_daily_cadence(),
        "phase_0_1_gate": phase_gate,
        "master_execution_phase": infer_master_execution_phase(
            phase_gate=phase_gate, weekly=weekly
        ),
        "gtm_codification": analyze_gtm_codification(),
        "pdpl_compliance_pass": analyze_pdpl_compliance_pass(),
        "weekly_one_decision": weekly,
        "max_ops_backlog": summarize_backlog(),
        "dogfooding": {
            "doc": "docs/ops/DEALIX_DOGFOODING_WAR_ROOM_AR.md",
            "sync_script": "scripts/founder_dogfooding_war_room_sync.py",
            "war_room_json": str(
                DEALIX_DOGFOODING_WAR_ROOM_JSON.relative_to(REPO_ROOT)
            ).replace("\\", "/"),
            "war_room_ready": dogfooding_file,
        },
    }


def init_weekly_decision(*, week_id: str | None = None) -> Path:
    """Create data/founder_weekly/decision_{week_id}.yaml from template."""
    if not FOUNDER_WEEKLY_DECISION_TEMPLATE.is_file():
        raise FileNotFoundError(str(FOUNDER_WEEKLY_DECISION_TEMPLATE))
    wid = week_id or datetime.now(UTC).strftime("%Y-W%V")
    template = yaml.safe_load(
        FOUNDER_WEEKLY_DECISION_TEMPLATE.read_text(encoding="utf-8")
    )
    if not isinstance(template, dict):
        raise ValueError("invalid weekly decision template")
    payload = dict(template)
    payload["week_id"] = wid
    payload["created_at"] = datetime.now(UTC).isoformat()
    FOUNDER_WEEKLY_DECISION_DIR.mkdir(parents=True, exist_ok=True)
    path = FOUNDER_WEEKLY_DECISION_DIR / f"decision_{wid}.yaml"
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path
