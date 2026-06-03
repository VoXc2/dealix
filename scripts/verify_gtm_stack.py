#!/usr/bin/env python3
"""Verify GTM stack docs, config, and snapshot."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

REQUIRED_DOCS = [
    "docs/commercial/GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md",
    "docs/commercial/operations/GTM_DUAL_TRACK_CLARIFICATION_AR.md",
    "docs/commercial/operations/FOUNDER_SALES_LOOP_AR.md",
    "docs/commercial/operations/PROOF_STACK_ORDER_AR.md",
    "docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md",
    "docs/commercial/operations/GTM_CHANNELS_PLAYBOOK_AR.md",
    "docs/commercial/operations/GTM_OBJECTION_MATRIX_AR.md",
    "docs/commercial/operations/GTM_WEEKLY_REVIEW_CHECKLIST_AR.md",
    "dealix/config/gtm_abm_wave1.yaml",
]


def main() -> int:
    missing = [p for p in REQUIRED_DOCS if not (REPO / p).is_file()]
    if missing:
        print("DEALIX_GTM_STACK_VERDICT=FAIL")
        for m in missing:
            print(f"missing: {m}")
        return 1

    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

    snap = build_gtm_stack_snapshot(abm_top_n=5)
    if not snap.get("dual_track"):
        print("DEALIX_GTM_STACK_VERDICT=FAIL")
        print("invalid snapshot")
        return 1

    print("DEALIX_GTM_STACK_VERDICT=PASS")
    print(f"track={snap['dual_track']['recommended_track']}")
    print(f"abm_active={snap['abm_wave1']['active_rows']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
