#!/usr/bin/env python3
"""Verify the OP2 sector-economy ranking artifact is present and research-only.

Prints: DEALIX_OP2_SECTOR_ECONOMY_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RANKING_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_economy_ranking_v1.json"

VERDICT_PASS = "DEALIX_OP2_SECTOR_ECONOMY_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_SECTOR_ECONOMY_VERDICT=FAIL"
MAX_STATUS = "RESEARCHED_WITH_SIGNALS"


def main() -> int:
    errors: list[str] = []
    if not RANKING_PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {RANKING_PATH}")
        return 1
    try:
        payload = json.loads(RANKING_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-sector-economy.v1":
        errors.append("unexpected schema")
    if payload.get("status_ceiling") != MAX_STATUS:
        errors.append(f"status_ceiling must be {MAX_STATUS}")
    if payload.get("counts_as_pipeline") is not False or payload.get("counts_as_revenue") is not False:
        errors.append("counts_as_pipeline/counts_as_revenue must be false")

    cells = payload.get("cells") or []
    if not cells:
        errors.append("no cells ranked")
    scores = [cell.get("research_rank_score") for cell in cells]
    if scores != sorted(scores, reverse=True):
        errors.append("cells must be sorted by descending research_rank_score")
    for cell in cells:
        if cell.get("status") != MAX_STATUS:
            errors.append(f"{cell.get('sector_id')}: status exceeds ceiling")
        if cell.get("counts_as_pipeline") is not False:
            errors.append(f"{cell.get('sector_id')}: counts_as_pipeline must be false")
        if not cell.get("evidence_refs"):
            errors.append(f"{cell.get('sector_id')}: missing evidence_refs")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
