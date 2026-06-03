#!/usr/bin/env python3
"""
Dealix Business Need Intelligence — Report Generator
Generates data-driven reports from the YAML source of truth so the reports
are never hand-faked:
  - reports/business_need_intelligence/TOP_NEEDS_BY_SECTOR.md
  - reports/business_need_intelligence/NEED_TO_SYSTEM_ROUTING_REVIEW.md
"""

from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent
DATA = BASE / "data" / "business_need_intelligence"
OUT = BASE / "reports" / "business_need_intelligence"

CORE_NAMES = {
    "revenue_os": "Revenue Operating System",
    "executive_command_os": "Executive Command OS",
    "followup_recovery_os": "Follow-up Recovery OS",
    "whatsapp_client_os": "WhatsApp Client OS",
    "proposal_proof_os": "Proposal & Proof OS",
}


def load(name: str):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gen_top_needs(sectors_doc, router) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    need_names = {n["id"]: n.get("name_ar", n["id"]) for n in router["needs"]}
    sectors = sectors_doc["sectors"]

    # Frequency of each need across sectors' top needs
    counter: Counter = Counter()
    for s in sectors:
        counter.update(s.get("top_needs", []))

    lines = [
        "# أعلى الاحتياجات حسب القطاع — Top Needs by Sector",
        f"*مولّد آليًا: {today} — المصدر: data/business_need_intelligence/*",
        "",
        "> تقرير مولّد من `scripts/business_need_report.py`. لا تحرير يدوي.",
        "",
        "## 1. أكثر الاحتياجات تكرارًا عبر القطاعات",
        "",
        "| الاحتياج | عدد القطاعات | النظام العام الأساسي |",
        "|----------|-------------:|----------------------|",
    ]
    primary = {n["id"]: n["primary_core_system"] for n in router["needs"]}
    for need, count in counter.most_common():
        lines.append(
            f"| {need} ({need_names.get(need, '')}) | {count} | "
            f"{CORE_NAMES.get(primary.get(need, ''), primary.get(need, ''))} |"
        )

    lines += ["", "## 2. أقوى احتياج + أول Sprint لكل قطاع", "",
              "| القطاع | أقوى الاحتياجات | النظام الأساسي | أول Sprint |",
              "|--------|------------------|----------------|------------|"]
    for s in sectors:
        top = "، ".join(s.get("top_needs", [])[:3])
        lines.append(
            f"| {s.get('name_ar')} | {top} | "
            f"{CORE_NAMES.get(s.get('primary_system'), s.get('primary_system'))} | "
            f"{s.get('first_sprint')} |"
        )
    lines.append("")
    return "\n".join(lines)


def gen_routing_review(router, sprints_doc) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# مراجعة توجيه الاحتياج → النظام — Routing Review",
        f"*مولّد آليًا: {today} — المصدر: data/business_need_intelligence/*",
        "",
        "> تقرير مولّد من `scripts/business_need_report.py`. لا تحرير يدوي.",
        "",
        "## 1. توزيع الأنظمة المتخصصة على الأنظمة العامة",
        "",
        "| النظام العام | عدد الأنظمة المتخصصة | عدد السبرنتات |",
        "|--------------|---------------------:|--------------:|",
    ]
    spec_counter: Counter = Counter(
        s["core_system"] for s in router.get("specialized_systems", [])
    )
    sprint_counter: Counter = Counter(
        sp["core_system"] for sp in sprints_doc.get("sprints", [])
    )
    for core, name in CORE_NAMES.items():
        lines.append(f"| {name} | {spec_counter.get(core, 0)} | {sprint_counter.get(core, 0)} |")

    lines += ["", "## 2. الاحتياجات الـ 15 وتوجيهها", "",
              "| الاحتياج | أساسي | ثانوي | النظام المتخصص |",
              "|----------|-------|-------|----------------|"]
    for n in router["needs"]:
        sec = "، ".join(n.get("secondary_core_systems", []) or ["—"])
        lines.append(
            f"| {n['id']} | {n['primary_core_system']} | {sec} | {n.get('specialized_system', '')} |"
        )

    # Coverage summary
    lines += ["", "## 3. ملخص التغطية", ""]
    lines.append(f"- الاحتياجات: {len(router['needs'])} / 15")
    lines.append(f"- الأنظمة المتخصصة: {len(router.get('specialized_systems', []))}")
    lines.append(f"- السبرنتات: {len(sprints_doc.get('sprints', []))}")
    lines.append(f"- الأنظمة العامة المستخدمة في السبرنتات: "
                 f"{len(set(sprint_counter))} / 5")
    lines.append("")
    return "\n".join(lines)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    router = load("need_to_system_router.yaml")
    sectors_doc = load("sector_need_map.yaml")
    sprints_doc = load("specialized_sprint_library.yaml")

    (OUT / "TOP_NEEDS_BY_SECTOR.md").write_text(
        gen_top_needs(sectors_doc, router), encoding="utf-8")
    (OUT / "NEED_TO_SYSTEM_ROUTING_REVIEW.md").write_text(
        gen_routing_review(router, sprints_doc), encoding="utf-8")
    print("Generated:")
    print("  reports/business_need_intelligence/TOP_NEEDS_BY_SECTOR.md")
    print("  reports/business_need_intelligence/NEED_TO_SYSTEM_ROUTING_REVIEW.md")


if __name__ == "__main__":
    main()
