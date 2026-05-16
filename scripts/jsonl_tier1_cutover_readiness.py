#!/usr/bin/env python3
"""Report JSONL tier-1 cutover readiness per engineering_cutover_policy.yaml."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "dealix/transformation/jsonl_migration_catalog.yaml"
POLICY = REPO / "dealix/transformation/engineering_cutover_policy.yaml"


def main() -> int:
    if not CATALOG.exists() or not POLICY.exists():
        print("missing catalog or policy", file=sys.stderr)
        return 1
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    signals = policy.get("minimum_signals_any_one") or []
    entries = catalog.get("entries") or catalog.get("paths") or []
    tier1 = [e for e in entries if str(e.get("tier", "")).lower() in ("1", "tier1", "tier_1")]
    print(f"tier1_entries: {len(tier1)}")
    print(f"external_signals_required: {len(signals)}")
    for row in tier1[:10]:
        path = row.get("path") or row.get("jsonl_path") or "?"
        pg = row.get("postgres_target") or row.get("target_table") or "?"
        print(f"  - {path} -> {pg}")
    print("JSONL_TIER1_CUTOVER: READY_FOR_SIGNAL (no cutover without founder external signal)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
