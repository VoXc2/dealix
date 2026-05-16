#!/usr/bin/env python3
"""Render first five personalized warm messages for founder execution."""
from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path


def _rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [r for r in reader if (r.get("name") or "").strip()]


def _msg_ar(r: dict[str, str]) -> str:
    return (
        f"السلام عليكم {r['name']}،\n"
        f"أحتاج ترشيح 1-2 شركة مناسبة في {r['city']} بقطاع {r['sector']}.\n"
        f"جهزنا Sprint واضح لمدة 7 أيام مع حوكمة كاملة (بدون cold outreach أو scraping).\n"
        f"لو عندك جهة مناسبة في {r['company']} أو شبكتك، أرسلني عليها اليوم."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build first 5 personalized messages")
    parser.add_argument("--csv", default="data/warm_list.csv")
    parser.add_argument("--out", default="data/outreach/first5_personalized_messages.md")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    csv_path = (root / args.csv).resolve()
    out_path = (root / args.out).resolve()
    rows = _rows(csv_path)[:5]
    if len(rows) < 5:
        raise SystemExit("Need at least 5 contacts in warm list")

    lines = [
        "# First 5 Personalized Messages",
        "",
        f"_Generated at {datetime.now(UTC).isoformat()}_",
        "",
    ]
    for i, r in enumerate(rows, start=1):
        lines.extend(
            [
                f"## {i}. {r['name']} — {r['role']} @ {r['company']}",
                f"- Sector: `{r['sector']}` · City: `{r['city']}` · Relationship: `{r['relationship']}`",
                "",
                "```",
                _msg_ar(r),
                "```",
                "",
            ]
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
