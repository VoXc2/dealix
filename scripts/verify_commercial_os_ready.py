"""Verify immutable Commercial OS source contracts, not mutable business state."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_CONTRACTS = (
    "docs/commercial/offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md",
    "docs/commercial/offers/P2_AI_SALES_OPS_ASSISTANT_AR.md",
    "docs/commercial/offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md",
    "docs/commercial/sales/DEALIX_OUTREACH_SEQUENCES_AR.md",
    "docs/commercial/sales/DEALIX_DISCOVERY_SCRIPT_AR.md",
    "docs/commercial/sales/DEALIX_OBJECTION_HANDLING_AR.md",
    "docs/commercial/proposals/P1_PROPOSAL_TEMPLATE_AR.md",
    "docs/commercial/ops/CEO_DAILY_OPERATING_SYSTEM_AR.md",
    "docs/commercial/scorecards/WEEKLY_REVENUE_SCORECARD_AR.md",
    "data/commercial/pipeline_sample.json",
    "data/outreach/approval_queue.csv",
    "data/outreach/saudi_target_intake.template.csv",
)

# These are runtime/business-state examples, not repository readiness authority.
NON_AUTHORITY_RUNTIME_STATE = (
    "data/commercial/pipeline.csv",
    "data/outreach/manual_approval_queue.csv",
)


def main() -> int:
    missing = [rel for rel in SOURCE_CONTRACTS if not (ROOT / rel).exists()]
    if missing:
        print("COMMERCIAL_OS_READY=FAIL")
        print("authority=IMMUTABLE_SOURCE_CONTRACTS")
        for item in missing:
            print(f"missing={item}")
        return 1

    print("COMMERCIAL_OS_READY=PASS")
    print("authority=IMMUTABLE_SOURCE_CONTRACTS")
    print("runtime_business_state_required=false")
    for item in SOURCE_CONTRACTS:
        print(f"ok={item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
