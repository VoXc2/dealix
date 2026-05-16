#!/usr/bin/env python3
"""Copy last successful checklist timestamp from weekly_ops_checklist.log into kpi_baselines.yaml.

Updates only ``weekly_ops.last_checklist_run_iso`` (UTC date YYYY-MM-DD from the log line).
Does not touch KPI numeric snapshots.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _last_pass_date(log_text: str) -> str | None:
    pat = re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+verify_global_ai_transformation=PASS\s*$"
    )
    for line in reversed(log_text.splitlines()):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = pat.match(line)
        if m:
            return m.group("ts")[:10]
    return None


def _patch_baselines(text: str, date_iso: str) -> str | None:
    """Replace last_checklist_run_iso under weekly_ops; return new text or None if anchor missing."""
    lines = text.splitlines(keepends=True)
    in_weekly = False
    replaced = False
    out: list[str] = []
    weekly_re = re.compile(r"^weekly_ops:\s*$")
    key_re = re.compile(r"^(\s*)last_checklist_run_iso:\s*.*\n?$")
    for line in lines:
        if weekly_re.match(line.rstrip("\n")):
            in_weekly = True
            out.append(line)
            continue
        if in_weekly:
            m = key_re.match(line.rstrip("\n"))
            if m:
                indent = m.group(1)
                nl = "\n" if line.endswith("\n") else ""
                out.append(f'{indent}last_checklist_run_iso: "{date_iso}"{nl}')
                replaced = True
                continue
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                in_weekly = False
        out.append(line)
    if not replaced:
        return None
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root: Path = args.repo_root
    log_path = root / "docs/transformation/evidence/weekly_ops_checklist.log"
    base_path = root / "dealix/transformation/kpi_baselines.yaml"
    if not log_path.exists():
        print("missing_log", file=sys.stderr)
        return 1
    ts_date = _last_pass_date(log_path.read_text(encoding="utf-8"))
    if not ts_date:
        print("no_pass_line_found", file=sys.stderr)
        return 1
    raw = base_path.read_text(encoding="utf-8")
    new_text = _patch_baselines(raw, ts_date)
    if new_text is None:
        print("kpi_baselines_missing_weekly_ops_anchor", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"would_set_last_checklist_run_iso:{ts_date}")
        return 0
    base_path.write_text(new_text, encoding="utf-8")
    print(f"updated_weekly_ops_last_checklist_run_iso:{ts_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
