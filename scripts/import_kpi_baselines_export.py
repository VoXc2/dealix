#!/usr/bin/env python3
"""Import founder CRM/finance KPI snapshots into kpi_baselines.yaml.

Usage:
  python3 scripts/import_kpi_baselines_export.py --file exports/kpi_week.json

JSON shape:
  {
    "updated_period_iso": "2026-05-16",
    "snapshots": {
      "measured_customer_value_sar": {"value_numeric": 12000, "source_ref": "crm:hubspot:deal-42"}
    }
  }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_BASELINES = _REPO / "dealix/transformation/kpi_baselines.yaml"
_REQUIRED_META = _REPO / "dealix/transformation/kpi_founder_required.yaml"


def _allowed_keys() -> set[str]:
    import yaml

    data = yaml.safe_load(_REQUIRED_META.read_text(encoding="utf-8")) or {}
    return set(data.get("founder_required_keys") or [])


def _patch_snapshot_line(text: str, key: str, value: float, source_ref: str) -> str:
    lines = text.splitlines(keepends=True)
    in_key = False
    out: list[str] = []
    val_re = re.compile(r"^(\s*)value_numeric:\s*.*\n?$")
    ref_re = re.compile(r"^(\s*)source_ref:\s*.*\n?$")
    for line in lines:
        if re.match(rf"^\s*{re.escape(key)}:\s*$", line.rstrip("\n")):
            in_key = True
            out.append(line)
            continue
        if in_key:
            m_val = val_re.match(line.rstrip("\n"))
            if m_val:
                indent = m_val.group(1)
                nl = "\n" if line.endswith("\n") else ""
                out.append(f"{indent}value_numeric: {value}{nl}")
                continue
            m_ref = ref_re.match(line.rstrip("\n"))
            if m_ref:
                indent = m_ref.group(1)
                nl = "\n" if line.endswith("\n") else ""
                safe_ref = source_ref.replace('"', "'")
                out.append(f'{indent}source_ref: "{safe_ref}"{nl}')
                in_key = False
                continue
            if line.strip() and not line.startswith(" "):
                in_key = False
        out.append(line)
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.file.exists():
        print(f"missing export file: {args.file}", file=sys.stderr)
        return 1
    if not _BASELINES.exists():
        print("missing kpi_baselines.yaml", file=sys.stderr)
        return 1

    payload = json.loads(args.file.read_text(encoding="utf-8"))
    snapshots = payload.get("snapshots") or {}
    allowed = _allowed_keys()
    unknown = set(snapshots) - allowed
    if unknown:
        print(f"warning: keys not in founder_required list (skipped): {sorted(unknown)}", file=sys.stderr)

    text = _BASELINES.read_text(encoding="utf-8")
    period = str(payload.get("updated_period_iso") or "").strip()
    if period:
        text = re.sub(
            r'^(updated_period_iso:\s*).*$',
            rf'\1"{period}"',
            text,
            count=1,
            flags=re.MULTILINE,
        )

    updated = 0
    for key, row in snapshots.items():
        if key not in allowed:
            continue
        val = row.get("value_numeric")
        ref = str(row.get("source_ref") or "").strip()
        if val is None or not ref:
            print(f"skip {key}: need value_numeric and source_ref", file=sys.stderr)
            continue
        text = _patch_snapshot_line(text, key, float(val), ref)
        updated += 1

    print(f"updated {updated} founder KPI snapshot(s)")
    if args.dry_run:
        print(text[:2000])
        return 0
    _BASELINES.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
