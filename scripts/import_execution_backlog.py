#!/usr/bin/env python3
"""Convert a CSV backlog export into docs/ops/EXECUTION_BACKLOG.md.

Expected CSV columns are flexible but simple:
- title or task
- priority
- status
- owner
- area
- notes
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "ops" / "EXECUTION_BACKLOG.md"


def pick(row: dict[str, str], *names: str, default: str = "") -> str:
    lowered = {key.strip().lower(): value for key, value in row.items()}
    for name in names:
        value = lowered.get(name)
        if value:
            return value.strip()
    return default


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    csv_path = args.csv if args.csv.is_absolute() else ROOT / args.csv
    output_path = args.output if args.output.is_absolute() else ROOT / args.output

    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            title = pick(row, "title", "task", "item", "المهمة", "العنوان")
            if title:
                rows.append(
                    {
                        "title": title,
                        "priority": pick(row, "priority", "prio", "الأولوية", default="P2"),
                        "status": pick(row, "status", "state", "الحالة", default="Not started"),
                        "owner": pick(row, "owner", "assignee", "المسؤول", default="Unassigned"),
                        "area": pick(row, "area", "category", "المجال", default="General"),
                        "notes": pick(row, "notes", "description", "الوصف"),
                    }
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Dealix Execution Backlog",
        "",
        "Generated from a CSV spreadsheet export.",
        "",
        "| Priority | Status | Owner | Area | Task | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for row in sorted(rows, key=lambda row: (row["priority"], row["area"], row["title"])):
        safe = {key: value.replace("|", "\\|") for key, value in row.items()}
        lines.append(
            f"| {safe['priority']} | {safe['status']} | {safe['owner']} | {safe['area']} | {safe['title']} | {safe['notes']} |"
        )
    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Imported {len(rows)} items into {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
