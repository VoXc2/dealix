#!/usr/bin/env python3
"""Phase 0–1 close helper — append evidence events from active deal config (no invented payments)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.evidence_append import append_evidence_row  # noqa: E402
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402
from dealix.commercial_ops.paths import REPO_ROOT  # noqa: E402

PHASE_DEAL = REPO_ROOT / "dealix/config/phase_0_1_active_deal.yaml"
EVIDENCE = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
DOD_DOC = REPO_ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"

ALLOWED_EVENTS = frozenset(
    {
        "invoice_sent",
        "payment_received",
        "proof_pack_delivered",
        "scope_requested",
        "demo_booked",
        "message_sent_manual",
        "reply_received",
    }
)


def _load_deal() -> dict[str, Any]:
    if not PHASE_DEAL.is_file():
        return {}
    data = yaml.safe_load(PHASE_DEAL.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _append_evidence_row(
    *,
    company: str,
    event_type: str,
    notes: str = "",
    contact: str = "",
    motion: str = "A",
    offer_id: str = "governed_diagnostic",
    source_channel: str = "warm",
) -> dict[str, str]:
    return append_evidence_row(
        event_type=event_type,
        company=company,
        contact=contact,
        motion=motion,
        offer_id=offer_id,
        source_channel=source_channel,
        notes=notes or f"phase_0_1_close_helper:{event_type}",
        war_room_status=event_type,
    )


def _dod_checklist(paid: dict[str, Any]) -> list[str]:
    lines = [
        f"  invoice_sent (real): {paid.get('invoice_sent_real', 0)}",
        f"  payment_received (real): {paid.get('payment_received_real', 0)}",
        f"  proof_pack_delivered (real): {paid.get('proof_pack_delivered_real', 0)}",
        f"  CRM KPI pending: {paid.get('crm_kpi_pending')}",
        f"  verdict: {paid.get('verdict')}",
        f"  dod_doc: {DOD_DOC.relative_to(REPO_ROOT)}",
    ]
    return lines


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--event",
        required=True,
        choices=sorted(ALLOWED_EVENTS),
        help="Evidence event type to append",
    )
    p.add_argument("--notes", default="", help="Optional notes (no payment refs invented)")
    p.add_argument("--amount-sar", default="", help="Only for payment_received — founder must supply")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--check-dod", action="store_true", help="Print DoD status without appending")
    args = p.parse_args()

    deal_cfg = _load_deal()
    active = deal_cfg.get("active_deal") if isinstance(deal_cfg.get("active_deal"), dict) else {}
    company = (active.get("company") or "").strip()
    if not company:
        print("REFUSE: active_deal.company is empty — fill dealix/config/phase_0_1_active_deal.yaml", file=sys.stderr)
        return 1

    if args.event == "payment_received" and not (args.amount_sar or "").strip():
        payment = deal_cfg.get("payment") if isinstance(deal_cfg.get("payment"), dict) else {}
        amount = payment.get("amount_sar")
        if amount is None or amount == "":
            print(
                "REFUSE: payment_received requires --amount-sar or payment.amount_sar in config",
                file=sys.stderr,
            )
            return 1

    paid = analyze_first_paid_diagnostic()
    if args.check_dod:
        print("== FIRST_PAID_DIAGNOSTIC DoD ==")
        for line in _dod_checklist(paid):
            print(line)
        return 0 if paid.get("first_close_ready") else 1

    amount = (args.amount_sar or "").strip()
    if not amount:
        payment = deal_cfg.get("payment") if isinstance(deal_cfg.get("payment"), dict) else {}
        if payment.get("amount_sar") is not None:
            amount = str(payment.get("amount_sar"))

    if args.dry_run:
        print(f"DRY-RUN append: company={company} event={args.event} amount_sar={amount or '-'}")
        return 0

    row = _append_evidence_row(
        company=company,
        event_type=args.event,
        notes=args.notes,
        contact=(active.get("contact") or "").strip(),
        motion=(active.get("motion") or "A").strip(),
        offer_id=(active.get("offer_id") or "governed_diagnostic").strip(),
        source_channel=(active.get("source_channel") or "warm").strip(),
    )
    print(
        f"APPENDED {EVIDENCE.relative_to(REPO_ROOT)}: "
        f"{row.get('event_date')} {row.get('company')} {row.get('event_type')}"
    )

    paid_after = analyze_first_paid_diagnostic()
    print("\n== DoD after append ==")
    for line in _dod_checklist(paid_after):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
