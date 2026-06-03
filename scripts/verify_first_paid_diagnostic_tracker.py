#!/usr/bin/env python3
"""Track first paid Diagnostic DoD from evidence CSV + KPI import (no invented revenue)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402


def analyze() -> dict[str, object]:
    return analyze_first_paid_diagnostic()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="Print machine-readable summary")
    args = p.parse_args()
    blob = analyze()

    if args.json:
        import json

        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== first_paid_diagnostic_tracker ==")
        print(f"  evidence: {blob['evidence_path']} ({blob['total_events']} rows)")
        print(f"  real-company events: {blob['real_company_events']}")
        print(f"  invoice_sent (real): {blob['invoice_sent_real']}")
        print(f"  payment_received (real): {blob['payment_received_real']}")
        print(f"  proof_pack_delivered (real): {blob['proof_pack_delivered_real']}")
        print(f"  kpi_import: {'ok' if blob['kpi_path'] else 'MISSING'}")
        print(f"  crm_kpi_pending: {blob['crm_kpi_pending']}")
        print(f"  DoD: {blob['dod_doc']}")

    print(f"FIRST_PAID_DIAGNOSTIC_VERDICT={blob['verdict']}")
    if blob["first_close_ready"]:
        return 0
    print("FOUNDER_ACTION: fill CRM KPI yaml + close one real Diagnostic per DoD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
