#!/usr/bin/env python3
"""Generate planning artifacts from CEO Top-50 tracker and latest run log."""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class TaskRow:
    task_id: int
    category: str
    action: str
    status: str
    impact: int
    evidence_path: str


def _load_tracker(path: Path) -> list[TaskRow]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[TaskRow] = []
        for r in reader:
            rows.append(
                TaskRow(
                    task_id=int(r["id"]),
                    category=r["category"],
                    action=r["action"],
                    status=r["status"],
                    impact=int(r["impact"]),
                    evidence_path=r["evidence_path"],
                )
            )
    return rows


def _latest_run_json(live_dir: Path) -> dict:
    candidates = sorted(live_dir.glob("ceo_top50_run_*.json"))
    if not candidates:
        return {"results": []}
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def _write_alignment(rows: list[TaskRow], out: Path) -> None:
    total = len(rows)
    done = sum(1 for r in rows if r.status == "DONE_NOW")
    next7 = [r for r in rows if r.status == "NEXT_7"]
    next30 = [r for r in rows if r.status == "NEXT_30"]
    done_pct = round((done / total) * 100, 1) if total else 0.0

    lines = [
        "# CEO 30/60/90 Alignment Snapshot",
        "",
        f"- Generated at (UTC): {datetime.now(UTC).isoformat()}",
        f"- Total tasks: {total}",
        f"- DONE_NOW: {done} ({done_pct}%)",
        f"- NEXT_7: {len(next7)}",
        f"- NEXT_30: {len(next30)}",
        "",
        "## NEXT_7 Priorities",
    ]
    for r in sorted(next7, key=lambda x: (-x.impact, x.task_id)):
        lines.append(f"- #{r.task_id} `{r.action}` (impact={r.impact})")

    lines.extend(["", "## NEXT_30 Priorities"])
    for r in sorted(next30, key=lambda x: (-x.impact, x.task_id)):
        lines.append(f"- #{r.task_id} `{r.action}` (impact={r.impact})")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_backlog(rows: list[TaskRow], latest_run: dict, out: Path) -> None:
    failed_actions = {
        str(r.get("action", "")): int(r.get("exit_code", 1))
        for r in latest_run.get("results", [])
        if r.get("status") == "FAIL"
    }
    next7 = [r for r in rows if r.status == "NEXT_7"]
    next30 = [r for r in rows if r.status == "NEXT_30"]
    p0 = [r for r in next7 if r.action in failed_actions]
    p1 = [r for r in next7 if r.action not in failed_actions]

    lines = [
        "# CEO Weekly P0/P1 Backlog",
        "",
        f"- Generated at (UTC): {datetime.now(UTC).isoformat()}",
        "",
        "## P0 — Failing or blocked this week",
    ]
    if not p0:
        lines.append("- None")
    else:
        for r in sorted(p0, key=lambda x: (-x.impact, x.task_id)):
            lines.append(
                f"- #{r.task_id} `{r.action}` (impact={r.impact}, exit={failed_actions.get(r.action, 'n/a')})"
            )

    lines.extend(["", "## P1 — High-impact queued (NEXT_7)"])
    if not p1:
        lines.append("- None")
    else:
        for r in sorted(p1, key=lambda x: (-x.impact, x.task_id)):
            lines.append(f"- #{r.task_id} `{r.action}` (impact={r.impact})")

    lines.extend(["", "## P2 — NEXT_30 candidates"])
    for r in sorted(next30, key=lambda x: (-x.impact, x.task_id)):
        lines.append(f"- #{r.task_id} `{r.action}` (impact={r.impact})")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build CEO planning sync artifacts")
    parser.add_argument("--mode", choices=["align", "backlog", "all"], default="all")
    parser.add_argument("--tracker", default="docs/ops/CEO_TOP50_TRACKER.csv")
    parser.add_argument("--live-dir", default="docs/ops/live")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    tracker = (root / args.tracker).resolve()
    live_dir = (root / args.live_dir).resolve()
    rows = _load_tracker(tracker)
    latest_run = _latest_run_json(live_dir)

    if args.mode in {"align", "all"}:
        _write_alignment(rows, live_dir / "CEO_30_60_90_ALIGNMENT.md")
    if args.mode in {"backlog", "all"}:
        _write_backlog(rows, latest_run, live_dir / "CEO_WEEKLY_P0_P1_BACKLOG.md")

    print("OK: planning artifacts generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
