"""CEO Master Plan snapshot — unified workstream status for founder/CEO cadence."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    load_evidence_rows,
    real_evidence_rows,
)
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.founder_comprehensive_plan import analyze_phase_0_1_gate
from dealix.commercial_ops.paths import REPO_ROOT

PHASE_DEAL = REPO_ROOT / "dealix/config/phase_0_1_active_deal.yaml"
WEEKLY_DECISION = REPO_ROOT / "dealix/config/founder_weekly_one_decision.yaml"
GTM_BLITZ = REPO_ROOT / "dealix/config/gtm_blitz_90d.yaml"
PHASE2 = REPO_ROOT / "dealix/config/phase_2_repeatability.yaml"
PDPL_PASS = REPO_ROOT / "docs/commercial/operations/founder_pdpl_compliance_pass.yaml"
ICP_CSV = REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
CONV_CSV = REPO_ROOT / "docs/commercial/operations/gtm_conversation_tracker.csv"
PROPOSALS_DIR = REPO_ROOT / "docs/commercial/operations/proposals"
TRUST_PROPOSAL = REPO_ROOT / "docs/commercial/operations/TRUST_PACK_PROPOSAL_AR.md"
LAYERS_CACHE = REPO_ROOT / "dealix/transformation/production_layers_cache.json"
KPI_IMPORT = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"

P2_ARTIFACTS = (
    "docs/commercial/operations/CASE_STUDY_TEMPLATE_AR.md",
    "docs/commercial/operations/FOUNDER_SALES_PLAYBOOK_AR.md",
    "docs/commercial/operations/PARTNER_REFERRAL_KIT_AR.md",
    "docs/commercial/operations/DELIVERY_OPERATOR_HIRE_SPEC_AR.md",
)


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _production_pct() -> float | None:
    if not LAYERS_CACHE.is_file():
        return None
    try:
        data = json.loads(LAYERS_CACHE.read_text(encoding="utf-8"))
        pct = data.get("overall_pct")
        return float(pct) if pct is not None else None
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def build_daily_five_metrics() -> dict[str, Any]:
    """David Sacks-style 90-second CEO scan (no invented CRM numbers)."""
    today = datetime.now(UTC).date().isoformat()
    paid = analyze_first_paid_diagnostic()
    evidence = count_evidence_events(exclude_placeholders=True)
    real_rows = real_evidence_rows(load_evidence_rows())
    pipeline_open = sum(
        1
        for r in real_rows
        if (r.get("war_room_status") or "").strip()
        not in {"paid", "proof_pack_delivered", "closed_lost"}
    )
    paid_today = evidence["today_by_type"].get("payment_received", 0)
    prod_pct = _production_pct()

    return {
        "date": today,
        "metrics": {
            "1_new_paid_revenue_events_today": paid_today,
            "2_payment_received_real_total": paid["payment_received_real"],
            "3_proof_packs_delivered_total": paid["proof_pack_delivered_real"],
            "4_open_pipeline_leads_real": pipeline_open,
            "5_production_layers_pct": prod_pct,
        },
        "evidence_today_total": evidence["today_total"],
        "evidence_week_total": evidence["week_total"],
        "phase_0_1_verdict": paid["verdict"],
        "first_close_ready": paid["first_close_ready"],
        "crm_kpi_pending": paid["crm_kpi_pending"],
        "founder_action_ar": (
            "أغلق payment_received + proof_pack_delivered + KPI من HubSpot"
            if not paid["first_close_ready"]
            else "Phase 0–1 مغلقة — انتقل لـ Motion A repeat"
        ),
    }


def _count_icp_accounts() -> dict[str, int]:
    if not ICP_CSV.is_file():
        return {"total": 0, "eligible": 0}
    with ICP_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    eligible = 0
    for row in rows:
        company = (row.get("company") or "").strip()
        if not company or company.startswith("REPLACE:"):
            continue
        if "مثال" in company or "لا ترسل" in company:
            continue
        eligible += 1
    return {"total": len(rows), "eligible": eligible}


def _count_conversations() -> dict[str, int]:
    if not CONV_CSV.is_file():
        return {"total": 0, "filled": 0, "qualified": 0, "proposals": 0, "in_person": 0}
    with CONV_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    qualified = sum(1 for r in rows if (r.get("qualified") or "").lower() in {"true", "1", "yes"})
    proposals = sum(1 for r in rows if (r.get("proposal_sent") or "").lower() in {"true", "1", "yes"})
    in_person = sum(
        1
        for r in rows
        if (r.get("meeting_type") or "").lower() == "in_person" and (r.get("meeting_date") or "").strip()
    )
    filled = sum(1 for r in rows if (r.get("company") or "").strip())
    return {
        "total": len(rows),
        "filled": filled,
        "qualified": qualified,
        "proposals": proposals,
        "in_person": in_person,
    }


def _count_proposal_templates() -> int:
    if not PROPOSALS_DIR.is_dir():
        return 0
    return len(list(PROPOSALS_DIR.glob("DIAGNOSTIC_PROPOSAL_*.md")))


def _pdpl_status() -> dict[str, Any]:
    data = _load_yaml(PDPL_PASS)
    items = data.get("items") or []
    if not isinstance(items, list):
        items = []
    done = sum(1 for i in items if isinstance(i, dict) and i.get("done"))
    return {"total": len(items), "done": done, "items": items}


def _production_trust() -> dict[str, Any]:
    if LAYERS_CACHE.is_file():
        cache = json.loads(LAYERS_CACHE.read_text(encoding="utf-8"))
        return {
            "source": "cache",
            "verdict": cache.get("verdict"),
            "overall_pct": cache.get("overall_pct"),
            "trust_ok": (cache.get("trust_layer") or {}).get("ok"),
            "blockers_ar": cache.get("blockers_ar") or [],
        }
    return {"source": "missing", "verdict": "UNKNOWN", "overall_pct": 0, "trust_ok": False}


def _ceo_decision_config() -> dict[str, Any]:
    data = _load_yaml(WEEKLY_DECISION)
    decision = (data.get("one_decision_ar") or "").strip()
    week = (data.get("week_iso") or "").strip()
    return {
        "week_iso": week,
        "active_phase": data.get("active_phase"),
        "one_decision_filled": bool(decision),
        "one_decision_ar": decision,
        "success_by_friday_ar": (data.get("success_by_friday_ar") or "").strip(),
        "no_build_acknowledged": data.get("no_build_acknowledged"),
        "blocked_by": (data.get("blocked_by") or "").strip(),
        "config_path": _rel(WEEKLY_DECISION),
    }


def _phase_deal_summary() -> dict[str, Any]:
    data = _load_yaml(PHASE_DEAL)
    deal = data.get("active_deal") if isinstance(data.get("active_deal"), dict) else {}
    company = (deal.get("company") or "").strip() if isinstance(deal, dict) else ""
    return {
        "status": data.get("status", "open"),
        "company_filled": bool(company),
        "company": company[:80] if company else "",
        "motion": deal.get("motion") if isinstance(deal, dict) else None,
        "config_path": _rel(PHASE_DEAL),
        "close_path": data.get("close_path") if isinstance(data.get("close_path"), dict) else {},
    }


def build_ceo_master_plan_snapshot() -> dict[str, Any]:
    """Full CEO Master Plan status for API, UI, and morning scripts."""
    blitz = _load_yaml(GTM_BLITZ)
    targets = blitz.get("targets") or {}
    icp = _count_icp_accounts()
    conv = _count_conversations()
    proposals = _count_proposal_templates()
    paid = analyze_first_paid_diagnostic()
    pdpl = _pdpl_status()
    prod = _production_trust()
    decision = _ceo_decision_config()
    phase_deal = _phase_deal_summary()
    phase_gate = analyze_phase_0_1_gate()
    daily_five = build_daily_five_metrics()
    kpi_bootstrap = KPI_IMPORT.is_file()

    p0_revenue = {
        "verdict": "PASS" if paid["first_close_ready"] else "OPEN",
        "first_paid": paid,
        "kpi_import_present": kpi_bootstrap,
        "phase_deal": phase_deal,
        "phase_0_1_gate": {
            "verdict": phase_gate.get("verdict"),
            "blockers_ar": phase_gate.get("blockers_ar") or [],
        },
    }

    prod_pct = prod.get("overall_pct") or 0
    trust_ok = prod.get("trust_ok")
    p0_prod = {
        "verdict": "PASS" if prod_pct >= 80 and trust_ok else "OPEN",
        "production": prod,
        "dns_doc": "docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md",
        "trust_close_doc": "docs/ops/CEO_PRODUCTION_TRUST_CLOSE_AR.md",
        "redeploy_script": "scripts/railway_redeploy_checklist.py",
    }

    p0_decision = {
        "verdict": "PASS" if decision["one_decision_filled"] and decision.get("week_iso") else "OPEN",
        "decision": decision,
    }

    icp_min = int(targets.get("icp_accounts_min") or 75)
    conv_min = int(targets.get("qualified_conversations") or 30)
    prop_min = int(targets.get("diagnostic_proposals_sent") or 5)
    meet_min = int(targets.get("in_person_meetings") or 3)
    infra_ready = (
        icp["eligible"] >= icp_min
        and proposals >= prop_min
        and CONV_CSV.is_file()
        and GTM_BLITZ.is_file()
    )
    execution_ready = (
        conv["qualified"] >= conv_min
        and conv["proposals"] >= prop_min
        and conv["in_person"] >= meet_min
    )
    p0_gtm = {
        "verdict": "PASS" if infra_ready else "OPEN",
        "execution_verdict": "PASS" if execution_ready else "OPEN",
        "icp": icp,
        "icp_target": icp_min,
        "conversations": conv,
        "conversation_targets": {
            "qualified": conv_min,
            "proposals": prop_min,
            "in_person": meet_min,
        },
        "proposal_templates": proposals,
        "blitz_config": _rel(GTM_BLITZ),
    }

    trust_doc_ok = TRUST_PROPOSAL.is_file()
    pdpl_infra = trust_doc_ok and pdpl["total"] > 0
    p1_trust = {
        "verdict": "PASS" if pdpl_infra else "OPEN",
        "compliance_verdict": "PASS" if pdpl["done"] >= pdpl["total"] and pdpl["total"] > 0 else "OPEN",
        "pdpl": {"done": pdpl["done"], "total": pdpl["total"]},
        "trust_pack_path": _rel(TRUST_PROPOSAL) if trust_doc_ok else None,
    }

    phase2 = _load_yaml(PHASE2)
    p2_paths = [REPO_ROOT / rel for rel in P2_ARTIFACTS]
    p2_ready = all(p.is_file() for p in p2_paths)
    gate_open = phase_gate.get("gate_open") is True
    p2 = {
        "verdict": "PASS" if p2_ready else "OPEN",
        "artifacts_present": sum(1 for p in p2_paths if p.is_file()),
        "artifacts_total": len(p2_paths),
        "unlocked_when": phase2.get("unlocked_when"),
        "phase_2_hint_ar": (
            "Phase 0–1 مغلقة — ابدأ case study + partner referrals"
            if gate_open
            else "مقفل حتى Phase 0–1 PASS"
        ),
    }

    workstreams = [p0_revenue, p0_prod, p0_decision, p0_gtm, p1_trust, p2]
    all_pass = all(w["verdict"] == "PASS" for w in workstreams)
    overall = "PASS" if all_pass else "IN_PROGRESS"

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "overall_verdict": overall,
        "daily_five_metrics": daily_five,
        "p0_revenue_close": p0_revenue,
        "p0_production_trust": p0_prod,
        "p0_ceo_decision": p0_decision,
        "p0_gtm_blitz": p0_gtm,
        "p1_trust_pack": p1_trust,
        "p2_repeatability": p2,
        "scripts": {
            "status": "scripts/run_ceo_master_plan_status.py",
            "daily_five": "scripts/founder_daily_five_metrics.py",
            "close_helper": "scripts/phase_0_1_close_helper.py",
            "morning": "scripts/run_founder_commercial_day.ps1",
        },
    }


# Back-compat alias for tests/scripts
analyze_ceo_master_plan = build_ceo_master_plan_snapshot
