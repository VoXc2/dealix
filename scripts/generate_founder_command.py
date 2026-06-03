#!/usr/bin/env python3
"""
Generate the Founder Control Engine reports from all data.

Outputs:
  reports/founder/DAILY_SUPER_COMMAND.md   — قرار واحد كل يوم
  reports/founder/WEEKLY_BOARD_REVIEW.md   — مراجعة أسبوعية

Run: python3 scripts/generate_founder_command.py
"""

from collections import Counter

from dealix_common import (
    SYSTEM_SHORT, TOP_QUALITY_THRESHOLD, load_jsonl, md_cell, now_ast, write_report,
)

FOOTER = "\n---\n*Auto-generated Founder Control Engine. AI drafts/sorts/suggests; founder approves all sends, prices, and commitments. Re-run: `python3 scripts/generate_founder_command.py`*\n"

DEAL_STATES = {"interested", "qualified", "mini_proposal_ready", "proposal_sent", "payment_handoff"}
DELIVERY_OPEN = {"won", "intake_required", "delivery_started", "first_output_ready", "client_review"}
ACTIVE = {"accepted", "weekly_value_report", "renewal_candidate"}


def main():
    print("Generating founder command reports ...")
    packs = load_jsonl("data/acquisition/company_intelligence_packs.jsonl")
    briefs = load_jsonl("data/acquisition/call_briefs.jsonl")
    proposals = load_jsonl("data/acquisition/mini_proposals.jsonl")
    sequences = load_jsonl("data/acquisition/follow_up_sequences.jsonl")
    pipelines = load_jsonl("data/delivery/pipelines.jsonl")
    tasks = load_jsonl("data/delivery/tasks.jsonl")
    weeklies = load_jsonl("data/delivery/weekly_value_reports.jsonl")
    gates = load_jsonl("data/delivery/acceptance_gates.jsonl")
    ts = now_ast()

    top_count = sum(1 for p in packs if (p.get("draft_quality") or {}).get("total", 0) >= TOP_QUALITY_THRESHOLD)
    brief_companies = {b.get("company") for b in briefs}
    briefs_ready = [b for b in briefs if b.get("status") == "ready"]
    need_brief = [p for p in packs if p.get("status") in ("sent", "follow_up_due") and p.get("company") not in brief_companies]
    proposals_pending = [p for p in proposals if p.get("status") in ("draft", "pending_approval")]
    interested = [p for p in pipelines if p.get("current_state") in DEAL_STATES]
    deliveries_open = [p for p in pipelines if p.get("current_state") in DELIVERY_OPEN]
    active = [p for p in pipelines if p.get("current_state") in ACTIVE]
    pipe_blockers = [p for p in pipelines if p.get("blockers") or (p.get("current_state") == "intake_required" and not p.get("required_inputs_received"))]
    blocked_tasks = [t for t in tasks if t.get("status") == "blocked"]

    # ---- build prioritized decision queue ----
    decisions = []
    if proposals_pending:
        decisions.append((f"اعتماد {len(proposals_pending)} Mini Proposal بانتظار الموافقة قبل الإرسال", "high"))
    waiting_inputs = [p for p in pipelines if p.get("current_state") == "intake_required" and not p.get("required_inputs_received")]
    if waiting_inputs:
        cos = "، ".join(md_cell(p.get("company")) for p in waiting_inputs)
        decisions.append((f"متابعة required_inputs لبدء التسليم: {cos}", "high"))
    approved_to_send = [p for p in packs if p.get("status") == "approved_to_send"]
    if top_count and not approved_to_send:
        decisions.append((f"مراجعة Top {min(top_count,100)} واعتماد دفعة للإرسال اليوم", "high"))
    if briefs_ready:
        decisions.append((f"توجيه المتصل لإنجاز {len(briefs_ready)} Call Brief جاهزة", "medium"))
    if need_brief:
        decisions.append((f"تجهيز Call Brief لـ {len(need_brief)} شركة مُرسل لها بلا brief", "medium"))
    pending_weekly = [p for p in pipelines if p.get("current_state") in ACTIVE and p.get("company") not in {w.get("company") for w in weeklies}]
    if pending_weekly:
        decisions.append((f"إصدار Weekly Value Report لـ {len(pending_weekly)} عميل نشط", "medium"))
    if not decisions:
        decisions.append(("لا قرار حرج اليوم — استمرار الإنتاج والمتابعة", "low"))

    # ================= DAILY_SUPER_COMMAND =================
    lines = [f"# Dealix — Founder Daily Super Command", f"Generated: {ts} AST", "",
             "قرار واحد كل يوم: ماذا ترسل، من يتصل، ماذا يعرض، ماذا يُسلّم، وما العوائق.", "",
             "## لوحة اليوم", "", "| المؤشر | القيمة |", "|---|---:|",
             f"| شركات تم تحليلها (Intelligence Packs) | {len(packs)} |",
             f"| مسودات إيميل مُجهّزة | {len(packs)} |",
             f"| مؤهّل لـ Top 100 (≥{TOP_QUALITY_THRESHOLD}) | {top_count} |",
             f"| Call Briefs جاهزة | {len(briefs_ready)} |",
             f"| شركات مُرسل لها تحتاج Call Brief | {len(need_brief)} |",
             f"| Mini Proposals بانتظار موافقة | {len(proposals_pending)} |",
             f"| عملاء في مسار الصفقة (interested→payment) | {len(interested)} |",
             f"| تسليمات مفتوحة | {len(deliveries_open)} |",
             f"| عملاء نشطون (accepted+) | {len(active)} |",
             f"| مسارات بها عوائق | {len(pipe_blockers)} |",
             "",
             "## أهم قرار اليوم (Decision Queue)", "", "| # | القرار | الأولوية |", "|---:|---|---|"]
    for i, (d, pr) in enumerate(decisions, 1):
        lines.append(f"| {i} | {md_cell(d)} | {pr} |")

    lines += ["", "## من يحتاج اتصال", "", "| Call Brief | Company | System | Next step |", "|---|---|---|---|"]
    if briefs_ready:
        for b in briefs_ready:
            lines.append("| {id} | {co} | {sys} | {ns} |".format(
                id=md_cell(b.get("id")), co=md_cell(b.get("company")),
                sys=md_cell(SYSTEM_SHORT.get(b.get("recommended_system"))), ns=md_cell(b.get("next_step"))[:45]))
    else:
        lines.append("| — | لا اتصالات جاهزة | — | — |")

    lines += ["", "## Mini Proposals بانتظار موافقة", "", "| ID | Company | System | Starter price |", "|---|---|---|---|"]
    if proposals_pending:
        for p in proposals_pending:
            sp = (p.get("starter_price") or {}).get("display", "")
            lines.append("| {id} | {co} | {sys} | {sp} |".format(
                id=md_cell(p.get("id")), co=md_cell(p.get("company")),
                sys=md_cell(SYSTEM_SHORT.get(p.get("recommended_system"))), sp=md_cell(sp)))
    else:
        lines.append("| — | لا عروض بانتظار موافقة | — | — |")

    lines += ["", "## التسليمات المفتوحة", "", "| Pipeline | Company | State | Inputs? |", "|---|---|---|---|"]
    if deliveries_open:
        for p in deliveries_open:
            lines.append("| {id} | {co} | {st} | {ir} |".format(
                id=md_cell(p.get("id")), co=md_cell(p.get("company")), st=md_cell(p.get("current_state")),
                ir="✅" if p.get("required_inputs_received") else "⛔"))
    else:
        lines.append("| — | لا تسليمات مفتوحة | — | — |")

    lines += ["", "## العوائق", "", "| Pipeline | Company | Blocker |", "|---|---|---|"]
    if pipe_blockers:
        for p in pipe_blockers:
            blk = "، ".join(p.get("blockers", [])) or "بانتظار required_inputs"
            lines.append(f"| {md_cell(p.get('id'))} | {md_cell(p.get('company'))} | {md_cell(blk)} |")
    else:
        lines.append("| — | لا عوائق | — |")
    lines.append(FOOTER)
    write_report("founder/DAILY_SUPER_COMMAND.md", "\n".join(lines))

    # ================= WEEKLY_BOARD_REVIEW =================
    sys_counts = Counter(p.get("recommended_system") for p in packs)
    state_counts = Counter(p.get("current_state") for p in pipelines)
    gate_status = Counter(g.get("status") for g in gates)
    lines = [f"# Dealix — Weekly Board Review", f"Generated: {ts} AST", "",
             "## ملخص الأسبوع", "", "| المؤشر | القيمة |", "|---|---:|",
             f"| شركات تم تحليلها | {len(packs)} |",
             f"| تسلسلات متابعة نشطة | {sum(1 for s in sequences if s.get('status') in ('scheduled','in_progress'))} |",
             f"| عملاء في مسار الصفقة | {len(interested)} |",
             f"| تسليمات مفتوحة | {len(deliveries_open)} |",
             f"| عملاء نشطون | {len(active)} |",
             f"| تقارير قيمة صادرة | {len(weeklies)} |",
             f"| بوابات قبول (passed/open/failed) | {gate_status.get('passed',0)}/{gate_status.get('open',0)}/{gate_status.get('failed',0)} |",
             "", "## الإنتاج حسب النظام", "", "| System | Packs |", "|---|---:|"]
    for s, label in SYSTEM_SHORT.items():
        lines.append(f"| {label} | {sys_counts.get(s,0)} |")
    lines += ["", "## مسارات التسليم حسب الحالة", "", "| State | Count |", "|---|---:|"]
    for st, n in state_counts.most_common():
        lines.append(f"| {st} | {n} |")
    lines += ["", "## مخاطر وتنبيهات", ""]
    risks = []
    if waiting_inputs:
        risks.append(f"- {len(waiting_inputs)} مسار عالق بانتظار required_inputs (لا يبدأ التسليم قبلها).")
    if blocked_tasks:
        risks.append(f"- {len(blocked_tasks)} مهمة موقوفة (blocked).")
    if proposals_pending:
        risks.append(f"- {len(proposals_pending)} Mini Proposal بانتظار موافقة founder.")
    risks.append("- تذكير حوكمة: لا إرسال/تسعير/التزام بدون موافقة founder؛ مصادر عامة فقط؛ بلا أسرار/PII.")
    lines += risks
    lines.append(FOOTER)
    write_report("founder/WEEKLY_BOARD_REVIEW.md", "\n".join(lines))

    print("Founder command reports done.")


if __name__ == "__main__":
    main()
