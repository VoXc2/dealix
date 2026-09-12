#!/usr/bin/env python3
"""Verify OP2 content drafts are draft-only, sourced, and claim-safe.

Prints: DEALIX_OP2_CONTENT_DRAFTS_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DRAFTS_PATH = REPO_ROOT / "data" / "commercial" / "op2_content_drafts_v1.json"
VERDICT_PASS = "DEALIX_OP2_CONTENT_DRAFTS_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_CONTENT_DRAFTS_VERDICT=FAIL"
BANNED = ("نضمن", "مضمون", "guaranteed", "blast", "scrape", "scraping", "cold outreach")


def main() -> int:
    errors: list[str] = []
    if not DRAFTS_PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {DRAFTS_PATH}")
        return 1
    try:
        payload = json.loads(DRAFTS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-content-drafts.v1":
        errors.append("unexpected schema")
    if payload.get("publish_authority") is not False:
        errors.append("publish_authority must be false")
    drafts = payload.get("drafts") or []
    if not drafts:
        errors.append("no drafts produced")

    for draft in drafts:
        did = draft.get("draft_id")
        if draft.get("status") != "draft" or draft.get("published") is not False:
            errors.append(f"{did}: must remain an unpublished draft")
        if draft.get("approval_required") is not True:
            errors.append(f"{did}: approval_required must be true")
        if not draft.get("source_ref") or not draft.get("authority_ref"):
            errors.append(f"{did}: must cite source_ref and authority_ref")
        if draft.get("allowed_use") != ["INTERNAL_DRAFT_ONLY"]:
            errors.append(f"{did}: allowed_use must be INTERNAL_DRAFT_ONLY")
        if draft.get("counts_as_relationship") is not False or draft.get("counts_as_pipeline") is not False:
            errors.append(f"{did}: must not count as relationship/pipeline")
        text = " ".join(atom.get("body", "") for atom in draft.get("atoms", [])).lower()
        for banned in BANNED:
            if banned.lower() in text:
                errors.append(f"{did}: banned claim term '{banned}'")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
