#!/usr/bin/env python3
"""Print founder strongest plan tasks grouped by section (human review)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dealix.commercial_ops.founder_strongest_plan import (  # noqa: E402
    load_strongest_plan_checklist,
    tasks_by_section,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def _refs(task: dict) -> list[str]:
    out: list[str] = []
    for key in ("docs", "commands", "configs", "artifacts", "ui", "api"):
        raw = task.get(key)
        if isinstance(raw, list):
            out.extend(str(x) for x in raw)
        elif raw:
            out.append(str(raw))
    return out


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description="Print strongest plan checklist by section.")
    parser.add_argument("--section", help="Filter to one section id (e.g. daily, governance)")
    args = parser.parse_args()

    checklist = load_strongest_plan_checklist()
    sections = {
        str(s.get("id")): str(s.get("label_ar") or s.get("id"))
        for s in checklist.get("sections") or []
        if isinstance(s, dict) and s.get("id")
    }
    grouped = tasks_by_section()
    section_ids = sorted(grouped.keys())
    if args.section:
        section_ids = [s for s in section_ids if s == args.section]
        if not section_ids:
            print(f"unknown section: {args.section}", file=sys.stderr)
            return 1

    print(checklist.get("title_ar") or "Founder strongest plan")
    print(f"tasks={len(checklist.get('tasks') or [])} min_task_count={checklist.get('min_task_count')}")
    print()

    for sid in section_ids:
        label = sections.get(sid, sid)
        print(f"## {sid} — {label}")
        for task in sorted(grouped.get(sid, []), key=lambda t: int(t.get("n") or 0)):
            tid = task.get("id", "?")
            n = task.get("n", "?")
            title = task.get("title_ar", "")
            print(f"  [{tid}] #{n} {title}")
            for ref in _refs(task):
                print(f"      - {ref}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
