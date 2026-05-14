#!/usr/bin/env python3
"""Bilingual summary of market feedback (last 30 days).

Reads data/_state/market_feedback.jsonl and writes:
  data/_state/market_feedback_summary.json
  data/_state/market_feedback_summary.md

No PII surfaced. No names. No emails.

Usage:
    python scripts/market_feedback_summary.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = REPO_ROOT / "data" / "_state" / "market_feedback.jsonl"
OUT_DIR = REPO_ROOT / "data" / "_state"


def _load_last_30() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    out = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = row.get("received_at")
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            continue
        if dt >= cutoff:
            out.append(row)
    return out


def summarize(rows: list[dict]) -> dict:
    by_type: Counter[str] = Counter()
    by_sector: Counter[str] = Counter()
    samples = []
    for row in rows:
        by_type[row.get("signal_type", "unknown")] += 1
        by_sector[row.get("sector") or "unspecified"] += 1
    for row in rows[-5:]:
        samples.append({
            "signal_type": row.get("signal_type"),
            "received_at": row.get("received_at"),
            "quote": (row.get("message_redacted") or "")[:200],
        })
    return {
        "window_days": 30,
        "total": len(rows),
        "by_signal_type": dict(by_type),
        "by_sector": dict(by_sector),
        "recent_anonymized": samples,
        "doctrine": "No names. No emails. No phone numbers.",
    }


def _md(summary: dict) -> str:
    lines: list[str] = []
    lines.append("# Market Feedback Summary — last 30 days")
    lines.append(f"_total: **{summary['total']}**_")
    lines.append("")
    lines.append("## By Signal Type")
    if not summary["by_signal_type"]:
        lines.append("- (no feedback yet)")
    for k in sorted(summary["by_signal_type"]):
        lines.append(f"- {k}: {summary['by_signal_type'][k]}")
    lines.append("")
    lines.append("## By Sector")
    if not summary["by_sector"]:
        lines.append("- (no feedback yet)")
    for k in sorted(summary["by_sector"]):
        lines.append(f"- {k}: {summary['by_sector'][k]}")
    lines.append("")
    lines.append("## Recent (anonymized)")
    for s in summary["recent_anonymized"]:
        lines.append(f"- **{s['signal_type']}** ({s['received_at'][:10]}): {s['quote']}")
    lines.append("")
    lines.append("---")
    lines.append("_Doctrine: " + summary["doctrine"] + "_")
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = _load_last_30()
    summary = summarize(rows)
    json_path = OUT_DIR / "market_feedback_summary.json"
    md_path = OUT_DIR / "market_feedback_summary.md"
    json_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_md(summary), encoding="utf-8")
    print(f"market feedback summary: {summary['total']} entries in last 30 days")
    print(f"  wrote: {md_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
