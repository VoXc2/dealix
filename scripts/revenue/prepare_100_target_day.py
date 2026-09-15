#!/usr/bin/env python3
"""
Prepare a bounded research-review batch for a single day. Never grants contact authority.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, today_str, write_csv

REQUIRED_COLUMNS = ["company", "sector", "city", "source_url", "pain_hypothesis", "offer_angle", "confidence", "verification_status"]


def validate_row(row: dict[str, str], idx: int) -> list[str]:
    issues: list[str] = []
    for col in REQUIRED_COLUMNS:
        if not row.get(col, "").strip():
            issues.append(f"Row {idx}: missing {col}")
    try:
        conf = float(row.get("confidence", "0"))
        if not 0 <= conf <= 1:
            issues.append(f"Row {idx}: confidence out of range")
    except ValueError:
        issues.append(f"Row {idx}: confidence not numeric")
    if not row.get("source_url", "").startswith("http"):
        issues.append(f"Row {idx}: source_url must be http/https")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare research-review target batch")
    parser.add_argument("--input", default="data/outreach/research_queue.csv")
    parser.add_argument("--output", default=None)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--min-confidence", type=float, default=0.5)
    args = parser.parse_args()

    if args.batch_size > 100:
        print("❌ Batch size cannot exceed 100")
        return 1

    rows = load_csv(REPO_ROOT / args.input)
    if not rows:
        print(f"No rows in {args.input}")
        return 1

    ready: list[dict[str, str]] = []
    issues: list[str] = []
    for idx, row in enumerate(rows, start=2):
        row_issues = validate_row(row, idx)
        if row_issues:
            issues.extend(row_issues)
            continue
        try:
            conf = float(row.get("confidence", "0"))
        except ValueError:
            conf = 0.0
        if conf < args.min_confidence:
            continue
        if row.get("status", "").lower() in {"contacted", "opted_out", "lost"}:
            continue
        candidate = dict(row)
        candidate["status"] = "research_only"
        candidate["outbound_authority"] = "false"
        ready.append(candidate)
        if len(ready) >= args.batch_size:
            break

    if issues:
        print("⚠️ Validation issues (excluded from batch):")
        for issue in issues[:20]:
            print(f"  {issue}")

    if not ready:
        print("❌ No verified-public research targets found")
        return 1

    out_path = REPO_ROOT / args.output if args.output else REPO_ROOT / "data" / "outreach" / f"research_batch_{today_str()}.csv"
    write_csv(out_path, ready, list(ready[0].keys()))
    print(f"✅ Prepared {len(ready)} research-review targets → {out_path}")
    print("OUTBOUND_AUTHORITY=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
