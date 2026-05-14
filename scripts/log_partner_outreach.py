#!/usr/bin/env python3
"""Log a real anchor-partner outreach event.

This is the ONLY honest way to bump `outreach_sent_count` in
`data/partner_outreach_log.json`. By design it has deliberate friction:

  - Requires --really-i-sent-this flag (no --force shortcut).
  - Requires --partner, --archetype, --channel.
  - Records git_author + git_commit_sha + entry_id on every entry.
  - The counter is kept in lockstep with len(entries) (anti-cheat).

After running, re-run the master verifier:

    python scripts/verify_all_dealix.py

Partner Motion should move from 4 → 5.

Usage:
    python scripts/log_partner_outreach.py \\
        --really-i-sent-this \\
        --partner "Big-4 Saudi assurance partner" \\
        --archetype "Big 4 / Assurance Partner" \\
        --channel email

NOTE: this script logs the FACT of an outreach. It never sends the
message. Sending is a human action. The script merely records that a
human did it.
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
LOG_PATH = REPO_ROOT / "data" / "partner_outreach_log.json"

VALID_ARCHETYPES = (
    "Big 4 / Assurance Partner",
    "SAMA / Regulated Technology Processor",
    "Saudi or GCC VC Platform Team",
)

VALID_CHANNELS = ("email", "linkedin_human", "in_person", "phone")


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


def _load_log() -> dict:
    if not LOG_PATH.exists():
        return {
            "log_id": "PARTNER-OUTREACH-LOG-001",
            "updated_at": datetime.now(timezone.utc).date().isoformat(),
            "outreach_sent_count": 0,
            "ceo_complete": False,
            "entries": [],
            "next_required_action": "Send one anchor partner outreach and append entry.",
            "completion_rule": "Score 5 requires at least one founder-confirmed outreach entry.",
        }
    try:
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"partner_outreach_log.json is invalid JSON: {e}")


def _write_log(data: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def log_outreach(
    partner: str,
    archetype: str,
    channel: str,
    sent_at: str | None = None,
    next_follow_up_at: str | None = None,
) -> dict:
    if archetype not in VALID_ARCHETYPES:
        raise SystemExit(
            f"unknown archetype {archetype!r}. Valid: {VALID_ARCHETYPES}"
        )
    if channel not in VALID_CHANNELS:
        raise SystemExit(
            f"unknown channel {channel!r}. Valid: {VALID_CHANNELS}"
        )
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "entry_id": uuid.uuid4().hex,
        "partner_name": partner.strip(),
        "archetype": archetype,
        "channel": channel,
        "sent_at": (sent_at or now)[:25],
        "next_follow_up_at": (next_follow_up_at or "")[:25],
        "status": "sent",
        "message_file": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md",
        "git_author": _git_author(),
        "git_commit_sha": _git_sha(),
    }
    data = _load_log()
    entries = list(data.get("entries") or [])
    entries.append(entry)
    data["entries"] = entries
    data["outreach_sent_count"] = len(entries)
    data["updated_at"] = now[:10]
    data["ceo_complete"] = len(entries) >= 1
    if data["ceo_complete"]:
        data["next_required_action"] = (
            "Follow up per the cadence (D+3 / D+7 / D+14); record outcomes."
        )
    _write_log(data)
    return entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="log a real anchor-partner outreach event"
    )
    parser.add_argument(
        "--really-i-sent-this",
        dest="really",
        action="store_true",
        help="REQUIRED. Confirms this is a real event, not a test.",
    )
    parser.add_argument("--partner", required=True, help="partner contact / company name")
    parser.add_argument(
        "--archetype", required=True,
        help=f"one of: {', '.join(VALID_ARCHETYPES)}",
    )
    parser.add_argument(
        "--channel", required=True,
        help=f"one of: {', '.join(VALID_CHANNELS)}",
    )
    parser.add_argument("--sent-at", default=None, help="ISO timestamp (default: now)")
    parser.add_argument("--next-follow-up-at", default=None, help="ISO timestamp")
    args = parser.parse_args(argv)

    if not args.really:
        print(
            "REFUSED. Pass --really-i-sent-this to confirm this is a real "
            "outreach, not a test. The verifier refuses to award the "
            "market-motion score without honest confirmation.",
            file=sys.stderr,
        )
        return 2

    entry = log_outreach(
        partner=args.partner,
        archetype=args.archetype,
        channel=args.channel,
        sent_at=args.sent_at,
        next_follow_up_at=args.next_follow_up_at,
    )
    print(f"logged outreach: {entry['entry_id']} ({entry['partner_name']})")
    log = _load_log()
    print(f"  outreach_sent_count: {log['outreach_sent_count']}")
    print(f"  ceo_complete: {log['ceo_complete']}")
    print("  re-run: python scripts/verify_all_dealix.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
