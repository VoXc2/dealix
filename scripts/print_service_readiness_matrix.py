#!/usr/bin/env python3
"""Print Markdown table: service folder, service_id, readiness score, tier."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from auto_client_acquisition.delivery_os.service_readiness import (  # noqa: E402
    compute_service_readiness_score,
)


def _tier(score: int) -> str:
    if score >= 90:
        return "Sellable/Excellent"
    if score >= 85:
        return "Sellable/Improve"
    if score >= 70:
        return "Beta"
    return "Not Ready"


def main() -> int:
    path = REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = list(data.get("mappings") or [])
    print("| Service folder | service_id | Score | Tier |")
    print("|----------------|------------|------:|------|")
    for row in rows:
        sid = row.get("service_id") or ""
        folder = row.get("folder") or sid
        if not sid:
            continue
        sc = int(compute_service_readiness_score(sid)["score"])
        print(f"| {folder} | {sid} | {sc} | {_tier(sc)} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
