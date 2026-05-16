#!/usr/bin/env python3
"""Verify OS tier registry structure and golden-chain alignment."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "dealix/transformation/os_tier_registry.yaml"


def main() -> int:
    if not REGISTRY.exists():
        print("missing os_tier_registry.yaml", file=sys.stderr)
        return 1
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    tiers = data.get("tiers") or {}
    for tier_id in ("T1_production", "T2_platform", "T3_doctrine"):
        if tier_id not in tiers:
            print(f"missing tier: {tier_id}", file=sys.stderr)
            return 1
        modules = tiers[tier_id].get("modules") or []
        if not modules:
            print(f"empty modules for {tier_id}", file=sys.stderr)
            return 1
    golden = set(data.get("golden_chain_modules") or [])
    t1_names = {m.split("/")[-1] for m in tiers["T1_production"]["modules"]}
    missing = golden - t1_names
    if missing:
        print(f"golden_chain not covered in T1 module names: {missing}", file=sys.stderr)
        return 1
    print("OS_TIER_REGISTRY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
