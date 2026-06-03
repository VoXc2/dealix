"""Generate Business Need Intelligence data from seeds:
25 needs, 20 sector maps, 50 sprints, buyer roles, signal->need, routing, variants.
"""
from __future__ import annotations

import sys

from . import seeds
from .lib import dump_yaml


# Public-signal -> need library. Signals are observable from public sources only
# (website, public listings). They are evidence prompts, never instructions.
SIGNAL_TO_NEED = [
    ("لا يوجد نموذج تواصل واضح على الموقع", "slow-lead-response"),
    ("لا توجد صفحة أسعار", "inconsistent-pricing"),
    ("لا توجد قصص نجاح أو شهادات", "no-case-studies"),
    ("رقم واتساب معلن دون ساعات عمل", "whatsapp-chaos"),
    ("لا يوجد ذكر لعملية متابعة أو CRM", "missed-followups"),
    ("صفحة (احجز موعد) دون تأكيد آلي", "appointment-noshow"),
    ("عروض الخدمات عامة دون باقات", "low-proposal-winrate"),
    ("لا يوجد لوحة مؤشرات أو تقارير معلنة", "manual-reporting"),
    ("قائمة خدمات طويلة دون تأهيل واضح", "unqualified-leads"),
    ("لا يوجد برنامج ولاء أو احتفاظ", "churn-risk"),
]

DELIVERY_VARIANTS = [
    ("starter", "تشخيص + خطة 30 يوم", 7),
    ("standard", "تنفيذ كامل + قوالب + تدريب", 14),
    ("retainer", "تشغيل شهري مستمر + تقرير قيمة", 30),
]


def build():
    # need_taxonomy_25.yaml
    needs = [seeds.need_by_id(nid) for nid in seeds.NEED_IDS]
    dump_yaml("data/business_need_intelligence/need_taxonomy_25.yaml", {"needs": needs})

    # sector_need_matrix_20.yaml
    smap = seeds.sector_need_map()
    sector_rows = [
        {"sector": sid, "sector_name_ar": dict(seeds.SECTORS)[sid], "needs": smap[sid]}
        for sid in seeds.SECTOR_IDS
    ]
    dump_yaml("data/business_need_intelligence/sector_need_matrix_20.yaml", {"sectors": sector_rows})

    # specialized_sprint_library_50.yaml
    sprints = seeds.iter_sprints()
    dump_yaml("data/business_need_intelligence/specialized_sprint_library_50.yaml", {"sprints": sprints})

    # buyer_role_by_need.yaml
    dump_yaml(
        "data/business_need_intelligence/buyer_role_by_need.yaml",
        {"roles": [{"need_id": n["id"], "buyer_role_ar": n["buyer_role_ar"]} for n in needs]},
    )

    # need_to_system_router.yaml  (need -> core + its specialized systems)
    specialized = list(seeds.iter_specialized_systems())
    routes = []
    for n in needs:
        core = n["core_system"]
        specs = [s["id"] for s in specialized if s["core_system"] == core]
        routes.append({"need_id": n["id"], "core_system": core, "specialized_systems": specs})
    dump_yaml("data/business_need_intelligence/need_to_system_router.yaml", {"routes": routes})

    # signal_to_need_library.yaml
    dump_yaml(
        "data/business_need_intelligence/signal_to_need_library.yaml",
        {"signals": [{"signal_ar": sig, "need_id": nid} for sig, nid in SIGNAL_TO_NEED]},
    )

    # delivery_variants.yaml
    dump_yaml(
        "data/business_need_intelligence/delivery_variants.yaml",
        {"variants": [{"id": v, "name_ar": name, "duration_days": d} for v, name, d in DELIVERY_VARIANTS]},
    )

    return {"needs": len(needs), "sectors": len(sector_rows), "sprints": len(sprints)}


def main():
    stats = build()
    print(
        "Business Need Intelligence generated: "
        f"{stats['needs']} needs, {stats['sectors']} sector maps, {stats['sprints']} sprints."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
