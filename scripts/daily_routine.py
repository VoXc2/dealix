#!/usr/bin/env python3
"""Dealix Daily Routine.

The one command the founder runs every morning. It composes:

  1. The master verifier (verify_all_dealix.py --json) — system scores.
  2. A delta diff against yesterday's run (read from
     data/_state/verifier_history.jsonl).
  3. The founder daily brief (dealix_founder_daily_brief.py --format json)
     — bottleneck radar + hard gates + service catalog snapshot.
  4. A single "Today's CEO bottleneck" sentence surfaced at the top.

Outputs (committed by the daily cron workflow, not by the founder):
  data/_state/verifier_history.jsonl     # one append-only row per run
  data/_state/daily_routine_<YYYY-MM-DD>.json
  data/_state/daily_brief_<YYYY-MM-DD>.md

Hard rules:
- Never auto-sends external messages.
- Never inflates marker counts.
- Never edits market-motion JSON files.
- Reads the existing brief script; does not duplicate its logic.

Usage:
    python scripts/daily_routine.py
    python scripts/daily_routine.py --date 2026-05-14   # backfill
    python scripts/daily_routine.py --no-history        # skip JSONL append
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date as _date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFIER = REPO_ROOT / "scripts" / "verify_all_dealix.py"
FOUNDER_BRIEF = REPO_ROOT / "scripts" / "dealix_founder_daily_brief.py"
STATE_DIR = REPO_ROOT / "data" / "_state"
HISTORY_PATH = STATE_DIR / "verifier_history.jsonl"


def _run_json(cmd: list[str]) -> dict[str, Any]:
    """Run a python script and parse its stdout as JSON."""
    out = subprocess.run(
        [sys.executable, *cmd],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return {
            "_error": "non-json stdout",
            "_stdout": out.stdout,
            "_stderr": out.stderr,
            "_returncode": out.returncode,
        }


def _load_history() -> list[dict[str, Any]]:
    """Load the JSONL history. Returns at most the last 60 rows."""
    if not HISTORY_PATH.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in HISTORY_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-60:]


def _previous_row(history: list[dict[str, Any]], today_iso: str) -> dict[str, Any] | None:
    """Return the most recent history row from a different date."""
    for row in reversed(history):
        if row.get("date") and row["date"] != today_iso:
            return row
    return None


def _system_score_map(verifier_payload: dict[str, Any]) -> dict[str, int]:
    return {s["name"]: int(s.get("score", 0)) for s in verifier_payload.get("systems", [])}


def _compute_deltas(today_v: dict[str, Any], prev_row: dict[str, Any] | None) -> dict[str, Any]:
    if prev_row is None:
        return {
            "vs_date": None,
            "system_score_changes": [],
            "overall_pass_changed": False,
            "ceo_complete_changed": False,
        }
    today_scores = _system_score_map(today_v)
    prev_scores = prev_row.get("system_scores") or {}
    changes: list[dict[str, Any]] = []
    for name, score in today_scores.items():
        prev = prev_scores.get(name)
        if prev is None or prev == score:
            continue
        changes.append({"system": name, "from": int(prev), "to": int(score)})
    return {
        "vs_date": prev_row.get("date"),
        "system_score_changes": changes,
        "overall_pass_changed": bool(today_v.get("overall_pass")) != bool(prev_row.get("overall_pass")),
        "ceo_complete_changed": bool(today_v.get("ceo_complete")) != bool(prev_row.get("ceo_complete")),
    }


def _bottleneck_sentence(verifier_payload: dict[str, Any]) -> str:
    """Single sentence the founder reads first."""
    if verifier_payload.get("overall_pass"):
        return "All 19 systems PASS. Keep the market motion going."
    failing = [s for s in verifier_payload.get("systems", []) if not s.get("passed")]
    failing.sort(key=lambda s: (not s.get("in_top_eight"), s.get("score", 0)))
    if not failing:
        return "Master verifier is silent — re-run to confirm."
    f = failing[0]
    why = f["missing"][0] if f.get("missing") else "score below threshold"
    where = "top-8" if f.get("in_top_eight") else "support"
    return f"{f['name']} ({where}): {why}."


def _market_motion_status() -> dict[str, Any]:
    """Read the two market-motion markers honestly (no mutation)."""
    out: dict[str, Any] = {}
    for label, rel, key in (
        ("partner_outreach", "data/partner_outreach_log.json", "outreach_sent_count"),
        ("first_invoice",    "data/first_invoice_log.json",    "invoice_sent_count"),
    ):
        p = REPO_ROOT / rel
        if not p.exists():
            out[label] = {"file_present": False, "count": None}
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out[label] = {
                "file_present": True,
                "count": int(data.get(key, 0)),
                "entries_len": len(data.get("entries") or []),
            }
        except Exception as e:
            out[label] = {"file_present": True, "error": str(e)}
    return out


def _markdown_brief(payload: dict[str, Any]) -> str:
    v = payload["verifier"]
    deltas = payload["deltas"]
    market = payload["market_motion"]
    today = payload["date"]
    lines: list[str] = []
    lines.append(f"# Dealix Daily Brief — {today}")
    lines.append("")
    lines.append(f"**Today's CEO bottleneck:** {payload['bottleneck']}")
    lines.append("")
    lines.append("## Master Verifier")
    overall = "PASS" if v.get("overall_pass") else "FAIL"
    ceo = "YES" if v.get("ceo_complete") else "NO"
    lines.append(f"- Overall: **{overall}**")
    lines.append(f"- CEO-complete (top 8 ≥ 4/5): **{ceo}**")
    systems = v.get("systems", [])
    passed = sum(1 for s in systems if s.get("passed"))
    lines.append(f"- Systems passed: **{passed} / {len(systems)}**")
    lines.append("")
    lines.append("## Day-over-Day Deltas")
    if not deltas.get("vs_date"):
        lines.append("- First run — no previous day to diff against.")
    else:
        lines.append(f"- vs {deltas['vs_date']}:")
        if deltas["overall_pass_changed"]:
            lines.append("  - **Overall PASS/FAIL changed.**")
        if deltas["ceo_complete_changed"]:
            lines.append("  - **CEO-complete status changed.**")
        if not deltas["system_score_changes"]:
            lines.append("  - No system score changes.")
        for ch in deltas["system_score_changes"]:
            arrow = "↑" if ch["to"] > ch["from"] else "↓"
            lines.append(f"  - {ch['system']}: {ch['from']} {arrow} {ch['to']}")
    lines.append("")
    lines.append("## Market Motion (read-only, honest)")
    po = market.get("partner_outreach", {})
    inv = market.get("first_invoice", {})
    lines.append(f"- Partner outreach sent: **{po.get('count', '—')}**")
    lines.append(f"- First invoices sent:    **{inv.get('count', '—')}**")
    lines.append("")
    lines.append("## Bottlenecks Failing in Verifier")
    failing = [s for s in systems if not s.get("passed")]
    if not failing:
        lines.append("- None.")
    for f in failing:
        tag = " [top-8]" if f.get("in_top_eight") else ""
        for m in f.get("missing", []):
            lines.append(f"- {f['name']}{tag}: {m}")
    lines.append("")
    fb = payload.get("founder_brief") or {}
    if isinstance(fb, dict) and not fb.get("_error"):
        lines.append("## Founder Brief Snapshot")
        for k in ("today_action", "top_bottleneck", "summary", "single_action"):
            if k in fb:
                lines.append(f"- {k}: {fb[k]}")
        lines.append("")
    lines.append("---")
    lines.append("_Produced by `scripts/daily_routine.py`._")
    lines.append("_The verifier is the judge; this brief is only the lens._")
    return "\n".join(lines) + "\n"


def run_daily(target_date: str | None = None, skip_history: bool = False) -> dict[str, Any]:
    today = target_date or _date.today().isoformat()
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    verifier_payload = _run_json([str(VERIFIER), "--json"])
    founder_brief: dict[str, Any] = {}
    if FOUNDER_BRIEF.exists():
        founder_brief = _run_json([str(FOUNDER_BRIEF), "--format", "json"])

    history = _load_history()
    prev_row = _previous_row(history, today)
    deltas = _compute_deltas(verifier_payload, prev_row)
    bottleneck = _bottleneck_sentence(verifier_payload)
    market = _market_motion_status()

    payload: dict[str, Any] = {
        "date": today,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bottleneck": bottleneck,
        "verifier": verifier_payload,
        "deltas": deltas,
        "market_motion": market,
        "founder_brief": founder_brief,
    }

    json_path = STATE_DIR / f"daily_routine_{today}.json"
    md_path = STATE_DIR / f"daily_brief_{today}.md"
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_markdown_brief(payload), encoding="utf-8")

    if not skip_history:
        history_row = {
            "date": today,
            "generated_at": payload["generated_at"],
            "overall_pass": bool(verifier_payload.get("overall_pass")),
            "ceo_complete": bool(verifier_payload.get("ceo_complete")),
            "system_scores": _system_score_map(verifier_payload),
            "market_motion": market,
        }
        with HISTORY_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(history_row, sort_keys=True, ensure_ascii=False) + "\n")

    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix daily routine")
    parser.add_argument("--date", default=None, help="ISO date (default: today)")
    parser.add_argument("--no-history", action="store_true", help="skip JSONL append")
    args = parser.parse_args(argv)

    if not VERIFIER.exists():
        print(f"verifier missing: {VERIFIER}", file=sys.stderr)
        return 2

    payload = run_daily(target_date=args.date, skip_history=args.no_history)
    overall = "PASS" if payload["verifier"].get("overall_pass") else "FAIL"
    ceo = "YES" if payload["verifier"].get("ceo_complete") else "NO"
    print(f"daily routine: {payload['date']}  overall={overall}  ceo-complete={ceo}")
    print(f"  {payload['bottleneck']}")
    print(f"  wrote: {(STATE_DIR / ('daily_brief_' + payload['date'] + '.md')).relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
