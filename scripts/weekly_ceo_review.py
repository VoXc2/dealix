#!/usr/bin/env python3
"""Dealix Weekly CEO Review.

Runs every Sunday at 06:00 KSA (via cron) or on demand. Composes:

  1. Current master-verifier state.
  2. Week-over-week deltas computed from data/_state/verifier_history.jsonl
     (Monday-to-Sunday delta if available, else first-vs-last in window).
  3. Market-motion activity over the week:
       - new entries in data/partner_outreach_log.json
       - new entries in data/first_invoice_log.json
       - new entries in data/capital_asset_index.json (if present)
  4. Top three actions for next week, derived from failing systems and
     the CEO-complete gate.

Hard rules:
- Never auto-sends. Founder reviews and forwards manually.
- Never inflates marker counts.
- Reuses the master verifier; does not duplicate its logic.

Outputs:
    data/_state/weekly_review_<YYYY-Www>.md
    data/_state/weekly_review_<YYYY-Www>.json

Usage:
    python scripts/weekly_ceo_review.py
    python scripts/weekly_ceo_review.py --week 2026-W20
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date as _date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFIER = REPO_ROOT / "scripts" / "verify_all_dealix.py"
STATE_DIR = REPO_ROOT / "data" / "_state"
HISTORY_PATH = STATE_DIR / "verifier_history.jsonl"


def _run_verifier_json() -> dict[str, Any]:
    out = subprocess.run(
        [sys.executable, str(VERIFIER), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"_error": "non-json", "_stderr": out.stderr}


def _isoweek_label(d: _date) -> str:
    year, week, _ = d.isocalendar()
    return f"{year}-W{week:02d}"


def _week_bounds(label: str) -> tuple[_date, _date]:
    """Return Monday and Sunday of a given ISO week label like 2026-W20."""
    year_str, week_str = label.split("-W")
    year, week = int(year_str), int(week_str)
    monday = _date.fromisocalendar(year, week, 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def _load_history() -> list[dict[str, Any]]:
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
    return rows


def _window(rows: list[dict[str, Any]], start: _date, end: _date) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        d = row.get("date")
        if not d:
            continue
        try:
            day = _date.fromisoformat(d)
        except ValueError:
            continue
        if start <= day <= end:
            out.append(row)
    out.sort(key=lambda r: r.get("date") or "")
    return out


def _weekly_deltas(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute first-vs-last delta across the week window."""
    if not rows:
        return {"system_score_changes": [], "first_date": None, "last_date": None}
    if len(rows) == 1:
        return {"system_score_changes": [], "first_date": rows[0].get("date"), "last_date": rows[0].get("date")}
    first = rows[0]
    last = rows[-1]
    f_scores = first.get("system_scores") or {}
    l_scores = last.get("system_scores") or {}
    changes = []
    for name in sorted(set(f_scores) | set(l_scores)):
        f = int(f_scores.get(name, 0))
        l_ = int(l_scores.get(name, 0))
        if f != l_:
            changes.append({"system": name, "from": f, "to": l_})
    return {
        "system_score_changes": changes,
        "first_date": first.get("date"),
        "last_date": last.get("date"),
        "overall_pass_first": bool(first.get("overall_pass")),
        "overall_pass_last": bool(last.get("overall_pass")),
        "ceo_complete_first": bool(first.get("ceo_complete")),
        "ceo_complete_last": bool(last.get("ceo_complete")),
    }


def _read_marker(rel: str, key: str) -> tuple[int, list[dict[str, Any]]]:
    p = REPO_ROOT / rel
    if not p.exists():
        return 0, []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return int(data.get(key, 0)), list(data.get("entries") or [])
    except Exception:
        return 0, []


def _market_activity(start: _date, end: _date) -> dict[str, Any]:
    """Count marker entries whose 'sent_at' falls in the week."""
    out: dict[str, Any] = {}
    for label, rel, key in (
        ("partner_outreach",  "data/partner_outreach_log.json", "outreach_sent_count"),
        ("first_invoice",     "data/first_invoice_log.json",    "invoice_sent_count"),
    ):
        total, entries = _read_marker(rel, key)
        in_week = 0
        for e in entries:
            ts = str(e.get("sent_at") or e.get("created_at") or "")[:10]
            try:
                d = _date.fromisoformat(ts)
            except ValueError:
                continue
            if start <= d <= end:
                in_week += 1
        out[label] = {"total": total, "in_week": in_week}

    # Capital asset index (introduced in PR3 — may not exist yet).
    ca_path = REPO_ROOT / "data" / "capital_asset_index.json"
    if ca_path.exists():
        try:
            data = json.loads(ca_path.read_text(encoding="utf-8"))
            entries = list(data.get("entries") or [])
            in_week = 0
            for e in entries:
                ts = str(e.get("created_at") or "")[:10]
                try:
                    d = _date.fromisoformat(ts)
                except ValueError:
                    continue
                if start <= d <= end:
                    in_week += 1
            out["capital_assets"] = {"total": len(entries), "in_week": in_week}
        except Exception:
            out["capital_assets"] = {"total": 0, "in_week": 0}
    else:
        out["capital_assets"] = {"total": 0, "in_week": 0}
    return out


def _top_three_next_actions(verifier: dict[str, Any], market: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    po = market.get("partner_outreach", {})
    inv = market.get("first_invoice", {})
    if po.get("total", 0) == 0:
        actions.append("Send one anchor partner outreach and append to data/partner_outreach_log.json.")
    if inv.get("total", 0) == 0:
        actions.append("Open invoice motion via docs/ops/FIRST_INVOICE_UNLOCK.md.")
    # Add the lowest-scoring top-8 failing system, if any.
    failing_top8 = [
        s for s in verifier.get("systems", [])
        if s.get("in_top_eight") and not s.get("passed")
    ]
    failing_top8.sort(key=lambda s: s.get("score", 0))
    for s in failing_top8:
        a = f"Lift {s['name']} (top-8) — score {s.get('score', 0)}/5."
        if a not in actions and len(actions) < 3:
            actions.append(a)
    if not actions:
        actions = [
            "All top-8 are PASS. Keep the cadence; defend the score.",
        ]
    return actions[:3]


def _markdown_review(payload: dict[str, Any]) -> str:
    week = payload["week_label"]
    start = payload["week_start"]
    end = payload["week_end"]
    v = payload["verifier"]
    deltas = payload["deltas"]
    market = payload["market_activity"]
    actions = payload["next_three_actions"]
    overall = "PASS" if v.get("overall_pass") else "FAIL"
    ceo = "YES" if v.get("ceo_complete") else "NO"

    lines: list[str] = []
    lines.append(f"# Dealix Weekly CEO Review — {week}")
    lines.append(f"_Week of {start} → {end}._")
    lines.append("")
    lines.append("## Verifier State (end of week)")
    lines.append(f"- Overall: **{overall}**")
    lines.append(f"- CEO-complete (top 8 ≥ 4/5): **{ceo}**")
    systems = v.get("systems", [])
    passed = sum(1 for s in systems if s.get("passed"))
    lines.append(f"- Systems passed: **{passed} / {len(systems)}**")
    lines.append("")
    lines.append("## Week-over-Week Score Changes")
    if not deltas.get("system_score_changes"):
        lines.append("- No system score changes this week.")
    else:
        lines.append(f"- Window: {deltas['first_date']} → {deltas['last_date']}")
        for ch in deltas["system_score_changes"]:
            arrow = "↑" if ch["to"] > ch["from"] else "↓"
            lines.append(f"  - {ch['system']}: {ch['from']} {arrow} {ch['to']}")
    lines.append("")
    lines.append("## Market Motion (honest counts)")
    po = market.get("partner_outreach", {})
    inv = market.get("first_invoice", {})
    ca = market.get("capital_assets", {})
    lines.append(f"- Partner outreach sent: total **{po.get('total', 0)}** (this week: **{po.get('in_week', 0)}**).")
    lines.append(f"- Invoices sent:         total **{inv.get('total', 0)}** (this week: **{inv.get('in_week', 0)}**).")
    lines.append(f"- Capital assets:        total **{ca.get('total', 0)}** (this week: **{ca.get('in_week', 0)}**).")
    lines.append("")
    lines.append("## Top 3 Actions Next Week")
    for i, a in enumerate(actions, 1):
        lines.append(f"{i}. {a}")
    lines.append("")
    lines.append("---")
    lines.append("_Produced by `scripts/weekly_ceo_review.py`._")
    lines.append("_No auto-sends. Founder reviews and forwards manually._")
    return "\n".join(lines) + "\n"


def run_weekly(week_label: str | None = None) -> dict[str, Any]:
    today = _date.today()
    if week_label:
        start, end = _week_bounds(week_label)
        label = week_label
    else:
        start, end = _week_bounds(_isoweek_label(today))
        label = _isoweek_label(today)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    verifier_payload = _run_verifier_json()
    rows = _window(_load_history(), start, end)
    deltas = _weekly_deltas(rows)
    market = _market_activity(start, end)
    actions = _top_three_next_actions(verifier_payload, market)

    payload: dict[str, Any] = {
        "week_label": label,
        "week_start": start.isoformat(),
        "week_end": end.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verifier": verifier_payload,
        "deltas": deltas,
        "market_activity": market,
        "next_three_actions": actions,
    }

    json_path = STATE_DIR / f"weekly_review_{label}.json"
    md_path = STATE_DIR / f"weekly_review_{label}.md"
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_markdown_review(payload), encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix weekly CEO review")
    parser.add_argument("--week", default=None, help="ISO week (e.g., 2026-W20)")
    args = parser.parse_args(argv)
    if not VERIFIER.exists():
        print(f"verifier missing: {VERIFIER}", file=sys.stderr)
        return 2
    payload = run_weekly(week_label=args.week)
    overall = "PASS" if payload["verifier"].get("overall_pass") else "FAIL"
    ceo = "YES" if payload["verifier"].get("ceo_complete") else "NO"
    print(
        f"weekly review: {payload['week_label']}  "
        f"({payload['week_start']} → {payload['week_end']})  "
        f"overall={overall}  ceo-complete={ceo}"
    )
    print(f"  next 3 actions:")
    for i, a in enumerate(payload["next_three_actions"], 1):
        print(f"    {i}. {a}")
    print(f"  wrote: data/_state/weekly_review_{payload['week_label']}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
