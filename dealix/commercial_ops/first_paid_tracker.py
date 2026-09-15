"""First verified commercial close tracker — free diagnostic → paid delivery.

Historical note: this module/file was originally named for a "first paid
Diagnostic" milestone. Dealix' current constitution makes *all* diagnostic
depths free. The canonical economic milestone tracked here is now the first
verified commercial close after a free diagnostic/discovery path. The legacy
function name remains as a compatibility alias for existing scripts and audit
history; it does not authorize diagnostic pricing.
"""

from __future__ import annotations

import csv
from typing import Any

from dealix.commercial_ops.evidence_csv import real_evidence_rows
from dealix.commercial_ops.paths import (
    EVIDENCE_TRACKER_CSV,
    REPO_ROOT,
    SOFT_LAUNCH_TRACKER_YAML,
    display_path,
)

EVIDENCE = EVIDENCE_TRACKER_CSV
KPI_YAML = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
# Historical DoD document retained for audit compatibility; current economic
# semantics are governed by DIAGNOSTIC_PRICE_POLICY below.
DOD_DOC = REPO_ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"
SOFT_LAUNCH_TRACKER = SOFT_LAUNCH_TRACKER_YAML
DIAGNOSTIC_PRICE_POLICY = "FREE_ALL_DEPTHS"

REVENUE_LADDER_AR = (
    "Free Execution Diagnostic → qualified discovery → customer-specific quote/intervention → "
    "verified payment/start authority → governed delivery → customer-validated Proof → stop / expand / redesign"
)


def _load_events() -> list[dict[str, str]]:
    if not EVIDENCE.is_file():
        return []
    with EVIDENCE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _company_key(row: dict[str, str]) -> str:
    """Normalize a company name without inventing entity resolution."""
    return " ".join((row.get("company") or "").strip().casefold().split())


def _companies_by_key(rows: list[dict[str, str]]) -> dict[str, str]:
    companies: dict[str, str] = {}
    for row in rows:
        key = _company_key(row)
        if not key:
            continue
        companies.setdefault(key, (row.get("company") or "").strip())
    return companies


def analyze_first_commercial_close() -> dict[str, Any]:
    """Track verified payment+proof closure after the free diagnostic path."""
    events = _load_events()
    real = real_evidence_rows(events)
    by_type: dict[str, list[dict[str, str]]] = {}
    for row in real:
        event_type = (row.get("event_type") or "").strip()
        by_type.setdefault(event_type, []).append(row)

    kpi_ok = KPI_YAML.is_file()
    crm_pending = True
    if kpi_ok:
        text = KPI_YAML.read_text(encoding="utf-8")
        crm_pending = "not_synced_yet" in text or "pending_founder_export" in text

    paid_real = by_type.get("payment_received", [])
    proof_real = by_type.get("proof_pack_delivered", [])
    paid_companies = _companies_by_key(paid_real)
    proof_companies = _companies_by_key(proof_real)

    matching_keys = sorted(set(paid_companies) & set(proof_companies))
    matching_close_companies = [
        paid_companies.get(key) or proof_companies[key] for key in matching_keys
    ]
    payment_without_proof_companies = [
        paid_companies[key]
        for key in sorted(set(paid_companies) - set(proof_companies))
    ]
    proof_without_payment_companies = [
        proof_companies[key]
        for key in sorted(set(proof_companies) - set(paid_companies))
    ]

    first_close_ready = bool(matching_close_companies and not crm_pending)
    if first_close_ready:
        verdict = "CLOSED"
    elif paid_real or proof_real:
        verdict = "IN_PROGRESS"
    else:
        verdict = "PIPELINE_OPEN"

    return {
        "evidence_path": display_path(EVIDENCE),
        "kpi_path": display_path(KPI_YAML) if kpi_ok else None,
        "total_events": len(events),
        "real_company_events": len(real),
        "invoice_sent_real": len(by_type.get("invoice_sent", [])),
        "payment_received_real": len(paid_real),
        "proof_pack_delivered_real": len(proof_real),
        "matching_close_real": len(matching_close_companies),
        "matching_close_companies": matching_close_companies,
        "payment_without_proof_companies": payment_without_proof_companies,
        "proof_without_payment_companies": proof_without_payment_companies,
        "crm_kpi_pending": crm_pending,
        "first_close_ready": first_close_ready,
        "dod_doc": display_path(DOD_DOC),
        "verdict": verdict,
        "revenue_ladder_ar": REVENUE_LADDER_AR,
        "soft_launch_tracker": display_path(SOFT_LAUNCH_TRACKER),
        "diagnostic_price_policy": DIAGNOSTIC_PRICE_POLICY,
        "canonical_milestone": "FIRST_VERIFIED_COMMERCIAL_CLOSE",
        "legacy_tracker_name": "first_paid_diagnostic",
    }


def analyze_first_paid_diagnostic() -> dict[str, Any]:
    """Compatibility alias; does *not* mean a diagnostic may be charged."""
    return analyze_first_commercial_close()


__all__ = [
    "DIAGNOSTIC_PRICE_POLICY",
    "REVENUE_LADDER_AR",
    "analyze_first_commercial_close",
    "analyze_first_paid_diagnostic",
]
