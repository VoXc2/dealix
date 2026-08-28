#!/usr/bin/env python3
"""Verify retired/synthetic CEO Top50 actions cannot be treated as current execution."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "docs/ops/CEO_TOP50_TRACKER.csv"
WARM_TEMPLATE = ROOT / "data/warm_list.csv.template"
CEO_RUNNER = ROOT / "scripts/ceo_top50_execute.py"

QUARANTINED_ACTIONS = {
    "create_warm_list_file",
    "generate_bilingual_drafts",
    "run_first10_board",
    "prepare_499_pilot_brief",
    "prepare_invoice_dry_run",
    "record_payment_intent_confirmation",
    "run_delivery_kickoff",
    "generate_proof_pack_allow_empty",
    "run_hello_world_lead_pipeline",
    "lock_price_discipline_assets",
}

RETIRED_RUNTIME_MARKERS = (
    "prepare_499_pilot_brief",
    "7_day_revenue_proof_sprint",
    "--amount-sar 499",
)


def main() -> int:
    with TRACKER.open("r", encoding="utf-8", newline="") as handle:
        rows = {row["action"]: row for row in csv.DictReader(handle)}

    missing = sorted(QUARANTINED_ACTIONS - rows.keys())
    if missing:
        raise SystemExit(f"FAIL=MISSING_TRACKER_ACTIONS:{','.join(missing)}")

    active_bad = sorted(
        action
        for action in QUARANTINED_ACTIONS
        if rows[action]["status"] in {"DONE_NOW", "NEXT_7"}
    )
    if active_bad:
        raise SystemExit(f"FAIL=LEGACY_ACTION_REACTIVATED:{','.join(active_bad)}")

    wrong_state = sorted(
        action
        for action in QUARANTINED_ACTIONS
        if rows[action]["status"] != "LEGACY_QUARANTINED"
    )
    if wrong_state:
        raise SystemExit(f"FAIL=LEGACY_ACTION_NOT_QUARANTINED:{','.join(wrong_state)}")

    with WARM_TEMPLATE.open("r", encoding="utf-8", newline="") as handle:
        warm_rows = list(csv.DictReader(handle))
    populated = [row for row in warm_rows if any((value or "").strip() for value in row.values())]
    if populated:
        raise SystemExit("FAIL=WARM_TEMPLATE_CONTAINS_FABRICATED_RELATIONSHIP")

    runner = CEO_RUNNER.read_text(encoding="utf-8").lower()
    # Historical commands may remain in the runner for audit compatibility, but
    # the tracker must fail closed. Print the markers so operators know they are
    # legacy implementation debt rather than active commercial authority.
    present_markers = [marker for marker in RETIRED_RUNTIME_MARKERS if marker.lower() in runner]

    print("DEALIX_LEGACY_COMMERCIAL_EXECUTION_QUARANTINE=PASS")
    print(f"QUARANTINED_ACTIONS={len(QUARANTINED_ACTIONS)}")
    print(f"WARM_TEMPLATE_POPULATED_ROWS={len(populated)}")
    print(f"LEGACY_RUNNER_MARKERS_PRESENT={len(present_markers)}")
    print("AUTHORITY=CEO_TOP50_TRACKER_FAIL_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
