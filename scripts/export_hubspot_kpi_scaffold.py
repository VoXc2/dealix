#!/usr/bin/env python3
"""Scaffold kpi_founder_commercial_import.yaml from HubSpot deals CSV export.

HubSpot export columns (flexible match):
  dealname, amount, closedate, dealstage, pipeline

Optional KPI mapping sources (extend entries when files exist):
  governance_integrity_rate  ← governance weekly report YAML/JSON (integrity_pct field)
  approval_cycle_time_hours  ← approval center export CSV (median hours column)
  time_to_proof_days         ← proof ledger CSV (days from payment to proof_pack)

Does NOT invent numbers — maps exported rows to registry keys where possible.
Founder must attest and fill remaining keys manually.

Usage:
  python scripts/export_hubspot_kpi_scaffold.py --hubspot-csv exports/deals.csv
  python scripts/export_hubspot_kpi_scaffold.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "dealix/transformation/kpi_founder_commercial_import.example.yaml"
TARGET = ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"


def _parse_amount(raw: str) -> float:
    cleaned = (raw or "").replace(",", "").replace(" SAR", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _summarize_hubspot_csv(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {"deal_count": 0, "total_amount_sar": 0.0, "period_label": "empty"}

    total = 0.0
    closed = 0
    for row in rows:
        keys = {k.lower(): v for k, v in row.items()}
        amount = _parse_amount(keys.get("amount") or keys.get("deal amount") or "0")
        total += amount
        stage = (keys.get("dealstage") or keys.get("deal stage") or "").lower()
        if "closed" in stage or "won" in stage:
            closed += 1

    period = datetime.now(UTC).strftime("%Y-W%V")
    return {
        "deal_count": len(rows),
        "closed_won_count": closed,
        "total_amount_sar": round(total, 2),
        "period_label": period,
        "source_ref": f"crm:hubspot:export:period={period}:deals={len(rows)}",
    }


def _summarize_governance(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            pct = data.get("integrity_pct") or data.get("governance_integrity_rate")
            if pct is not None:
                return {
                    "value_numeric": float(pct),
                    "source_ref": f"governance:weekly_report:{path.name}:integrity_pct",
                }
    return None


def _summarize_approval_export(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    hours: list[float] = []
    for row in rows:
        keys = {k.lower(): v for k, v in row.items()}
        raw = keys.get("cycle_hours") or keys.get("approval_cycle_time_hours") or keys.get("hours")
        try:
            hours.append(float(str(raw).replace(",", "")))
        except (TypeError, ValueError):
            continue
    if not hours:
        return None
    hours.sort()
    median = hours[len(hours) // 2]
    return {
        "value_numeric": round(median, 2),
        "source_ref": f"approval_center:export:{path.name}:median_hours",
    }


def _summarize_proof_ledger(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    days: list[float] = []
    for row in rows:
        keys = {k.lower(): v for k, v in row.items()}
        raw = keys.get("time_to_proof_days") or keys.get("days")
        try:
            days.append(float(str(raw).replace(",", "")))
        except (TypeError, ValueError):
            continue
    if not days:
        return None
    return {
        "value_numeric": round(sum(days) / len(days), 2),
        "source_ref": f"proof_ledger:{path.name}:avg_days",
    }


def build_import_yaml(
    *,
    hubspot_summary: dict[str, Any] | None = None,
    period_iso: str | None = None,
    governance_summary: dict[str, Any] | None = None,
    approval_summary: dict[str, Any] | None = None,
    proof_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    period = period_iso or datetime.now(UTC).date().isoformat()
    base = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8")) if EXAMPLE.is_file() else {}
    entries = dict(base.get("entries") or {})

    if hubspot_summary and hubspot_summary.get("deal_count", 0) > 0:
        ref = hubspot_summary["source_ref"]
        entries["measured_customer_value_sar"] = {
            "value_numeric": hubspot_summary["total_amount_sar"],
            "source_ref": ref,
        }
        if hubspot_summary["closed_won_count"] > 0:
            pct = round(
                100.0 * hubspot_summary["closed_won_count"] / max(hubspot_summary["deal_count"], 1),
                2,
            )
            entries["conversion_discovery_to_pilot"] = {
                "value_numeric": pct,
                "source_ref": f"{ref};metric=closed_won_ratio",
            }

    if governance_summary:
        entries["governance_integrity_rate"] = governance_summary
    if approval_summary:
        entries["approval_cycle_time_hours"] = approval_summary
    if proof_summary:
        entries["time_to_proof_days"] = proof_summary

    return {
        "version": 1,
        "founder_attestation": "أقر أن source_ref يشير إلى تصدير CRM/مالية فعلي",
        "updated_period_iso": period,
        "crm_sync_status": "hubspot_export_scaffolded" if hubspot_summary else "pending_founder_export",
        "entries": entries,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hubspot-csv", type=Path, help="HubSpot deals CSV export path")
    p.add_argument("--governance-report", type=Path, help="Governance weekly report YAML/JSON")
    p.add_argument("--approval-export", type=Path, help="Approval center CSV export")
    p.add_argument("--proof-ledger", type=Path, help="Proof ledger CSV (time_to_proof_days)")
    p.add_argument("--dry-run", action="store_true", help="Print YAML without writing")
    p.add_argument("--force", action="store_true", help="Overwrite existing import file")
    args = p.parse_args()

    summary = None
    if args.hubspot_csv:
        if not args.hubspot_csv.is_file():
            print(f"Missing CSV: {args.hubspot_csv}", file=sys.stderr)
            return 1
        summary = _summarize_hubspot_csv(args.hubspot_csv)

    gov = _summarize_governance(args.governance_report) if args.governance_report else None
    appr = _summarize_approval_export(args.approval_export) if args.approval_export else None
    proof = _summarize_proof_ledger(args.proof_ledger) if args.proof_ledger else None

    if TARGET.is_file() and not args.force and not args.dry_run:
        print(f"SKIP: {TARGET} exists (use --force to overwrite)")
        return 0

    doc = build_import_yaml(
        hubspot_summary=summary,
        governance_summary=gov,
        approval_summary=appr,
        proof_summary=proof,
    )
    text = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False)

    if args.dry_run:
        print(text)
        return 0

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(text, encoding="utf-8")
    print(f"WROTE {TARGET}")
    if summary:
        print(
            f"  deals={summary['deal_count']} total_sar={summary['total_amount_sar']} "
            f"ref={summary['source_ref']}"
        )
    print("Next: python scripts/apply_kpi_founder_commercial.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
