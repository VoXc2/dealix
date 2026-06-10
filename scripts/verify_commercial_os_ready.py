from __future__ import annotations

import sys
from pathlib import Path

required = [
    "docs/commercial/offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md",
    "docs/commercial/offers/P2_AI_SALES_OPS_ASSISTANT_AR.md",
    "docs/commercial/offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md",
    "docs/commercial/sales/DEALIX_OUTREACH_SEQUENCES_AR.md",
    "docs/commercial/sales/DEALIX_DISCOVERY_SCRIPT_AR.md",
    "docs/commercial/sales/DEALIX_OBJECTION_HANDLING_AR.md",
    "docs/commercial/proposals/P1_PROPOSAL_TEMPLATE_AR.md",
    "docs/commercial/ops/CEO_DAILY_OPERATING_SYSTEM_AR.md",
    "docs/commercial/scorecards/WEEKLY_REVENUE_SCORECARD_AR.md",
    "data/commercial/pipeline.csv",
    "data/outreach/manual_approval_queue.csv",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("COMMERCIAL_OS_READY=FAIL")
    for item in missing:
        print(f"missing={item}")
    sys.exit(1)

print("COMMERCIAL_OS_READY=PASS")
for item in required:
    print(f"ok={item}")
