# -*- coding: utf-8 -*-
"""Canonical Dealix taxonomies (single source of truth for generated assets).

Everything downstream — docs, data files, schemas, reports, account packs,
drafts, proposals — is derived from these seeds so the whole repo stays
internally consistent. Counts here must match scripts/checks/_common.py.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# 5 Core Systems (الأنظمة الخمسة الأساسية)
# --------------------------------------------------------------------------
CORE_SYSTEMS = [
    {
        "id": "revenue_operating_system",
        "name_en": "Revenue Operating System",
        "name_ar": "نظام تشغيل الإيرادات",
        "pain_ar": "لا توجد عملية مبيعات موحدة؛ الفرص تتسرب وخط الأنابيب غير واضح.",
        "ideal_client_ar": "شركة خدمات أو B2B لديها طلب لكن بلا عملية بيع منضبطة.",
        "starter_price": 7500,
        "first_sprint_ar": "بناء خط أنابيب موحد + تأهيل + لوحة متابعة خلال 14 يومًا.",
        "delivery_pack": [
            "خريطة عملية بيع من أول تواصل حتى الإغلاق",
            "نموذج تأهيل (qualification) موحد",
            "قوالب متابعة ورسائل جاهزة",
            "لوحة خط أنابيب أسبوعية",
        ],
        "required_inputs": ["قائمة الخدمات والأسعار", "سجل الفرص الحالية", "صلاحية بريد/واتساب للتواصل"],
        "acceptance_criteria": ["خط أنابيب موحد فعّال", "كل فرصة لها مرحلة وحالة", "تقرير أسبوعي يصدر تلقائيًا"],
        "cta_ar": "ابدأ سبرنت تشغيل الإيرادات",
        "buyer_role_ar": "مدير المبيعات / المؤسس",
        "email_angle_ar": "وقّفنا تسرب الفرص ببناء خط أنابيب واحد واضح خلال أسبوعين.",
    },
    {
        "id": "executive_command_os",
        "name_en": "Executive Command OS",
        "name_ar": "نظام القيادة التنفيذية",
        "pain_ar": "القائد لا يرى الأرقام يوميًا، والقرارات تتأخر بسبب تشتت البيانات.",
        "ideal_client_ar": "مؤسس/مدير عام يريد لوحة قيادة يومية وقرارات مبنية على أرقام.",
        "starter_price": 9000,
        "first_sprint_ar": "لوحة قيادة تنفيذية يومية + تقرير قيمة أسبوعي خلال 14 يومًا.",
        "delivery_pack": [
            "لوحة قيادة يومية (إيراد، فرص، متابعات)",
            "تقرير قيمة أسبوعي للقيادة",
            "بوابات قرار (decision gates) واضحة",
            "تنبيهات على المؤشرات الحرجة",
        ],
        "required_inputs": ["مصادر الأرقام الحالية", "أهداف الربع", "صلاحية قراءة البيانات"],
        "acceptance_criteria": ["لوحة قيادة محدثة يوميًا", "تقرير أسبوعي يصل القيادة", "كل مؤشر له مالك"],
        "cta_ar": "فعّل لوحة القيادة التنفيذية",
        "buyer_role_ar": "المؤسس / المدير العام",
        "email_angle_ar": "أعطيناك رؤية يومية واحدة لكل أرقام الإيراد والمتابعات.",
    },
    {
        "id": "follow_up_recovery_os",
        "name_en": "Follow-up Recovery OS",
        "name_ar": "نظام استعادة المتابعات",
        "pain_ar": "المتابعات بطيئة والعملاء المهتمون يضيعون بلا رد في الوقت المناسب.",
        "ideal_client_ar": "نشاط يستقبل استفسارات كثيرة لكن نسبة المتابعة والإغلاق ضعيفة.",
        "starter_price": 6000,
        "first_sprint_ar": "أتمتة متابعات + استرجاع العملاء الخاملين خلال 10 أيام.",
        "delivery_pack": [
            "تسلسلات متابعة مؤتمتة",
            "حملة استرجاع للعملاء الخاملين",
            "قواعد توقيت وتذكير",
            "قائمة أولوية يومية للمتابعة",
        ],
        "required_inputs": ["سجل العملاء/المهتمين", "قنوات التواصل المسموح بها", "قائمة عدم التواصل (إن وجدت)"],
        "acceptance_criteria": ["لا فرصة بلا متابعة خلال 24 ساعة", "حملة استرجاع تعمل", "قائمة أولوية يومية تصدر"],
        "cta_ar": "أوقف تسرب المتابعات",
        "buyer_role_ar": "مدير المبيعات / خدمة العملاء",
        "email_angle_ar": "استعدنا العملاء المهتمين الذين لم يُتابَعوا في الوقت المناسب.",
    },
    {
        "id": "whatsapp_client_os",
        "name_en": "WhatsApp Client OS",
        "name_ar": "نظام عملاء واتساب",
        "pain_ar": "قناة واتساب فوضوية: ردود متأخرة وطلبات غير موثقة وتجربة حجز ضعيفة.",
        "ideal_client_ar": "نشاط يعتمد على واتساب للاستقبال والحجز والطلب.",
        "starter_price": 5500,
        "first_sprint_ar": "تنظيم قناة واتساب + توثيق الطلبات + ردود منظمة خلال 10 أيام.",
        "delivery_pack": [
            "هيكلة قناة واتساب وتصنيف المحادثات",
            "قوالب رد سريعة موثّقة",
            "مسار حجز/طلب واضح",
            "سجل طلبات موثّق",
        ],
        "required_inputs": ["رقم/حساب واتساب للأعمال", "قائمة الخدمات", "صلاحية الردود"],
        "acceptance_criteria": ["زمن رد أقل", "كل طلب موثّق", "مسار حجز واضح يعمل"],
        "cta_ar": "نظّم قناة واتساب",
        "buyer_role_ar": "مدير العمليات / صاحب النشاط",
        "email_angle_ar": "حوّلنا فوضى واتساب إلى قناة منظمة بطلبات موثّقة وردود أسرع.",
    },
    {
        "id": "proposal_proof_os",
        "name_en": "Proposal & Proof OS",
        "name_ar": "نظام العروض والإثبات",
        "pain_ar": "إعداد العروض بطيء، والتسعير غير واضح، وإثبات النتائج للعميل ضعيف.",
        "ideal_client_ar": "نشاط يقدّم عروضًا مخصّصة ويحتاج إثبات قيمة سريع.",
        "starter_price": 6500,
        "first_sprint_ar": "مصنع عروض مصغّرة + بنك تسعير + تقارير إثبات خلال 12 يومًا.",
        "delivery_pack": [
            "قوالب عروض مصغّرة سريعة",
            "بنك تسعير واضح",
            "تقارير إثبات نتائج",
            "بوابة اعتماد قبل الإرسال",
        ],
        "required_inputs": ["الخدمات والنطاقات", "هيكل التسعير", "أمثلة نتائج سابقة (إن وجدت)"],
        "acceptance_criteria": ["عرض مصغّر يُجهّز في دقائق", "كل عرض له سعر ونطاق", "اعتماد قبل الإرسال إلزامي"],
        "cta_ar": "سرّع عروضك وأثبت قيمتك",
        "buyer_role_ar": "المؤسس / مدير الحسابات",
        "email_angle_ar": "اختصرنا زمن إعداد العروض وأضفنا إثبات قيمة واضح قبل الإرسال.",
    },
]

CORE_SYSTEM_IDS = [s["id"] for s in CORE_SYSTEMS]

# --------------------------------------------------------------------------
# 25 Business Needs (تصنيف الاحتياجات) — each mapped to a core system
# --------------------------------------------------------------------------
# (id, name_ar, category, core_system_id)
NEEDS = [
    ("need_01", "ضعف توليد العملاء المحتملين", "acquisition", "revenue_operating_system"),
    ("need_02", "بطء متابعة العملاء المهتمين", "retention", "follow_up_recovery_os"),
    ("need_03", "تسرّب الصفقات قبل الإغلاق", "conversion", "follow_up_recovery_os"),
    ("need_04", "غياب رؤية تنفيذية للأرقام", "visibility", "executive_command_os"),
    ("need_05", "فوضى قناة واتساب", "operations", "whatsapp_client_os"),
    ("need_06", "ضعف معدل تحويل العروض", "conversion", "proposal_proof_os"),
    ("need_07", "عدم وجود عملية مبيعات موحدة", "operations", "revenue_operating_system"),
    ("need_08", "ضعف الاحتفاظ بالعملاء", "retention", "follow_up_recovery_os"),
    ("need_09", "بطء إعداد العروض", "operations", "proposal_proof_os"),
    ("need_10", "غياب لوحة قيادة يومية", "visibility", "executive_command_os"),
    ("need_11", "تأخر الرد على الاستفسارات", "operations", "whatsapp_client_os"),
    ("need_12", "ضعف تأهيل العملاء", "conversion", "revenue_operating_system"),
    ("need_13", "عدم وضوح خط أنابيب المبيعات", "visibility", "revenue_operating_system"),
    ("need_14", "ضعف إثبات النتائج للعميل", "conversion", "proposal_proof_os"),
    ("need_15", "تشتّت بيانات العملاء", "operations", "executive_command_os"),
    ("need_16", "ضعف استرجاع العملاء الخاملين", "retention", "follow_up_recovery_os"),
    ("need_17", "غياب أتمتة المتابعات", "operations", "follow_up_recovery_os"),
    ("need_18", "ضعف تجربة الحجز عبر واتساب", "conversion", "whatsapp_client_os"),
    ("need_19", "عدم وجود تسعير واضح", "finance", "proposal_proof_os"),
    ("need_20", "ضعف انضباط الفريق على الأهداف", "operations", "executive_command_os"),
    ("need_21", "غياب تقارير قيمة أسبوعية", "visibility", "executive_command_os"),
    ("need_22", "ضعف توثيق الطلبات الواردة", "operations", "whatsapp_client_os"),
    ("need_23", "طول دورة البيع", "conversion", "revenue_operating_system"),
    ("need_24", "ضعف إدارة الاعتراضات", "conversion", "revenue_operating_system"),
    ("need_25", "غياب مسار تأهيل العميل بعد البيع", "retention", "follow_up_recovery_os"),
]

# --------------------------------------------------------------------------
# 20 Sectors (القطاعات) — first 8 have dedicated site solution pages
# --------------------------------------------------------------------------
# (id, slug, name_ar, name_en, has_site_page)
SECTORS = [
    ("sector_01", "marketing-agencies", "وكالات التسويق", "Marketing Agencies", True),
    ("sector_02", "training-companies", "شركات التدريب", "Training Companies", True),
    ("sector_03", "clinics", "العيادات", "Clinics", True),
    ("sector_04", "real-estate", "العقارات", "Real Estate", True),
    ("sector_05", "professional-services", "الخدمات الاحترافية", "Professional Services", True),
    ("sector_06", "recruitment", "التوظيف", "Recruitment", True),
    ("sector_07", "saas", "البرمجيات (SaaS)", "SaaS", True),
    ("sector_08", "logistics", "اللوجستيات", "Logistics", True),
    ("sector_09", "restaurants", "المطاعم والأغذية", "Restaurants & F&B", False),
    ("sector_10", "ecommerce", "التجارة الإلكترونية", "E-commerce", False),
    ("sector_11", "law-firms", "مكاتب المحاماة", "Law Firms", False),
    ("sector_12", "accounting-firms", "مكاتب المحاسبة", "Accounting Firms", False),
    ("sector_13", "construction", "المقاولات", "Construction", False),
    ("sector_14", "education", "التعليم", "Education", False),
    ("sector_15", "healthcare", "الرعاية الصحية", "Healthcare", False),
    ("sector_16", "hospitality", "الضيافة والفنادق", "Hospitality", False),
    ("sector_17", "automotive", "السيارات", "Automotive", False),
    ("sector_18", "fitness", "اللياقة والنوادي", "Fitness", False),
    ("sector_19", "beauty", "التجميل والصالونات", "Beauty & Salons", False),
    ("sector_20", "manufacturing", "التصنيع", "Manufacturing", False),
]

# Top needs per sector (3-4 need ids each). Drives the sector→need matrix.
SECTOR_TOP_NEEDS = {
    "sector_01": ["need_01", "need_06", "need_13", "need_14"],
    "sector_02": ["need_01", "need_02", "need_09", "need_25"],
    "sector_03": ["need_05", "need_11", "need_18", "need_02"],
    "sector_04": ["need_02", "need_03", "need_16", "need_23"],
    "sector_05": ["need_06", "need_09", "need_14", "need_19"],
    "sector_06": ["need_01", "need_12", "need_23", "need_24"],
    "sector_07": ["need_04", "need_10", "need_13", "need_08"],
    "sector_08": ["need_05", "need_11", "need_22", "need_15"],
    "sector_09": ["need_05", "need_11", "need_18", "need_22"],
    "sector_10": ["need_03", "need_16", "need_18", "need_06"],
    "sector_11": ["need_06", "need_09", "need_14", "need_19"],
    "sector_12": ["need_04", "need_10", "need_15", "need_21"],
    "sector_13": ["need_07", "need_13", "need_09", "need_19"],
    "sector_14": ["need_01", "need_02", "need_18", "need_25"],
    "sector_15": ["need_05", "need_11", "need_18", "need_02"],
    "sector_16": ["need_05", "need_11", "need_18", "need_22"],
    "sector_17": ["need_02", "need_03", "need_06", "need_16"],
    "sector_18": ["need_02", "need_16", "need_18", "need_25"],
    "sector_19": ["need_05", "need_11", "need_18", "need_02"],
    "sector_20": ["need_07", "need_13", "need_04", "need_15"],
}

# --------------------------------------------------------------------------
# Delivery variants (أنماط التسليم)
# --------------------------------------------------------------------------
# (id, name_ar, duration_days, price_band_ar, scope_ar)
DELIVERY_VARIANTS = [
    ("variant_diagnostic", "تشخيص", 3, "منخفض", "تشخيص سريع وخطة بدء بلا تنفيذ كامل."),
    ("variant_lite", "خفيف", 7, "منخفض", "تنفيذ مركّز لاحتياج واحد محدد."),
    ("variant_standard", "قياسي", 14, "متوسط", "سبرنت كامل لنظام واحد مع تسليمات معتمدة."),
    ("variant_pro", "احترافي", 21, "مرتفع", "سبرنت موسّع مع تكامل وتقارير قيمة."),
    ("variant_retainer", "اشتراك شهري", 30, "متوسط", "تشغيل وتحسين مستمر شهريًا."),
    ("variant_recovery", "استعادة", 10, "منخفض", "حملة استرجاع وإحياء للعملاء الخاملين."),
]
DELIVERY_VARIANT_IDS = [v[0] for v in DELIVERY_VARIANTS]

# --------------------------------------------------------------------------
# 40 Business Systems (كتالوج الأنظمة الداخلي)
# --------------------------------------------------------------------------
# (name_ar, core_system_id, primary_sector_id, buyer_role_ar, starter_price, complexity)
BUSINESS_SYSTEMS = [
    ("نظام توليد الفرص للوكالات", "revenue_operating_system", "sector_01", "مدير النمو", 7500, "medium"),
    ("نظام إغلاق عروض الوكالات", "proposal_proof_os", "sector_01", "مدير الحسابات", 6500, "medium"),
    ("نظام متابعة المتدربين المحتملين", "follow_up_recovery_os", "sector_02", "مدير المبيعات", 6000, "low"),
    ("نظام تسجيل الدورات", "whatsapp_client_os", "sector_02", "مدير التسجيل", 5500, "low"),
    ("نظام حجوزات العيادات", "whatsapp_client_os", "sector_03", "مدير العيادة", 5500, "medium"),
    ("نظام تذكير المواعيد", "follow_up_recovery_os", "sector_03", "منسق المرضى", 5000, "low"),
    ("نظام متابعة العملاء العقاريين", "follow_up_recovery_os", "sector_04", "مدير المبيعات", 6500, "medium"),
    ("نظام تأهيل المشترين العقاريين", "revenue_operating_system", "sector_04", "مدير المبيعات", 7000, "medium"),
    ("نظام عروض الخدمات الاحترافية", "proposal_proof_os", "sector_05", "الشريك", 7000, "medium"),
    ("نظام تسعير الاستشارات", "proposal_proof_os", "sector_05", "الشريك", 6500, "medium"),
    ("نظام فرز المرشحين", "revenue_operating_system", "sector_06", "مدير التوظيف", 6500, "medium"),
    ("نظام متابعة العملاء التوظيفيين", "follow_up_recovery_os", "sector_06", "مدير الحسابات", 6000, "low"),
    ("نظام لوحة قيادة SaaS", "executive_command_os", "sector_07", "المؤسس", 9000, "high"),
    ("نظام تقليل التسرّب (Churn)", "follow_up_recovery_os", "sector_07", "مدير النجاح", 8000, "high"),
    ("نظام تتبّع شحنات اللوجستيات", "whatsapp_client_os", "sector_08", "مدير العمليات", 6000, "medium"),
    ("نظام توثيق طلبات اللوجستيات", "whatsapp_client_os", "sector_08", "مدير العمليات", 5500, "medium"),
    ("نظام حجوزات المطاعم", "whatsapp_client_os", "sector_09", "مدير الفرع", 5000, "low"),
    ("نظام استرجاع عملاء المتجر", "follow_up_recovery_os", "sector_10", "مدير التسويق", 6000, "medium"),
    ("نظام تحويل سلة المتجر", "proposal_proof_os", "sector_10", "مدير التجارة", 6500, "medium"),
    ("نظام عروض المكاتب القانونية", "proposal_proof_os", "sector_11", "الشريك", 7000, "medium"),
    ("نظام لوحة مكاتب المحاسبة", "executive_command_os", "sector_12", "المدير", 8000, "medium"),
    ("نظام عروض المقاولات", "proposal_proof_os", "sector_13", "مدير المشاريع", 7500, "high"),
    ("نظام خط أنابيب المقاولات", "revenue_operating_system", "sector_13", "مدير التطوير", 8000, "high"),
    ("نظام تسجيل الطلاب", "whatsapp_client_os", "sector_14", "مدير القبول", 5500, "low"),
    ("نظام متابعة أولياء الأمور", "follow_up_recovery_os", "sector_14", "منسق العلاقات", 5500, "low"),
    ("نظام حجوزات الرعاية الصحية", "whatsapp_client_os", "sector_15", "مدير العيادة", 6000, "medium"),
    ("نظام لوحة قيادة الفنادق", "executive_command_os", "sector_16", "مدير الفندق", 8500, "medium"),
    ("نظام حجوزات الضيافة", "whatsapp_client_os", "sector_16", "مدير الحجوزات", 6000, "medium"),
    ("نظام متابعة عملاء السيارات", "follow_up_recovery_os", "sector_17", "مدير المعرض", 6000, "medium"),
    ("نظام عروض السيارات", "proposal_proof_os", "sector_17", "مدير المبيعات", 6500, "medium"),
    ("نظام اشتراكات النوادي", "follow_up_recovery_os", "sector_18", "مدير النادي", 5500, "low"),
    ("نظام حجوزات الصالونات", "whatsapp_client_os", "sector_19", "مدير الصالون", 5000, "low"),
    ("نظام خط أنابيب التصنيع", "revenue_operating_system", "sector_20", "مدير المبيعات", 8500, "high"),
    ("نظام عروض التصنيع", "proposal_proof_os", "sector_20", "مدير الحسابات", 8000, "high"),
    ("نظام القيادة التنفيذية الموحّد", "executive_command_os", "sector_05", "المؤسس", 9000, "medium"),
    ("نظام تقارير القيمة الأسبوعية", "executive_command_os", "sector_01", "المؤسس", 7000, "low"),
    ("نظام أتمتة المتابعة العامة", "follow_up_recovery_os", "sector_05", "مدير المبيعات", 6000, "low"),
    ("نظام بنك التسعير", "proposal_proof_os", "sector_05", "المؤسس", 6000, "low"),
    ("نظام تأهيل ما بعد البيع", "follow_up_recovery_os", "sector_07", "مدير النجاح", 6500, "medium"),
    ("نظام مركز قيادة المبيعات", "revenue_operating_system", "sector_06", "مدير المبيعات", 8000, "high"),
]

# --------------------------------------------------------------------------
# 50 Specialized Sprints (مكتبة السبرنتات المتخصصة)
# --------------------------------------------------------------------------
# (name_ar, need_id, sector_id, variant_id)  — system derived from need.
SPRINTS = [
    ("سبرنت توليد فرص الوكالات", "need_01", "sector_01", "variant_standard"),
    ("سبرنت تحويل عروض الوكالات", "need_06", "sector_01", "variant_standard"),
    ("سبرنت وضوح خط أنابيب الوكالات", "need_13", "sector_01", "variant_lite"),
    ("سبرنت إثبات نتائج الوكالات", "need_14", "sector_01", "variant_lite"),
    ("سبرنت توليد فرص التدريب", "need_01", "sector_02", "variant_standard"),
    ("سبرنت متابعة المتدربين", "need_02", "sector_02", "variant_recovery"),
    ("سبرنت تسريع عروض التدريب", "need_09", "sector_02", "variant_lite"),
    ("سبرنت تأهيل ما بعد التدريب", "need_25", "sector_02", "variant_standard"),
    ("سبرنت تنظيم واتساب العيادات", "need_05", "sector_03", "variant_standard"),
    ("سبرنت ردود العيادات السريعة", "need_11", "sector_03", "variant_lite"),
    ("سبرنت حجوزات العيادات", "need_18", "sector_03", "variant_standard"),
    ("سبرنت تذكير مواعيد العيادات", "need_02", "sector_03", "variant_recovery"),
    ("سبرنت متابعة العملاء العقاريين", "need_02", "sector_04", "variant_recovery"),
    ("سبرنت استرجاع العقاريين الخاملين", "need_16", "sector_04", "variant_recovery"),
    ("سبرنت تقصير دورة البيع العقاري", "need_23", "sector_04", "variant_standard"),
    ("سبرنت منع تسرّب الصفقات العقارية", "need_03", "sector_04", "variant_standard"),
    ("سبرنت عروض الخدمات الاحترافية", "need_06", "sector_05", "variant_standard"),
    ("سبرنت تسريع عروض الاستشارات", "need_09", "sector_05", "variant_lite"),
    ("سبرنت إثبات قيمة الاستشارات", "need_14", "sector_05", "variant_lite"),
    ("سبرنت تسعير الخدمات الاحترافية", "need_19", "sector_05", "variant_diagnostic"),
    ("سبرنت توليد فرص التوظيف", "need_01", "sector_06", "variant_standard"),
    ("سبرنت تأهيل عملاء التوظيف", "need_12", "sector_06", "variant_lite"),
    ("سبرنت تقصير دورة بيع التوظيف", "need_23", "sector_06", "variant_standard"),
    ("سبرنت معالجة اعتراضات التوظيف", "need_24", "sector_06", "variant_lite"),
    ("سبرنت لوحة قيادة SaaS", "need_10", "sector_07", "variant_pro"),
    ("سبرنت رؤية أرقام SaaS", "need_04", "sector_07", "variant_standard"),
    ("سبرنت تقليل تسرّب SaaS", "need_08", "sector_07", "variant_pro"),
    ("سبرنت وضوح خط أنابيب SaaS", "need_13", "sector_07", "variant_lite"),
    ("سبرنت تنظيم واتساب اللوجستيات", "need_05", "sector_08", "variant_standard"),
    ("سبرنت ردود اللوجستيات السريعة", "need_11", "sector_08", "variant_lite"),
    ("سبرنت توثيق طلبات اللوجستيات", "need_22", "sector_08", "variant_standard"),
    ("سبرنت توحيد بيانات اللوجستيات", "need_15", "sector_08", "variant_standard"),
    ("سبرنت حجوزات المطاعم", "need_18", "sector_09", "variant_lite"),
    ("سبرنت ردود المطاعم", "need_11", "sector_09", "variant_lite"),
    ("سبرنت استرجاع عملاء المتجر", "need_16", "sector_10", "variant_recovery"),
    ("سبرنت تحويل سلة المتجر", "need_06", "sector_10", "variant_standard"),
    ("سبرنت منع تسرّب طلبات المتجر", "need_03", "sector_10", "variant_standard"),
    ("سبرنت عروض المكاتب القانونية", "need_06", "sector_11", "variant_standard"),
    ("سبرنت تسعير الخدمات القانونية", "need_19", "sector_11", "variant_diagnostic"),
    ("سبرنت لوحة مكاتب المحاسبة", "need_10", "sector_12", "variant_standard"),
    ("سبرنت تقارير قيمة المحاسبة", "need_21", "sector_12", "variant_lite"),
    ("سبرنت عروض المقاولات", "need_09", "sector_13", "variant_standard"),
    ("سبرنت خط أنابيب المقاولات", "need_13", "sector_13", "variant_pro"),
    ("سبرنت تسجيل الطلاب", "need_18", "sector_14", "variant_lite"),
    ("سبرنت متابعة أولياء الأمور", "need_02", "sector_14", "variant_recovery"),
    ("سبرنت حجوزات الرعاية الصحية", "need_18", "sector_15", "variant_standard"),
    ("سبرنت لوحة قيادة الفنادق", "need_10", "sector_16", "variant_standard"),
    ("سبرنت متابعة عملاء السيارات", "need_02", "sector_17", "variant_recovery"),
    ("سبرنت اشتراكات النوادي", "need_25", "sector_18", "variant_standard"),
    ("سبرنت حجوزات الصالونات", "need_18", "sector_19", "variant_lite"),
]

# --------------------------------------------------------------------------
# Signal → Need library (إشارات تدل على احتياج)
# --------------------------------------------------------------------------
# (signal_ar, need_id, evidence_level)
SIGNALS = [
    ("نموذج تواصل بلا رد آلي", "need_11", "high"),
    ("لا يوجد رقم واتساب أعمال واضح", "need_05", "medium"),
    ("صفحة أسعار غير موجودة", "need_19", "high"),
    ("لا توجد صفحة حجز", "need_18", "high"),
    ("إعلانات نشطة بلا صفحة هبوط", "need_01", "medium"),
    ("شكاوى عن تأخر الرد في المراجعات", "need_11", "high"),
    ("لا يوجد إثبات نتائج أو دراسات حالة", "need_14", "medium"),
    ("فريق مبيعات بلا CRM ظاهر", "need_07", "medium"),
    ("توسّع في التوظيف (مبيعات)", "need_13", "low"),
    ("منتج SaaS بلا لوحة مؤشرات", "need_10", "medium"),
    ("معدل مغادرة مرتفع في المراجعات", "need_08", "medium"),
    ("عروض تُرسل يدويًا وببطء", "need_09", "medium"),
    ("قائمة عملاء خاملين كبيرة", "need_16", "low"),
    ("استفسارات كثيرة على واتساب بلا تنظيم", "need_22", "high"),
    ("غياب تقارير دورية للقيادة", "need_21", "low"),
    ("تعدّد قنوات بلا توحيد بيانات", "need_15", "medium"),
    ("اعتراضات سعرية متكررة", "need_24", "low"),
    ("دورة بيع طويلة معلنة", "need_23", "low"),
    ("لا يوجد مسار ما بعد البيع", "need_25", "low"),
    ("ضعف تأهيل الفرص الواردة", "need_12", "medium"),
    ("تسرّب واضح في مرحلة التفاوض", "need_03", "medium"),
    ("لا توجد لوحة قيادة تنفيذية", "need_04", "medium"),
    ("بطء متابعة بعد أول تواصل", "need_02", "high"),
    ("ضعف عملية التحويل من زائر لعميل", "need_06", "medium"),
    ("غياب أتمتة المتابعة", "need_17", "medium"),
    ("ضعف توليد الفرص رغم وجود طلب", "need_01", "medium"),
    ("عدم وضوح خط الأنابيب", "need_13", "medium"),
    ("ضعف انضباط الفريق على الأهداف", "need_20", "low"),
    ("طلبات غير موثّقة", "need_22", "medium"),
    ("تجربة حجز مربكة", "need_18", "medium"),
]

# Sample client roster used by delivery/finance demos (clearly synthetic).
SAMPLE_CLIENTS = [
    ("عميل تجريبي 01", "sector_01", "revenue_operating_system"),
    ("عميل تجريبي 02", "sector_03", "whatsapp_client_os"),
    ("عميل تجريبي 03", "sector_04", "follow_up_recovery_os"),
    ("عميل تجريبي 04", "sector_05", "proposal_proof_os"),
    ("عميل تجريبي 05", "sector_07", "executive_command_os"),
    ("عميل تجريبي 06", "sector_02", "follow_up_recovery_os"),
    ("عميل تجريبي 07", "sector_08", "whatsapp_client_os"),
    ("عميل تجريبي 08", "sector_06", "revenue_operating_system"),
    ("عميل تجريبي 09", "sector_11", "proposal_proof_os"),
    ("عميل تجريبي 10", "sector_12", "executive_command_os"),
]


def need_by_id() -> dict:
    return {n[0]: {"id": n[0], "name_ar": n[1], "category": n[2], "core_system": n[3]} for n in NEEDS}


def sector_by_id() -> dict:
    return {s[0]: {"id": s[0], "slug": s[1], "name_ar": s[2], "name_en": s[3], "has_site_page": s[4]} for s in SECTORS}


def core_by_id() -> dict:
    return {s["id"]: s for s in CORE_SYSTEMS}
