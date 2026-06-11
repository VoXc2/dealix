"""Mark a deal as lost with reason.

Usage:
    python3 scripts/mark_deal_lost.py --account-id demo-002 --reason "No budget"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "business" / "_data" / "deals.ledger.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()

    data = {"deals": [], "version": "1.0"}
    if LEDGER_PATH.exists():
        try:
            data = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    data.setdefault("deals", []).append(
        {
            "id": f"deal-{args.account_id}-{dt.date.today().isoformat()}",
            "accountId": args.account_id,
            "status": "lost",
            "value": 0,
            "monthlyRecurring": 0,
            "closedAt": dt.date.today().isoformat(),
            "reason": args.reason,
            "demo": True,
        }
    )
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"marked lost: {args.account_id} (reason: {args.reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
