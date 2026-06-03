#!/usr/bin/env python3
"""
Dealix Ultimate Scale OS — command-line entrypoint.

Thin dispatcher over the scale-readiness check scripts plus the Founder
War Room generator. Stdlib only.

Commands:
    scale-score           Compute the Ultimate Scale scorecard + readiness mode
    agent-audit           Run agent governance + permission (red-line) checks
    deliverability-check  Validate email deliverability readiness
    experiment-review     Validate the revenue experimentation registry
    delivery-capacity     Review delivery capacity utilization
    war-room [--dry-run]  Build the Founder War Room daily brief
    scale-all             Run every scale-readiness check

Examples:
    python dealix.py scale-score
    python dealix.py agent-audit
    python dealix.py war-room --dry-run
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
CHECKS_DIR = REPO_ROOT / "scripts" / "checks"
sys.path.insert(0, str(CHECKS_DIR))

import check_agent_governance  # noqa: E402
import check_agent_permissions  # noqa: E402
import check_delivery_capacity  # noqa: E402
import check_deliverability_readiness  # noqa: E402
import check_prompt_injection_defense  # noqa: E402
import check_revenue_experiments  # noqa: E402
import check_scale_readiness  # noqa: E402


def _load_json(rel_path: str):
    try:
        with open(REPO_ROOT / rel_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_prospects() -> list[dict]:
    rows: list[dict] = []
    try:
        with open(REPO_ROOT / "company_os" / "revenue" / "prospects.csv",
                  "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows


def _score(p: dict) -> int:
    try:
        return int(p.get("score", 0))
    except (ValueError, TypeError):
        return 0


def build_war_room() -> str:
    """Render the Founder War Room daily brief from company_os data."""
    today = datetime.now().strftime("%Y-%m-%d")
    prospects = _load_prospects()
    prospects_sorted = sorted(prospects, key=_score, reverse=True)
    top10 = prospects_sorted[:10]

    approvals = _load_json("company_os/governance/approval_queue.json") or []
    pending = [a for a in approvals if not a.get("approved", False)]
    offers = pending[:5]

    scale = _load_json("company_os/scale/scale_state.json") or {}
    cap = _load_json("company_os/delivery/capacity.json") or {}
    deliver = _load_json("company_os/deliverability/deliverability_state.json") or {}
    experiments = _load_json("company_os/experiments/experiments.json") or {}

    total = cap.get("total_capacity_hours_per_week", 0)
    committed = cap.get("committed_hours_per_week", 0)
    util = round(committed / total * 100, 1) if total else 0
    block = cap.get("scale_block_threshold_pct", 80)
    spam = deliver.get("spam", {}).get("spam_rate_pct", 0)
    mode = scale.get("current_mode", "unknown")

    # Production decision: capacity + deliverability gate.
    if util >= block:
        prod_decision = (f"❌ لا ترفع الإنتاج — استغلال التسليم {util}% "
                         f"تجاوز حد {block}%. ركّز على التسليم أو فوّض.")
    elif spam >= deliver.get("spam", {}).get("spam_rate_warn_pct", 0.1):
        prod_decision = "⚠️ ثبّت الإرسال — معدل السبام يقترب من الحد. راقب قبل الرفع."
    else:
        prod_decision = (f"✅ يمكن رفع الإنتاج تدريجيًا — الاستغلال {util}% "
                         f"تحت {block}% والسبام {spam}%.")

    top_company = top10[0]["company"] if top10 else "—"
    running = [e for e in experiments.get("experiments", []) if e.get("status") == "running"]
    learning = running[0]["hypothesis"] if running else "لا توجد تجربة نشطة هذا الأسبوع."

    lines: list[str] = []
    lines.append("# Founder War Room — Daily")
    lines.append(f"*Date: {today} | Mode: {mode}*")
    lines.append("")
    lines.append("> هذا تقرير داخلي. لا يُرسل أي شيء خارجيًا بدون موافقة المؤسس.")
    lines.append("")

    lines.append("## 1. أهم قرار اليوم")
    lines.append(f"- مراجعة واعتماد أفضل {len(offers)} عروض/رسائل في قائمة الموافقة قبل أي إرسال.")
    lines.append("")

    lines.append("## 2. أكبر فرصة نقدية")
    lines.append(f"- {top_company} — أعلى Score في القائمة اليوم.")
    lines.append("")

    lines.append("## 3. أكبر خطر")
    if util >= block:
        lines.append(f"- استغلال التسليم {util}% — خطر البيع أكثر من القدرة.")
    else:
        lines.append("- لا خطر تشغيلي حرج اليوم. راقب deliverability ومعدل الردود.")
    lines.append("")

    lines.append("## 4. أفضل 10 شركات اليوم")
    lines.append("| # | Company | Segment | Score | Next Action |")
    lines.append("|---|---------|---------|------:|-------------|")
    for i, p in enumerate(top10, 1):
        lines.append(f"| {i} | {p.get('company','')} | {p.get('segment','')} "
                     f"| {p.get('score','')} | {p.get('next_action','')} |")
    if not top10:
        lines.append("| — | لا توجد شركات | — | — | — |")
    lines.append("")

    lines.append("## 5. أفضل 5 عروض تنتظر موافقة")
    lines.append("| # | Company | Type | Risk |")
    lines.append("|---|---------|------|------|")
    for i, o in enumerate(offers, 1):
        lines.append(f"| {i} | {o.get('company','')} | {o.get('type','')} "
                     f"| {o.get('risk','')} |")
    if not offers:
        lines.append("| — | لا عروض معلّقة | — | — |")
    lines.append("")

    lines.append("## 6. الصفقات المتوقفة")
    stalled = [p for p in prospects if p.get("status") in ("Contacted", "Replied")
               and p.get("status") != "Won"]
    if stalled:
        for p in stalled[:5]:
            lines.append(f"- {p.get('company','')} — الحالة: {p.get('status','')}")
    else:
        lines.append("- لا صفقات متوقفة مسجّلة.")
    lines.append("")

    lines.append("## 7. التسليمات المتأخرة")
    lines.append("- لا تسليمات متأخرة مسجّلة (راجع pipeline قبل الرفع).")
    lines.append("")

    lines.append("## 8. هل نرفع أو نخفض الإنتاج؟")
    lines.append(f"- {prod_decision}")
    lines.append("")

    lines.append("## 9. ماذا نتعلم من السوق؟")
    lines.append(f"- {learning}")
    lines.append("")

    lines.append("---")
    lines.append(f"*Generated by `dealix.py war-room` | {today} | No external action taken.*")
    return "\n".join(lines) + "\n"


def cmd_war_room(args) -> int:
    content = build_war_room()
    if args.dry_run:
        print(content)
        print("[dry-run] War Room rendered to stdout only — no file written, "
              "no external action.")
        return 0
    out = REPO_ROOT / "reports" / "founder" / "FOUNDER_WAR_ROOM_DAILY.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"War Room written to {out.relative_to(REPO_ROOT)}")
    return 0


def cmd_agent_audit(_args) -> int:
    ok_gov = check_agent_governance.run()
    print()
    ok_perm = check_agent_permissions.run()
    return 0 if (ok_gov and ok_perm) else 1


def _single(check) -> int:
    return 0 if check.run() else 1


def cmd_scale_all(_args) -> int:
    checks = [
        check_agent_governance,
        check_agent_permissions,
        check_deliverability_readiness,
        check_delivery_capacity,
        check_revenue_experiments,
        check_prompt_injection_defense,
        check_scale_readiness,
    ]
    results = []
    for c in checks:
        results.append(c.run())
        print()
    passed = sum(1 for r in results if r)
    print(f"==> scale-all: {passed}/{len(results)} checks passed")
    return 0 if all(results) else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="dealix.py", description="Dealix Ultimate Scale OS CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scale-score", help="Ultimate Scale scorecard + readiness mode")
    sub.add_parser("agent-audit", help="Agent governance + permission red-line audit")
    sub.add_parser("deliverability-check", help="Email deliverability readiness")
    sub.add_parser("experiment-review", help="Revenue experimentation registry")
    sub.add_parser("delivery-capacity", help="Delivery capacity utilization review")
    sub.add_parser("scale-all", help="Run every scale-readiness check")
    war = sub.add_parser("war-room", help="Founder War Room daily brief")
    war.add_argument("--dry-run", action="store_true",
                     help="Print to stdout only; write no file, take no action")

    args = parser.parse_args()

    if args.command == "scale-score":
        return _single(check_scale_readiness)
    if args.command == "agent-audit":
        return cmd_agent_audit(args)
    if args.command == "deliverability-check":
        return _single(check_deliverability_readiness)
    if args.command == "experiment-review":
        return _single(check_revenue_experiments)
    if args.command == "delivery-capacity":
        return _single(check_delivery_capacity)
    if args.command == "scale-all":
        return cmd_scale_all(args)
    if args.command == "war-room":
        return cmd_war_room(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
