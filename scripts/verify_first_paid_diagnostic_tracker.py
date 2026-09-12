#!/usr/bin/env python3
"""Verify first commercial close after a free diagnostic (legacy filename)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_commercial_close


def analyze() -> dict[str, object]:
    return analyze_first_commercial_close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable summary")
    args = parser.parse_args()
    blob = analyze()

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== first_verified_commercial_close_tracker ==")
        print("  legacy_filename: verify_first_paid_diagnostic_tracker.py")
        print(f"  diagnostic_price_policy: {blob['diagnostic_price_policy']}")
        print(f"  evidence: {blob['evidence_path']} ({blob['total_events']} rows)")
        print(f"  real-company events: {blob['real_company_events']}")
        print(f"  invoice_sent (real): {blob['invoice_sent_real']}")
        print(f"  payment_received (real): {blob['payment_received_real']}")
        print(f"  proof_pack_delivered (real): {blob['proof_pack_delivered_real']}")
        print(f"  kpi_import: {'ok' if blob['kpi_path'] else 'MISSING'}")
        print(f"  crm_kpi_pending: {blob['crm_kpi_pending']}")
        print(f"  historical_DoD: {blob['dod_doc']}")

    print(f"FIRST_VERIFIED_COMMERCIAL_CLOSE_VERDICT={blob['verdict']}")
    # Backward-compatible machine key for older dashboards/scripts. The key name
    # is historical only and must not be interpreted as diagnostic price authority.
    print(f"FIRST_PAID_DIAGNOSTIC_VERDICT={blob['verdict']}")
    if blob["first_close_ready"]:
        return 0
    print(
        "FOUNDER_ACTION: keep diagnostics free; qualify discovery, approve a customer-specific "
        "paid pilot/implementation, verify payment, deliver, then capture proof."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
