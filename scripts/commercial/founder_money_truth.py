#!/usr/bin/env python3
"""Build a conservative founder money-truth snapshot from repository evidence.

This script is read-only. It never sends, charges, publishes, quotes, deploys,
or mutates production. Unknown financial amounts remain UNKNOWN.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EVIDENCE = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
PUBLIC_SURFACES = (
    ROOT / "landing/pricing.html",
    ROOT / "landing/services.html",
    ROOT / "landing/ai-team.html",
    ROOT / "landing/start.html",
    ROOT / "landing/launchpad.html",
    ROOT / "landing/workflow.html",
)

NON_REAL_MARKERS = (
    "template_funnel_seed",
    "synthetic",
    "demo_only",
    "placeholder",
    "internal go-live validation",
)

PUBLIC_FORBIDDEN_MARKERS = (
    "499 sar",
    "٤٩٩",
    "5,000 sar",
    "٥٬٠٠٠",
    "12,000 sar",
    "١٢٬٠٠٠",
    "1,500–2,500",
    "١٬٥٠٠–٢٬٥٠٠",
    "7-day pilot",
    "7-day sprint",
    "buy today",
    "اشتر اليوم",
    "استرجاع كامل",
    "refund guarantee",
    "pdpl compliant",
    "pdpl-ready",
    "saudi data residency",
    "zatca-ready",
    "sla 99",
)


def _read_rows() -> list[dict[str, str]]:
    if not EVIDENCE.exists():
        return []
    with EVIDENCE.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _looks_real_customer_event(row: dict[str, str]) -> bool:
    event_id = (row.get("event_id") or "").strip()
    company = (row.get("company") or "").strip()
    notes = (row.get("notes") or "").strip().lower()
    source = (row.get("source_channel") or "").strip().lower()
    if not event_id or not company:
        return False
    joined = f"{company.lower()} {notes} {source}"
    if any(marker in joined for marker in NON_REAL_MARKERS):
        return False
    if company.lower().startswith("dealix founder") or company.lower().startswith("dealix internal"):
        return False
    return True


def _public_truth() -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    for path in PUBLIC_SURFACES:
        relative = str(path.relative_to(ROOT))
        if not path.exists():
            findings.append({"path": relative, "issue": "missing_surface"})
            continue
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for marker in PUBLIC_FORBIDDEN_MARKERS:
            if marker.lower() in text:
                findings.append(
                    {
                        "path": relative,
                        "issue": "legacy_public_commercial_marker",
                        "marker": marker,
                    }
                )
        if path.name in {"start.html", "launchpad.html"}:
            if "<form" in text or "fetch(" in text:
                findings.append(
                    {
                        "path": relative,
                        "issue": "legacy_direct_capture_or_submit_surface",
                    }
                )
    return {
        "status": "PASS" if not findings else "BLOCKED",
        "findings": findings,
        "authority": "Free Execution Diagnostic -> Qualified Discovery -> Customer-specific Quote/Intervention -> Verified Payment/Start Authority -> Governed Delivery -> Customer-Validated Proof -> STOP/EXPAND/REDESIGN",
    }


def _finance_policies() -> dict[str, Any]:
    try:
        from dealix.commercial_finance import DEFAULT_POLICIES
    except Exception as exc:  # read-only visibility; do not fail the whole snapshot
        return {"status": "UNKNOWN", "reason": type(exc).__name__}

    policies: dict[str, Any] = {}
    for offer_class, policy in DEFAULT_POLICIES.items():
        policies[str(offer_class.value)] = {
            "gross_margin_floor_pct": float(policy.gross_margin_floor * 100),
            "contribution_margin_floor_pct": float(policy.contribution_margin_floor * 100),
            "max_discount_pct": float(policy.max_discount_pct),
            "max_upfront_cash_exposure_sar": float(policy.max_upfront_cash_exposure_sar),
            "max_payment_terms_days": policy.max_payment_terms_days,
            "max_capacity_required_pct": float(policy.max_capacity_required_pct),
        }
    return {
        "status": "AVAILABLE",
        "approval_required": True,
        "external_action_allowed": False,
        "policies": policies,
    }


def build_snapshot() -> dict[str, Any]:
    rows = _read_rows()
    real_rows = [row for row in rows if _looks_real_customer_event(row)]
    payments = [row for row in real_rows if (row.get("event_type") or "").strip() == "payment_received"]
    invoices = [row for row in real_rows if (row.get("event_type") or "").strip() == "invoice_sent"]
    proofs = [row for row in real_rows if (row.get("event_type") or "").strip() == "proof_pack_delivered"]

    paid_companies = {(row.get("company") or "").strip() for row in payments}
    collection_candidates = [
        row for row in invoices if (row.get("company") or "").strip() not in paid_companies
    ]

    fieldnames: list[str] = []
    if EVIDENCE.exists():
        with EVIDENCE.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            fieldnames = next(reader, [])
    amount_fields = {"amount", "amount_sar", "revenue_sar", "cash_sar", "invoice_amount_sar"}
    schema_has_amount = bool(amount_fields.intersection({name.strip() for name in fieldnames}))

    public = _public_truth()
    finance = _finance_policies()

    blockers: list[dict[str, str]] = []
    if public["status"] != "PASS":
        blockers.append(
            {
                "priority": "P0",
                "area": "public_commercial_truth",
                "action": "Remove legacy public fixed-price, direct-capture, refund, compliance-certification, or buy-now authority before growth traffic.",
            }
        )
    if not payments:
        blockers.append(
            {
                "priority": "P0",
                "area": "cash",
                "action": "Advance one qualified real company through discovery, approved customer-specific quote, verified payment evidence, then delivery proof.",
            }
        )
    if not proofs:
        blockers.append(
            {
                "priority": "P1",
                "area": "proof",
                "action": "Do not claim customer value; create a Proof Pack only after real delivery evidence exists.",
            }
        )
    if not schema_has_amount:
        blockers.append(
            {
                "priority": "P1",
                "area": "finance_data",
                "action": "Connect an approved accounting/payment source for cash amount, invoices, expenses, VAT fields, and runway; event counts alone are insufficient.",
            }
        )

    return {
        "source": str(EVIDENCE.relative_to(ROOT)),
        "source_exists": EVIDENCE.exists(),
        "source_schema_has_cash_amount": schema_has_amount,
        "verified_customer_event_count": len(real_rows),
        "verified_payment_event_count": len(payments),
        "verified_proof_pack_event_count": len(proofs),
        "verified_invoice_event_count": len(invoices),
        "verified_collection_candidate_count": len(collection_candidates),
        "verified_cash_sar": "UNKNOWN" if not schema_has_amount else "REQUIRES_AMOUNT_PARSER",
        "outstanding_collections_sar": "UNKNOWN" if not schema_has_amount else "REQUIRES_AMOUNT_PARSER",
        "monthly_burn_sar": "UNKNOWN",
        "cash_on_hand_sar": "UNKNOWN",
        "runway_months": "UNKNOWN",
        "gross_margin_actual_pct": "UNKNOWN" if not payments else "REQUIRES_VERIFIED_PAYMENT_AMOUNT_AND_DELIVERY_COST",
        "public_commercial_truth": public,
        "commercial_finance_policy": finance,
        "top_blockers": blockers[:5],
        "safety": {
            "live_send": False,
            "live_charge": False,
            "quote_authority": False,
            "production_mutation": False,
            "fake_proof": False,
        },
    }


def main() -> int:
    print(json.dumps(build_snapshot(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
