"""Canonical seed data for the Dealix Revenue Factory.

This module is the single source of truth. Generators read these seeds and
emit the committed data files (YAML / JSONL) and the public website catalog.
Check scripts validate the emitted files against the schemas.

Design rules enforced by the data here:
  - The public site exposes only 5 Core Systems + sector solutions.
  - Internally Dealix routes every account through:
        sector -> need -> core system -> specialized system / sprint -> delivery
  - Every specialized system maps to exactly one core system.
  - No invented contacts, no guaranteed claims (enforced in gates, not data).
"""

# ---------------------------------------------------------------------------
# 5 Public Core Systems
# ---------------------------------------------------------------------------
CORE_SYSTEMS = [
    {
        "id": "revenue-operating-system",
        "name_ar": "نظام تشغيل الإيرادات",
        "name_en": "Revenue Operating System",
        "promise_ar": "نُنظّم رحلة العميل من أول تواصل حتى تكرار الشراء، ونكشف أين تضيع الإيرادات.",
        "outcome_ar": "خريطة تسرب إيرادات + عملية مبيعات واضحة + لوحة عملاء موحّدة.",
    },
    {
        "id": "executive-command-os",
        "name_ar": "نظام القيادة التنفيذية",
        "name_en": "Executive Command OS",
        "promise_ar": "نعطي المؤسس صورة يومية واضحة: ماذا يحدث، ما الأولوية، وأين الخطر.",
        "outcome_ar": "لوحة مؤشرات + أولويات يومية + مراجعة أسبوعية + توقع إيرادات.",
    },
    {
        "id": "follow-up-recovery-os",
        "name_ar": "نظام استرجاع المتابعات",
        "name_en": "Follow-up Recovery OS",
        "promise_ar": "نلتقط كل عميل لم تتم متابعته ونعيد تفعيل الصفقات المهجورة.",
        "outcome_ar": "تسلسل متابعة منظم + سرعة رد + استرجاع صفقات + تقرير استرجاع.",
    },
    {
        "id": "whatsapp-client-os",
        "name_ar": "نظام عملاء واتساب",
        "name_en": "WhatsApp Client OS",
        "promise_ar": "نُحوّل فوضى واتساب إلى قناة منظمة بقوالب وفرز ومواعيد.",
        "outcome_ar": "صندوق منظم + قوالب معتمدة + إدارة مواعيد + تقارير محادثات.",
    },
    {
        "id": "proposal-proof-os",
        "name_ar": "نظام العروض والإثبات",
        "name_en": "Proposal & Proof OS",
        "promise_ar": "نبني عروضًا تُقنع وتُثبت القيمة برقم وقصة نجاح، لا بوعود.",
        "outcome_ar": "عروض جاهزة + تسعير منضبط + حزمة إثبات + مكتبة اعتراضات.",
    },
]
CORE_SYSTEM_IDS = [c["id"] for c in CORE_SYSTEMS]

# ---------------------------------------------------------------------------
# 20 Sector Maps (public solutions)
# ---------------------------------------------------------------------------
SECTORS = [
    ("marketing-agencies", "وكالات التسويق"),
    ("training-companies", "شركات التدريب"),
    ("clinics", "العيادات"),
    ("real-estate", "العقار"),
    ("professional-services", "الخدمات المهنية"),
    ("recruitment", "التوظيف"),
    ("saas", "منتجات SaaS"),
    ("logistics", "اللوجستيات"),
    ("restaurants", "المطاعم"),
    ("education", "التعليم"),
    ("ecommerce", "التجارة الإلكترونية"),
    ("healthcare", "الرعاية الصحية"),
    ("legal-services", "الخدمات القانونية"),
    ("accounting-firms", "مكاتب المحاسبة"),
    ("construction", "المقاولات"),
    ("automotive", "السيارات"),
    ("beauty-wellness", "التجميل والعناية"),
    ("events-management", "إدارة الفعاليات"),
    ("interior-design", "التصميم الداخلي"),
    ("financial-services", "الخدمات المالية"),
]
SECTOR_IDS = [s[0] for s in SECTORS]

# ---------------------------------------------------------------------------
# 25 Business Needs (taxonomy). Each maps to exactly one core system.
# ---------------------------------------------------------------------------
# (id, name_ar, category, core_system, buyer_role_ar)
NEEDS = [
    ("revenue-leak-detection", "كشف تسرب الإيرادات", "revenue", "revenue-operating-system", "المؤسس / المدير العام"),
    ("slow-lead-response", "بطء الرد على العملاء", "lead-response", "follow-up-recovery-os", "مدير المبيعات"),
    ("missed-followups", "متابعات ضائعة", "follow-up", "follow-up-recovery-os", "مدير المبيعات"),
    ("weak-pipeline-visibility", "ضعف وضوح خط الأنابيب", "visibility", "executive-command-os", "المؤسس / المدير العام"),
    ("low-proposal-winrate", "ضعف قبول العروض", "proposal", "proposal-proof-os", "مدير المبيعات"),
    ("no-proof-of-value", "غياب إثبات القيمة", "proof", "proposal-proof-os", "مدير التسويق"),
    ("whatsapp-chaos", "فوضى واتساب", "channel", "whatsapp-client-os", "مدير خدمة العملاء"),
    ("manual-reporting", "تقارير يدوية متعبة", "reporting", "executive-command-os", "المؤسس / المدير العام"),
    ("inconsistent-pricing", "تسعير غير منضبط", "pricing", "proposal-proof-os", "مدير المبيعات"),
    ("weak-onboarding", "ضعف إدماج العملاء الجدد", "retention", "revenue-operating-system", "مدير العمليات"),
    ("churn-risk", "خطر فقد العملاء", "retention", "revenue-operating-system", "مدير نجاح العملاء"),
    ("no-sales-process", "غياب عملية مبيعات واضحة", "process", "revenue-operating-system", "المؤسس / المدير العام"),
    ("lead-source-blindness", "عمى مصادر العملاء", "visibility", "executive-command-os", "مدير التسويق"),
    ("unqualified-leads", "عملاء غير مؤهّلين", "lead-response", "follow-up-recovery-os", "مدير المبيعات"),
    ("slow-quote-turnaround", "بطء إصدار العروض", "proposal", "proposal-proof-os", "مدير المبيعات"),
    ("weak-upsell", "ضعف البيع الإضافي", "revenue", "revenue-operating-system", "مدير المبيعات"),
    ("team-accountability-gap", "فجوة المساءلة في الفريق", "process", "executive-command-os", "المؤسس / المدير العام"),
    ("no-daily-priorities", "غياب أولويات يومية واضحة", "process", "executive-command-os", "المؤسس / المدير العام"),
    ("customer-data-scatter", "تشتت بيانات العملاء", "data", "revenue-operating-system", "مدير العمليات"),
    ("abandoned-deals", "صفقات مهجورة بلا متابعة", "follow-up", "follow-up-recovery-os", "مدير المبيعات"),
    ("no-case-studies", "غياب قصص النجاح", "proof", "proposal-proof-os", "مدير التسويق"),
    ("inbound-overflow", "تدفق رسائل غير منظّم", "channel", "whatsapp-client-os", "مدير خدمة العملاء"),
    ("appointment-noshow", "غياب العملاء عن المواعيد", "channel", "whatsapp-client-os", "مدير العمليات"),
    ("weak-reactivation", "ضعف إعادة تفعيل العملاء", "follow-up", "follow-up-recovery-os", "مدير المبيعات"),
    ("revenue-forecast-gap", "غياب توقع الإيرادات", "reporting", "executive-command-os", "المؤسس / المدير العام"),
]
NEED_IDS = [n[0] for n in NEEDS]

# ---------------------------------------------------------------------------
# 40 Internal Business Systems (8 specialized per core system).
# These power the engine but are NEVER exposed publicly as a list.
# ---------------------------------------------------------------------------
# core_system -> list of (id, name_ar, complexity)
_SPECIALIZED = {
    "revenue-operating-system": [
        ("sales-process-os", "نظام عملية المبيعات", "medium"),
        ("customer-data-os", "نظام بيانات العملاء الموحّد", "medium"),
        ("onboarding-os", "نظام إدماج العملاء", "low"),
        ("retention-os", "نظام الاحتفاظ بالعملاء", "high"),
        ("upsell-os", "نظام البيع الإضافي", "medium"),
        ("revenue-leak-map", "خريطة تسرب الإيرادات", "low"),
        ("lead-qualification-os", "نظام تأهيل العملاء", "medium"),
        ("revenue-playbook-os", "نظام دليل الإيرادات", "high"),
    ],
    "executive-command-os": [
        ("daily-command-os", "نظام الأوامر اليومية", "low"),
        ("kpi-dashboard-os", "نظام لوحة المؤشرات", "medium"),
        ("pipeline-visibility-os", "نظام وضوح خط الأنابيب", "medium"),
        ("forecast-os", "نظام توقع الإيرادات", "high"),
        ("accountability-os", "نظام المساءلة", "medium"),
        ("lead-source-os", "نظام مصادر العملاء", "low"),
        ("weekly-review-os", "نظام المراجعة الأسبوعية", "low"),
        ("founder-briefing-os", "نظام إحاطة المؤسس", "low"),
    ],
    "follow-up-recovery-os": [
        ("speed-to-lead-os", "نظام سرعة الرد", "low"),
        ("followup-sequence-os", "نظام تسلسل المتابعة", "medium"),
        ("abandoned-deal-os", "نظام الصفقات المهجورة", "medium"),
        ("reactivation-os", "نظام إعادة التفعيل", "medium"),
        ("lead-routing-os", "نظام توجيه العملاء", "medium"),
        ("no-show-recovery-os", "نظام استرجاع الغياب", "low"),
        ("recovery-report-os", "نظام تقرير الاسترجاع", "low"),
        ("followup-quality-os", "نظام جودة المتابعة", "medium"),
    ],
    "whatsapp-client-os": [
        ("whatsapp-inbox-os", "نظام صندوق واتساب", "medium"),
        ("whatsapp-template-os", "نظام قوالب واتساب", "low"),
        ("appointment-os", "نظام المواعيد", "medium"),
        ("broadcast-os", "نظام الإرسال الجماعي المنظّم", "medium"),
        ("inbound-triage-os", "نظام فرز الوارد", "medium"),
        ("whatsapp-handoff-os", "نظام تسليم المحادثات", "low"),
        ("whatsapp-faq-os", "نظام الأسئلة الشائعة", "low"),
        ("whatsapp-report-os", "نظام تقارير واتساب", "low"),
    ],
    "proposal-proof-os": [
        ("proposal-builder-os", "نظام بناء العروض", "medium"),
        ("pricing-os", "نظام التسعير المنضبط", "medium"),
        ("proof-pack-os", "نظام حزمة الإثبات", "medium"),
        ("case-study-os", "نظام قصص النجاح", "low"),
        ("quote-turnaround-os", "نظام سرعة العروض", "low"),
        ("proposal-approval-os", "نظام اعتماد العروض", "low"),
        ("value-report-os", "نظام تقرير القيمة", "medium"),
        ("objection-library-os", "نظام مكتبة الاعتراضات", "low"),
    ],
}

COMPLEXITY_PRICE_SAR = {"low": 2500, "medium": 5000, "high": 9000}
COMPLEXITY_DELIVERABLES = {"low": 3, "medium": 5, "high": 8}
COMPLEXITY_DURATION_DAYS = {"low": 7, "medium": 14, "high": 30}


def iter_specialized_systems():
    """Yield the 40 specialized systems as dicts."""
    for core_id, items in _SPECIALIZED.items():
        for sid, name_ar, complexity in items:
            yield {
                "id": sid,
                "name_ar": name_ar,
                "core_system": core_id,
                "complexity": complexity,
                "starter_price_sar": COMPLEXITY_PRICE_SAR[complexity],
                "deliverables_count": COMPLEXITY_DELIVERABLES[complexity],
                "internal_only": True,
            }


def need_by_id(need_id):
    for nid, name_ar, category, core, buyer in NEEDS:
        if nid == need_id:
            return {
                "id": nid,
                "name_ar": name_ar,
                "category": category,
                "core_system": core,
                "buyer_role_ar": buyer,
            }
    raise KeyError(need_id)


# Sector -> ordered list of the needs that matter most in that sector.
# Deterministic: rotate the needs list so every sector has a distinct top-5.
def sector_need_map():
    mapping = {}
    n = len(NEED_IDS)
    for i, sid in enumerate(SECTOR_IDS):
        top = [NEED_IDS[(i * 3 + k) % n] for k in range(5)]
        # de-dup while preserving order
        seen, ordered = set(), []
        for need in top:
            if need not in seen:
                seen.add(need)
                ordered.append(need)
        mapping[sid] = ordered
    return mapping


# 50 Specialized Sprints = 25 general (one per need) + 25 sector-specialized.
def iter_sprints():
    sprints = []
    # 25 general sprints, one per need
    for idx, need_id in enumerate(NEED_IDS, start=1):
        need = need_by_id(need_id)
        complexity = ["low", "medium", "high"][idx % 3]
        sprints.append(_build_sprint(idx, need, sector_id=None, complexity=complexity))
    # 25 sector-specialized sprints. Walk (sector, need-slot) pairs so 20 sectors
    # still yield exactly 25 distinct sector sprints.
    smap = sector_need_map()
    counter = 26
    for slot in range(2):  # up to 2 needs per sector
        for sid in SECTOR_IDS:
            if counter > 50:
                break
            needs_for_sector = smap[sid]
            if slot >= len(needs_for_sector):
                continue
            need = need_by_id(needs_for_sector[slot])
            complexity = ["medium", "high", "low"][counter % 3]
            sprints.append(_build_sprint(counter, need, sector_id=sid, complexity=complexity))
            counter += 1
        if counter > 50:
            break
    return sprints


def _build_sprint(n, need, sector_id, complexity):
    name_core = need["name_ar"]
    if sector_id:
        sector_ar = dict(SECTORS)[sector_id]
        name_ar = f"سبرنت {name_core} لقطاع {sector_ar}"
    else:
        name_ar = f"سبرنت {name_core}"
    return {
        "id": f"sprint-{n:02d}",
        "name_ar": name_ar,
        "need_id": need["id"],
        "core_system": need["core_system"],
        "sector": sector_id or "general",
        "complexity": complexity,
        "duration_days": COMPLEXITY_DURATION_DAYS[complexity],
        "starter_price_sar": COMPLEXITY_PRICE_SAR[complexity],
        "deliverables": _deliverables_for(need, COMPLEXITY_DELIVERABLES[complexity]),
        "required_inputs": [
            "قائمة عملاء آخر 90 يومًا (CSV) يوفّرها العميل",
            "صلاحية وصول للقناة المستهدفة بموافقة العميل",
            "اسم مسؤول واحد من جهة العميل",
        ],
        "acceptance_criteria": [
            "تسليم كل المخرجات المتفق عليها خلال المدة المحددة",
            f"مؤشر نجاح قابل للقياس مرتبط بـ {need['name_ar']}",
            "اعتماد العميل الكتابي على المخرجات",
        ],
    }


def _deliverables_for(need, count):
    base = [
        f"تشخيص سريع لحالة: {need['name_ar']}",
        "خطة تنفيذ من 30 يومًا",
        "قوالب جاهزة للاستخدام",
        "لوحة متابعة بسيطة",
        "تدريب فريق العميل (جلسة)",
        "تقرير قيمة نهائي",
        "دليل تشغيل مكتوب",
        "مراجعة بعد أسبوعين",
    ]
    return base[:count]
