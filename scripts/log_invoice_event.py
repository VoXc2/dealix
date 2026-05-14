#!/usr/bin/env python3
"""Log a real invoice event (Invoice #1 or later).

This is the ONLY honest way to bump `invoice_sent_count` in
`data/first_invoice_log.json`. Discipline:

  - Requires --really-i-sent-this flag.
  - Requires --capital-asset-id of an entry that ALREADY exists in
    data/capital_asset_index.json (per FIRST_INVOICE_UNLOCK.md step 1:
    "Register Capital Asset first.").
  - Requires --buyer, --scope, --proof-target.
  - Records git_author + git_commit_sha + entry_id.
  - The counter is kept in lockstep with len(entries).

Usage:
    python scripts/log_invoice_event.py \\
        --really-i-sent-this \\
        --capital-asset-id <hex> \\
        --buyer "Saudi B2B services client X" \\
        --scope "Revenue Intelligence Sprint" \\
        --proof-target "1 Proof Pack + 1 Value Ledger entry"
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = REPO_ROOT / "data" / "first_invoice_log.json"
CAPITAL_INDEX = REPO_ROOT / "data" / "capital_asset_index.json"


def _git_author() -> str:
    try:
        out = subprocess.run(
            ["git", "config", "user.email"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _capital_asset_exists(asset_id: str) -> bool:
    if not CAPITAL_INDEX.exists():
        return False
    try:
        data = json.loads(CAPITAL_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    for e in (data.get("entries") or []):
        if str(e.get("entry_id")) == asset_id:
            return True
    return False


def _load_log() -> dict:
    if not LOG_PATH.exists():
        return {
            "log_id": "FIRST-INVOICE-LOG-001",
            "updated_at": datetime.now(timezone.utc).date().isoformat(),
            "invoice_sent_count": 0,
            "invoice_paid_count": 0,
            "ceo_complete": False,
            "entries": [],
            "next_required_action": "Send invoice after qualified buyer accepts scope.",
            "completion_rule": "Score 5 requires at least one invoice entry with proof target.",
        }
    try:
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"first_invoice_log.json is invalid JSON: {e}")


def _write_log(data: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def log_invoice(
    capital_asset_id: str,
    buyer: str,
    scope: str,
    proof_target: str,
    amount_sar: int | None = None,
    sent_at: str | None = None,
) -> dict:
    if not _capital_asset_exists(capital_asset_id):
        raise SystemExit(
            f"capital asset id {capital_asset_id!r} not found in "
            f"data/capital_asset_index.json. Register it first via "
            f"scripts/register_capital_asset.py (FIRST_INVOICE_UNLOCK step 1)."
        )
    if not buyer.strip() or not scope.strip() or not proof_target.strip():
        raise SystemExit("--buyer, --scope, and --proof-target must be non-empty")

    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "entry_id": uuid.uuid4().hex,
        "capital_asset_id": capital_asset_id,
        "buyer": buyer.strip(),
        "scope": scope.strip(),
        "proof_target": proof_target.strip(),
        "amount_sar_disclosed_internally": amount_sar,  # NEVER in public projection
        "sent_at": (sent_at or now)[:25],
        "status": "sent",
        "runbook": "docs/ops/FIRST_INVOICE_UNLOCK.md",
        "git_author": _git_author(),
        "git_commit_sha": _git_sha(),
    }
    data = _load_log()
    entries = list(data.get("entries") or [])
    entries.append(entry)
    data["entries"] = entries
    data["invoice_sent_count"] = len(entries)
    data["updated_at"] = now[:10]
    data["ceo_complete"] = len(entries) >= 1
    _write_log(data)
    return entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="log a real invoice event")
    parser.add_argument(
        "--really-i-sent-this",
        dest="really",
        action="store_true",
        help="REQUIRED. Confirms this is a real invoice, not a test.",
    )
    parser.add_argument("--capital-asset-id", required=True,
                        help="entry_id of an existing capital asset")
    parser.add_argument("--buyer", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--proof-target", required=True)
    parser.add_argument("--amount-sar", type=int, default=None,
                        help="optional; NEVER returned by the public endpoint")
    parser.add_argument("--sent-at", default=None)
    args = parser.parse_args(argv)

    if not args.really:
        print(
            "REFUSED. Pass --really-i-sent-this to confirm this is a real "
            "invoice, not a test.",
            file=sys.stderr,
        )
        return 2

    entry = log_invoice(
        capital_asset_id=args.capital_asset_id,
        buyer=args.buyer,
        scope=args.scope,
        proof_target=args.proof_target,
        amount_sar=args.amount_sar,
        sent_at=args.sent_at,
    )
    print(f"logged invoice: {entry['entry_id']} (buyer={entry['buyer']})")
    log = _load_log()
    print(f"  invoice_sent_count: {log['invoice_sent_count']}")
    print(f"  ceo_complete: {log['ceo_complete']}")
    print("  re-run: python scripts/verify_all_dealix.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
