#!/usr/bin/env python3
"""Draft a BU decision memo from a monthly snapshot.

Given a BU slug, reads its current entry from `data/business_units.json`,
applies the recommendation from
`auto_client_acquisition/holding_os/unit_governance.py:evaluate_unit_decision()`
against a provided (or default) monthly snapshot, and produces a board-
ready memo:

    data/_state/bu_memos/<slug>_<YYYY-MM>.md

The memo is buyer/auditor-readable and ends with an explicit
recommended action. No external send.

Usage:
    python scripts/draft_bu_decision_memo.py --unit core-os

    # Provide snapshot values explicitly (any unspecified flag defaults
    # to a conservative `False` / `0.0`):
    python scripts/draft_bu_decision_memo.py --unit core-os \\
        --revenue-growing --margin-ok --qa-score 82 \\
        --retainers-growing --governance-risk-acceptable \\
        --client-health-ok --proof-delivery-on-track \\
        --playbook-maturity-ok
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date as _date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "business_units.json"
OUT_DIR = REPO_ROOT / "data" / "_state" / "bu_memos"

sys.path.insert(0, str(REPO_ROOT))
from auto_client_acquisition.holding_os.unit_governance import (  # noqa: E402
    UnitMonthlySnapshot,
    evaluate_unit_decision,
)


def _load_registry() -> dict:
    if not REGISTRY.exists():
        return {"entries": []}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _find_unit(slug: str) -> dict | None:
    for e in _load_registry().get("entries") or []:
        if str(e.get("slug")) == slug:
            return e
    return None


def _md(unit: dict, snapshot: UnitMonthlySnapshot, decision: str) -> str:
    today = _date.today().isoformat()
    lines = [
        f"# Board Memo — `{unit['slug']}` ({unit.get('name', '')})",
        "",
        f"_Date:_ **{today}**  ",
        f"_Current status:_ **`{unit.get('status', '')}`**  ",
        f"_Owner:_ **{unit.get('owner', '')}**",
        "",
        "## Monthly Snapshot",
        "",
        f"- revenue_growing: `{snapshot.revenue_growing}`",
        f"- margin_ok: `{snapshot.margin_ok}`",
        f"- retainers_growing: `{snapshot.retainers_growing}`",
        f"- proof_delivery_on_track: `{snapshot.proof_delivery_on_track}`",
        f"- qa_score: `{snapshot.qa_score}`",
        f"- governance_risk_acceptable: `{snapshot.governance_risk_acceptable}`",
        f"- module_usage_growing: `{snapshot.module_usage_growing}`",
        f"- playbook_maturity_ok: `{snapshot.playbook_maturity_ok}`",
        f"- client_health_ok: `{snapshot.client_health_ok}`",
        f"- venture_signal_strong: `{snapshot.venture_signal_strong}`",
        "",
        "## Engine Recommendation",
        "",
        f"`evaluate_unit_decision()` recommends: **`{decision.upper()}`**.",
        "",
        "_Source: `auto_client_acquisition/holding_os/unit_governance.py`._",
        "",
        "## Rules Triggered",
        "",
        _rule_explanation(snapshot, decision),
        "",
        "## Suggested Next Step",
        "",
        _next_step(unit, decision),
        "",
        "---",
        f"_Produced by `scripts/draft_bu_decision_memo.py`. Reviewer signs at the board cycle following this draft date._",
    ]
    return "\n".join(lines) + "\n"


def _rule_explanation(s: UnitMonthlySnapshot, decision: str) -> str:
    decision = decision.lower()
    if decision == "hold" and not s.governance_risk_acceptable:
        return "- Rule 1 (Governance Risk): governance posture not acceptable."
    if decision == "pilot" and not s.client_health_ok:
        return "- Rule 2 (Client Health): client health gate failed."
    if decision == "kill":
        return ("- Rule 3 (Kill Threshold): qa_score < 55 AND revenue_growing == False. "
                "Both conditions are required.")
    if decision == "spinout":
        return ("- Rule 4 (Spinout Eligibility): venture_signal_strong AND "
                "module_usage_growing AND qa_score >= 85.")
    if decision == "scale":
        return ("- Rule 5 (Scale Eligibility): revenue_growing AND margin_ok AND "
                "qa_score >= 80 AND retainers_growing.")
    if decision == "build":
        return "- Rule 6 (Build Eligibility): playbook_maturity_ok AND proof_delivery_on_track."
    return "- Rule 7 (Default): none of the higher-rule conditions met."


def _next_step(unit: dict, decision: str) -> str:
    slug = unit.get("slug", "")
    decision = decision.upper()
    if decision == "KILL":
        return (
            f"Run `python scripts/register_business_unit.py "
            f"--really-this-is-a-bu --slug {slug} --update-status KILL "
            f"--reason \"<short rationale>\"`. Then register a final "
            f"Capital Asset summarizing salvageable work."
        )
    if decision == "HOLD":
        return (
            f"Run `python scripts/register_business_unit.py "
            f"--really-this-is-a-bu --slug {slug} --update-status HOLD "
            f"--reason \"<governance gap>\"`. Plan a remediation cycle."
        )
    if decision in ("SCALE", "BUILD", "PILOT", "SPINOUT"):
        return (
            f"Run `python scripts/register_business_unit.py "
            f"--really-this-is-a-bu --slug {slug} --update-status {decision}`. "
            f"Update `landing/group.html` portfolio via "
            f"`python scripts/render_holding_portfolio.py`."
        )
    return f"No automatic step; review with board."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="draft a BU decision memo")
    parser.add_argument("--unit", required=True, help="BU slug")
    parser.add_argument("--revenue-growing", action="store_true")
    parser.add_argument("--margin-ok", action="store_true")
    parser.add_argument("--retainers-growing", action="store_true")
    parser.add_argument("--proof-delivery-on-track", action="store_true")
    parser.add_argument("--qa-score", type=float, default=0.0)
    parser.add_argument("--governance-risk-acceptable", action="store_true")
    parser.add_argument("--module-usage-growing", action="store_true")
    parser.add_argument("--playbook-maturity-ok", action="store_true")
    parser.add_argument("--client-health-ok", action="store_true")
    parser.add_argument("--venture-signal-strong", action="store_true")
    args = parser.parse_args(argv)

    unit = _find_unit(args.unit)
    if unit is None:
        print(f"unit {args.unit!r} not found in {REGISTRY.name}", file=sys.stderr)
        return 1

    snapshot = UnitMonthlySnapshot(
        revenue_growing=args.revenue_growing,
        margin_ok=args.margin_ok,
        retainers_growing=args.retainers_growing,
        proof_delivery_on_track=args.proof_delivery_on_track,
        qa_score=args.qa_score,
        governance_risk_acceptable=args.governance_risk_acceptable,
        module_usage_growing=args.module_usage_growing,
        playbook_maturity_ok=args.playbook_maturity_ok,
        client_health_ok=args.client_health_ok,
        venture_signal_strong=args.venture_signal_strong,
    )
    decision = str(evaluate_unit_decision(snapshot))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    yyyymm = datetime.now(timezone.utc).strftime("%Y-%m")
    out_path = OUT_DIR / f"{args.unit}_{yyyymm}.md"
    out_path.write_text(_md(unit, snapshot, decision), encoding="utf-8")
    try:
        display = out_path.relative_to(REPO_ROOT)
    except ValueError:
        display = out_path
    print(f"drafted memo for {args.unit}: recommendation={decision.upper()}")
    print(f"  wrote: {display}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
