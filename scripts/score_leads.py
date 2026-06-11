"""Deterministic lead scoring.

Usage:
    python3 scripts/score_leads.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
OUT_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"


# Segment weights: how likely each segment is to close at our price points
SEGMENT_WEIGHT = {
    "marketing_agency": 25,
    "training": 20,
    "consulting": 18,
    "b2b_services": 18,
    "logistics": 15,
    "real_estate": 12,
    "clinic": 10,
    "retail": 8,
}


def score(account: dict) -> int:
    base = 30
    base += SEGMENT_WEIGHT.get(account.get("segment", ""), 5)
    if account.get("sourceNote"):
        base += 10
    if account.get("visibleSignal"):
        base += 10
    if account.get("weaknessHypothesis"):
        base += 10
    if account.get("demo"):
        base -= 5  # demo is not traction
    return min(100, max(0, base))


def main() -> int:
    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])
    scored = []
    for a in accounts:
        a["score"] = score(a)
        scored.append(a)
    scored.sort(key=lambda a: a["score"], reverse=True)
    OUT_PATH.write_text(
        json.dumps({"accounts": scored, "version": "1.0"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"scored {len(scored)} -> {OUT_PATH}")
    for a in scored[:5]:
        print(f"  {a['score']:3d}  {a['id']}  {a['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
