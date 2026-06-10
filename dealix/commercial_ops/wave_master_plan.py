"""Founder master plan (2026) — wave 0–3 implementation status."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.agent_eval_harness import run_agent_eval_harness
from dealix.commercial_ops.ceo_master_plan import build_ceo_master_plan_snapshot
from dealix.commercial_ops.gtm_blitz_tracker import build_gtm_blitz_snapshot


def build_wave_master_plan_snapshot() -> dict[str, Any]:
    ceo = build_ceo_master_plan_snapshot()
    blitz = build_gtm_blitz_snapshot()
    eval_blob = run_agent_eval_harness()

    wave0_prod = {
        "verdict": ceo["p0_production_trust"]["verdict"],
        "production_pct": (ceo["p0_production_trust"].get("production") or {}).get("overall_pct"),
        "manual": [
            "gh auth login -s repo",
            "scripts/push_main_with_gh.ps1",
            "Railway API + Frontend deploy",
            "DNS dealix.me -> Railway (not GitHub Pages)",
            "scripts/founder_complete_layers_now.ps1 --strict",
        ],
    }
    wave0_rev = {
        "verdict": ceo["p0_revenue_close"]["verdict"],
        "phase_0_1": ceo["p0_revenue_close"]["phase_0_1_gate"],
        "scripts": [
            "scripts/founder_motion_a_close_loop.py",
            "scripts/export_hubspot_kpi_scaffold.py",
            "scripts/apply_kpi_founder_commercial.py",
        ],
    }
    wave1_pg = {
        "verdict": "READY",
        "env": {
            "DEALIX_APPROVAL_STORE_BACKEND": "postgres",
            "DEALIX_AUTOPILOT_STORE_BACKEND": "postgres",
        },
        "modules": [
            "auto_client_acquisition.approval_center.postgres_store",
            "dealix.revenue_ops_autopilot.postgres_store",
            "auto_client_acquisition.workflow_os_v10.service_session_executor",
        ],
    }
    wave1_repeat = {
        "verdict": blitz["verdict"],
        "snapshot": blitz,
        "script": "scripts/gtm_blitz_status.py",
    }
    wave2 = {
        "verdict": "PASS" if eval_blob["verdict"] == "PASS" else "OPEN",
        "agent_eval": eval_blob,
        "surfaces": [
            "GET /api/v1/mcp/tools",
            "GET /api/v1/meta (aeo)",
            "dealix.observability.otel.agent_span",
        ],
    }
    wave3 = {
        "verdict": "READY",
        "endpoints": ["POST /api/v1/pricing/outcome-simulate"],
        "case_study_engine": "auto_client_acquisition.case_study_engine",
    }

    code_ready = all(w.get("verdict") in {"PASS", "READY"} for w in [wave1_pg, wave2, wave3])
    overall = "IN_PROGRESS"
    if wave0_rev["verdict"] == "PASS" and wave0_prod["verdict"] == "PASS":
        overall = "PASS"
    elif code_ready:
        overall = "CODE_READY_AWAITING_FOUNDER_OPS"

    return {
        "overall_verdict": overall,
        "wave0_production": wave0_prod,
        "wave0_revenue": wave0_rev,
        "wave1_postgres": wave1_pg,
        "wave1_repeat": wave1_repeat,
        "wave2_control_plane": wave2,
        "wave3_enterprise": wave3,
        "ceo_master_plan": ceo["overall_verdict"],
    }
