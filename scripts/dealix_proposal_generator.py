#!/usr/bin/env python3
"""Compatibility entrypoint for Dealix proposal preparation.

The historical implementation in this path selected fixed-price tiers (including
499 SAR / 7-day Sprint and fixed Revenue/Command/Delivery prices). That is not
current Dealix commercial authority.

This compatibility command now does one safe thing only: delegate to the
canonical **Free Mini Diagnostic** draft renderer. It cannot create a paid Pilot
price, payment URL, invoice, contract term, ROI claim, or send an external
message.

Current path:
    Free Mini Diagnostic
    -> Qualified Discovery
    -> Customer-Specific Quote
    -> Revenue Command Pilot — 30 days
    -> Proof Pack
    -> Stop / Expand / Redesign
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_RENDERER = ROOT / "scripts/render_diagnostic_proposal.py"

RETIRED_TIERS = {
    "sprint",
    "revenue_os",
    "command_center",
    "delivery_os",
    "review_os",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a canonical Free Mini Diagnostic draft. Historical fixed-price "
            "tiers are retired and cannot be generated from this command."
        )
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--contact", default="", help="Contact name")
    parser.add_argument("--sector", default="", help="Context only; does not select a price/tier")
    parser.add_argument("--tier", default=None, help="Historical option accepted only to fail closed")
    parser.add_argument("--kpi", default=None, help="Historical context; not used for promises")
    parser.add_argument("--response-time", default=None, help="Historical context; not used for claims")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-sectors", action="store_true")
    args = parser.parse_args()

    if args.list_sectors:
        print("LEGACY_SECTOR_TIER_RECOMMENDATION=RETIRED")
        print("CURRENT_PATH=FREE_MINI_DIAGNOSTIC_THEN_QUALIFIED_DISCOVERY")
        print("PUBLIC_FIXED_PILOT_PRICE_ALLOWED=false")
        return 0

    if not args.company:
        parser.error("--company is required (or use --list-sectors)")

    if args.tier:
        tier = args.tier.strip().lower()
        if tier in RETIRED_TIERS:
            print(
                f"NOTICE=RETIRED_TIER_IGNORED:{tier}; "
                "rendering Free Mini Diagnostic only",
                file=sys.stderr,
            )
        else:
            print(
                f"NOTICE=UNRECOGNIZED_TIER_NOT_AUTHORITY:{tier}; "
                "rendering Free Mini Diagnostic only",
                file=sys.stderr,
            )

    if not CANONICAL_RENDERER.is_file():
        print(f"ERROR=MISSING_CANONICAL_RENDERER:{CANONICAL_RENDERER}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(CANONICAL_RENDERER),
        "--company",
        args.company,
        "--contact",
        args.contact,
    ]
    if args.dry_run:
        command.append("--dry-run")

    completed = subprocess.run(command, cwd=ROOT, check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
