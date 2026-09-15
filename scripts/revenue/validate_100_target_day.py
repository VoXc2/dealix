#!/usr/bin/env python3
"""
Validate a legacy research batch. Validation never grants contact authority.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, normalize_email

REQUIRED_COLUMNS = ["company", "sector", "city", "source_url", "verification_status", "confidence"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate research-review batch")
    parser.add_argument("--input", default="data/outreach/ready_batch_2026-06-15.csv")
    parser.add_argument("--max-batch", type=int, default=100)
    args = parser.parse_args()

    rows = load_csv(REPO_ROOT / args.input)
    issues: list[str] = []

    if not rows:
        issues.append("Batch file is empty")
    if len(rows) > args.max_batch:
        issues.append(f"Batch size {len(rows)} exceeds max {args.max_batch}")

    seen_emails: set[str] = set()
    for idx, row in enumerate(rows, start=2):
        for col in REQUIRED_COLUMNS:
            if not row.get(col, "").strip():
                issues.append(f"Row {idx}: missing {col}")
        try:
            conf = float(row.get("confidence", "0"))
            if conf < 0.5:
                issues.append(f"Row {idx}: confidence {conf} below 0.5 threshold")
        except ValueError:
            issues.append(f"Row {idx}: invalid confidence")
        vstatus = row.get("verification_status", "").lower()
        if vstatus == "placeholder":
            issues.append(f"Row {idx}: placeholder verification_status not allowed in reviewed research")
        email = normalize_email(row.get("email", ""))
        if email:
            if email in seen_emails:
                issues.append(f"Row {idx}: duplicate email {email}")
            seen_emails.add(email)

    if issues:
        print("❌ 100-target day validation failed:")
        for issue in issues:
            print(f"  {issue}")
        print("DEALIX_100_TARGET_VALID=0")
        return 1

    print(f"✅ {len(rows)} targets validated for research review.")
    print("OUTBOUND_AUTHORITY=false")
    print("DEALIX_100_TARGET_VALID=1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
