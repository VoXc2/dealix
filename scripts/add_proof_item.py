"""Add a proof item to the vault.

Usage:
    python3 scripts/add_proof_item.py --account-id demo-001 --type "workflow_improvement" --note "Reduced manual follow-up steps"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "business" / "_data" / "proof_vault.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--note", required=True)
    args = parser.parse_args()

    data = {"items": [], "version": "1.0"}
    if PROOF_PATH.exists():
        try:
            data = json.loads(PROOF_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    data.setdefault("items", []).append(
        {
            "id": f"proof-{args.account_id}-{dt.date.today().isoformat()}",
            "accountId": args.account_id,
            "type": args.type,
            "note": args.note,
            "addedAt": dt.date.today().isoformat(),
        }
    )
    PROOF_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROOF_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added proof item for {args.account_id} -> {PROOF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
