"""Generate delivery automation sample data: pipelines, acceptance gates,
weekly value reports, and supporting acquisition objection responses.

Delivery pipelines are only created for WON accounts. In the seed run we mark a
small deterministic subset as won so the pipeline contract is exercised. A
pipeline never advances past 'intake' until inputs_received is true.
"""
from __future__ import annotations

import argparse
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl


OBJECTIONS = [
    ("السعر مرتفع", "نبدأ بسبرنت محدد المخرجات بسعر مبدئي ثابت، فتقيس القيمة قبل أي التزام أكبر."),
    ("ليس لدينا وقت", "نطلب مدخلات محدودة جدًا، والتنفيذ علينا؛ دوركم المراجعة والاعتماد فقط."),
    ("جربنا أدوات ولم تنفع", "لا نبيع أداة، نبيع نظامًا بمخرجات ومعايير قبول واضحة وتقرير قيمة."),
    ("سنفكر لاحقًا", "نقترح تشخيصًا سريعًا بدون التزام ليكون القرار مبنيًا على أرقامكم."),
]


def build_objections(dry_run=False):
    rows = [{"objection_ar": o, "response_ar": r} for o, r in OBJECTIONS]
    if not dry_run:
        dump_jsonl("data/acquisition/objection_responses.jsonl", rows)
    return rows


def build_pipelines(dry_run=False):
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    won = [p for p in packs if not p.get("suppressed")][:5]
    pipelines, gates, reports = [], [], []
    for p in won:
        sprint = next((s for s in seeds.iter_sprints() if s["id"] == p["sector_specific_sprint"]), None)
        sprint = sprint or seeds.iter_sprints()[0]
        pipelines.append(
            {
                "client": p["company_name"],
                "selected_system": p["recommended_core_system"],
                "sprint_id": sprint["id"],
                "scope": sprint["name_ar"],
                "required_inputs": sprint["required_inputs"],
                "success_metric": f"تحسّن قابل للقياس في {seeds.need_by_id(p['primary_need'])['name_ar']}",
                "acceptance_criteria": sprint["acceptance_criteria"],
                "owner": "مدير التسليم",
                "stage": "intake",
                "inputs_received": False,
            }
        )
        gates.append(
            {
                "sprint_id": sprint["id"],
                "criteria": sprint["acceptance_criteria"],
                "owner": "مدير التسليم",
                "required_inputs": sprint["required_inputs"],
            }
        )
        reports.append(
            {
                "client": p["company_name"],
                "week_of": "2026-W23",
                "system": p["recommended_core_system"],
                "metrics": [
                    {"name": "مدخلات مستلمة", "value": "0/3", "evidence": "بانتظار العميل"},
                ],
                "next_actions": ["جمع المدخلات المطلوبة من العميل قبل بدء التنفيذ"],
            }
        )
    if not dry_run:
        dump_jsonl("data/delivery/pipelines.jsonl", pipelines)
        dump_jsonl("data/delivery/acceptance_gates.jsonl", gates)
        dump_jsonl("data/delivery/weekly_value_reports.jsonl", reports)
        dump_jsonl(
            "data/delivery/tasks.jsonl",
            [
                {"client": p["client"], "task": "intake مدخلات العميل", "status": "todo", "owner": p["owner"]}
                for p in pipelines
            ],
        )
    return pipelines


def build(dry_run=False):
    build_objections(dry_run=dry_run)
    return build_pipelines(dry_run=dry_run)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    pipelines = build(dry_run=args.dry_run)
    print(f"Generated {len(pipelines)} delivery pipelines + acceptance gates + value reports (dry_run={args.dry_run}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
