#!/usr/bin/env python3
"""Print a scorecard from dealix/transformation/reliability_drills.yaml."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    path = args.repo_root / "dealix/transformation/reliability_drills.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    drills = data.get("drills") or []
    slo = data.get("slo_review") or {}

    print("Reliability drills scorecard")
    print("=" * 72)
    print(f"{'name':<28} {'frequency':<14} {'owner_os':<14} {'weight':>8}")
    print("-" * 72)
    total_w = 0.0
    for d in drills:
        w = float(d.get("scoring_weight") or 0.0)
        total_w += w
        print(
            f"{str(d.get('name','')):<28} {str(d.get('frequency','')):<14} "
            f"{str(d.get('owner_os','')):<14} {w:>8.1f}"
        )
    print("-" * 72)
    print(f"{'TOTAL weight':<56} {total_w:>8.1f}")
    print()
    print("SLO review:", slo.get("cadence", ""), "| owner:", slo.get("owner_os", ""))
    topics = slo.get("minimum_topics") or []
    for t in topics:
        print(f"  - {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
