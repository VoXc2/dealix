"""Mark a proposal as sent (status change, no actual send).

Usage:
    python3 scripts/mark_proposal_sent.py --account-id demo-001 --proposal-id latest
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "business" / "_data" / "proposals.index.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--proposal-id", default="latest")
    args = parser.parse_args()

    if not INDEX_PATH.exists():
        print(f"missing: {INDEX_PATH}")
        return 1
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    proposals = data.get("proposals", [])
    candidates = [p for p in proposals if p.get("accountId") == args.account_id]
    if not candidates:
        print(f"no proposal for {args.account_id}")
        return 1
    if args.proposal_id == "latest":
        target = candidates[-1]
    else:
        target = next((p for p in candidates if p.get("id") == args.proposal_id), None)
    if not target:
        print(f"proposal not found: {args.proposal_id}")
        return 1
    target["status"] = "sent"
    target["sentAt"] = dt.date.today().isoformat()
    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"marked sent: {target.get('id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
