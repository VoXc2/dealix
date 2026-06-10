"""Phase 0–1 close path — payment + proof + CRM KPI before platform expansion."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.evidence_csv import load_evidence_rows, real_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import REPO_ROOT

PHASE_GATE_DOC = REPO_ROOT / "docs/ops/FOUNDER_PHASE_0_1_GATE_AR.md"


def build_phase_01_close_path() -> dict[str, Any]:
    paid = analyze_first_paid_diagnostic()
    real_rows = real_evidence_rows(load_evidence_rows())
    discoveries = sum(
        1
        for r in real_rows
        if (r.get("event_type") or "").strip() in ("demo_booked", "scope_requested")
    )

    blockers: list[str] = []
    if not paid.get("payment_received_real"):
        blockers.append("سجّل payment_received حقيقي في evidence_events_tracker.csv")
    if not paid.get("proof_pack_delivered_real"):
        blockers.append("سجّل proof_pack_delivered بعد تسليم Proof Pack")
    if paid.get("crm_kpi_pending"):
        blockers.append("حدّث kpi_founder_commercial_import.yaml من CRM (لا أرقام مخترعة)")

    gate_open = paid.get("first_close_ready") and discoveries >= 1
    verdict = "PASS" if gate_open else ("IN_PROGRESS" if paid.get("verdict") == "IN_PROGRESS" else "BLOCKED")

    return {
        "verdict": verdict,
        "gate_open": gate_open,
        "no_platform_v10_until_pass": not gate_open,
        "first_paid": paid,
        "real_evidence_count": len(real_rows),
        "discovery_count": discoveries,
        "blockers_ar": blockers,
        "phase_doc": str(PHASE_GATE_DOC.relative_to(REPO_ROOT)).replace("\\", "/")
        if PHASE_GATE_DOC.is_file()
        else None,
    }
