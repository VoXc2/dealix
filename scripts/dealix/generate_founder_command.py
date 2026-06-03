"""Generate the Founder Daily Super Command report + finance cash-priority data.

The command answers the founder's four daily questions:
  1) what to send   2) who to call   3) what to propose   4) what to deliver
It only ever recommends DRAFTS for human approval — it never sends or calls.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl, write_text, ROOT


def _load(path):
    p = ROOT / path
    return load_jsonl(path) if p.exists() else []


def build_finance(packs, dry_run=False):
    rows = [
        {
            "company_name": p["company_name"],
            "urgency": 0,
            "ticket_potential": 0,
            "speed_to_cash": 0,
            "score": p["cash_priority_score"],
        }
        for p in packs
    ]
    if not dry_run:
        dump_jsonl("data/finance/cash_priority_scores.jsonl", rows)
    return rows


def build(dry_run=False):
    packs = _load("data/account_intelligence/account_packs.jsonl")
    drafts = _load("data/outreach/top_100_approval_queue.jsonl")
    briefs = _load("data/acquisition/call_briefs.jsonl")
    proposals = _load("data/proposals/mini_proposals.jsonl")
    pipelines = _load("data/delivery/pipelines.jsonl")

    active = [p for p in packs if not p.get("suppressed")]
    build_finance(active, dry_run=dry_run)

    today = dt.date.today().isoformat()
    top_send = active[:5]
    top_call = active[:5]
    top_propose = active[:3]
    blocked_delivery = [p for p in pipelines if not p.get("inputs_received")]

    def row(p):
        return f"| {p['company_name']} | {p['sector']} | {p['primary_need']} | {p['recommended_core_system']} | {p['final_account_score']} |"

    lines = []
    lines.append("# Dealix — أمر المؤسس اليومي (Daily Super Command)")
    lines.append("")
    lines.append(f"التاريخ: {today}")
    lines.append("")
    lines.append("> كل ما يلي مسودات للاعتماد البشري. لا يتم أي إرسال أو اتصال آلي.")
    lines.append("")
    lines.append("## 1) ماذا ترسل اليوم (Top 5 Email Drafts)")
    lines.append("")
    lines.append("| الشركة | القطاع | الاحتياج | النظام | السكور |")
    lines.append("| --- | --- | --- | --- | --- |")
    for p in top_send:
        lines.append(row(p))
    lines.append("")
    lines.append(f"عدد المسودات في طابور الاعتماد: **{len(drafts)}**")
    lines.append("")
    lines.append("## 2) من تتصل به (Top 5 Calls)")
    lines.append("")
    lines.append("| الشركة | القطاع | الاحتياج | النظام | السكور |")
    lines.append("| --- | --- | --- | --- | --- |")
    for p in top_call:
        lines.append(row(p))
    lines.append("")
    lines.append(f"عدد Call Briefs الجاهزة: **{len(briefs)}**")
    lines.append("")
    lines.append("## 3) ماذا تعرض (Top 3 Mini Proposals)")
    lines.append("")
    lines.append("| الشركة | العنوان | السعر المبدئي | المدة |")
    lines.append("| --- | --- | --- | --- |")
    by_name = {p["company_name"]: p for p in proposals}
    for p in top_propose:
        mp = by_name.get(p["company_name"])
        if mp:
            lines.append(f"| {mp['company_name']} | {mp['title']} | {mp['starter_price_sar']} ر.س | {mp['timeline_days']} يوم |")
    lines.append("")
    lines.append(f"إجمالي العروض المسودة: **{len(proposals)}** (كلها تحتاج اعتماد).")
    lines.append("")
    lines.append("## 4) ماذا تسلّم (Delivery Blockers)")
    lines.append("")
    if blocked_delivery:
        lines.append("| العميل | النظام | الحالة | الإجراء |")
        lines.append("| --- | --- | --- | --- |")
        for p in blocked_delivery:
            lines.append(f"| {p['client']} | {p['selected_system']} | {p['stage']} | بانتظار مدخلات العميل |")
    else:
        lines.append("لا يوجد عملاء في مرحلة التسليم حاليًا.")
    lines.append("")
    lines.append("## بوابات الاعتماد المطلوبة من المؤسس")
    lines.append("")
    lines.append("- اعتماد إرسال أي بريد (لا إرسال آلي).")
    lines.append("- اعتماد أي Mini Proposal أو تغيير تسعير.")
    lines.append("- اعتماد بدء أي تسليم (بعد اكتمال المدخلات).")
    lines.append("")
    report = "\n".join(lines) + "\n"
    if not dry_run:
        write_text("reports/founder/DAILY_SUPER_COMMAND.md", report)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    report = build(dry_run=args.dry_run)
    print("Founder daily super command generated"
          + (" (dry-run, not written)." if args.dry_run else " -> reports/founder/DAILY_SUPER_COMMAND.md"))
    if args.dry_run:
        print("\n".join(report.splitlines()[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
