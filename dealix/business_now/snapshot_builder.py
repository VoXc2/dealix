"""Assemble Business NOW snapshot from repo truth (no invented CRM numbers)."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.business_now.cache import apply_cache_to_platform, write_cache

_REPO = Path(__file__).resolve().parents[2]
_BASELINES = _REPO / "dealix" / "transformation" / "kpi_baselines.yaml"
_REGISTRY = _REPO / "dealix" / "transformation" / "kpi_founder_commercial_registry.yaml"
_PILOT = _REPO / "docs" / "transformation" / "evidence" / "pilot_sprint_tracker.yaml"
_HIRING = _REPO / "dealix" / "transformation" / "hiring_slots.yaml"
_OWNERSHIP = _REPO / "dealix" / "transformation" / "ownership_matrix.yaml"
_PHASE2 = _REPO / "dealix" / "transformation" / "phase2_checklist_status.yaml"

PILLAR_KEYS = (
    "commercial",
    "gtm",
    "delivery",
    "product",
    "compliance",
    "finance",
    "team",
    "platform",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _commercial_registry_status() -> dict[str, Any]:
    registry = _load_yaml(_REGISTRY)
    commercial = registry.get("commercial_entries") or {}
    pending: list[str] = []
    ready: list[str] = []
    for key, row in commercial.items():
        if not isinstance(row, dict):
            continue
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or not ref:
            pending.append(key)
        else:
            ready.append(key)
    return {
        "pending_keys": pending,
        "ready_keys": ready,
        "pending_count": len(pending),
        "ready_count": len(ready),
    }


def _kpi_snapshots() -> dict[str, Any]:
    baselines = _load_yaml(_BASELINES)
    return {
        "updated_period_iso": baselines.get("updated_period_iso"),
        "weekly_ops": baselines.get("weekly_ops"),
        "snapshots": baselines.get("snapshots") or {},
        "commercial_registry": _commercial_registry_status(),
    }


def _offers_summary() -> list[dict[str, Any]]:
    from api.routers.commercial_map import _build_payload

    payload = _build_payload()
    out: list[dict[str, Any]] = []
    for o in payload.get("offers") or []:
        w = o.get("wiring") or {}
        out.append(
            {
                "service_id": o.get("service_id"),
                "name_ar": o.get("name_ar"),
                "name_en": o.get("name_en"),
                "price_sar": o.get("price_sar"),
                "price_unit": o.get("price_unit"),
                "intake_endpoint": w.get("intake_endpoint") or w.get("lead_capture_endpoint"),
                "founder_surface": w.get("founder_surface"),
                "landing_url": w.get("landing_url"),
            }
        )
    return out


def _run_verify_transformation() -> str:
    script = _REPO / "scripts" / "verify_global_ai_transformation.py"
    try:
        proc = subprocess.run(  # noqa: S603 — internal script path; sys.executable is trusted
            [sys.executable, str(script)],
            cwd=str(_REPO),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        combined = (proc.stdout or "") + (proc.stderr or "")
        if "GLOBAL AI TRANSFORMATION: PASS" in combined:
            return "PASS"
        return "FAIL"
    except Exception:
        return "UNKNOWN"


def _run_verify_enterprise_control_plane() -> str:
    script = _REPO / "scripts" / "verify_enterprise_control_plane.sh"
    if not script.exists():
        return "UNKNOWN"
    try:
        proc = subprocess.run(  # noqa: S603 — internal verify script; controlled args
            ["bash", str(script)],  # noqa: S607 — PATH-resolved trusted tool
            cwd=str(_REPO),
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
        combined = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode == 0 and "ENTERPRISE CONTROL PLANE: PASS" in combined:
            return "PASS"
        if proc.returncode != 0:
            return "FAIL"
        return "FAIL"
    except Exception:
        return "UNKNOWN"


def _governed_domain_count() -> int:
    try:
        from auto_client_acquisition.governance_os.workflow_control_registry import (
            governed_domain_count,
        )

        return governed_domain_count()
    except Exception:
        return 0


def _phase2_items() -> list[dict[str, Any]]:
    data = _load_yaml(_PHASE2)
    return list(data.get("items") or [])


def _pilot_sprints() -> list[dict[str, Any]]:
    data = _load_yaml(_PILOT)
    return list(data.get("sprints") or [])


def _hiring_open() -> list[dict[str, Any]]:
    data = _load_yaml(_HIRING)
    slots = data.get("slots") or []
    return [s for s in slots if isinstance(s, dict) and s.get("status") == "open"]


def _ownership_review() -> dict[str, Any]:
    data = _load_yaml(_OWNERSHIP)
    return dict(data.get("executive_review") or {})


def _moyasar_env_hint() -> dict[str, Any]:
    key = (os.environ.get("MOYASAR_SECRET_KEY") or "").strip()
    if not key:
        return {
            "mode": "unset",
            "moyasar_live_allowed": False,
            "env_hint": "MOYASAR_SECRET_KEY not set (test keys only when configured)",
        }
    lower = key.lower()
    if "live" in lower:
        return {
            "mode": "live_key_present",
            "moyasar_live_allowed": False,
            "env_hint": "Live key detected — billing gate blocks auto-charge in non-prod",
        }
    return {
        "mode": "test",
        "moyasar_live_allowed": False,
        "env_hint": "Test/sandbox Moyasar key configured",
    }


def _compliance_pillar() -> dict[str, Any]:
    from api.routers.compliance_status import _module_present, _pdpl_status

    pdpl = _pdpl_status()
    pdpl_impl = sum(
        1 for v in pdpl.values() if isinstance(v, dict) and v.get("implemented")
    )
    return {
        "pdpl_doc": "docs/SECURITY_PDPL_CHECKLIST.md",
        "dpa_doc": "docs/DPA_PILOT_TEMPLATE.md",
        "whatsapp_doc": "docs/WHATSAPP_OPERATOR_FLOW.md",
        "gtm_bundle_cmd": "bash scripts/run_compliance_gtm_gate_bundle.sh",
        "pdpl_module_present": _module_present("integrations.pdpl"),
        "pdpl_articles_implemented": pdpl_impl,
        "pdpl_articles_total": len(pdpl),
        "overall_posture": f"{pdpl_impl}/{len(pdpl)} PDPL articles wired",
        "compliance_status_path": "/api/v1/compliance/status",
    }


def _gtm_pillar() -> dict[str, Any]:
    return {
        "leads_endpoint": "POST /api/v1/leads",
        "anti_waste_path": "/api/v1/revenue-os/anti-waste/check",
        "warm_list_doc": "docs/ops/SAUDI_LEAD_MACHINE_AR.md",
        "gtm_playbook_ref": "docs/GTM_PLAYBOOK.md",
        "channel_policy_path": "/api/v1/channel-policy/status",
        "trust_check_ui": "/trust-check",
    }


def build_today_actions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    commercial = snapshot["pillars"]["commercial"]
    delivery = snapshot["pillars"]["delivery"]
    platform = snapshot["pillars"]["platform"]

    if commercial.get("commercial_kpi_pending", 0) > 0:
        actions.append(
            {
                "priority": 1,
                "action_ar": "عبّئ KPIs التجارية من CRM في kpi_founder_commercial_import.yaml ثم apply",
                "href": "/business-now",
            }
        )

    verdict = platform.get("transformation_verdict")
    if verdict not in ("PASS",):
        actions.append(
            {
                "priority": 1,
                "action_ar": "أصلح فشل verify_global_ai_transformation قبل أي توسع GTM",
                "href": "/cloud",
            }
        )

    ecp = platform.get("enterprise_control_plane_verdict")
    if ecp == "FAIL":
        actions.append(
            {
                "priority": 1,
                "action_ar": "أصلح ENTERPRISE CONTROL PLANE — bash scripts/verify_enterprise_control_plane.sh",
                "href": "/cloud",
            }
        )

    sprints = delivery.get("pilot_sprints") or []
    template_ready = [s for s in sprints if s.get("status") == "template_ready"]
    if template_ready:
        actions.append(
            {
                "priority": 2,
                "action_ar": f"ابدأ بايلوت {template_ready[0].get('id', '')} — نفّذ PILOT_EXECUTION_RUNBOOK",
                "href": "/business-now",
            }
        )

    actions.append(
        {
            "priority": 3,
            "action_ar": "راجع موافقات اليوم — لا إرسال خارجي بدون جواز",
            "href": "/approvals",
        }
    )
    actions.append(
        {
            "priority": 4,
            "action_ar": "شغّل anti-waste قبل أي حملة أو رسالة خارجية",
            "href": "/trust-check",
        }
    )

    has_p1 = any(a["priority"] == 1 for a in actions)
    if not has_p1:
        summary = snapshot.get("commercial_strategy_summary") or {}
        preview = summary.get("weekly_motions_preview") or []
        if preview:
            m = preview[0]
            actions.append(
                {
                    "priority": 5,
                    "action_ar": str(m.get("action_ar", "حركة تجارية أسبوعية")),
                    "href": str(m.get("href", "/business-now")),
                }
            )

    actions.sort(key=lambda x: x["priority"])
    return actions


def build_business_now_snapshot(
    *,
    run_verify: bool = False,
    run_enterprise_cp: bool = False,
    persist_cache: bool = False,
) -> dict[str, Any]:
    """Build full snapshot. run_verify=True for offline generator (slow)."""
    if run_verify:
        transformation_verdict = _run_verify_transformation()
    else:
        transformation_verdict = "SKIP"

    if run_enterprise_cp or run_verify:
        enterprise_cp_verdict = _run_verify_enterprise_control_plane()
    else:
        enterprise_cp_verdict = "SKIP"

    governed = _governed_domain_count()
    commercial_reg = _commercial_registry_status()
    kpi = _kpi_snapshots()
    phase2 = _phase2_items()
    phase2_pending = sum(1 for i in phase2 if i.get("status") == "pending")
    moyasar = _moyasar_env_hint()

    platform: dict[str, Any] = {
        "transformation_verdict": transformation_verdict,
        "enterprise_control_plane_verdict": enterprise_cp_verdict,
        "governed_domains": governed,
        "weekly_anchor_cmd": "bash scripts/run_cto_weekly_anchor.sh",
        "business_now_cmd": "bash scripts/run_business_now.sh",
        "repair_cmd": "bash scripts/verify_enterprise_control_plane.sh",
    }

    if not run_verify:
        platform = apply_cache_to_platform(platform)
    else:
        platform["verdict_source"] = "live_verify"

    snapshot: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "pillars": {
            "commercial": {
                "offers": _offers_summary(),
                "commercial_kpi_pending": commercial_reg["pending_count"],
                "commercial_kpi_ready": commercial_reg["ready_count"],
                "pending_keys": commercial_reg["pending_keys"],
                "value_ladder_doc": "docs/value_capture/VALUE_CAPTURE_LADDER.md",
            },
            "gtm": _gtm_pillar(),
            "delivery": {
                "pilot_sprints": _pilot_sprints(),
                "pilot_tracker_ref": "docs/transformation/evidence/pilot_sprint_tracker.yaml",
                "runbook_ref": "docs/transformation/enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md",
            },
            "product": {
                "cloud_hub_path": "/cloud",
                "phase2_checklist_ref": "docs/PHASE2_PRIVATE_BETA_CHECKLIST.md",
                "phase2_pending_count": phase2_pending,
                "phase2_items": phase2,
            },
            "compliance": _compliance_pillar(),
            "finance": {
                "platform_snapshots": kpi.get("snapshots") or {},
                "moyasar_gate_doc": "docs/transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md",
                "moyasar_live_allowed": moyasar["moyasar_live_allowed"],
                "moyasar_mode": moyasar["mode"],
                "env_hint": moyasar["env_hint"],
            },
            "team": {
                "executive_review": _ownership_review(),
                "hiring_open": _hiring_open(),
                "hiring_open_count": len(_hiring_open()),
                "hiring_slots_ref": "dealix/transformation/hiring_slots.yaml",
            },
            "platform": platform,
        },
    }

    sprints = snapshot["pillars"]["delivery"].get("pilot_sprints") or []
    all_pilots_tr = bool(sprints) and all(s.get("status") == "template_ready" for s in sprints)
    from dealix.business_now.commercial_strategy import commercial_strategy_summary

    strat_summary = commercial_strategy_summary(
        commercial_kpi_pending=commercial_reg["pending_count"],
        transformation_verdict=str(platform.get("transformation_verdict") or "SKIP"),
        all_pilots_template_ready=all_pilots_tr,
    )
    snapshot["commercial_strategy_summary"] = strat_summary
    snapshot["pillars"]["commercial"]["commercial_strategy"] = strat_summary

    snapshot["today_actions"] = build_today_actions(snapshot)

    if persist_cache and run_verify:
        write_cache(
            transformation_verdict=platform["transformation_verdict"],
            enterprise_control_plane_verdict=platform["enterprise_control_plane_verdict"],
            governed_domains=governed,
            generated_at=snapshot["generated_at"],
        )

    return snapshot


def render_snapshot_markdown(snapshot: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Business NOW snapshot — {snapshot['generated_at'][:10]}")
    lines.append("")
    lines.append("## Platform")
    p = snapshot["pillars"]["platform"]
    lines.append(f"- transformation_verdict: {p.get('transformation_verdict')}")
    lines.append(f"- enterprise_control_plane_verdict: {p.get('enterprise_control_plane_verdict')}")
    lines.append(f"- governed_domains: {p.get('governed_domains')}")
    lines.append("")
    lines.append("## Commercial KPIs")
    c = snapshot["pillars"]["commercial"]
    lines.append(f"- pending: {c.get('commercial_kpi_pending')}")
    lines.append(f"- ready: {c.get('commercial_kpi_ready')}")
    lines.append("")
    lines.append("## Pilot sprints")
    for s in snapshot["pillars"]["delivery"].get("pilot_sprints") or []:
        lines.append(f"- {s.get('id')}: {s.get('status')}")
    lines.append("")
    lines.append("## Today actions")
    for a in snapshot.get("today_actions") or []:
        lines.append(f"- P{a['priority']}: {a['action_ar']}")
    lines.append("")
    lines.append("## Offers (summary)")
    for o in c.get("offers") or []:
        lines.append(
            f"- {o.get('service_id')}: {o.get('price_sar')} SAR — {o.get('name_ar', o.get('name_en'))}"
        )
    return "\n".join(lines) + "\n"
