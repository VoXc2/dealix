#!/usr/bin/env python3
"""
Dealix Account Intelligence — report generator.

Reads the data backbone produced by generate_account_packs.py and writes the
human-facing reports plus the Founder Daily Command:

  reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md
  reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md
  reports/account_intelligence/ACCOUNT_PACK_QUALITY_REVIEW.md
  reports/contacts/DAILY_CONTACT_DISCOVERY_REPORT.md
  reports/contacts/MISSING_CONTACTS_REVIEW.md
  reports/proposals/MINI_PROPOSAL_QUEUE.md
  reports/proposals/PROPOSAL_APPROVAL_QUEUE.md
  reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md
  reports/founder/DAILY_SUPER_COMMAND.md

It also emits data/account_intelligence/account_scoring.jsonl (Top-100 scoring).

Usage:
  python3 scripts/generate_account_reports.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import dealix_account_lib as lib


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def fmt_int(n: int) -> str:
    return f"{n:,}"


def build_scoring(packs: list[dict]) -> list[dict]:
    rows = []
    for p in packs:
        reasons = lib.top100_exclusions(p)
        rows.append({
            "pack_id": p["pack_id"],
            "company_name": p["company_name"],
            "recommended_system": p["recommended_system"],
            "account_score": p["account_score"],
            "bucket": lib.account_bucket(p["account_score"]),
            "eligible_for_top100": len(reasons) == 0,
            "exclusion_reasons": reasons,
            "breakdown": p["account_score_breakdown"],
            "evidence_level": p["evidence_level"],
            "risk_level": p["risk_level"],
            "contact_confidence": p["contact_confidence"],
        })
    return rows


def main() -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    packs = load_jsonl(lib.DATA_DIR / "account_intelligence" / "account_packs.jsonl")
    discovery = load_jsonl(lib.DATA_DIR / "contacts" / "contact_discovery.jsonl")
    proposals = load_jsonl(lib.DATA_DIR / "proposals" / "mini_proposals.jsonl")
    cash = load_jsonl(lib.DATA_DIR / "finance" / "cash_priority_scores.jsonl")
    cash_by_id = {c["pack_id"]: c for c in cash}

    # scoring + emit data file
    scoring = build_scoring(packs)
    write_jsonl(lib.DATA_DIR / "account_intelligence" / "account_scoring.jsonl", scoring)
    score_by_id = {s["pack_id"]: s for s in scoring}

    eligible = [p for p in packs if score_by_id[p["pack_id"]]["eligible_for_top100"]]
    eligible_sorted = sorted(eligible, key=lambda p: p["account_score"], reverse=True)
    top100 = eligible_sorted[:100]

    # buckets
    buckets = Counter(score_by_id[p["pack_id"]]["bucket"] for p in packs)
    by_system = Counter(p["recommended_system"] for p in packs)
    by_sector = Counter(p["sector"] for p in packs)
    by_city = Counter(p["city"] for p in packs)

    # contacts
    disc_status = Counter(d["discovery_status"] for d in discovery)
    missing = [d for d in discovery if d["discovery_status"] == "missing"]
    partial = [d for d in discovery if d["discovery_status"] == "partial"]

    # outreach candidates
    reachable = [p for p in eligible_sorted
                 if p["contact_confidence"] != "C0" and not p["do_not_contact"]]
    send_candidates = reachable[:20]
    call_candidates = eligible_sorted[:30]

    # proposals
    approval_queue = [pr for pr in proposals if pr["status"] == "approval_queue"]
    approval_queue_sorted = sorted(
        approval_queue, key=lambda pr: score_by_id[pr["pack_id"]]["account_score"], reverse=True)

    # finance
    cash_sorted = sorted(cash, key=lambda c: c["cash_priority_score"], reverse=True)
    top_cash = cash_sorted[:30]
    pipeline_value_top100 = sum(
        cash_by_id[p["pack_id"]]["expected_starter_price_sar"] for p in top100)
    cash_by_system: dict[str, int] = {}
    for c in cash:
        cash_by_system[c["recommended_system"]] = (
            cash_by_system.get(c["recommended_system"], 0) + c["expected_starter_price_sar"])

    # quality review checks
    q = run_quality_checks(packs, proposals)

    # ---- best-of signals for founder command -------------------------------
    best_system = max(by_system_score(top100).items(), key=lambda kv: kv[1], default=("—", 0))
    best_sector = max(by_sector_score(top100).items(), key=lambda kv: kv[1], default=("—", 0))
    best_city = max(by_city_score(top100).items(), key=lambda kv: kv[1], default=("—", 0))

    # ===================================================================== #
    # 1. Nightly 400 report
    # ===================================================================== #
    md = [f"# Nightly 400 Account Packs — Report", f"*Run date: {today}*", "",
          "هذا التقرير يلخّص مخرج المصنع الليلي: 400 Account Intelligence Pack، كل Pack فرصة تجارية كاملة (شركة → تواصل → نظام → إيميل → اتصال → عرض مصغر → تسليم → قيمة → قرار).", "",
          "---", "", "## 1. الإجمالي", "",
          f"- إجمالي الباقات: **{len(packs)}**",
          f"- مؤهلة لـTop 100 (بدون استبعاد): **{len(eligible)}**",
          f"- مستبعدة (suppression / مخاطرة عالية / دليل ناقص / ادعاء مضمون): **{len(packs) - len(eligible)}**", "",
          "## 2. التوزيع حسب النظام (التوزيع الليلي المستهدف)", "",
          "| النظام | عدد الباقات |", "|--------|------------:|"]
    target = {n: lib.SYSTEMS[n]["nightly_count"] for n in lib.SYSTEM_NAMES}
    for name in lib.SYSTEM_NAMES:
        md.append(f"| {name} | {by_system.get(name,0)} (هدف {target[name]}) |")
    md += ["", "## 3. التوزيع حسب الـBucket", "",
           "| Bucket | المعنى | العدد |", "|--------|--------|------:|",
           f"| top_priority (85+) | أولوية قصوى | {buckets.get('top_priority',0)} |",
           f"| approval_queue (75–84) | طابور الاعتماد | {buckets.get('approval_queue',0)} |",
           f"| more_research (65–74) | بحث/إعادة صياغة | {buckets.get('more_research',0)} |",
           f"| reject_nurture (<65) | رفض/تنمية | {buckets.get('reject_nurture',0)} |", "",
           "## 4. التوزيع حسب القطاع", "", "| القطاع | العدد |", "|--------|------:|"]
    for sector, n in by_sector.most_common():
        md.append(f"| {sector} | {n} |")
    md += ["", "## 5. أعلى المدن", "", "| المدينة | العدد |", "|---------|------:|"]
    for city, n in by_city.most_common(8):
        md.append(f"| {city} | {n} |")
    md += ["", "## 6. التواصل", "",
           f"- جهات اتصال موجودة/جزئية (قناة عامة): **{disc_status.get('found',0)+disc_status.get('partial',0)}**",
           f"- بدون جهة اتصال عامة (تحويل لاستهداف بالدور): **{disc_status.get('missing',0)}**", "",
           "> ملاحظة أمانة: هذه بيانات seed تركيبية. لم نخترع أي هاتف أو إيميل؛ الباقات بدون قناة عامة تنتقل تلقائيًا إلى role-based outreach وإلى طابور اكتشاف التواصل.", "",
           "---", f"*Generated: {today} | Source: data/account_intelligence/account_packs.jsonl*", ""]
    write(lib.REPORTS_DIR / "account_intelligence" / "NIGHTLY_400_ACCOUNT_PACKS_REPORT.md", "\n".join(md))

    # ===================================================================== #
    # 2. Top 100 queue
    # ===================================================================== #
    md = [f"# Top 100 Account Queue", f"*Run date: {today}*", "",
          "أفضل 100 فرصة من أصل 400، مرتّبة حسب Account Score (من 100). الترتيب:",
          "Pain clarity 25 · Contact availability 20 · System fit 20 · Ability-to-pay 15 · Evidence 10 · Low risk 10.", "",
          "قواعد الاستبعاد المطبقة قبل الترتيب: لا نظام موصى به · لا مسار تواصل · مخاطرة عالية · دليل ناقص · suppression/do-not-contact · ادعاء مضمون في الإيميل · ألم مكتوب كحقيقة بلا دليل.", "",
          "| # | Pack | الشركة | القطاع | المدينة | النظام | Score | Bucket | Evidence | Contact | Cash |",
          "|--:|------|--------|--------|---------|--------|------:|--------|:-------:|:-------:|----:|"]
    for i, p in enumerate(top100, 1):
        s = score_by_id[p["pack_id"]]
        md.append(
            f"| {i} | {p['pack_id']} | {p['company_name']} | {p['sector']} | {p['city']} | "
            f"{p['recommended_system']} | {p['account_score']} | {s['bucket']} | "
            f"{p['evidence_level']} | {p['contact_confidence']} | {cash_by_id[p['pack_id']]['cash_priority_score']} |")
    md += ["", "---", f"*Total eligible: {len(eligible)} · shown: {len(top100)} · Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "account_intelligence" / "TOP_100_ACCOUNT_QUEUE.md", "\n".join(md))

    # ===================================================================== #
    # 3. Quality review
    # ===================================================================== #
    md = [f"# Account Pack Quality Review", f"*Run date: {today}*", "",
          "فحص جودة آلي على كل الباقات. يتأكد أن كل Pack يحترم بوابات الجودة والأمن والخصوصية.", "",
          "| الفحص | النتيجة | تفاصيل |", "|-------|:-------:|--------|"]
    for name, ok, detail in q["rows"]:
        md.append(f"| {name} | {'✅ PASS' if ok else '❌ FAIL'} | {detail} |")
    overall = "✅ كل الفحوص نجحت" if q["all_pass"] else "❌ توجد فحوص فاشلة"
    md += ["", f"**الحالة العامة: {overall}** ({q['passed']}/{q['total']} فحص).", "",
           "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "account_intelligence" / "ACCOUNT_PACK_QUALITY_REVIEW.md", "\n".join(md))

    # ===================================================================== #
    # 4. Daily contact discovery
    # ===================================================================== #
    chan = Counter(d["best_contact_route"] for d in discovery)
    md = [f"# Daily Contact Discovery Report", f"*Run date: {today}*", "",
          "اكتشاف التواصل يعتمد **فقط** على مصادر عامة وبيانات يزودنا بها المؤسس. لا قوائم مشتراة، لا قواعد مسربة، ولا اختراع أسماء/أرقام/إيميلات.", "",
          "## 1. حالة الاكتشاف", "", "| الحالة | العدد |", "|--------|------:|",
          f"| found (قناة رسمية) | {disc_status.get('found',0)} |",
          f"| partial (قناة عامة غير مؤكدة) | {disc_status.get('partial',0)} |",
          f"| missing (لا قناة عامة) | {disc_status.get('missing',0)} |", "",
          "## 2. المسار المختار للتواصل", "", "| المسار | العدد |", "|--------|------:|"]
    for route, n in chan.most_common():
        md.append(f"| {route} | {n} |")
    md += ["", "## 3. مستوى الثقة", "", "| Confidence | العدد |", "|-----------|------:|"]
    cc = Counter(d["contact_confidence"] for d in discovery)
    for level in lib.CONTACT_LEVELS:
        if cc.get(level):
            md.append(f"| {level} | {cc[level]} |")
    md += ["", "> كل القنوات في بيانات الـseed غير مؤكدة (verified=false) وقيمتها null؛ يلزم تحقق بشري قبل أي إرسال.", "",
           "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "contacts" / "DAILY_CONTACT_DISCOVERY_REPORT.md", "\n".join(md))

    # ===================================================================== #
    # 5. Missing contacts review
    # ===================================================================== #
    md = [f"# Missing Contacts Review", f"*Run date: {today}*", "",
          f"الباقات التي لا تملك قناة تواصل عامة ({len(missing)}). هذه ليست مرفوضة — تنتقل إلى استهداف بالدور (role-based) وإلى اكتشاف تواصل بشري. لا يُطلب أبدًا اختراع جهة اتصال.", "",
          "| Pack | الشركة | القطاع | المدينة | الدور المستهدف | المسار البديل |",
          "|------|--------|--------|---------|----------------|----------------|"]
    for d in missing[:120]:
        md.append(f"| {d['pack_id']} | {d['company_name']} | {d['sector']} | {d['city']} | "
                  f"{d['likely_decision_maker_role']} | {d['best_contact_route']} |")
    md += ["", f"*عرض {min(len(missing),120)} من {len(missing)}.*", "",
           "## التوصية", "",
           "1. اكتشاف القناة الرسمية (موقع/صفحة تواصل/سجل عام) قبل أي محاولة إرسال.",
           "2. حتى ذلك الحين: استهداف بالدور عبر قناة عامة واحدة فقط.",
           "3. أي جهة اتصال جديدة تُسجّل بمصدرها ومستوى ثقتها (C0→C4).", "",
           "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "contacts" / "MISSING_CONTACTS_REVIEW.md", "\n".join(md))

    # ===================================================================== #
    # 6. Mini proposal queue
    # ===================================================================== #
    ready = sorted(proposals, key=lambda pr: score_by_id[pr["pack_id"]]["account_score"], reverse=True)
    md = [f"# Mini Proposal Queue", f"*Run date: {today}*", "",
          f"إجمالي العروض المصغرة الجاهزة كمسودات: **{len(proposals)}**. كل عرض يبقى مسودة حتى اعتماد المؤسس (approval_required=true) ولا يحتوي أي ادعاء مضمون.", "",
          "| Proposal | الشركة | النظام | Sprint | السعر (ريال) | Timeline | الحالة |",
          "|----------|--------|--------|--------|------------:|----------|--------|"]
    for pr in ready[:60]:
        md.append(f"| {pr['proposal_id']} | {pr['company_name']} | {pr['recommended_system']} | "
                  f"{pr['first_sprint']} | {fmt_int(pr['starter_price_sar'])} | {pr['timeline']} | {pr['status']} |")
    md += ["", f"*عرض أعلى 60 من {len(proposals)}.*", "", "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "proposals" / "MINI_PROPOSAL_QUEUE.md", "\n".join(md))

    # ===================================================================== #
    # 7. Proposal approval queue
    # ===================================================================== #
    md = [f"# Proposal Approval Queue", f"*Run date: {today}*", "",
          f"العروض المرشّحة للاعتماد الآن (أعلى الفرص): **{len(approval_queue_sorted)}**. لا يُرسل أي عرض قبل اعتماد المؤسس.", "",
          "| Proposal | الشركة | النظام | السعر (ريال) | Account Score | يحتاج اعتماد؟ |",
          "|----------|--------|--------|------------:|--------------:|:-------------:|"]
    for pr in approval_queue_sorted[:40]:
        sc = score_by_id[pr["pack_id"]]["account_score"]
        md.append(f"| {pr['proposal_id']} | {pr['company_name']} | {pr['recommended_system']} | "
                  f"{fmt_int(pr['starter_price_sar'])} | {sc} | نعم |")
    md += ["", f"*عرض أعلى {min(len(approval_queue_sorted),40)} من {len(approval_queue_sorted)}.*", "",
           "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "proposals" / "PROPOSAL_APPROVAL_QUEUE.md", "\n".join(md))

    # ===================================================================== #
    # 8. Daily revenue opportunity (finance)
    # ===================================================================== #
    md = [f"# Daily Revenue Opportunity Report", f"*Run date: {today}*", "",
          "عدسة مالية على فرص اليوم: قيمة الفرصة، أولوية الكاش، وأي الأنظمة أسرع تحويلًا للكاش.", "",
          "## 1. قيمة خط الأنابيب (Top 100)", "",
          f"- مجموع الأسعار الافتتاحية المحتملة لـTop 100: **{fmt_int(pipeline_value_top100)} ريال**",
          f"- متوسط السعر الافتتاحي: **{fmt_int(pipeline_value_top100 // max(len(top100),1))} ريال**", "",
          "## 2. قيمة الفرص حسب النظام (كل 400)", "",
          "| النظام | عدد | إجمالي الأسعار الافتتاحية (ريال) |", "|--------|----:|-------------------------------:|"]
    for name in lib.SYSTEM_NAMES:
        md.append(f"| {name} | {by_system.get(name,0)} | {fmt_int(cash_by_system.get(name,0))} |")
    md += ["", "## 3. أعلى 30 فرصة بأولوية الكاش", "",
           "Cash Priority: Ability-to-pay 25 · Urgency 25 · Ease-of-delivery 20 · Upsell 15 · Contact 15.", "",
           "| Pack | الشركة | النظام | السعر | Complexity | Cash Score |",
           "|------|--------|--------|------:|:----------:|----------:|"]
    for c in top_cash:
        md.append(f"| {c['pack_id']} | {c['company_name']} | {c['recommended_system']} | "
                  f"{fmt_int(c['expected_starter_price_sar'])} | {c['delivery_complexity']} | {c['cash_priority_score']} |")
    md += ["", "## 4. ملاحظة الأنظمة الأسرع للكاش", "",
           "الأنظمة الأقل اعتمادًا على تكاملات خارجية والأسرع تسليمًا (هامش أعلى أولًا): "
           "**Proposal & Proof OS**، **Follow-up Recovery OS**، **Executive Command OS**.", "",
           "---", f"*Generated: {today}*", ""]
    write(lib.REPORTS_DIR / "finance" / "DAILY_REVENUE_OPPORTUNITY_REPORT.md", "\n".join(md))

    # ===================================================================== #
    # 9. Founder Daily Super Command
    # ===================================================================== #
    won = [p for p in packs if p["status"] == "won"]
    critical_decision = (
        "أكبر فجوة اليوم: "
        f"{disc_status.get('missing',0)} فرصة بدون قناة تواصل عامة. القرار: هل نخصّص الصباح "
        "لاكتشاف تواصل لأعلى 20 فرصة، أم نبدأ بالإرسال على الفرص القابلة للوصول حالًا؟ "
        "التوصية: ابدأ بأعلى 20 قابلة للوصول، وبالتوازي اكتشف تواصل أعلى 20 غير قابلة."
    )
    md = [f"# Dealix — Founder Daily Super Command", f"*Date: {today}*", "",
          "لوحة القرار اليومية للمؤسس. كل قسم يعطي قرارًا أو إجراءً واضحًا، لا مجرد أرقام.", "",
          "---", "", "## 1. القرار الحرج اليوم", "", f"> {critical_decision}", "",
          "## 2. حالة الـ400 Account Pack", "",
          f"- مُنتَج الليلة: **{len(packs)}** Pack",
          f"- مؤهلة للأولوية: **{len(eligible)}** · مستبعدة: **{len(packs)-len(eligible)}**",
          f"- top_priority: {buckets.get('top_priority',0)} · approval_queue: {buckets.get('approval_queue',0)} · "
          f"more_research: {buckets.get('more_research',0)} · nurture: {buckets.get('reject_nurture',0)}", "",
          "## 3. جهات الاتصال", "",
          f"- موجودة/جزئية: **{disc_status.get('found',0)+disc_status.get('partial',0)}**",
          f"- ناقصة (role-based + اكتشاف): **{disc_status.get('missing',0)}**", "",
          "## 4. Top 100 Accounts", "",
          f"- جاهزة في `reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md`",
          f"- أعلى فرصة: **{top100[0]['company_name']}** ({top100[0]['recommended_system']}, score {top100[0]['account_score']})" if top100 else "- لا توجد فرص مؤهلة.", "",
          "## 5. Top 20 Send Candidates (قابلة للوصول الآن)", "",
          "| # | الشركة | النظام | المسار | Score |", "|--:|--------|--------|--------|------:|"]
    for i, p in enumerate(send_candidates, 1):
        md.append(f"| {i} | {p['company_name']} | {p['recommended_system']} | {p['best_contact_route']} | {p['account_score']} |")
    if not send_candidates:
        md.append("| — | لا توجد فرص قابلة للوصول حالًا — ابدأ باكتشاف التواصل | — | — | — |")
    md += ["", "## 6. Top 30 Call Candidates", "",
           "أعلى 30 فرصة للاتصال (الهاتف يحتاج اكتشافًا عامًا قبل الاتصال — لا أرقام مخترعة).", "",
           "| # | الشركة | النظام | Score | هاتف |", "|--:|--------|--------|------:|------|"]
    for i, p in enumerate(call_candidates, 1):
        md.append(f"| {i} | {p['company_name']} | {p['recommended_system']} | {p['account_score']} | يحتاج اكتشاف |")
    md += ["", "## 7. Mini Proposals جاهزة", "",
           f"- إجمالي: **{len(proposals)}** (كلها مسودات بانتظار الاعتماد)",
           f"- في طابور الاعتماد الآن: **{len(approval_queue_sorted)}**", "",
           "## 8. اعتمادات العروض المطلوبة", "",
           f"- تحتاج قرار المؤسس: **{len(approval_queue_sorted)}** عرض (انظر PROPOSAL_APPROVAL_QUEUE).", "",
           "## 9. خطوط التسليم (Delivery Pipelines)", "",
           f"- صفقات won نشطة: **{len(won)}**",
           "- أتمتة التسليم جاهزة وتنطلق عند `won`: workspace + required inputs + tasks + first output + acceptance gate + weekly value report + renewal trigger.", "",
           "## 10. عوائق التسليم", "",
           "- لا عوائق تسليم نشطة (لا صفقات won بعد). البوابة تمنع بدء التسليم بدون: نظام مختار، نطاق، مدخلات، مقياس نجاح، معايير قبول، مالك.", "",
           "## 11. عملاء الموقع (Website Leads)", "",
           "- 0 (الموقع لم يُنشر بعد لالتقاط العملاء — انظر `docs/site/WEBSITE_MAX_STRUCTURE_AR.md`).", "",
           "## 12. أفضل نظام اليوم", "", f"- **{best_system[0]}** (أعلى وزن في Top 100).", "",
           "## 13. أفضل قطاع", "", f"- **{best_sector[0]}**.", "",
           "## 14. أفضل مدينة", "", f"- **{best_city[0]}**.", "",
           "## 15. فرصة الكاش", "",
           f"- قيمة Top 100 المحتملة: **{fmt_int(pipeline_value_top100)} ريال**.",
           f"- أعلى فرصة كاش: **{top_cash[0]['company_name']}** (score {top_cash[0]['cash_priority_score']}, {top_cash[0]['recommended_system']})." if top_cash else "", "",
           "## 16. أكبر خطر", "",
           f"- نقص قنوات التواصل العامة ({disc_status.get('missing',0)} فرصة): الخطر هو محاولة الإرسال بدون قناة موثوقة. الضابط: اكتشاف تواصل أولًا + استهداف بالدور، وعدم اختراع أي بيانات.", "",
           "## 17. خطة الغد", "",
           "1. اعتمد أعلى 20 إيميل قابل للإرسال (بعد مراجعة بشرية).",
           "2. اكتشف تواصلًا عامًا لأعلى 20 فرصة ناقصة.",
           "3. راجع واعتمد أعلى 10 Mini Proposals.",
           "4. جهّز بوابة التسليم لأول صفقة متوقعة.",
           "5. أعد تشغيل المصنع الليلي لـ400 Pack جديدة.", "",
           "---", f"*Generated: {today} | Next run: {tomorrow} 09:00 | Source: data/account_intelligence/*", ""]
    write(lib.REPORTS_DIR / "founder" / "DAILY_SUPER_COMMAND.md", "\n".join(md))

    print(f"✅ Reports generated for {today}")
    print(f"   Top 100 size: {len(top100)} (eligible {len(eligible)} / {len(packs)})")
    print(f"   Missing contacts: {len(missing)} · Partial: {len(partial)}")
    print(f"   Mini proposals: {len(proposals)} · Approval queue: {len(approval_queue_sorted)}")
    print(f"   Quality checks: {q['passed']}/{q['total']} passed")
    print(f"   Pipeline value (Top 100): {fmt_int(pipeline_value_top100)} SAR")


def by_system_score(packs: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for p in packs:
        out[p["recommended_system"]] = out.get(p["recommended_system"], 0) + p["account_score"]
    return out


def by_sector_score(packs: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for p in packs:
        out[p["sector"]] = out.get(p["sector"], 0) + p["account_score"]
    return out


def by_city_score(packs: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for p in packs:
        out[p["city"]] = out.get(p["city"], 0) + p["account_score"]
    return out


def run_quality_checks(packs: list[dict], proposals: list[dict]) -> dict:
    rows = []

    def add(name, ok, detail):
        rows.append((name, ok, detail))

    n = len(packs)
    # every pack has a recommended system
    miss_sys = [p for p in packs if not p.get("recommended_system")]
    add("كل Pack له recommended_system", len(miss_sys) == 0, f"{n-len(miss_sys)}/{n}")

    # recommended_system maps to a contact role
    bad_role = [p for p in packs if not p.get("likely_decision_maker_role")]
    add("النظام يربط بدور تواصل", len(bad_role) == 0, f"{n-len(bad_role)}/{n}")

    # missing contacts handled gracefully
    bad_missing = [p for p in packs if p.get("missing_contact") and not p.get("best_contact_route")]
    add("جهات الاتصال الناقصة تُعالَج بمسار بديل", len(bad_missing) == 0,
        f"{sum(1 for p in packs if p.get('missing_contact'))} ناقصة، كلها لها مسار")

    # no invented contacts required
    invented = [p for p in packs if p.get("phone_if_public") or p.get("email_if_public")]
    add("لا جهات اتصال مخترعة في الـseed", len(invented) == 0, f"{len(invented)} قيم هاتف/إيميل")

    # L0/L1 use hedging language in pain + email
    bad_hedge = [p for p in packs if p["evidence_level"] in ("L0", "L1")
                 and not (lib._hedge_ok(p["likely_pain"]) and lib._hedge_ok(p["email_body"]))]
    add("L0/L1 تستخدم لغة احتمالية (غالبًا/قد/likely)", len(bad_hedge) == 0,
        f"{len(bad_hedge)} مخالفة من {sum(1 for p in packs if p['evidence_level'] in ('L0','L1'))}")

    # no guaranteed claims in emails
    bad_claim = [p for p in packs if lib.has_guaranteed_claim(p["email_body"])
                 or lib.has_guaranteed_claim(p["email_subject"])]
    add("لا ادعاءات مضمونة في الإيميلات", len(bad_claim) == 0, f"{len(bad_claim)} مخالفة")

    # email gate: one system, exactly 3 deliverable bullets, single CTA
    bad_email = []
    for p in packs:
        body = p["email_body"]
        sys_mentions = sum(1 for s in lib.SYSTEM_NAMES if s in body)
        cta = body.count("Mini Proposal")
        if sys_mentions != 1 or cta != 1 or p["company_name"] not in body:
            bad_email.append(p)
    add("بوابة الإيميل: نظام واحد + سياق الشركة + CTA واحد", len(bad_email) == 0, f"{len(bad_email)} مخالفة")

    # mini proposal has starter price + approval_required + 3 deliverables, no claim
    bad_prop = [pr for pr in proposals if not pr.get("starter_price_sar")
                or pr.get("approval_required") is not True
                or len(pr.get("deliverables", [])) < 3
                or lib.has_guaranteed_claim(" ".join(pr.get("deliverables", [])) + pr.get("why_this_system", ""))]
    add("Mini Proposal: سعر + approval + 3 مخرجات + بلا ادعاء", len(bad_prop) == 0, f"{len(bad_prop)} مخالفة")

    # no prompt-injection markers leaked into any pack text
    inj = [p for p in packs if lib.has_injection_marker(p["email_body"] + p["buying_signal"] + p["company_name"])]
    add("لا علامات حقن أوامر في نصوص الباقات", len(inj) == 0, f"{len(inj)} مخالفة")

    passed = sum(1 for _, ok, _ in rows if ok)
    return {"rows": rows, "passed": passed, "total": len(rows),
            "all_pass": passed == len(rows)}


if __name__ == "__main__":
    main()
