#!/usr/bin/env python3
"""Print daily/weekly agent work packets from data/agent_work_packets/daily_packets.yaml."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKETS_YAML = ROOT / "data/agent_work_packets/daily_packets.yaml"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cadence", choices=("daily", "weekly", "all"), default="daily")
    args = p.parse_args()

    if not PACKETS_YAML.is_file():
        print(f"MISSING: {PACKETS_YAML}", file=sys.stderr)
        return 1

    data = yaml.safe_load(PACKETS_YAML.read_text(encoding="utf-8")) or {}
    packets = data.get("packets") or {}

    print("== Dealix agent work packets ==")
    print("  guide: docs/ops/AGENT_DAILY_WORK_PACKETS_AR.md")
    print("  playbook: docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md")
    print("")

    for packet_id, spec in packets.items():
        cadence = (spec.get("cadence") or "daily").lower()
        if args.cadence == "daily" and cadence != "daily":
            continue
        if args.cadence == "weekly" and cadence != "weekly":
            continue
        agent = spec.get("agent") or "?"
        print(f"## {packet_id} → {agent} ({cadence})")
        for inp in spec.get("inputs") or []:
            print(f"  IN:  {inp}")
        for out in spec.get("outputs") or []:
            print(f"  OUT: {out}")
        for cmd in spec.get("verify_commands") or []:
            print(f"  VERIFY: {cmd}")
        print("")

    print("AGENT_WORK_PACKETS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
