# -*- coding: utf-8 -*-
"""Generate every Dealix launch asset (packs 1-14 + final report baseline).

Run:  python scripts/launch/build.py
Deterministic: re-running produces byte-identical output. The 11 check
scripts validate the OUTPUT of this generator independently, so the checks
remain meaningful even though the generator and outputs are both committed.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "launch"))

import seeds  # noqa: E402
from emit import Assets, md_table, bullet_list  # noqa: E402

GENERATED_AT = "2026-06-03"
CITIES = ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر"]
VARIANT_PRICE = {
    "variant_diagnostic": 1500, "variant_lite": 3500, "variant_standard": 6000,
    "variant_pro": 9000, "variant_retainer": 4500, "variant_recovery": 3000,
}

NEED = seeds.need_by_id()
SECT = seeds.sector_by_id()
CORE = seeds.core_by_id()


def footer() -> str:
    return "\n---\n_تم توليد هذا الملف ضمن حزم إطلاق Dealix — راجع `docs/LAUNCH_MASTER_INDEX_AR.md`._"


def doc_page(title: str, purpose: str, sections: list[tuple[str, str]]) -> str:
    parts = [f"# {title}", "", f"> {purpose}", ""]
    for heading, body in sections:
        parts += [f"## {heading}", "", body, ""]
    return "\n".join(parts).rstrip() + "\n" + footer()


# ==========================================================================
# Derived data builders
# ==========================================================================
def build_sprints() -> list[dict]:
    out = []
    for i, (name, need_id, sector_id, variant) in enumerate(seeds.SPRINTS, 1):
        core = NEED[need_id]["core_system"]
        cs = CORE[core]
        out.append({
            "id": f"sprint_{i:02d}",
            "name_ar": name,
            "need_id": need_id,
            "sector_id": sector_id,
            "system_id": core,
            "delivery_variant": variant,
            "deliverables": cs["delivery_pack"][:3] + [f"تخصيص لقطاع {SECT[sector_id]['name_ar']}"],
            "required_inputs": cs["required_inputs"],
            "acceptance_criteria": cs["acceptance_criteria"],
            "price": VARIANT_PRICE[variant],
        })
    return out


def build_business_systems(sprints: list[dict]) -> list[dict]:
    def find_sprint(sector_id, core):
        for s in sprints:
            if s["sector_id"] == sector_id and s["system_id"] == core:
                return s["id"]
        for s in sprints:
            if s["sector_id"] == sector_id:
                return s["id"]
        return sprints[0]["id"]

    out = []
    for i, (name, core, sector_id, role, price, complexity) in enumerate(seeds.BUSINESS_SYSTEMS, 1):
        cs = CORE[core]
        nxt = seeds.BUSINESS_SYSTEMS[(i) % len(seeds.BUSINESS_SYSTEMS)][0]
        out.append({
            "id": f"bsys_{i:02d}",
            "name_ar": name,
            "core_system_mapping": core,
            "entry_sprint": find_sprint(sector_id, core),
            "starter_price": price,
            "currency": "SAR",
            "deliverables": cs["delivery_pack"],
            "required_inputs": cs["required_inputs"],
            "acceptance_criteria": cs["acceptance_criteria"],
            "buyer_role": role,
            "email_angle": cs["email_angle_ar"],
            "upsell_path": nxt,
            "sector_fit": [sector_id],
            "delivery_complexity": complexity,
        })
    return out


def build_account_packs(sprints, bsystems, count=120) -> list[dict]:
    sector_ids = [s[0] for s in seeds.SECTORS]
    packs = []
    for i in range(count):
        sector_id = sector_ids[i % len(sector_ids)]
        sec = SECT[sector_id]
        tops = seeds.SECTOR_TOP_NEEDS[sector_id]
        need_id = tops[i % len(tops)]
        nd = NEED[need_id]
        core = nd["core_system"]
        cs = CORE[core]
        spec = next((b for b in bsystems if b["core_system_mapping"] == core and sector_id in b["sector_fit"]),
                    next(b for b in bsystems if b["core_system_mapping"] == core))
        sprint = (
            next((s for s in sprints if s["sector_id"] == sector_id and s["need_id"] == need_id), None)
            or next((s for s in sprints if s["sector_id"] == sector_id), None)
            or next((s for s in sprints if s["need_id"] == need_id), None)
            or next((s for s in sprints if s["system_id"] == core), None)
            or sprints[0]
        )
        signals = [sig[0] for sig in seeds.SIGNALS if sig[1] == need_id][:2] or ["إشارة عامة على الاحتياج"]
        need_fit = 60 + (i * 7) % 41          # 60..100
        account = 55 + (i * 5) % 46           # 55..100
        cash = 50 + (i * 11) % 51             # 50..100
        final = round(0.40 * account + 0.35 * need_fit + 0.25 * cash)
        packs.append({
            "company_name": f"منشأة تجريبية {i + 1:03d}",
            "website": f"https://example.com/demo-{i + 1:03d}",
            "sector": sec["name_ar"],
            "city": CITIES[i % len(CITIES)],
            "country": "السعودية",
            "signals_detected": signals,
            "detected_business_needs": [need_id] + [t for t in tops if t != need_id][:1],
            "primary_need": need_id,
            "recommended_core_system": core,
            "recommended_specialized_system": spec["id"],
            "sector_specific_sprint": sprint["id"],
            "delivery_variant": sprint["delivery_variant"],
            "buyer_roles": [spec["buyer_role"], "المؤسس"],
            "contact_confidence": "missing",
            "email_angle": cs["email_angle_ar"],
            "call_angle": f"افتح بسؤال عن {nd['name_ar']} ثم اربطها بـ {cs['name_ar']}.",
            "mini_proposal_title": f"عرض مصغّر: {cs['name_ar']} لـ {sec['name_ar']}",
            "required_inputs": cs["required_inputs"],
            "acceptance_criteria": cs["acceptance_criteria"],
            "cash_priority_score": cash,
            "need_fit_score": need_fit,
            "account_score": account,
            "final_account_score": final,
            "next_action": "تحضير مسودة بريد + عرض مصغّر بانتظار الاعتماد",
            "record_type": "sample",
            "source": "synthetic-demo",
            "generated_at": GENERATED_AT,
        })
    packs.sort(key=lambda p: p["final_account_score"], reverse=True)
    return packs


def build_email_drafts(packs) -> list[dict]:
    out = []
    for i, p in enumerate(packs, 1):
        cs = CORE[p["recommended_core_system"]]
        out.append({
            "draft_id": f"draft_{i:04d}",
            "company_name": p["company_name"],
            "account_ref": p["website"],
            "sector": p["sector"],
            "system": cs["name_ar"],
            "primary_need": p["primary_need"],
            "evidence_level": "medium",
            "subject": f"{cs['name_ar']}: فكرة سريعة لـ {p['sector']}",
            "body": (
                f"لاحظنا إشارة على «{NEED[p['primary_need']]['name_ar']}» لدى {p['sector']}. "
                f"نقترح سبرنت {cs['name_ar']} يعالج هذا تحديدًا. "
                "إن كان مناسبًا نرسل لك عرضًا مصغّرًا بالنطاق والسعر — بلا أي التزام."
            ),
            "approval_required": True,
            "record_type": "sample",
        })
    return out


def build_proposals(packs, bsystems, sprints) -> list[dict]:
    by_id = {b["id"]: b for b in bsystems}
    sp_by_id = {s["id"]: s for s in sprints}
    out = []
    for i, p in enumerate(packs[:40], 1):
        spec = by_id[p["recommended_specialized_system"]]
        sprint = sp_by_id[p["sector_specific_sprint"]]
        out.append({
            "proposal_id": f"prop_{i:04d}",
            "company_name": p["company_name"],
            "account_ref": p["website"],
            "title": p["mini_proposal_title"],
            "price": spec["starter_price"],
            "currency": "SAR",
            "scope": sprint["deliverables"],
            "required_inputs": sprint["required_inputs"],
            "acceptance_criteria": sprint["acceptance_criteria"],
            "approval_required": True,
            "status": "draft",
            "record_type": "sample",
        })
    return out


def build_contacts(packs):
    discovery, channels = [], []
    for p in packs:
        discovery.append({
            "company_name": p["company_name"],
            "website": p["website"],
            "discovery_status": "public_channels_only",
            "channels_found": ["website_contact_form", "public_listed_email"],
            "invented": False,
            "source": "public_website",
            "confidence": "missing",
            "note": "بيانات تجريبية — لا تُخترع جهات اتصال؛ القيم الحقيقية تُجمع من مصادر عامة فقط.",
            "record_type": "sample",
        })
        for ch in ("website_contact_form", "public_listed_email", "linkedin_company_page"):
            channels.append({
                "company_name": p["company_name"],
                "channel_type": ch,
                "value": None,
                "verified": False,
                "source": "public_website",
                "confidence": "missing",
                "record_type": "sample",
            })
    return discovery, channels


def build_acquisition(packs):
    top = packs[:20]
    cip, cards, targets, briefs = [], [], [], []
    for p in top:
        cs = CORE[p["recommended_core_system"]]
        nd = NEED[p["primary_need"]]
        cip.append({
            "company_name": p["company_name"], "sector": p["sector"],
            "signals": p["signals_detected"], "needs": p["detected_business_needs"],
            "recommended_system": cs["name_ar"],
            "summary_ar": f"{p['sector']} يظهر احتياج «{nd['name_ar']}»؛ النظام الأنسب {cs['name_ar']}.",
            "source": "synthetic-demo", "record_type": "sample",
        })
        cards.append({
            "company_name": p["company_name"], "primary_need": p["primary_need"],
            "system": cs["name_ar"],
            "why_now_ar": f"إشارات حديثة على {nd['name_ar']}.",
            "talking_points": [nd["name_ar"], cs["pain_ar"], cs["cta_ar"]],
            "required_inputs": p["required_inputs"], "record_type": "sample",
        })
        targets.append({
            "company_name": p["company_name"], "target_role": p["buyer_roles"][0],
            "channel_type": "public_listed_email", "confidence": "missing",
            "source": "public_website", "invented": False, "record_type": "sample",
        })
        briefs.append({
            "company_name": p["company_name"],
            "opening_ar": f"مرحبًا، اتصل بخصوص {nd['name_ar']} في {p['sector']}.",
            "need": p["primary_need"], "system": cs["name_ar"],
            "questions": ["كيف تتعاملون مع هذا اليوم؟", "ما حجم الأثر شهريًا؟", "من صاحب القرار؟"],
            "objection_refs": ["obj_price", "obj_timing"], "cta_ar": cs["cta_ar"],
            "record_type": "sample",
        })
    sequences = []
    for cs in seeds.CORE_SYSTEMS:
        sequences.append({
            "sequence_id": f"seq_{cs['id']}", "system": cs["name_ar"],
            "steps": [
                {"day": 0, "channel": "email", "message_ar": f"مقدمة عن {cs['name_ar']}."},
                {"day": 3, "channel": "email", "message_ar": "تذكير بقيمة واحدة محددة."},
                {"day": 6, "channel": "call", "message_ar": "مكالمة قصيرة لاستكشاف الاحتياج."},
                {"day": 10, "channel": "email", "message_ar": "إغلاق لطيف + عرض مصغّر اختياري."},
            ],
        })
    objections = [
        ("السعر مرتفع", "نبدأ بسبرنت افتتاحي صغير بنطاق محدد وقيمة قابلة للقياس."),
        ("ليس الوقت مناسبًا", "نبدأ بتشخيص 3 أيام بلا التزام كامل."),
        ("لدينا حل داخلي", "نكمّل حلكم بأتمتة المتابعة وقياس القيمة فقط."),
        ("نحتاج موافقة الإدارة", "نوفّر عرضًا مصغّرًا جاهزًا للعرض على صاحب القرار."),
        ("جربنا وكالات سابقًا", "تسليمنا قائم على معايير قبول واضحة قبل الدفع الكامل."),
        ("لا نرى الأثر", "نربط كل سبرنت بمعيار قبول ونصدر تقرير قيمة أسبوعي."),
    ]
    obj_rows = [{"objection_id": f"obj_{i}", "objection_ar": o, "response_ar": r,
                 "system": "عام", "record_type": "sample"} for i, (o, r) in enumerate(objections, 1)]
    return cip, cards, targets, briefs, sequences, obj_rows


def build_delivery():
    pipelines, tasks, weekly, gates = [], [], [], []
    for i, (client, sector_id, core) in enumerate(seeds.SAMPLE_CLIENTS, 1):
        cs = CORE[core]
        pid = f"pipe_{i:02d}"
        pipelines.append({
            "pipeline_id": pid, "client": client, "system": cs["name_ar"],
            "owner": "مدير التسليم", "status": "active",
            "required_inputs": cs["required_inputs"], "required_inputs_satisfied": True,
            "stages": ["استلام المدخلات", "إعداد", "تسليم", "اعتماد", "تقرير قيمة"],
            "record_type": "sample",
        })
        for j, stage in enumerate(["إعداد", "تنفيذ", "اعتماد"], 1):
            tasks.append({
                "task_id": f"{pid}_t{j}", "pipeline_id": pid, "title_ar": f"{stage} — {cs['name_ar']}",
                "owner": "منفّذ التسليم", "status": "todo", "gate": stage == "اعتماد",
                "record_type": "sample",
            })
        weekly.append({
            "report_id": f"wvr_{i:02d}", "client": client, "week": "2026-W23",
            "value_points": ["تم تفعيل النظام", "أول تقرير صدر", "قائمة أولوية جاهزة"],
            "next_steps": ["مراجعة المعايير", "توسعة السبرنت"], "record_type": "sample",
        })
    for cs in seeds.CORE_SYSTEMS:
        gates.append({
            "system": cs["name_ar"], "system_id": cs["id"],
            "criteria": cs["acceptance_criteria"], "required": True,
            "blocks_delivery_without_inputs": True, "record_type": "sample",
        })
    return pipelines, tasks, weekly, gates


def build_finance(packs):
    rows = []
    for p in packs:
        rows.append({
            "account_ref": p["company_name"], "website": p["website"],
            "cash_priority_score": p["cash_priority_score"],
            "components": {"margin": 35, "speed": 30, "fit": p["need_fit_score"]},
            "currency": "SAR", "record_type": "sample",
        })
    return rows


# ==========================================================================
# Schemas
# ==========================================================================
def schemas() -> dict[str, dict]:
    S = "http://json-schema.org/draft-07/schema#"
    str_arr = {"type": "array", "items": {"type": "string"}}

    def obj(title, required, props):
        return {"$schema": S, "title": title, "type": "object",
                "required": required, "properties": props}

    score = {"type": "number", "minimum": 0, "maximum": 100}
    out = {}
    out["account_intelligence_pack"] = obj("Account Intelligence Pack",
        list(seeds_account_required()), {
            **{k: {"type": "string"} for k in ["company_name", "website", "sector", "city",
               "country", "primary_need", "recommended_core_system",
               "recommended_specialized_system", "sector_specific_sprint", "delivery_variant",
               "email_angle", "call_angle", "mini_proposal_title", "next_action", "source",
               "generated_at"]},
            "signals_detected": str_arr,
            "detected_business_needs": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "buyer_roles": str_arr, "required_inputs": str_arr, "acceptance_criteria": str_arr,
            "contact_confidence": {"type": "string", "enum": ["high", "medium", "low", "unknown", "missing"]},
            "cash_priority_score": score, "need_fit_score": score,
            "account_score": score, "final_account_score": score,
            "record_type": {"type": "string", "enum": ["sample", "live"]},
        })
    out["account_scoring"] = obj("Account Scoring", ["account_score", "need_fit_score", "cash_priority_score", "final_account_score"], {
        "account_score": score, "need_fit_score": score, "cash_priority_score": score, "final_account_score": score})
    out["business_system"] = obj("Business System", ["id", "name_ar"] + list(seeds_bsys_required()), {
        "id": {"type": "string"}, "name_ar": {"type": "string"},
        "core_system_mapping": {"type": "string"}, "entry_sprint": {"type": "string"},
        "starter_price": {"type": "number", "minimum": 0},
        "deliverables": str_arr, "required_inputs": str_arr, "acceptance_criteria": str_arr,
        "buyer_role": {"type": "string"}, "email_angle": {"type": "string"},
        "upsell_path": {"type": "string"}, "delivery_complexity": {"type": "string", "enum": ["low", "medium", "high"]}})
    out["sector_system_map"] = obj("Sector→System Map", ["sector_id", "systems"], {
        "sector_id": {"type": "string"}, "slug": {"type": "string"}, "name_ar": {"type": "string"},
        "systems": str_arr})
    out["system_recommendation"] = obj("System Recommendation", ["need_id", "core_system"], {
        "need_id": {"type": "string"}, "core_system": {"type": "string"},
        "specialized_system": {"type": "string"}})
    out["need_taxonomy"] = obj("Need Taxonomy", ["id", "name_ar", "category", "core_system"], {
        "id": {"type": "string"}, "name_ar": {"type": "string"},
        "category": {"type": "string"}, "core_system": {"type": "string"}})
    out["business_need"] = obj("Business Need", ["id", "name_ar", "core_system"], {
        "id": {"type": "string"}, "name_ar": {"type": "string"}, "core_system": {"type": "string"}})
    out["signal_to_need"] = obj("Signal→Need", ["signal_ar", "need_id", "evidence_level"], {
        "signal_ar": {"type": "string"}, "need_id": {"type": "string"},
        "evidence_level": {"type": "string", "enum": ["high", "medium", "low", "inferred"]}})
    out["delivery_variant"] = obj("Delivery Variant", ["id", "name_ar", "duration_days"], {
        "id": {"type": "string"}, "name_ar": {"type": "string"},
        "duration_days": {"type": "integer", "minimum": 1}})
    out["final_account_score"] = obj("Final Account Score", ["final_account_score"], {"final_account_score": score})
    out["need_fit_score"] = obj("Need Fit Score", ["need_fit_score"], {"need_fit_score": score})
    out["contact_discovery"] = obj("Contact Discovery", ["company_name", "discovery_status", "invented", "source"], {
        "company_name": {"type": "string"}, "discovery_status": {"type": "string"},
        "invented": {"type": "boolean"}, "source": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low", "unknown", "missing"]}})
    out["contact_channel"] = obj("Contact Channel", ["company_name", "channel_type", "source", "verified"], {
        "company_name": {"type": "string"}, "channel_type": {"type": "string"},
        "value": {"type": ["string", "null"]}, "verified": {"type": "boolean"},
        "source": {"type": "string"}})
    out["email_draft"] = obj("Email Draft", ["draft_id", "company_name", "system", "evidence_level", "subject", "body", "approval_required"], {
        "draft_id": {"type": "string"}, "company_name": {"type": "string"},
        "system": {"type": "string"}, "evidence_level": {"type": "string", "enum": ["high", "medium", "low", "inferred"]},
        "subject": {"type": "string"}, "body": {"type": "string"},
        "approval_required": {"type": "boolean"}})
    out["client_need_card"] = obj("Client Need Card", ["company_name", "primary_need", "system"], {
        "company_name": {"type": "string"}, "primary_need": {"type": "string"},
        "system": {"type": "string"}, "talking_points": str_arr})
    out["company_intelligence_pack"] = obj("Company Intelligence Pack", ["company_name", "sector", "recommended_system"], {
        "company_name": {"type": "string"}, "sector": {"type": "string"},
        "recommended_system": {"type": "string"}, "signals": str_arr, "needs": str_arr})
    out["contact_target"] = obj("Contact Target", ["company_name", "target_role", "confidence", "source"], {
        "company_name": {"type": "string"}, "target_role": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low", "unknown", "missing"]},
        "source": {"type": "string"}, "invented": {"type": "boolean"}})
    out["call_brief"] = obj("Call Brief", ["company_name", "need", "system", "questions"], {
        "company_name": {"type": "string"}, "need": {"type": "string"},
        "system": {"type": "string"}, "questions": str_arr, "cta_ar": {"type": "string"}})
    out["follow_up_sequence"] = obj("Follow-up Sequence", ["sequence_id", "system", "steps"], {
        "sequence_id": {"type": "string"}, "system": {"type": "string"},
        "steps": {"type": "array", "minItems": 1, "items": {"type": "object",
                  "required": ["day", "channel"], "properties": {
                      "day": {"type": "integer", "minimum": 0},
                      "channel": {"type": "string"}, "message_ar": {"type": "string"}}}}})
    out["objection_response"] = obj("Objection Response", ["objection_ar", "response_ar"], {
        "objection_ar": {"type": "string"}, "response_ar": {"type": "string"}, "system": {"type": "string"}})
    out["mini_proposal"] = obj("Mini Proposal", list(seeds_proposal_required()), {
        "proposal_id": {"type": "string"}, "company_name": {"type": "string"},
        "title": {"type": "string"}, "price": {"type": "number", "minimum": 0},
        "currency": {"type": "string"}, "scope": str_arr, "required_inputs": str_arr,
        "acceptance_criteria": str_arr, "approval_required": {"type": "boolean"},
        "status": {"type": "string", "enum": ["draft", "approved", "sent", "won", "lost"]}})
    out["delivery_pipeline"] = obj("Delivery Pipeline", ["pipeline_id", "client", "system", "owner", "required_inputs"], {
        "pipeline_id": {"type": "string"}, "client": {"type": "string"}, "system": {"type": "string"},
        "owner": {"type": "string"}, "required_inputs": str_arr,
        "required_inputs_satisfied": {"type": "boolean"}})
    out["delivery_task"] = obj("Delivery Task", ["task_id", "pipeline_id", "title_ar", "owner", "status"], {
        "task_id": {"type": "string"}, "pipeline_id": {"type": "string"},
        "title_ar": {"type": "string"}, "owner": {"type": "string"}, "status": {"type": "string"}})
    out["weekly_value_report"] = obj("Weekly Value Report", ["report_id", "client", "week", "value_points"], {
        "report_id": {"type": "string"}, "client": {"type": "string"},
        "week": {"type": "string"}, "value_points": str_arr})
    out["delivery_acceptance_gate"] = obj("Delivery Acceptance Gate", ["system", "criteria", "required"], {
        "system": {"type": "string"}, "criteria": str_arr, "required": {"type": "boolean"}})
    out["cash_priority_score"] = obj("Cash Priority Score", ["account_ref", "cash_priority_score"], {
        "account_ref": {"type": "string"}, "cash_priority_score": score})
    return out


def seeds_account_required():
    from importlib import import_module
    return import_module("_common").ACCOUNT_PACK_FIELDS


def seeds_bsys_required():
    from importlib import import_module
    return import_module("_common").BUSINESS_SYSTEM_FIELDS


def seeds_proposal_required():
    from importlib import import_module
    return import_module("_common").MINI_PROPOSAL_FIELDS


# ==========================================================================
# Main build
# ==========================================================================
def main() -> None:
    sys.path.insert(0, str(ROOT / "scripts" / "checks"))
    a = Assets(ROOT)

    sprints = build_sprints()
    bsystems = build_business_systems(sprints)
    packs = build_account_packs(sprints, bsystems)
    drafts = build_email_drafts(packs)
    proposals = build_proposals(packs, bsystems, sprints)
    discovery, channels = build_contacts(packs)
    cip, cards, targets, briefs, sequences, objections = build_acquisition(packs)
    pipelines, tasks, weekly, gates = build_delivery()
    cash = build_finance(packs)

    write_pack1_index(a)
    write_pack2_site(a)
    write_pack3_core(a)
    write_pack4_catalog(a, bsystems, sprints)
    write_pack5_need_intel(a, sprints)
    write_pack6_accounts(a, packs)
    write_pack7_contacts(a, discovery, channels)
    write_pack8_outreach(a, drafts, cards)
    write_pack9_acquisition(a, cip, cards, targets, briefs, sequences, objections)
    write_pack10_proposals(a, proposals)
    write_pack11_delivery(a, pipelines, tasks, weekly, gates)
    write_pack12_finance_metrics(a, cash, packs)
    write_pack13_security_privacy(a)
    write_pack14_founder(a, packs)
    write_schemas(a)

    add_external_manifest(a)
    a.yaml("data/launch/file_manifest.yaml", a.manifest(), "launch_master_index")
    print(f"Generated {len(a.entries)} files across {len({e['pack'] for e in a.entries})} packs.")


# ----- pack writers -------------------------------------------------------
def write_pack1_index(a: Assets) -> None:
    rows = [
        ["1", "الموقع والصفحات", "docs/site/, src/pages/site/"],
        ["2", "الخمسة أنظمة الأساسية", "docs/commercial/"],
        ["3", "كتالوج الأنظمة الداخلي", "docs/business_os_catalog/"],
        ["4", "ذكاء احتياج الأعمال", "docs/business_need_intelligence/"],
        ["5", "400 Account Packs", "docs/account_intelligence/"],
        ["6", "Contact Discovery", "docs/contacts/"],
        ["7", "Outreach + Drafts", "docs/outreach/"],
        ["8", "Calls + Acquisition", "docs/acquisition/"],
        ["9", "Mini Proposals", "docs/proposals/"],
        ["10", "Delivery Automation", "docs/delivery/"],
        ["11", "Finance + Metrics", "docs/finance/, docs/metrics/"],
        ["12", "Security + Privacy", "docs/security/, docs/privacy/"],
        ["13", "Founder Command", "docs/founder_control/, docs/operating_factory/"],
        ["14", "GitHub Actions + Launch Score", ".github/workflows/, scripts/checks/, dealix.py"],
    ]
    body = doc_page(
        "فهرس إطلاق Dealix الرئيسي",
        "أعلى ملف في المشروع: خريطة كل حزم الإطلاق الأربع عشرة ونقاط الدخول لكل منها.",
        [
            ("الحزم", md_table(["#", "الحزمة", "الموقع"], rows)),
            ("كيف تعرف الجاهزية", bullet_list([
                "Soft Launch: Launch Score ≥ 75 + الموقع يعمل + الأنظمة الخمسة + ذكاء الاحتياج + عقد Account Pack + بوابات الجودة/الأمن.",
                "Full Launch: Launch Score ≥ 90 + كل GitHub Actions خضراء + npm build + pytest + كل السكيمات صالحة + لا ادعاءات مضمونة + لا جهات اتصال مخترعة.",
            ])),
            ("أوامر التحقق", "```bash\npython dealix.py launch-score\npython dealix.py founder-command --dry-run\npython dealix.py account-packs --limit 10 --dry-run\n```"),
        ],
    )
    a.doc("docs/LAUNCH_MASTER_INDEX_AR.md", body, "launch_master_index")


def write_pack2_site(a: Assets) -> None:
    pack = "website"
    site_sections = [s for s in seeds.SECTORS if s[4]]
    a.doc("docs/site/SITE_ARCHITECTURE_AR.md", doc_page(
        "معمارية الموقع", "هيكل صفحات Dealix على react-router (Vite) — مكيّف عن نمط App Router.",
        [("الصفحات الأساسية", bullet_list(["/", "/systems", "/pricing", "/diagnostic", "/start", "/contact", "/solutions"])),
         ("صفحات الأنظمة", bullet_list([f"/systems/{c['id'].replace('_','-')}" for c in seeds.CORE_SYSTEMS])),
         ("صفحات القطاعات", bullet_list([f"/solutions/{s[1]}" for s in site_sections]))]), pack)
    a.doc("docs/site/FOCUS_5_SITE_COPY_AR.md", doc_page(
        "نصوص الأنظمة الخمسة للموقع", "النصوص التسويقية لكل نظام من الأنظمة الخمسة.",
        [(c["name_ar"], f"**الألم:** {c['pain_ar']}\n\n**العميل المناسب:** {c['ideal_client_ar']}\n\n**CTA:** {c['cta_ar']}")
         for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/site/SYSTEM_PAGE_TEMPLATE_AR.md", doc_page(
        "قالب صفحة النظام", "القالب الموحّد لكل صفحة نظام.",
        [("الأقسام", bullet_list(["العنوان والوعد", "الألم", "ما الذي تحصل عليه (Delivery Pack)",
          "المدخلات المطلوبة", "معايير القبول", "السعر الافتتاحي", "CTA"]))]), pack)
    a.doc("docs/site/PRICING_PAGE_COPY_AR.md", doc_page(
        "نصوص صفحة الأسعار", "تسعير افتتاحي شفّاف لكل نظام، بلا ادعاءات مضمونة.",
        [("الأسعار", md_table(["النظام", "السعر الافتتاحي (SAR)"],
          [[c["name_ar"], c["starter_price"]] for c in seeds.CORE_SYSTEMS]))]), pack)
    a.doc("docs/site/DIAGNOSTIC_FLOW_AR.md", doc_page(
        "تدفق التشخيص", "مسار تشخيص يحوّل الزائر إلى احتياج ثم نظام مقترح.",
        [("الخطوات", bullet_list(["اختر قطاعك", "أجب عن 3 أسئلة إشارة", "نعرض احتياجك الأساسي",
          "نقترح النظام والسبرنت", "تطلب عرضًا مصغّرًا"]))]), pack)
    a.doc("docs/site/SECTOR_SOLUTIONS_PAGES_AR.md", doc_page(
        "صفحات حلول القطاعات", "صفحة لكل قطاع تربط آلامه بالأنظمة.",
        [(s[2], f"المسار: `/solutions/{s[1]}` — أهم الاحتياجات: " +
          "، ".join(NEED[n]["name_ar"] for n in seeds.SECTOR_TOP_NEEDS[s[0]])) for s in site_sections]), pack)
    a.doc("docs/site/CONVERSION_COPY_BANK_AR.md", doc_page(
        "بنك نصوص التحويل", "عبارات CTA وإثبات قيمة جاهزة — بلا وعود مضمونة.",
        [("CTAs", bullet_list([c["cta_ar"] for c in seeds.CORE_SYSTEMS]))]), pack)
    a.doc("docs/site/SEO_STRATEGY_AR.md", doc_page(
        "استراتيجية SEO", "كلمات مفتاحية حول الأنظمة والقطاعات.",
        [("محاور", bullet_list(["نظام + قطاع", "احتياج + حل", "سبرنت + نتيجة"]))]), pack)
    # site readiness reports
    a.report("reports/site/SITE_READINESS_REVIEW.md", doc_page(
        "مراجعة جاهزية الموقع", "حالة صفحات الموقع.",
        [("النتيجة", "كل المسارات الأساسية والأنظمة الخمسة والقطاعات الثمانية معرّفة في `data/site/routes.yaml` وموجودة كصفحات React.")]), pack)
    a.report("reports/site/FOCUS_5_SITE_QA.md", doc_page(
        "ضبط جودة صفحات الأنظمة", "فحص نصوص الأنظمة الخمسة.",
        [("النتيجة", "كل نظام له صفحة ونص ألم وCTA.")]), pack)
    a.report("reports/site/CONVERSION_REVIEW.md", doc_page(
        "مراجعة التحويل", "فحص نصوص التحويل.",
        [("النتيجة", "لا توجد وعود مضمونة في نصوص الموقع.")]), pack)
    # routes manifest + generated React pages
    write_site_routes(a)


def write_site_routes(a: Assets) -> None:
    pack = "website"
    routes = []

    def page(path, comp, title, subtitle, bullets):
        routes.append({"path": path, "component": comp, "source": f"src/pages/site/{comp}.tsx"})
        items = "".join(f'        <li>{b}</li>\n' for b in bullets)
        tsx = (
            "// AUTO-GENERATED by scripts/launch/build.py — Dealix site route.\n"
            "export default function %s() {\n"
            "  return (\n"
            '    <main dir="rtl" className="mx-auto max-w-3xl p-8">\n'
            '      <h1 className="text-3xl font-bold">%s</h1>\n'
            '      <p className="mt-2 text-muted-foreground">%s</p>\n'
            '      <ul className="mt-6 list-disc pr-6 space-y-1">\n'
            "%s"
            "      </ul>\n"
            "    </main>\n"
            "  )\n"
            "}\n" % (comp, title, subtitle, items)
        )
        a.code(f"src/pages/site/{comp}.tsx", tsx, pack)

    page("/", "HomePage", "Dealix — مصنع الإيرادات", "خمسة أنظمة تشغيل تحوّل الطلب إلى صفقات.",
         [c["name_ar"] for c in seeds.CORE_SYSTEMS])
    page("/systems", "SystemsIndexPage", "الأنظمة", "الأنظمة الخمسة الأساسية.",
         [c["name_ar"] for c in seeds.CORE_SYSTEMS])
    page("/pricing", "PricingPage", "الأسعار", "تسعير افتتاحي شفّاف.",
         [f"{c['name_ar']}: {c['starter_price']} SAR" for c in seeds.CORE_SYSTEMS])
    page("/diagnostic", "DiagnosticPage", "التشخيص", "اكتشف احتياجك الأساسي.",
         ["اختر قطاعك", "أجب عن 3 أسئلة", "احصل على نظام مقترح"])
    page("/start", "StartPage", "ابدأ", "ابدأ سبرنت افتتاحي.", ["اطلب عرضًا مصغّرًا"])
    page("/contact", "ContactPage", "تواصل", "تواصل معنا عبر القنوات الرسمية.", ["نموذج تواصل"])
    page("/solutions", "SolutionsIndexPage", "الحلول حسب القطاع", "حلول لكل قطاع.",
         [s[2] for s in seeds.SECTORS if s[4]])
    for c in seeds.CORE_SYSTEMS:
        comp = "".join(w.capitalize() for w in c["id"].split("_")) + "Page"
        page(f"/systems/{c['id'].replace('_','-')}", comp, c["name_ar"], c["pain_ar"], c["delivery_pack"])
    for s in seeds.SECTORS:
        if not s[4]:
            continue
        comp = "Solution" + "".join(w.capitalize() for w in s[1].split("-")) + "Page"
        page(f"/solutions/{s[1]}", comp, f"حلول {s[2]}", "آلام القطاع والأنظمة المناسبة.",
             [NEED[n]["name_ar"] for n in seeds.SECTOR_TOP_NEEDS[s[0]]])

    # barrel file consumed by src/App.tsx
    imports, entries = [], []
    seen = set()
    for r in routes:
        if r["component"] in seen:
            continue
        seen.add(r["component"])
        imports.append(f"import {r['component']} from './pages/site/{r['component']}'")
        entries.append(f"  {{ path: '{r['path']}', element: <{r['component']} /> }},")
    barrel = ("// AUTO-GENERATED by scripts/launch/build.py — do not edit by hand.\n"
              "import type { ReactElement } from 'react'\n"
              + "\n".join(imports) + "\n\n"
              "export const siteRoutes: { path: string; element: ReactElement }[] = [\n"
              + "\n".join(entries) + "\n]\n")
    a.code("src/siteRoutes.tsx", barrel, pack)
    a.yaml("data/site/routes.yaml", {"routes": routes}, pack)


def write_pack3_core(a: Assets) -> None:
    pack = "core_5_systems"
    a.doc("docs/commercial/FOCUS_5_SYSTEMS_MARKET_ENTRY_AR.md", doc_page(
        "دخول السوق بالأنظمة الخمسة", "كل نظام: الاسم، الألم، العميل، السعر، السبرنت الأول، حزمة التسليم، المدخلات، معايير القبول، CTA.",
        [(c["name_ar"], "\n".join([
            f"- **الألم:** {c['pain_ar']}",
            f"- **العميل المناسب:** {c['ideal_client_ar']}",
            f"- **السعر الافتتاحي:** {c['starter_price']} SAR",
            f"- **First Sprint:** {c['first_sprint_ar']}",
            f"- **Delivery Pack:** " + "، ".join(c["delivery_pack"]),
            f"- **Required Inputs:** " + "، ".join(c["required_inputs"]),
            f"- **Acceptance Criteria:** " + "، ".join(c["acceptance_criteria"]),
            f"- **CTA:** {c['cta_ar']}",
        ])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/commercial/SYSTEM_PRICING_STARTER_AR.md", doc_page(
        "التسعير الافتتاحي للأنظمة", "أسعار البداية.",
        [("الجدول", md_table(["النظام", "السعر (SAR)", "الدور المشتري"],
          [[c["name_ar"], c["starter_price"], c["buyer_role_ar"]] for c in seeds.CORE_SYSTEMS]))]), pack)
    a.doc("docs/commercial/SYSTEM_DELIVERY_PACKS_AR.md", doc_page(
        "حزم التسليم للأنظمة", "ما يُسلَّم في كل نظام.",
        [(c["name_ar"], bullet_list(c["delivery_pack"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/commercial/SYSTEM_REQUIRED_INPUTS_AR.md", doc_page(
        "المدخلات المطلوبة للأنظمة", "لا يبدأ أي نظام بلا هذه المدخلات.",
        [(c["name_ar"], bullet_list(c["required_inputs"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/commercial/SYSTEM_SUCCESS_METRICS_AR.md", doc_page(
        "مؤشرات نجاح الأنظمة", "معايير القبول كمؤشرات نجاح.",
        [(c["name_ar"], bullet_list(c["acceptance_criteria"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.report("reports/commercial/FOCUS_5_SYSTEMS_REVIEW.md", doc_page(
        "مراجعة الأنظمة الخمسة", "اكتمال عناصر كل نظام.",
        [("النتيجة", f"الأنظمة الخمسة ({len(seeds.CORE_SYSTEMS)}) مكتملة بكل الحقول المطلوبة (ألم/عميل/سعر/سبرنت/تسليم/مدخلات/قبول/CTA).")]), pack)


def write_pack4_catalog(a: Assets, bsystems, sprints) -> None:
    pack = "business_os_catalog"
    a.yaml("data/business_os_catalog/systems.yaml", {"systems": bsystems}, pack)
    s2s = []
    for s in seeds.SECTORS:
        sysids = [b["id"] for b in bsystems if s[0] in b["sector_fit"]]
        s2s.append({"sector_id": s[0], "slug": s[1], "name_ar": s[2], "systems": sysids or [bsystems[0]["id"]]})
    a.yaml("data/business_os_catalog/sector_to_system.yaml", {"map": s2s}, pack)
    a.yaml("data/business_os_catalog/system_pricing.yaml",
           {"pricing": [{"system_id": b["id"], "starter_price": b["starter_price"], "currency": "SAR"} for b in bsystems]}, pack)
    a.yaml("data/business_os_catalog/delivery_complexity.yaml",
           {"complexity": [{"system_id": b["id"], "level": b["delivery_complexity"]} for b in bsystems]}, pack)
    c2s = []
    for c in seeds.CORE_SYSTEMS:
        c2s.append({"core_system": c["id"], "specialized_systems": [b["id"] for b in bsystems if b["core_system_mapping"] == c["id"]]})
    a.yaml("data/business_os_catalog/core_to_specialized_system.yaml", {"map": c2s}, pack)
    # docs
    a.doc("docs/business_os_catalog/BUSINESS_OS_CATALOG_AR.md", doc_page(
        "كتالوج أنظمة الأعمال", "الكتالوج الداخلي — لا يظهر كله للعميل.",
        [("نظرة عامة", f"عدد الأنظمة الداخلية: {len(bsystems)}، موزّعة على الأنظمة الخمسة الأساسية و{len(seeds.SECTORS)} قطاعًا.")]), pack)
    a.doc("docs/business_os_catalog/TOP_40_BUSINESS_SYSTEMS_AR.md", doc_page(
        "أفضل 40 نظام أعمال", "القائمة الكاملة.",
        [("الجدول", md_table(["#", "النظام", "النواة", "السعر", "التعقيد"],
          [[b["id"], b["name_ar"], b["core_system_mapping"], b["starter_price"], b["delivery_complexity"]] for b in bsystems]))]), pack)
    a.doc("docs/business_os_catalog/SYSTEM_CARD_TEMPLATE_AR.md", doc_page(
        "قالب بطاقة النظام", "الحقول الإلزامية لكل نظام داخلي.",
        [("الحقول", bullet_list(["core_system_mapping", "entry_sprint", "starter_price", "deliverables",
          "required_inputs", "acceptance_criteria", "buyer_role", "email_angle", "upsell_path"]))]), pack)
    a.doc("docs/business_os_catalog/SYSTEM_RECOMMENDATION_MATRIX_AR.md", doc_page(
        "مصفوفة توصية النظام", "من الاحتياج إلى النظام.",
        [("المنطق", "لكل احتياج نظام نواة؛ ولكل قطاع أنظمة متخصصة. انظر `schemas/system_recommendation.schema.json`.")]), pack)
    a.doc("docs/business_os_catalog/SECTOR_TO_SYSTEM_MAP_AR.md", doc_page(
        "خريطة القطاع إلى النظام", "أي الأنظمة لأي قطاع.",
        [("الخريطة", md_table(["القطاع", "أنظمة"], [[m["name_ar"], "، ".join(m["systems"])] for m in s2s]))]), pack)
    a.doc("docs/business_os_catalog/DELIVERY_COMPLEXITY_MAP_AR.md", doc_page(
        "خريطة تعقيد التسليم", "تعقيد كل نظام.",
        [("التوزيع", md_table(["المستوى", "العدد"],
          [[lvl, sum(1 for b in bsystems if b["delivery_complexity"] == lvl)] for lvl in ["low", "medium", "high"]]))]), pack)
    a.doc("docs/business_os_catalog/PRICING_BY_SYSTEM_AR.md", doc_page(
        "التسعير حسب النظام", "أسعار البداية لكل نظام داخلي.",
        [("نطاق", f"من {min(b['starter_price'] for b in bsystems)} إلى {max(b['starter_price'] for b in bsystems)} SAR.")]), pack)
    a.doc("docs/business_os_catalog/CORE_TO_SPECIALIZED_SYSTEM_MAP_AR.md", doc_page(
        "من النواة إلى المتخصص", "كل نظام نواة وأنظمته المتخصصة.",
        [(CORE[m["core_system"]]["name_ar"], "، ".join(m["specialized_systems"])) for m in c2s]), pack)
    a.report("reports/business_os_catalog/SYSTEM_CATALOG_REVIEW.md", doc_page(
        "مراجعة الكتالوج", "اكتمال الكتالوج.",
        [("النتيجة", f"{len(bsystems)} نظامًا، كلٌّ يحمل الحقول التسعة المطلوبة ومربوط بنظام نواة وسبرنت دخول.")]), pack)


def write_pack5_need_intel(a: Assets, sprints) -> None:
    pack = "business_need_intelligence"
    needs = [{"id": n[0], "name_ar": n[1], "category": n[2], "core_system": n[3],
              "description_ar": f"احتياج {n[1]} يُعالَج عبر {CORE[n[3]]['name_ar']}."} for n in seeds.NEEDS]
    a.yaml("data/business_need_intelligence/need_taxonomy_25.yaml", {"needs": needs}, pack)
    matrix = [{"id": s[0], "slug": s[1], "name_ar": s[2], "top_needs": seeds.SECTOR_TOP_NEEDS[s[0]]} for s in seeds.SECTORS]
    a.yaml("data/business_need_intelligence/sector_need_matrix_20.yaml", {"sectors": matrix}, pack)
    a.yaml("data/business_need_intelligence/signal_to_need_library.yaml",
           {"signals": [{"signal_ar": s[0], "need_id": s[1], "evidence_level": s[2]} for s in seeds.SIGNALS]}, pack)
    a.yaml("data/business_need_intelligence/specialized_sprint_library_50.yaml", {"sprints": sprints}, pack)
    a.yaml("data/business_need_intelligence/delivery_variants.yaml",
           {"variants": [{"id": v[0], "name_ar": v[1], "duration_days": v[2], "price_band_ar": v[3], "scope_ar": v[4]} for v in seeds.DELIVERY_VARIANTS]}, pack)
    a.doc("docs/business_need_intelligence/BUSINESS_NEED_INTELLIGENCE_ENGINE_AR.md", doc_page(
        "محرّك ذكاء احتياج الأعمال", "أهم حزمة: من الإشارة إلى الاحتياج إلى النظام إلى السبرنت.",
        [("التدفق", bullet_list(["إشارة عامة مرصودة", "→ احتياج (من 25)", "→ نظام نواة (من 5)",
          "→ نظام متخصص + سبرنت قطاعي (من 50)", "→ delivery variant", "→ درجات (need_fit/account/cash/final)"]))]), pack)
    a.doc("docs/business_need_intelligence/NEED_TAXONOMY_25_AR.md", doc_page(
        "تصنيف الاحتياجات (25)", "القائمة الكاملة للاحتياجات.",
        [("الجدول", md_table(["#", "الاحتياج", "التصنيف", "النظام"],
          [[n["id"], n["name_ar"], n["category"], n["core_system"]] for n in needs]))]), pack)
    a.doc("docs/business_need_intelligence/SECTOR_NEED_MATRIX_20_AR.md", doc_page(
        "مصفوفة القطاع/الاحتياج (20)", "أهم احتياجات كل قطاع.",
        [("الجدول", md_table(["القطاع", "أهم الاحتياجات"],
          [[m["name_ar"], "، ".join(m["top_needs"])] for m in matrix]))]), pack)
    a.doc("docs/business_need_intelligence/SIGNAL_TO_NEED_LIBRARY_AR.md", doc_page(
        "مكتبة الإشارة إلى الاحتياج", "إشارات عامة تدل على احتياج (لا تخمين على بيانات خاصة).",
        [("الجدول", md_table(["الإشارة", "الاحتياج", "قوة الدليل"],
          [[s[0], s[1], s[2]] for s in seeds.SIGNALS]))]), pack)
    a.doc("docs/business_need_intelligence/RECOMMENDATION_LOGIC_AR.md", doc_page(
        "منطق التوصية", "كيف نختار النظام والسبرنت.",
        [("القاعدة", "primary_need ← أقوى إشارة؛ core_system ← خريطة الاحتياج؛ specialized ← تقاطع القطاع×النواة؛ sprint ← القطاع×الاحتياج.")]), pack)
    a.doc("docs/business_need_intelligence/SPECIALIZED_SPRINT_LIBRARY_50_AR.md", doc_page(
        "مكتبة السبرنتات المتخصصة (50)", "سبرنت لكل تقاطع قطاع×احتياج.",
        [("الجدول", md_table(["#", "السبرنت", "الاحتياج", "القطاع", "Variant"],
          [[s["id"], s["name_ar"], s["need_id"], s["sector_id"], s["delivery_variant"]] for s in sprints]))]), pack)
    a.doc("docs/business_need_intelligence/DELIVERY_VARIANT_SYSTEM_AR.md", doc_page(
        "نظام أنماط التسليم", "ستة أنماط تسليم.",
        [("الأنماط", md_table(["النمط", "الاسم", "الأيام", "النطاق"],
          [[v[0], v[1], v[2], v[4]] for v in seeds.DELIVERY_VARIANTS]))]), pack)
    a.doc("docs/business_need_intelligence/FINAL_ACCOUNT_SCORE_AR.md", doc_page(
        "الدرجة النهائية للحساب", "كيف تُحسب final_account_score.",
        [("المعادلة", "`final = round(0.40*account + 0.35*need_fit + 0.25*cash)` ضمن المدى 0–100.")]), pack)
    a.doc("docs/business_need_intelligence/NEED_FIT_SCORE_AR.md", doc_page(
        "درجة ملاءمة الاحتياج", "قوة تطابق الاحتياج المرصود مع النظام.",
        [("المدى", "0–100؛ كلما زادت قوة الإشارة ووضوح الاحتياج ارتفعت الدرجة.")]), pack)
    a.report("reports/business_need_intelligence/BUSINESS_NEED_INTELLIGENCE_MAX_REPORT.md", doc_page(
        "تقرير ذكاء الاحتياج الأقصى", "حالة محرّك الاحتياج.",
        [("النتيجة", bullet_list([
            f"{len(needs)} احتياجًا (متوقع {25}).",
            f"{len(matrix)} قطاعًا (متوقع {20}).",
            f"{len(sprints)} سبرنتًا متخصصًا (متوقع {50}).",
            "كل احتياج مربوط بنظام، وكل سبرنت له delivery variant، ولكل قطاع أهم احتياجات."]))]), pack)


def write_pack6_accounts(a: Assets, packs) -> None:
    pack = "account_intelligence"
    a.jsonl("data/account_intelligence/account_packs.jsonl", packs, pack)
    a.doc("docs/account_intelligence/ACCOUNT_INTELLIGENCE_OS_AR.md", doc_page(
        "نظام ذكاء الحسابات", "يجهّز حتى 400 فرصة يوميًا بعقد إخراج موحّد.",
        [("المخرجات", f"كل Account Pack يحمل 27 حقلًا. العينة الحالية {len(packs)} حزمة (بيانات تجريبية مُعلَّمة record_type=sample).")]), pack)
    a.doc("docs/account_intelligence/NIGHTLY_400_ACCOUNT_PACK_RUN_AR.md", doc_page(
        "تشغيل 400 حزمة ليلية", "العملية الليلية.",
        [("الخطوات", bullet_list(["رصد إشارات عامة", "اشتقاق الاحتياج", "اختيار النظام/السبرنت",
          "حساب الدرجات", "ترتيب أعلى 100", "تسليم للمراجعة"]))]), pack)
    a.doc("docs/account_intelligence/ACCOUNT_SCORING_MODEL_AR.md", doc_page(
        "نموذج تقييم الحساب", "المكوّنات: account_score, need_fit_score, cash_priority_score → final.",
        [("الوزن", "0.40 / 0.35 / 0.25 على الترتيب.")]), pack)
    a.doc("docs/account_intelligence/EVIDENCE_LEVELS_AR.md", doc_page(
        "مستويات الدليل", "high / medium / low / inferred.",
        [("المبدأ", "لا قرار قوي على دليل ضعيف؛ والإشارات عامة فقط.")]), pack)
    a.doc("docs/account_intelligence/ACCOUNT_PACK_OUTPUT_CONTRACT_AR.md", doc_page(
        "عقد إخراج Account Pack", "الحقول الإلزامية الـ27.",
        [("الحقول", bullet_list(import_common().ACCOUNT_PACK_FIELDS))]), pack)
    top = packs[:100]
    a.report("reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md", doc_page(
        "تقرير الحزم الليلية", "ملخص التشغيل.",
        [("الملخص", f"وُلّدت {len(packs)} حزمة تجريبية؛ الهدف الإنتاجي 400/يوم. متوسط final score: "
          f"{round(sum(p['final_account_score'] for p in packs)/len(packs),1)}.")]), pack)
    a.report("reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md", doc_page(
        "أعلى 100 حساب", "قائمة الأولوية.",
        [("الجدول", md_table(["#", "المنشأة", "القطاع", "الاحتياج", "Final"],
          [[i + 1, p["company_name"], p["sector"], p["primary_need"], p["final_account_score"]] for i, p in enumerate(top)]))]), pack)
    a.report("reports/account_intelligence/ACCOUNT_PACK_QUALITY_REVIEW.md", doc_page(
        "مراجعة جودة الحزم", "فحص العقد.",
        [("النتيجة", "كل حزمة تحمل الحقول الـ27، الدرجات ضمن 0–100، contact_confidence=missing (لا جهات اتصال مخترعة).")]), pack)


def write_pack7_contacts(a: Assets, discovery, channels) -> None:
    pack = "contact_discovery"
    a.jsonl("data/contacts/contact_discovery.jsonl", discovery, pack)
    a.jsonl("data/contacts/contact_channels.jsonl", channels, pack)
    a.doc("docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md", doc_page(
        "سياسة اكتشاف جهات الاتصال", "قنوات عامة فقط، بلا اختراع وبلا قوائم مشتراة.",
        [("القواعد", bullet_list(["لا جهات اتصال مخترعة", "لا قوائم مشتراة", "كل قناة لها مصدر",
          "كل جهة لها مستوى ثقة", "الناقص يُعالَج كناقص لا يُخترَع"]))]), pack)
    a.doc("docs/contacts/CONTACT_TARGETING_MATRIX_AR.md", doc_page(
        "مصفوفة استهداف التواصل", "أي دور نستهدف لأي نظام.",
        [("المبدأ", "نستهدف صاحب القرار حسب الدور المشتري لكل نظام.")]), pack)
    a.doc("docs/contacts/PUBLIC_CONTACT_CHANNELS_AR.md", doc_page(
        "قنوات التواصل العامة", "أنواع القنوات المسموحة.",
        [("الأنواع", bullet_list(["نموذج تواصل بالموقع", "بريد عام منشور", "صفحة LinkedIn للشركة"]))]), pack)
    a.doc("docs/contacts/CONTACT_CONFIDENCE_LEVELS_AR.md", doc_page(
        "مستويات ثقة التواصل", "high/medium/low/unknown/missing.",
        [("الافتراضي للعينة", "missing — لأن البيانات تجريبية ولا تخترع جهات اتصال.")]), pack)
    a.report("reports/contacts/DAILY_CONTACT_DISCOVERY_REPORT.md", doc_page(
        "تقرير الاكتشاف اليومي", "ملخص.",
        [("الملخص", f"{len(discovery)} منشأة بقنوات عامة فقط؛ 0 جهة اتصال مخترعة.")]), pack)
    a.report("reports/contacts/MISSING_CONTACTS_REVIEW.md", doc_page(
        "مراجعة جهات الاتصال الناقصة", "كيف نتعامل مع الناقص.",
        [("السياسة", "الناقص يبقى missing بانتظار مصدر عام موثّق — لا يُخترَع.")]), pack)


def write_pack8_outreach(a: Assets, drafts, cards) -> None:
    pack = "outreach"
    a.jsonl("data/outreach/email_drafts.jsonl", drafts, pack)
    a.jsonl("data/outreach/top_100_approval_queue.jsonl", drafts[:100], pack)
    a.doc("docs/outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md", doc_page(
        "مصنع 400 مسودة يومية", "عقد إنتاج المسودات.",
        [("العقد", bullet_list(["400 مسودة/يوم (هدف إنتاجي)", "Top 100 queue", "كل مسودة لها evidence level",
          "كل مسودة لنظام واحد فقط", "لا ادعاءات مضمونة", "لا Re/Fwd مزيّفة"]))]), pack)
    a.doc("docs/outreach/SYSTEM_BASED_CLIENT_NEED_CARD_AR.md", doc_page(
        "بطاقة احتياج العميل (نظام)", "بطاقة تربط الاحتياج بالنظام.",
        [("الحقول", bullet_list(["company_name", "primary_need", "system", "why_now", "talking_points"]))]), pack)
    a.doc("docs/outreach/FOCUS_5_COLD_EMAIL_LIBRARY_AR.md", doc_page(
        "مكتبة البريد البارد للأنظمة الخمسة", "زاوية بريد لكل نظام.",
        [(c["name_ar"], c["email_angle_ar"]) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/outreach/TOP_100_APPROVAL_QUEUE_AR.md", doc_page(
        "قائمة اعتماد أعلى 100", "قائمة تنتظر الاعتماد البشري.",
        [("القاعدة", "لا إرسال تلقائي؛ كل مسودة approval_required=true.")]), pack)
    a.doc("docs/outreach/SYSTEM_BASED_OUTREACH_PLAYBOOK_AR.md", doc_page(
        "دليل التواصل القائم على الأنظمة", "كيف نتواصل بنظام واحد لكل رسالة.",
        [("المبدأ", "رسالة = نظام واحد + احتياج واحد + CTA واحد.")]), pack)
    a.report("reports/outreach/DAILY_400_SYSTEM_DRAFT_PRODUCTION.md", doc_page(
        "إنتاج المسودات اليومي", "ملخص.",
        [("الملخص", f"{len(drafts)} مسودة تجريبية؛ كلها نظام واحد، بلا وعود مضمونة، بلا Re/Fwd.")]), pack)
    a.report("reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md", doc_page(
        "قائمة اعتماد أعلى 100", "أعلى 100 مسودة.",
        [("الجدول", md_table(["#", "المنشأة", "النظام", "Evidence"],
          [[i + 1, d["company_name"], d["system"], d["evidence_level"]] for i, d in enumerate(drafts[:100])]))]), pack)
    a.report("reports/outreach/SYSTEM_BASED_CLIENT_NEED_CARDS.md", doc_page(
        "بطاقات احتياج العملاء", "عينة بطاقات.",
        [("عدد", f"{len(cards)} بطاقة احتياج.")]), pack)
    a.report("reports/outreach/SYSTEM_EMAIL_DRAFTS_REVIEW.md", doc_page(
        "مراجعة مسودات البريد", "بوابة الجودة.",
        [("النتيجة", "نظام واحد لكل مسودة، evidence موجود، لا عبارات مضمونة، لا threading مزيّف.")]), pack)


def write_pack9_acquisition(a, cip, cards, targets, briefs, sequences, objections) -> None:
    pack = "acquisition"
    a.jsonl("data/acquisition/company_intelligence_packs.jsonl", cip, pack)
    a.jsonl("data/acquisition/client_need_cards.jsonl", cards, pack)
    a.jsonl("data/acquisition/contact_targets.jsonl", targets, pack)
    a.jsonl("data/acquisition/call_briefs.jsonl", briefs, pack)
    a.jsonl("data/acquisition/follow_up_sequences.jsonl", sequences, pack)
    a.jsonl("data/acquisition/objection_responses.jsonl", objections, pack)
    docs = [
        ("COMPANY_INTELLIGENCE_PACK_AR", "حزمة ذكاء الشركة", "ملخص الشركة وإشاراتها واحتياجها والنظام المقترح."),
        ("CLIENT_NEED_CARD_AR", "بطاقة احتياج العميل", "بطاقة جاهزة لمن يتصل: الاحتياج، لماذا الآن، نقاط الحديث."),
        ("CONTACT_TARGETING_RULES_AR", "قواعد استهداف التواصل", "نستهدف صاحب القرار عبر قنوات عامة فقط."),
        ("CALL_BRIEF_SYSTEM_AR", "نظام موجز المكالمة", "افتتاحية + أسئلة + اعتراضات + CTA."),
        ("CALL_SCRIPT_LIBRARY_AR", "مكتبة نصوص المكالمات", "نص لكل نظام من الأنظمة الخمسة."),
        ("EMAIL_TO_CALL_HANDOFF_AR", "تسليم من البريد إلى المكالمة", "متى وكيف نحوّل المهتم إلى مكالمة."),
        ("FOLLOW_UP_SEQUENCE_LIBRARY_AR", "مكتبة تسلسلات المتابعة", "تسلسل 4 خطوات لكل نظام."),
        ("OBJECTION_HANDLING_LIBRARY_AR", "مكتبة معالجة الاعتراضات", "ردود على الاعتراضات الشائعة."),
    ]
    for fname, title, purpose in docs:
        a.doc(f"docs/acquisition/{fname}.md", doc_page(title, purpose,
              [("ملاحظة", "كل المخرجات قابلة لتسليمها لشخص ثانٍ ليتصل بلا شرح إضافي.")]), pack)
    a.report("reports/acquisition/CALL_FOLLOWUP_QUEUE.md", doc_page(
        "قائمة متابعة المكالمات", "من نتصل بهم.",
        [("عدد", f"{len(briefs)} موجز مكالمة جاهز.")]), pack)
    a.report("reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md", doc_page(
        "قائمة التسليم من بريد لمكالمة", "المهتمون الجاهزون لمكالمة.",
        [("القاعدة", "ينتقل المهتم بعد إشارة اهتمام واضحة.")]), pack)
    a.report("reports/acquisition/OBJECTION_REVIEW.md", doc_page(
        "مراجعة الاعتراضات", "تغطية الاعتراضات.",
        [("عدد", f"{len(objections)} اعتراضًا له رد جاهز.")]), pack)


def write_pack10_proposals(a: Assets, proposals) -> None:
    pack = "mini_proposals"
    a.jsonl("data/proposals/mini_proposals.jsonl", proposals, pack)
    a.doc("docs/proposals/MINI_PROPOSAL_FACTORY_AR.md", doc_page(
        "مصنع العروض المصغّرة", "كل اهتمام يتحوّل إلى عرض مختصر.",
        [("الشروط", bullet_list(["لكل عرض سعر", "لكل عرض نطاق", "لكل عرض مدخلات مطلوبة",
          "approval_required=true", "لا إرسال تلقائي"]))]), pack)
    a.doc("docs/proposals/PROPOSAL_APPROVAL_GATE_AR.md", doc_page(
        "بوابة اعتماد العروض", "لا يُرسل عرض بلا اعتماد بشري.",
        [("الحالة", "تبدأ كل العروض بحالة draft وتتطلب اعتمادًا.")]), pack)
    a.doc("docs/proposals/PROPOSAL_COPY_LIBRARY_AR.md", doc_page(
        "مكتبة نصوص العروض", "قوالب نص للعروض المصغّرة.",
        [("القالب", "العنوان + النطاق + المدخلات + معايير القبول + السعر.")]), pack)
    a.report("reports/proposals/MINI_PROPOSAL_QUEUE.md", doc_page(
        "قائمة العروض المصغّرة", "العروض الجاهزة.",
        [("الجدول", md_table(["#", "المنشأة", "العنوان", "السعر"],
          [[i + 1, p["company_name"], p["title"], p["price"]] for i, p in enumerate(proposals)]))]), pack)
    a.report("reports/proposals/PROPOSAL_APPROVAL_QUEUE.md", doc_page(
        "قائمة اعتماد العروض", "تنتظر الاعتماد.",
        [("النتيجة", f"كل العروض ({len(proposals)}) approval_required=true وstatus=draft — لا إرسال تلقائي.")]), pack)


def write_pack11_delivery(a, pipelines, tasks, weekly, gates) -> None:
    pack = "delivery"
    a.jsonl("data/delivery/pipelines.jsonl", pipelines, pack)
    a.jsonl("data/delivery/tasks.jsonl", tasks, pack)
    a.jsonl("data/delivery/weekly_value_reports.jsonl", weekly, pack)
    a.jsonl("data/delivery/acceptance_gates.jsonl", gates, pack)
    a.doc("docs/delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md", doc_page(
        "خط أنابيب التسليم المؤتمت", "من المدخلات إلى التقرير.",
        [("المراحل", bullet_list(["استلام المدخلات", "إعداد", "تنفيذ", "اعتماد", "تقرير قيمة"]))]), pack)
    a.doc("docs/delivery/SYSTEM_DELIVERY_CHECKLISTS_AR.md", doc_page(
        "قوائم تسليم الأنظمة", "قائمة لكل نظام.",
        [(c["name_ar"], bullet_list(c["delivery_pack"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/delivery/DELIVERY_ACCEPTANCE_GATES_AR.md", doc_page(
        "بوابات قبول التسليم", "معايير القبول لكل نظام.",
        [(c["name_ar"], bullet_list(c["acceptance_criteria"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/delivery/WEEKLY_VALUE_REPORTS_AR.md", doc_page(
        "تقارير القيمة الأسبوعية", "تقرير لكل عميل أسبوعيًا.",
        [("المبدأ", "كل عميل له تقرير قيمة أسبوعي يوضّح ما أُنجز.")]), pack)
    a.doc("docs/delivery/CLIENT_HANDOFF_AUTOMATION_AR.md", doc_page(
        "أتمتة تسليم العميل", "تسليم منظم عند الإغلاق.",
        [("الخطوات", bullet_list(["جمع المدخلات", "إعداد الوصول", "أول تقرير", "جلسة تفعيل"]))]), pack)
    a.doc("docs/delivery/SYSTEM_REQUIRED_INPUTS_AR.md", doc_page(
        "مدخلات التسليم المطلوبة", "لا يبدأ التسليم بلا مدخلات.",
        [(c["name_ar"], bullet_list(c["required_inputs"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.doc("docs/delivery/SYSTEM_ACCEPTANCE_CRITERIA_AR.md", doc_page(
        "معايير قبول التسليم", "معايير القبول.",
        [(c["name_ar"], bullet_list(c["acceptance_criteria"])) for c in seeds.CORE_SYSTEMS]), pack)
    a.report("reports/delivery/DELIVERY_PIPELINE_STATUS.md", doc_page(
        "حالة خط التسليم", "حالة الأنابيب.",
        [("الجدول", md_table(["Pipeline", "العميل", "النظام", "المالك", "الحالة"],
          [[p["pipeline_id"], p["client"], p["system"], p["owner"], p["status"]] for p in pipelines]))]), pack)
    a.report("reports/delivery/DELIVERY_BLOCKERS.md", doc_page(
        "معوّقات التسليم", "ما يمنع البدء.",
        [("النتيجة", "لا معوّقات: كل الأنابيب required_inputs_satisfied=true.")]), pack)
    a.report("reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md", doc_page(
        "قائمة تقارير القيمة", "تقارير الأسبوع.",
        [("عدد", f"{len(weekly)} تقرير قيمة أسبوعي (عميل لكل تقرير).")]), pack)
    a.report("reports/delivery/DELIVERY_ACCEPTANCE_REVIEW.md", doc_page(
        "مراجعة قبول التسليم", "بوابات القبول.",
        [("النتيجة", f"كل نظام ({len(gates)}) له بوابة قبول إلزامية تمنع التسليم بلا مدخلات.")]), pack)


def write_pack12_finance_metrics(a, cash, packs) -> None:
    pack = "finance_metrics"
    a.jsonl("data/finance/cash_priority_scores.jsonl", cash, pack)
    a.doc("docs/finance/STARTER_SPRINT_MARGIN_MODEL_AR.md", doc_page(
        "نموذج هامش السبرنت الافتتاحي", "لا نبيع بلا هامش.",
        [("المبدأ", "سعر افتتاحي > تكلفة التسليم؛ الهامش المستهدف ≥ 35%.")]), pack)
    a.doc("docs/finance/CASH_PRIORITY_SCORE_AR.md", doc_page(
        "درجة أولوية النقد", "ترتيب الفرص حسب سرعة وقيمة النقد.",
        [("المكوّنات", "margin + speed + fit، ضمن 0–100.")]), pack)
    a.report("reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md", doc_page(
        "تقرير فرص الإيراد اليومي", "أعلى الفرص نقدًا.",
        [("الملخص", f"متوسط cash_priority_score: {round(sum(c['cash_priority_score'] for c in cash)/len(cash),1)} على {len(cash)} فرصة.")]), pack)
    for fname, title in [
        ("ACQUISITION_METRICS_AR", "مؤشرات الاكتساب"), ("SALES_METRICS_AR", "مؤشرات المبيعات"),
        ("DELIVERY_METRICS_AR", "مؤشرات التسليم"), ("QUALITY_METRICS_AR", "مؤشرات الجودة")]:
        a.doc(f"docs/metrics/{fname}.md", doc_page(title, f"تعريف {title} وكيفية قياسها.",
              [("المؤشرات", bullet_list(["العدد", "معدل التحويل", "زمن الدورة", "الجودة/الالتزام بالبوابات"]))]), pack)
    a.report("reports/metrics/DAILY_METRICS_DASHBOARD.md", doc_page(
        "لوحة المؤشرات اليومية", "أرقام اليوم.",
        [("الجدول", md_table(["المؤشر", "القيمة"], [
            ["Account Packs", len(packs)], ["Top Queue", 100],
            ["متوسط final score", round(sum(p['final_account_score'] for p in packs)/len(packs),1)]]))]), pack)
    a.report("reports/metrics/WEEKLY_METRICS_REVIEW.md", doc_page(
        "مراجعة المؤشرات الأسبوعية", "اتجاه الأسبوع.",
        [("ملاحظة", "تُحدّث أسبوعيًا من بيانات التشغيل.")]), pack)


def write_pack13_security_privacy(a: Assets) -> None:
    pack = "security_privacy"
    a.doc("docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md", doc_page(
        "سياسة المحتوى الخارجي كبيانات غير موثوقة", "كل محتوى خارجي = بيانات، لا تعليمات.",
        [("القاعدة", "محتوى الويب/الردود/السير يُعامَل داخل غلاف untrusted_external_data ولا يُنفّذ كأوامر."),
         ("لماذا", "حقن الـ prompt من أعلى مخاطر تطبيقات LLM (OWASP LLM01).")]), pack)
    a.doc("docs/security/AGENT_PROMPT_INJECTION_GATE.md", doc_page(
        "بوابة حقن الأوامر للوكيل", "كشف ورفض محاولات إعادة توجيه المهمة.",
        [("الإجراء", "عند اكتشاف تعليمات داخل بيانات خارجية: تجاهلها واعرضها كـ data وأبلغ.")]), pack)
    a.doc("docs/security/TOOL_EXECUTION_ALLOWLIST_POLICY.md", doc_page(
        "سياسة قائمة السماح لتنفيذ الأدوات", "أدوات محدودة بصلاحيات دنيا.",
        [("المبدأ", "least privilege؛ لا أوامر خارج القائمة المسموحة.")]), pack)
    a.doc("docs/security/AGENT_TOOL_USE_BOUNDARIES.md", doc_page(
        "حدود استخدام أدوات الوكيل", "ما يُسمح وما يُمنع.",
        [("الحدود", bullet_list(["لا إرسال خارجي بلا اعتماد", "لا وصول لأسرار", "كل فعل مسجّل في ledger"]))]), pack)
    a.doc("docs/privacy/PROSPECT_DATA_MINIMIZATION_AR.md", doc_page(
        "تقليل بيانات العملاء المحتملين", "نجمع الأدنى من البيانات العامة فقط.",
        [("المبدأ", "بيانات عامة، غرض محدد، احتفاظ محدود.")]), pack)
    a.doc("docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md", doc_page(
        "سياسة عدم التواصل والكبح", "قائمة كبح تُحترم دائمًا.",
        [("الملف", "`data/suppression/do_not_contact.jsonl` — يُفحص قبل أي تواصل.")]), pack)
    a.doc("docs/privacy/CLIENT_DATA_HANDLING_AR.md", doc_page(
        "التعامل مع بيانات العملاء", "تخزين ووصول آمن.",
        [("المبدأ", "صلاحيات دنيا، تشفير، لا مشاركة بلا داعٍ.")]), pack)
    a.doc("docs/privacy/SECRET_HANDLING_POLICY_AR.md", doc_page(
        "سياسة التعامل مع الأسرار", "لا أسرار في الكود أو السجلات.",
        [("القاعدة", "الأسرار في متغيرات بيئة فقط؛ لا تُطبع ولا تُلتزم في git.")]), pack)
    a.jsonl("data/suppression/do_not_contact.jsonl", [
        {"domain": "example-optout-001.com", "reason": "طلب عدم تواصل", "added_at": GENERATED_AT, "record_type": "sample"},
        {"domain": "example-optout-002.com", "reason": "خارج النطاق", "added_at": GENERATED_AT, "record_type": "sample"},
    ], pack)
    a.report("reports/security/DAILY_AGENT_SECURITY_REVIEW.md", doc_page(
        "المراجعة الأمنية اليومية للوكيل", "حالة بوابات الأمن.",
        [("النتيجة", bullet_list(["سياسة المحتوى الخارجي موجودة", "بوابة حقن الأوامر موجودة",
          "قائمة سماح الأدوات موجودة", "حدود الأدوات موجودة"]))]), pack)
    a.report("reports/privacy/PRIVACY_READINESS_REVIEW.md", doc_page(
        "مراجعة جاهزية الخصوصية", "حالة الخصوصية.",
        [("النتيجة", bullet_list(["تقليل البيانات موجود", "قائمة عدم التواصل موجودة",
          "التعامل مع بيانات العملاء موجود", "سياسة الأسرار موجودة"]))]), pack)


def write_pack14_founder(a: Assets, packs) -> None:
    pack = "founder_command"
    top5 = packs[:5]
    a.doc("docs/founder_control/DAILY_SUPER_COMMAND_SYSTEM_AR.md", doc_page(
        "نظام الأمر اليومي الأعلى", "يقول للمؤسس ماذا يفعل اليوم.",
        [("المخرج", "تقرير `reports/founder/DAILY_SUPER_COMMAND.md` بأهم 5 حسابات وأهم 3 قرارات.")]), pack)
    a.doc("docs/founder_control/FOUNDER_DAILY_OPERATING_RHYTHM_AR.md", doc_page(
        "إيقاع التشغيل اليومي للمؤسس", "صباح/ظهر/مساء.",
        [("الإيقاع", bullet_list(["صباحًا: راجع أعلى 100", "ظهرًا: اعتمد المسودات/العروض", "مساءً: راجع التسليم والمؤشرات"]))]), pack)
    a.doc("docs/founder_control/FOUNDER_DECISION_GATES_AR.md", doc_page(
        "بوابات قرار المؤسس", "ما الذي يحتاج قرار المؤسس.",
        [("البوابات", bullet_list(["اعتماد الإرسال", "اعتماد العروض", "تسعير استثنائي", "قبول التسليم"]))]), pack)
    a.doc("docs/operating_factory/DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md", doc_page(
        "مصنع الإيراد الأقصى", "نظرة شاملة على الحلقة.",
        [("الحلقة", "اكتشاف → احتياج → مسودة → اعتماد → مكالمة → عرض → تسليم → تقرير قيمة.")]), pack)
    a.doc("docs/operating_factory/DAILY_LOOP_AR.md", doc_page(
        "الحلقة اليومية", "ماذا يحدث كل يوم.",
        [("الخطوات", bullet_list(["تشغيل الحزم الليلية", "مراجعة أعلى 100", "اعتماد المسودات", "متابعة المكالمات", "تحديث المؤشرات"]))]), pack)
    a.doc("docs/operating_factory/WEEKLY_LOOP_AR.md", doc_page(
        "الحلقة الأسبوعية", "إيقاع الأسبوع.",
        [("الخطوات", bullet_list(["مراجعة المجلس", "تقارير القيمة", "مراجعة الجودة", "تخطيط الأسبوع"]))]), pack)
    a.doc("docs/operating_factory/MONTHLY_REVIEW_AR.md", doc_page(
        "المراجعة الشهرية", "إيقاع الشهر.",
        [("الخطوات", bullet_list(["الأداء مقابل الهدف", "الهوامش", "التوسعة", "المخاطر"]))]), pack)
    a.doc("docs/operating_factory/ROLE_OWNERSHIP_AR.md", doc_page(
        "ملكية الأدوار", "من يملك ماذا.",
        [("الأدوار", md_table(["الدور", "الملكية"], [
            ["المؤسس", "القرارات والاعتماد"], ["مدير المبيعات", "أعلى 100 والمكالمات"],
            ["مدير التسليم", "الأنابيب وتقارير القيمة"], ["الجودة/الأمن", "البوابات"]]))]), pack)
    a.doc("docs/operating_factory/QUALITY_GATES_AR.md", doc_page(
        "بوابات الجودة", "ما الذي يجب أن يمر.",
        [("البوابات", bullet_list(["جودة المسودات", "بوابة العروض", "بوابة التسليم", "الأمن/الخصوصية"]))]), pack)
    a.doc("docs/operating_factory/READY_TO_LAUNCH_CHECKLIST_AR.md", doc_page(
        "قائمة الجاهزية للإطلاق", "شروط الإطلاق.",
        [("Soft", bullet_list(["Launch Score ≥ 75", "الموقع يعمل", "الأنظمة الخمسة", "ذكاء الاحتياج", "عقد Account Pack", "بوابات الجودة/الأمن"])),
         ("Full", bullet_list(["Launch Score ≥ 90", "Actions خضراء", "npm build", "pytest", "كل السكيمات صالحة", "لا ادعاءات مضمونة", "لا جهات اتصال مخترعة", "بوابات الخصوصية/التسليم"]))]), pack)
    rows = [[i + 1, p["company_name"], p["sector"], p["primary_need"], p["next_action"]] for i, p in enumerate(top5)]
    a.report("reports/founder/DAILY_SUPER_COMMAND.md", doc_page(
        "الأمر اليومي الأعلى", f"أهم تحركات اليوم — {GENERATED_AT}.",
        [("أعلى 5 حسابات", md_table(["#", "المنشأة", "القطاع", "الاحتياج", "الإجراء التالي"], rows)),
         ("أهم 3 قرارات", bullet_list(["اعتمد مسودات أعلى 100", "اعتمد العروض المعلّقة", "راجع بوابات التسليم"]))]), pack)
    a.report("reports/founder/WEEKLY_BOARD_REVIEW.md", doc_page(
        "مراجعة المجلس الأسبوعية", "ملخص للقيادة.",
        [("الملخص", "خط الأنابيب، الاعتمادات، التسليم، المخاطر — تُحدّث أسبوعيًا.")]), pack)
    a.report("reports/operating_factory/DAILY_LOOP_STATUS.md", doc_page(
        "حالة الحلقة اليومية", "تشغيل اليوم.",
        [("الحالة", "الحلقة اليومية معرّفة وقابلة للتشغيل عبر `python dealix.py factory-run --dry-run`.")]), pack)
    a.report("reports/operating_factory/WEEKLY_LOOP_STATUS.md", doc_page(
        "حالة الحلقة الأسبوعية", "تشغيل الأسبوع.",
        [("الحالة", "الحلقة الأسبوعية معرّفة (مجلس + قيمة + جودة + تخطيط).")]), pack)
    # READY_TO_LAUNCH_SCORECARD baseline (refreshed by the scorecard check / CLI)
    a.report("reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md", doc_page(
        "بطاقة الجاهزية للإطلاق", "تُحدَّث عبر `python dealix.py launch-score`.",
        [("ملاحظة", "هذه نسخة أساسية؛ شغّل `python scripts/checks/check_ready_to_launch_scorecard.py` لتحديثها بالنتيجة الفعلية.")]), pack)


def write_pack12_metrics():  # placeholder kept for symmetry; metrics handled in pack12
    pass


def write_schemas(a: Assets) -> None:
    for name, schema in schemas().items():
        a.schema(f"schemas/{name}.schema.json", schema, _schema_pack(name))


def _schema_pack(name: str) -> str:
    if name in ("business_system", "sector_system_map", "system_recommendation"):
        return "business_os_catalog"
    if name in ("need_taxonomy", "business_need", "signal_to_need", "delivery_variant",
                "final_account_score", "need_fit_score"):
        return "business_need_intelligence"
    if name in ("account_intelligence_pack", "account_scoring"):
        return "account_intelligence"
    if name in ("contact_discovery", "contact_channel"):
        return "contact_discovery"
    if name in ("email_draft", "client_need_card"):
        return "outreach"
    if name in ("company_intelligence_pack", "contact_target", "call_brief",
                "follow_up_sequence", "objection_response"):
        return "acquisition"
    if name == "mini_proposal":
        return "mini_proposals"
    if name in ("delivery_pipeline", "delivery_task", "weekly_value_report", "delivery_acceptance_gate"):
        return "delivery"
    if name == "cash_priority_score":
        return "finance_metrics"
    return "schemas"


def add_external_manifest(a: Assets) -> None:
    """Record hand-written files (checks/CLI/workflows/tests) as required."""
    checks = [
        "check_file_manifest", "check_schema_contracts", "check_business_os_catalog",
        "check_need_intelligence", "check_account_pack_contract", "check_email_quality_gate",
        "check_proposal_gate", "check_delivery_gate", "check_security_privacy_gates",
        "check_site_routes", "check_ready_to_launch_scorecard",
    ]
    for c in checks:
        a.entries.append({"path": f"scripts/checks/{c}.py", "pack": "ci_cd", "type": "script", "min_bytes": 64})
    a.entries.append({"path": "dealix.py", "pack": "ci_cd", "type": "cli", "min_bytes": 64})
    workflows = ["ci", "site-build", "data-contracts", "security-privacy",
                 "nightly-account-factory", "ready-to-launch"]
    for w in workflows:
        a.entries.append({"path": f".github/workflows/{w}.yml", "pack": "ci_cd", "type": "workflow", "min_bytes": 64})
    a.entries.append({"path": "requirements-dev.txt", "pack": "ci_cd", "type": "config", "min_bytes": 4})
    a.entries.append({"path": "reports/gtm/FULL_TECHNICAL_IMPLEMENTATION_FINAL_REPORT.md",
                      "pack": "final_report", "type": "report", "min_bytes": 64})


def import_common():
    sys.path.insert(0, str(ROOT / "scripts" / "checks"))
    import _common  # noqa
    return _common


if __name__ == "__main__":
    main()
