#!/usr/bin/env python3
"""Append a governed win/loss row to dealix/registers/win_loss.yaml (category GTM)."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "dealix/registers/win_loss.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outcome", choices=("win", "loss"), required=True)
    parser.add_argument("--account", required=True)
    parser.add_argument("--evidence-ref", required=True, help="Proof path or CRM ref — required")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    if not REGISTRY.exists():
        print("missing win_loss.yaml", file=sys.stderr)
        return 1
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    entries = list(data.get("entries") or [])
    entries.append(
        {
            "recorded_at": datetime.now(UTC).isoformat(),
            "outcome": args.outcome,
            "account": args.account,
            "evidence_ref": args.evidence_ref,
            "notes": args.notes,
        }
    )
    data["entries"] = entries
    REGISTRY.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"recorded {args.outcome} for {args.account}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
