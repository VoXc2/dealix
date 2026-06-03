"""First paid Diagnostic DoD — evidence CSV + KPI import (no invented revenue)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_csv import real_evidence_rows
from dealix.commercial_ops.paths import REPO_ROOT

EVIDENCE = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
KPI_YAML = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
DOD_DOC = REPO_ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"
SOFT_LAUNCH_TRACKER = REPO_ROOT / "docs/commercial/operations/soft_launch_meetings_tracker.yaml"

REVENUE_LADDER_AR = (
    "Diagnostic (Ops) 4,999–15,000 SAR → Sprint/Data Pack بعد الدفع → Growth 2,999 بعد Proof"
)


def _load_events() -> list[dict[str, str]]:
    if not EVIDENCE.is_file():
        return []
    with EVIDENCE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def analyze_first_paid_diagnostic() -> dict[str, Any]:
    events = _load_events()
    real = real_evidence_rows(events)
    by_type: dict[str, list[dict[str, str]]] = {}
    for row in real:
        et = (row.get("event_type") or "").strip()
        by_type.setdefault(et, []).append(row)

    kpi_ok = KPI_YAML.is_file()
    crm_pending = True
    if kpi_ok:
        text = KPI_YAML.read_text(encoding="utf-8")
        crm_pending = "not_synced_yet" in text or "pending_founder_export" in text

    paid_real = by_type.get("payment_received", [])
    proof_real = by_type.get("proof_pack_delivered", [])

    if paid_real and proof_real and not crm_pending:
        verdict = "CLOSED"
    elif paid_real or proof_real:
        verdict = "IN_PROGRESS"
    else:
        verdict = "PIPELINE_OPEN"

    return {
        "evidence_path": str(EVIDENCE.relative_to(REPO_ROOT)).replace("\\", "/"),
        "kpi_path": str(KPI_YAML.relative_to(REPO_ROOT)).replace("\\", "/") if kpi_ok else None,
        "total_events": len(events),
        "real_company_events": len(real),
        "invoice_sent_real": len(by_type.get("invoice_sent", [])),
        "payment_received_real": len(paid_real),
        "proof_pack_delivered_real": len(proof_real),
        "crm_kpi_pending": crm_pending,
        "first_close_ready": bool(paid_real and proof_real and not crm_pending),
        "dod_doc": str(DOD_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
        "verdict": verdict,
        "revenue_ladder_ar": REVENUE_LADDER_AR,
        "soft_launch_tracker": str(SOFT_LAUNCH_TRACKER.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
