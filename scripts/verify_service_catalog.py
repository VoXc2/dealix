#!/usr/bin/env python3
"""Verify SERVICE_ID_MAP service_id keys exist in service_readiness_defaults.yaml."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    map_path = REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml"
    yml_path = REPO / "auto_client_acquisition" / "governance_os" / "policies" / "service_readiness_defaults.yaml"
    mp = yaml.safe_load(map_path.read_text(encoding="utf-8")) or {}
    yb = yaml.safe_load(yml_path.read_text(encoding="utf-8")) or {}
    known = set((yb.get("services") or {}).keys())
    missing: list[str] = []
    for row in mp.get("mappings") or []:
        sid = row.get("service_id")
        if sid and sid not in known:
            missing.append(f"missing_readiness_defaults:{sid}")
    for m in missing:
        print(m, file=sys.stderr)
    ok = not missing
    print(f"SERVICE_CATALOG_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
