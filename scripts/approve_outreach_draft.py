"""Approve an outreach draft. NO send — only status change.

Usage:
    python3 scripts/approve_outreach_draft.py --draft-id draft-demo-acc-001-ar --reviewer Sami
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    if not QUEUE_PATH.exists():
        print(f"missing: {QUEUE_PATH}")
        return 1
    data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    drafts = data.get("drafts", [])
    found = None
    for d in drafts:
        if d["draftId"] == args.draft_id:
            d["reviewStatus"] = "approved"
            d["reviewer"] = args.reviewer
            d["reviewedAt"] = dt.date.today().isoformat()
            found = d
            break
    if not found:
        print(f"draft not found: {args.draft_id}")
        return 1
    QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"approved {args.draft_id} by {args.reviewer} (NO SEND — manual send only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
