"""Revenue learning loop — fill weekly template from evidence CSV + KPI registry.

Never invents CRM numbers. KPI values appear only when founder import has
real source_ref (no not_synced_yet / pending_founder_export placeholders).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.revenue_os.learning_weekly import weekly_learning_report_skeleton
from dealix.commercial_ops.evidence_csv import (
    COMMERCIAL_EVIDENCE_TYPES,
    count_evidence_events,
    load_evidence_rows,
    real_evidence_rows,
)
from dealix.commercial_ops.paths import REPO_ROOT

KPI_REGISTRY_PATH = REPO_ROOT / "dealix/transformation/kpi_registry.yaml"
KPI_IMPORT_PATH = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
KPI_IMPORT_EXAMPLE = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.example.yaml"

_POSITIVE_EVENT_TYPES: frozenset[str] = frozenset(
    {
        "reply_received",
        "demo_booked",
        "scope_requested",
        "invoice_sent",
        "payment_received",
        "proof_pack_delivered",
        "partner_intro_created",
    }
)

_STALL_EVENT_TYPES: frozenset[str] = frozenset(
    {
        "message_sent_manual",
        "referral_requested",
    }
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _source_ref_is_real(source_ref: str) -> bool:
    ref = (source_ref or "").strip().lower()
    if not ref:
        return False
    blocked = ("not_synced_yet", "pending_founder_export", "replace:", "placeholder")
    return not any(token in ref for token in blocked)


def _week_anchor(on_date: datetime | None = None) -> str:
    dt = on_date or datetime.now(UTC)
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _kpi_registry_fields() -> list[dict[str, Any]]:
    data = _load_yaml(KPI_REGISTRY_PATH)
    rows: list[dict[str, Any]] = []
    buckets = data.get("kpis") or {}
    for bucket in ("north_star", "leading", "guardrails"):
        for row in buckets.get(bucket, []):
            if not isinstance(row, dict):
                continue
            ev = row.get("evidence") or {}
            rows.append(
                {
                    "key": row.get("key"),
                    "bucket": bucket,
                    "owner_os": row.get("owner_os"),
                    "weekly_proof_fields": list(ev.get("weekly_proof_fields") or []),
                    "primary_source": ev.get("primary_source"),
                }
            )
    return rows


def _kpi_import_entries() -> dict[str, Any]:
    path = KPI_IMPORT_PATH if KPI_IMPORT_PATH.is_file() else KPI_IMPORT_EXAMPLE
    data = _load_yaml(path)
    crm_status = str(data.get("crm_sync_status") or "").strip()
    entries = data.get("entries") or {}
    out: dict[str, Any] = {}
    for key, row in entries.items():
        if not isinstance(row, dict):
            continue
        source_ref = str(row.get("source_ref") or "")
        if _source_ref_is_real(source_ref):
            out[str(key)] = {
                "value_numeric": row.get("value_numeric"),
                "source_ref": source_ref,
                "synced": True,
            }
        else:
            out[str(key)] = {
                "value_numeric": None,
                "source_ref": source_ref,
                "synced": False,
            }
    return {
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "crm_sync_status": crm_status,
        "entries": out,
    }


def _learning_signals_from_evidence(
    *,
    week_by_type: dict[str, int],
    real_rows: list[dict[str, str]],
) -> dict[str, list[str]]:
    worked: list[str] = []
    failed: list[str] = []
    segments_stop: list[str] = []
    offer_signals: list[str] = []

    for et, count in sorted(week_by_type.items()):
        if count <= 0:
            continue
        if et in _POSITIVE_EVENT_TYPES:
            worked.append(f"أسبوع حالي: {count}× {et} (من evidence CSV — شركات حقيقية)")
        elif et in _STALL_EVENT_TYPES:
            failed.append(f"أسبوع حالي: {count}× {et} بدون تحويل لاحق في نفس الأسبوع")

    motions: dict[str, int] = {}
    for row in real_rows:
        motion = (row.get("motion") or "").strip()
        if motion:
            motions[motion] = motions.get(motion, 0) + 1
    for motion, count in sorted(motions.items(), key=lambda x: (-x[1], x[0])):
        if count >= 3:
            offer_signals.append(f"حركة {motion}: {count} أحداث — راجع ICP/عرض")

    if not week_by_type.get("reply_received") and week_by_type.get("message_sent_manual", 0) >= 2:
        segments_stop.append("رسائل يدوية بدون رد هذا الأسبوع — راجع القائمة أو القناة")

    return {
        "what_worked_ar": worked,
        "what_failed_ar": failed,
        "segments_to_stop_ar": segments_stop,
        "offer_price_signals_ar": offer_signals,
    }


def _funnel_metrics_from_evidence(counts: dict[str, Any]) -> dict[str, float | None]:
    week = counts.get("week_by_type") or {}
    signal = int(week.get("message_sent_manual", 0)) + int(week.get("reply_received", 0))
    lead = int(week.get("scope_requested", 0)) + int(week.get("demo_booked", 0))
    passport = int(week.get("scope_requested", 0))
    approved = int(week.get("invoice_sent", 0))
    proof = int(week.get("proof_pack_delivered", 0))
    expansion = int(week.get("partner_intro_created", 0)) + int(week.get("referral_requested", 0))

    def _ratio(num: int, den: int) -> float | None:
        if den <= 0:
            return None
        return round(num / den, 4)

    return {
        "signal_to_lead": _ratio(lead, signal) if signal else None,
        "lead_to_passport": _ratio(passport, lead) if lead else None,
        "passport_to_approved_action": _ratio(approved, passport) if passport else None,
        "delivery_to_proof": _ratio(proof, approved) if approved else None,
        "proof_to_expansion": _ratio(expansion, proof) if proof else None,
    }


def build_weekly_learning_report(
    *,
    on_date: datetime | None = None,
    evidence_path: Path | None = None,
) -> dict[str, Any]:
    """Merge skeleton + evidence counts + KPI registry (no invented CRM)."""
    skeleton = weekly_learning_report_skeleton()
    anchor = _week_anchor(on_date)
    rows = load_evidence_rows(evidence_path)
    real = real_evidence_rows(rows)
    counts = count_evidence_events(real, exclude_placeholders=False)
    signals = _learning_signals_from_evidence(
        week_by_type=counts.get("week_by_type") or {},
        real_rows=real,
    )

    kpi_import = _kpi_import_entries()
    kpi_registry = _kpi_registry_fields()
    synced_keys = [k for k, v in kpi_import["entries"].items() if v.get("synced")]

    report: dict[str, Any] = {
        **skeleton,
        "period": anchor,
        "generated_at": datetime.now(UTC).isoformat(),
        "what_worked_ar": signals["what_worked_ar"],
        "what_failed_ar": signals["what_failed_ar"],
        "segments_to_stop_ar": signals["segments_to_stop_ar"],
        "offer_price_signals_ar": signals["offer_price_signals_ar"],
        "repeated_feature_requests_ar": [],
        "workflow_simplifications_ar": [],
        "funnel_metrics": _funnel_metrics_from_evidence(counts),
        "evidence_summary": {
            "path": str((evidence_path or REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv").relative_to(REPO_ROOT)).replace("\\", "/"),
            "week_total": counts.get("week_total", 0),
            "week_by_type": counts.get("week_by_type") or {},
            "real_company_events": len(real),
            "tracked_event_types": sorted(COMMERCIAL_EVIDENCE_TYPES),
        },
        "kpi_registry": kpi_registry,
        "kpi_import": kpi_import,
        "crm_numbers_policy": (
            "No invented CRM numbers — values only when kpi_founder_commercial_import "
            "source_ref is real (not not_synced_yet)."
        ),
        "kpi_values_available": synced_keys,
        "notes_en": (
            f"Week {anchor}: evidence-backed funnel ratios; "
            f"{len(synced_keys)} KPI keys with real source_ref."
        ),
        "governance_decision": "allow_with_review",
    }
    return report


__all__ = ["build_weekly_learning_report"]
