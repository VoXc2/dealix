"""Emit data-derived reference docs and domain reports (kept in sync with seeds)."""
from __future__ import annotations

import datetime as dt
import sys

from . import seeds
from .lib import ROOT, load_jsonl, write_text
from .generate_account_packs import dict_core


def _today():
    return dt.date.today().isoformat()


def build_catalog_doc():
    lines = ["# كتالوج أنظمة الأعمال الداخلية (40 نظام)", "",
             "> داخلي فقط — لا يُعرض كقائمة للعميل. العميل يرى 5 أنظمة جوهرية + حلول قطاعه.",
             "", f"تاريخ التوليد: {_today()}", ""]
    specialized = list(seeds.iter_specialized_systems())
    for core in seeds.CORE_SYSTEMS:
        lines.append(f"## {core['name_ar']} ({core['id']})")
        lines.append("")
        lines.append("| النظام الداخلي | المعرّف | التعقيد | السعر المبدئي |")
        lines.append("| --- | --- | --- | ---: |")
        for s in specialized:
            if s["core_system"] == core["id"]:
                lines.append(f"| {s['name_ar']} | `{s['id']}` | {s['complexity']} | {s['starter_price_sar']} ر.س |")
        lines.append("")
    write_text("docs/business_os_catalog/BUSINESS_OS_CATALOG_AR.md", "\n".join(lines) + "\n")


def build_need_taxonomy_doc():
    lines = ["# تصنيف الاحتياجات (25 احتياج)", "",
             "كل احتياج يُوجَّه إلى نظام جوهري واحد ودور شرائي.", "",
             f"تاريخ التوليد: {_today()}", "",
             "| المعرّف | الاحتياج | الفئة | النظام الجوهري | الدور الشرائي |",
             "| --- | --- | --- | --- | --- |"]
    for nid, name_ar, category, core, buyer in seeds.NEEDS:
        lines.append(f"| `{nid}` | {name_ar} | {category} | {dict_core(core)} | {buyer} |")
    write_text("docs/business_need_intelligence/NEED_TAXONOMY_25_AR.md", "\n".join(lines) + "\n")


def build_reports():
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl") if (ROOT / "data/account_intelligence/account_packs.jsonl").exists() else []
    active = [p for p in packs if not p.get("suppressed")]

    # Nightly 400 packs report
    by_sector = {}
    for p in active:
        by_sector[p["sector"]] = by_sector.get(p["sector"], 0) + 1
    lines = ["# تقرير حزم الحسابات الليلية (400/يوم)", "", f"تاريخ: {_today()}", "",
             f"إجمالي الحزم: **{len(packs)}** | نشطة: **{len(active)}** | موقوفة: **{len(packs) - len(active)}**", "",
             "## التوزيع حسب القطاع", "", "| القطاع | عدد |", "| --- | ---: |"]
    for sec, n in sorted(by_sector.items(), key=lambda x: -x[1]):
        lines.append(f"| {dict(seeds.SECTORS).get(sec, sec)} | {n} |")
    write_text("reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md", "\n".join(lines) + "\n")

    # Top 100 account queue
    top = active[:100]
    lines = ["# طابور أفضل 100 حساب", "", f"تاريخ: {_today()}", "",
             "| # | الشركة | القطاع | الاحتياج | النظام | السكور النهائي |",
             "| ---: | --- | --- | --- | --- | ---: |"]
    for i, p in enumerate(top, 1):
        lines.append(f"| {i} | {p['company_name']} | {p['sector']} | {p['primary_need']} | {p['recommended_core_system']} | {p['final_account_score']} |")
    write_text("reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md", "\n".join(lines) + "\n")

    # Outreach approval queue
    queue = load_jsonl("data/outreach/top_100_approval_queue.jsonl") if (ROOT / "data/outreach/top_100_approval_queue.jsonl").exists() else []
    lines = ["# طابور اعتماد أفضل 100 بريد", "",
             "> كل بريد هنا مسودة تحتاج اعتماد المؤسس قبل الإرسال. لا إرسال آلي.", "",
             f"تاريخ: {_today()} | العدد: **{len(queue)}**", "",
             "| الشركة | الدور | الموضوع |", "| --- | --- | --- |"]
    for d in queue[:100]:
        lines.append(f"| {d['company_name']} | {d['to_role']} | {d['subject']} |")
    write_text("reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md", "\n".join(lines) + "\n")

    # Delivery status
    pipelines = load_jsonl("data/delivery/pipelines.jsonl") if (ROOT / "data/delivery/pipelines.jsonl").exists() else []
    lines = ["# حالة خط التسليم", "", f"تاريخ: {_today()}", "",
             "| العميل | النظام | المرحلة | المدخلات مستلمة |", "| --- | --- | --- | :---: |"]
    for p in pipelines:
        lines.append(f"| {p['client']} | {p['selected_system']} | {p['stage']} | {'نعم' if p.get('inputs_received') else 'لا'} |")
    write_text("reports/delivery/DELIVERY_PIPELINE_STATUS.md", "\n".join(lines) + "\n")

    # Daily metrics dashboard
    lines = ["# لوحة المؤشرات اليومية", "", f"تاريخ: {_today()}", "",
             "| المؤشر | القيمة |", "| --- | ---: |",
             f"| حزم حسابات | {len(packs)} |",
             f"| حسابات نشطة | {len(active)} |",
             f"| مسودات بريد | {len(load_jsonl('data/outreach/email_drafts.jsonl')) if (ROOT / 'data/outreach/email_drafts.jsonl').exists() else 0} |",
             f"| Call Briefs | {len(load_jsonl('data/acquisition/call_briefs.jsonl')) if (ROOT / 'data/acquisition/call_briefs.jsonl').exists() else 0} |",
             f"| عروض مصغّرة | {len(load_jsonl('data/proposals/mini_proposals.jsonl')) if (ROOT / 'data/proposals/mini_proposals.jsonl').exists() else 0} |",
             f"| خطوط تسليم | {len(pipelines)} |"]
    write_text("reports/metrics/DAILY_METRICS_DASHBOARD.md", "\n".join(lines) + "\n")


def build():
    build_catalog_doc()
    build_need_taxonomy_doc()
    build_reports()


def main():
    build()
    print("Data-derived docs + domain reports generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
