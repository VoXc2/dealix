#!/usr/bin/env python3
"""Verify OP2 B2G/partner research stays research-only with a no-bid default.

Prints: DEALIX_OP2_B2G_PARTNER_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PATH = REPO_ROOT / "data" / "commercial" / "op2_b2g_partner_research_v1.json"
VERDICT_PASS = "DEALIX_OP2_B2G_PARTNER_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_B2G_PARTNER_VERDICT=FAIL"


def main() -> int:
    errors: list[str] = []
    if not PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {PATH}")
        return 1
    try:
        payload = json.loads(PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-b2g-partner-research.v1":
        errors.append("unexpected schema")
    if payload.get("default_bid_posture") != "PARTNER_OR_NO_BID":
        errors.append("default_bid_posture must be PARTNER_OR_NO_BID")
    if any(bool(v) for v in (payload.get("authority") or {}).values()):
        errors.append("authority flags must all be false")
    if payload.get("counts_as_relationship") is not False or payload.get("counts_as_pipeline") is not False:
        errors.append("must not count as relationship/pipeline")

    for item in payload.get("b2g_items") or []:
        if item.get("bid_posture") != "PARTNER_OR_NO_BID":
            errors.append(f"{item.get('signal_id')}: bid posture must default to PARTNER_OR_NO_BID")
        if item.get("truth_class") != "RESEARCH_ONLY_NOT_SUBMISSION":
            errors.append(f"{item.get('signal_id')}: must be RESEARCH_ONLY_NOT_SUBMISSION")
        if item.get("counts_as_relationship") is not False:
            errors.append(f"{item.get('signal_id')}: must not count as relationship")

    for partner in payload.get("partner_candidates") or []:
        if partner.get("relationship_state") != "RESEARCH_ONLY":
            errors.append(f"{partner.get('partner_id')}: partner must stay RESEARCH_ONLY")
        if partner.get("counts_as_relationship") is not False:
            errors.append(f"{partner.get('partner_id')}: must not count as relationship")

    scores = [p.get("economic_score", 0) for p in payload.get("partner_candidates") or []]
    if scores != sorted(scores, reverse=True):
        errors.append("partner candidates must be ranked by descending economic_score")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
