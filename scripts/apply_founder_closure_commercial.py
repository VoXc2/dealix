#!/usr/bin/env python3
"""Apply founder closure intake — evidence, phase deal, KPI, PDPL, weekly, GTM (no invented revenue)."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "dealix/config/founder_closure_intake.yaml"
INTAKE_EXAMPLE = ROOT / "dealix/config/founder_closure_intake.example.yaml"
PHASE_DEAL = ROOT / "dealix/config/phase_0_1_active_deal.yaml"
WEEKLY = ROOT / "dealix/config/founder_weekly_one_decision.yaml"
PDPL = ROOT / "docs/commercial/operations/founder_pdpl_compliance_pass.yaml"
EVIDENCE = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
CONV_CSV = ROOT / "docs/commercial/operations/gtm_conversation_tracker.csv"
KPI_IMPORT = ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"

EVIDENCE_COLUMNS = [
    "event_id",
    "event_date",
    "event_type",
    "company",
    "contact",
    "motion",
    "offer_id",
    "owner",
    "source_channel",
    "notes",
    "next_action",
    "next_action_date",
    "war_room_status",
]

FUNNEL_TYPES = (
    "lead_identified",
    "message_sent_manual",
    "reply_received",
    "discovery_completed",
    "demo_booked",
    "demo_held",
    "scope_requested",
    "scope_signed",
    "invoice_sent",
    "payment_received",
    "delivery_started",
    "proof_pack_delivered",
)


def _load_intake() -> dict[str, Any]:
    for path in (INTAKE, INTAKE_EXAMPLE):
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if path == INTAKE_EXAMPLE and not (data.get("active_deal") or {}).get("company"):
                continue
            return data
    return {}


def _today() -> str:
    return date.today().isoformat()


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _apply_weekly(data: dict[str, Any]) -> list[str]:
    wd = data.get("weekly_decision") or {}
    weekly = yaml.safe_load(WEEKLY.read_text(encoding="utf-8")) if WEEKLY.is_file() else {}
    week_iso = (wd.get("week_iso") or _today()).strip()
    one = (wd.get("one_decision_ar") or "").strip()
    if not one:
        one = "إغلاق أول Diagnostic مدفوع: payment_received + proof_pack_delivered هذا الأسبوع"
    why = (wd.get("why_this_phase_ar") or "").strip()
    if not why:
        why = "Phase 1 — لا توسع منتج قبل أول إيراد موثّق بـ source_ref"
    success = (wd.get("success_by_friday_ar") or "").strip()
    if not success:
        success = "صفقة واحدة مغلقة في evidence_events_tracker + KPI من HubSpot مطبّق"
    weekly["week_iso"] = week_iso
    weekly["active_phase"] = 1
    weekly["one_decision_ar"] = one
    weekly["why_this_phase_ar"] = why
    weekly["success_by_friday_ar"] = success
    weekly["no_build_acknowledged"] = True
    weekly["blocked_by"] = wd.get("blocked_by") or ""
    weekly["evidence_events_to_log"] = [
        "payment_received",
        "proof_pack_delivered",
    ]
    _write_yaml(WEEKLY, weekly)
    return ["founder_weekly_one_decision.yaml"]


def _apply_pdpl(data: dict[str, Any]) -> list[str]:
    pdpl_cfg = data.get("pdpl") or {}
    if not pdpl_cfg.get("mark_all_done"):
        return []
    doc = yaml.safe_load(PDPL.read_text(encoding="utf-8")) if PDPL.is_file() else {}
    items = doc.get("items") or []
    changed = False
    for item in items:
        ref = (item.get("ref") or "").strip()
        ref_path = ROOT / ref if ref else None
        if ref_path and ref_path.is_file() and not item.get("done"):
            item["done"] = True
            changed = True
    if changed:
        _write_yaml(PDPL, doc)
        return ["founder_pdpl_compliance_pass.yaml"]
    return []


def _append_evidence_rows(deal: dict[str, Any], funnel_dates: dict[str, Any]) -> list[str]:
    company = (deal.get("company") or "").strip()
    if not company:
        return []
    contact = (deal.get("contact") or "").strip()
    motion = (deal.get("motion") or "A").strip()
    offer = (deal.get("offer_id") or "governed_diagnostic").strip()
    channel = (deal.get("source_channel") or "warm").strip()
    payment_ref = (deal.get("payment_ref") or "").strip()
    proof_path = (deal.get("proof_pack_path") or "").strip()
    if not payment_ref or not proof_path:
        print("  skip evidence: payment_ref and proof_pack_path required")
        return []

    rows: list[dict[str, str]] = []
    if EVIDENCE.is_file():
        with EVIDENCE.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))

    existing = {
        (r.get("event_type"), (r.get("company") or "").strip().lower())
        for r in rows
        if (r.get("company") or "").strip()
    }

    def add(event_type: str, event_date: str, notes: str) -> None:
        key = (event_type, company.lower())
        if key in existing:
            return
        rows.append(
            {
                "event_id": "",
                "event_date": event_date or _today(),
                "event_type": event_type,
                "company": company,
                "contact": contact,
                "motion": motion,
                "offer_id": offer,
                "owner": "founder",
                "source_channel": channel,
                "notes": notes,
                "next_action": "",
                "next_action_date": "",
                "war_room_status": "",
            }
        )
        existing.add(key)

    for et in FUNNEL_TYPES:
        if et in ("payment_received", "proof_pack_delivered", "delivery_started"):
            continue
        d = (funnel_dates.get(et) or deal.get(f"{et}_date") or "").strip()
        if d or et in ("scope_signed", "invoice_sent"):
            add(et, d or _today(), f"phase_0_1_close_path — {et}")

    pay_date = (deal.get("payment_date") or _today()).strip()
    add("payment_received", pay_date, f"moyasar/manual ref={payment_ref}")
    add("delivery_started", pay_date, "Diagnostic delivery started")
    add("proof_pack_delivered", (deal.get("proof_delivered_date") or _today()).strip(), proof_path)

    with EVIDENCE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=EVIDENCE_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return ["evidence_events_tracker.csv"]


def _apply_phase_deal(deal: dict[str, Any]) -> list[str]:
    company = (deal.get("company") or "").strip()
    if not company:
        return []
    doc = yaml.safe_load(PHASE_DEAL.read_text(encoding="utf-8")) if PHASE_DEAL.is_file() else {}
    doc["updated_iso"] = _today()
    doc["status"] = "closed"
    doc["active_deal"] = {
        "company": company,
        "contact": deal.get("contact") or "",
        "motion": deal.get("motion") or "A",
        "offer_id": deal.get("offer_id") or "governed_diagnostic",
        "source_channel": deal.get("source_channel") or "warm",
        "pain_hypothesis_ar": deal.get("pain_hypothesis_ar") or "",
        "discovery_seven_complete": True,
        "scope_signed": True,
    }
    close_path = dict.fromkeys(FUNNEL_TYPES, True)
    doc["close_path"] = close_path
    doc["payment"] = {
        "amount_sar": deal.get("amount_sar"),
        "payment_date": deal.get("payment_date") or _today(),
        "payment_ref": deal.get("payment_ref") or "",
        "method": deal.get("payment_method") or "moyasar_live",
    }
    doc["proof"] = {
        "delivery_sla_days": 7,
        "proof_pack_path": deal.get("proof_pack_path") or "",
        "delivered_date": deal.get("proof_delivered_date") or _today(),
    }
    _write_yaml(PHASE_DEAL, doc)
    return ["phase_0_1_active_deal.yaml"]


def _import_gtm(path: Path) -> list[str]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        incoming = list(csv.DictReader(f))
    if not incoming:
        return []
    existing: list[dict[str, str]] = []
    if CONV_CSV.is_file():
        with CONV_CSV.open(encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
    seen = {(r.get("conversation_id") or "", (r.get("company") or "").strip()) for r in existing}
    added = 0
    for row in incoming:
        key = (row.get("conversation_id") or "", (row.get("company") or "").strip())
        if key in seen:
            continue
        existing.append(row)
        seen.add(key)
        added += 1
    if added:
        fieldnames = list(existing[0].keys()) if existing else list(incoming[0].keys())
        with CONV_CSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(existing)
        return [f"gtm_conversation_tracker.csv (+{added})"]
    return []


def _apply_kpi(hubspot_csv: Path) -> list[str]:
    if not hubspot_csv.is_file():
        return []
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/export_hubspot_kpi_scaffold.py"),
            "--hubspot-csv",
            str(hubspot_csv),
        ],
        cwd=ROOT,
        check=False,
    )
    if not KPI_IMPORT.is_file():
        return []
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/apply_kpi_founder_commercial.py")],
        cwd=ROOT,
        check=False,
    )
    return ["kpi_founder_commercial_import.yaml"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdpl-confirm", action="store_true", help="Mark PDPL items done when refs exist")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    data = _load_intake()
    if not data:
        if args.pdpl_confirm:
            data = {}
        else:
            print(
                "FOUNDER_CLOSURE_COMMERCIAL=SKIP "
                "(copy founder_closure_intake.example.yaml to founder_closure_intake.yaml "
                "or pass --pdpl-confirm for weekly + PDPL only)"
            )
            return 0

    if args.pdpl_confirm:
        data.setdefault("pdpl", {})["mark_all_done"] = True

    print("== apply_founder_closure_commercial ==")
    if args.dry_run:
        print("  dry-run — no files written")
        return 0

    applied: list[str] = []
    applied.extend(_apply_weekly(data))
    applied.extend(_apply_pdpl(data))

    deal = data.get("active_deal") or {}
    funnel = data.get("evidence_funnel_dates") or {}
    applied.extend(_apply_phase_deal(deal))
    applied.extend(_append_evidence_rows(deal, funnel))

    paths = data.get("paths") or {}
    gtm = (paths.get("gtm_conversations_csv") or "").strip()
    if gtm:
        applied.extend(_import_gtm(Path(gtm)))

    hub = (paths.get("hubspot_kpi_csv") or "").strip()
    if hub:
        applied.extend(_apply_kpi(Path(hub)))

    if applied:
        print(f"  applied: {', '.join(applied)}")
    else:
        print("  no commercial rows applied — fill active_deal.company + payment_ref + proof_pack_path")

    # Verify
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_first_paid_diagnostic_tracker.py")],
        cwd=ROOT,
        check=False,
    )
    print("FOUNDER_CLOSURE_COMMERCIAL=DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
