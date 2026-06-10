"""Founder strongest plan checklist — load paths and CI status."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import REPO_ROOT

CHECKLIST_PATH = REPO_ROOT / "dealix" / "config" / "founder_strongest_plan_checklist.yaml"
WEEKLY_DECISION_PATH = REPO_ROOT / "dealix" / "config" / "founder_weekly_one_decision.yaml"
DOC_PATH = REPO_ROOT / "docs" / "commercial" / "FOUNDER_STRONGEST_PLAN_AR.md"


@lru_cache(maxsize=1)
def load_strongest_plan_checklist() -> dict[str, Any]:
    if not CHECKLIST_PATH.is_file():
        return {"version": "0", "tasks": [], "phases": []}
    data = yaml.safe_load(CHECKLIST_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _collect_paths(task: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for key in ("docs", "configs", "artifacts"):
        raw = task.get(key)
        if isinstance(raw, list):
            paths.extend(str(p) for p in raw)
    phase = task.get("phase")
    if phase is not None:
        for ph in load_strongest_plan_checklist().get("phases") or []:
            if isinstance(ph, dict) and ph.get("id") == phase and ph.get("doc"):
                paths.append(str(ph["doc"]))
    return paths


def strongest_plan_status() -> dict[str, Any]:
    """PASS when doc + checklist exist and linked repo paths resolve."""
    checklist = load_strongest_plan_checklist()
    tasks = checklist.get("tasks") or []
    missing: list[str] = []
    required_roots = [
        str(DOC_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        str(CHECKLIST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        str(WEEKLY_DECISION_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
    ]
    for rel in required_roots:
        if not (REPO_ROOT / rel).is_file():
            missing.append(rel)

    for task in tasks:
        if not isinstance(task, dict):
            continue
        for rel in _collect_paths(task):
            rel = rel.strip()
            if not rel or rel.startswith("POST ") or rel.startswith("GET "):
                continue
            if rel.startswith("/ar/"):
                continue
            if rel.endswith("/"):
                p = REPO_ROOT / rel.rstrip("/")
                if not p.is_dir() and not p.is_file():
                    missing.append(rel)
                continue
            p = REPO_ROOT / rel
            if not p.is_file() and not p.is_dir():
                missing.append(rel)

    weekly = checklist.get("weekly_one_decision") or {}
    tmpl = weekly.get("template_path")
    if tmpl and not (REPO_ROOT / str(tmpl)).is_file():
        missing.append(str(tmpl))

    task_count = len([t for t in tasks if isinstance(t, dict)])
    min_tasks = checklist.get("min_task_count")
    if not isinstance(min_tasks, int) or min_tasks < 1:
        min_tasks = 122 if str(checklist.get("version", "")).strip() == "2" else 28
    ok = (
        DOC_PATH.is_file()
        and CHECKLIST_PATH.is_file()
        and WEEKLY_DECISION_PATH.is_file()
        and task_count >= min_tasks
        and not missing
    )
    return {
        "ok": ok,
        "task_count": task_count,
        "min_task_count": min_tasks,
        "version": checklist.get("version"),
        "phase_count": len(checklist.get("phases") or []),
        "section_count": len(checklist.get("sections") or []),
        "missing_paths": sorted(set(missing)),
        "doc_path": str(DOC_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "checklist_path": str(CHECKLIST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def tasks_by_section() -> dict[str, list[dict[str, Any]]]:
    """Group checklist tasks by section id for Ops UI."""
    checklist = load_strongest_plan_checklist()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for task in checklist.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        section = str(task.get("section") or "other")
        grouped.setdefault(section, []).append(task)
    return grouped


def _build_full_ops_bridge(*, top_n: int = 10) -> dict[str, Any]:
    """Link strongest plan checklist to governed autonomous ops (no external send)."""
    from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
    from dealix.commercial_ops.founder_full_autopilot import (
        analyze_customer_stage_band,
        analyze_pls_readiness,
        build_autopilot_queue,
        compute_autopilot_verdict,
    )
    from dealix.commercial_ops.founder_max_ops_backlog import summarize_backlog
    from dealix.commercial_ops.full_ops_autopilot import (
        RESEARCH_ALIGNMENT_AR,
        build_full_autonomous_ops_snapshot,
    )

    comprehensive = build_comprehensive_status()
    autonomous = build_full_autonomous_ops_snapshot(top_n=top_n, include_nested=False)
    backlog = summarize_backlog()
    return {
        "research_verdict_ar": RESEARCH_ALIGNMENT_AR.get("verdict_ar"),
        "automation_readiness": autonomous.get("automation_readiness"),
        "founder_autopilot_verdict": compute_autopilot_verdict(comprehensive),
        "founder_queue": build_autopilot_queue(comprehensive)[:7],
        "customer_stage": analyze_customer_stage_band(),
        "pls_readiness": analyze_pls_readiness(),
        "max_ops_backlog": {
            "verdict": backlog.get("verdict"),
            "percent_done": backlog.get("percent_done"),
            "total": backlog.get("total"),
        },
        "commands": {
            "unified_run": "python scripts/run_founder_strongest_ops.py --full --run-checks",
            "morning_core": "python scripts/run_full_commercial_ops_autopilot.py --execute",
            "full_autopilot": "python scripts/run_founder_full_autopilot.py --mode full",
            "status": "python scripts/founder_strongest_plan_status.py",
        },
        "doc_path": "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
    }


def strongest_plan_snapshot(*, top_n: int = 10) -> dict[str, Any]:
    """Full payload for API: checklist metadata + wiring status + grouped tasks."""
    checklist = load_strongest_plan_checklist()
    status = strongest_plan_status()
    sections = checklist.get("sections") or []
    section_labels = {
        str(s.get("id")): str(s.get("label_ar") or s.get("id"))
        for s in sections
        if isinstance(s, dict) and s.get("id")
    }
    grouped = tasks_by_section()
    completion_blob: dict[str, Any] = {}
    try:
        from dealix.commercial_ops.founder_strongest_plan_completion import (
            enrich_checklist_with_completion,
        )

        completion_blob = enrich_checklist_with_completion(wiring_ok=status.get("ok"))
        by_id = {
            t["id"]: t
            for t in completion_blob.get("tasks") or []
            if isinstance(t, dict) and t.get("id")
        }
    except Exception as exc:
        by_id = {}
        completion_blob = {"error": str(exc)}

    sections_out = []
    for sid in sorted(grouped.keys()):
        tasks_enriched = []
        for task in grouped.get(sid, []):
            if not isinstance(task, dict):
                continue
            tid = task.get("id")
            merged = {**task}
            if tid and tid in by_id:
                merged["completion"] = by_id[tid].get("completion")
            tasks_enriched.append(merged)
        sections_out.append(
            {
                "id": sid,
                "label_ar": section_labels.get(sid, sid),
                "tasks": tasks_enriched,
            }
        )
    bridge: dict[str, Any] | None = None
    try:
        bridge = _build_full_ops_bridge(top_n=top_n)
    except Exception as exc:
        bridge = {"error": str(exc)}

    return {
        "status": status,
        "title_ar": checklist.get("title_ar"),
        "no_build_rule_ar": checklist.get("no_build_rule_ar"),
        "phases": checklist.get("phases") or [],
        "weekly_one_decision": checklist.get("weekly_one_decision") or {},
        "sections": sections_out,
        "full_ops_bridge": bridge,
        "completion": completion_blob.get("summary"),
        "completion_policy_ar": completion_blob.get("policy_ar"),
        "policy_ar": (
            "فل أوبس ذاتي = أتمتة داخلية كاملة حتى الموافقة الخارجية — "
            "لا واتساب/LinkedIn بارد."
        ),
    }
