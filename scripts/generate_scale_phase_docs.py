#!/usr/bin/env python3
"""Generate docs/26_service_catalog … docs/44_ventures (Repeatability → Venture path).

Run: py -3 scripts/generate_scale_phase_docs.py

Complements docs/00–25 from generate_layered_execution_docs.py; links back to
docs/strategic/DEALIX_EXECUTION_WAVES_AR.md and master blueprint.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SEE = """
## روابط

- [DEALIX_EXECUTION_WAVES_AR.md](../strategic/DEALIX_EXECUTION_WAVES_AR.md)
- [DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md](../from_zero/DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md)
"""


def md(title: str, role: str, bullets: list[str]) -> str:
    b = "\n".join(f"- {x}" for x in bullets)
    return textwrap.dedent(
        f"""# {title}

## الدور

{role}

## نقاط تشغيلية

{b}
{SEE}
""",
    ).strip() + "\n"


SPECS: list[tuple[str, str, list[tuple[str, str, str, list[str]]]]] = [
    (
        "26_service_catalog",
        "Service Catalog — عروض محددة قابلة للتكرار",
        [
            (
                "SERVICE_CATALOG.md",
                "كتالوج الخدمات",
                "كل عرض له نطاق ومدخلات ومخرجات وProof metrics ومسار Retainer.",
                ["لا عروض مفتوحة", "Exclusions صريحة", "Price logic مرتبط بالمخاطر"],
            ),
            (
                "CAPABILITY_DIAGNOSTIC_SERVICE.md",
                "خدمة التشخيص",
                "Who / Problem / Inputs / Deliverables / Exclusions / Proof / Retainer.",
                ["للمؤسسين الذين يريدون وضوحًا قبل Sprint"],
            ),
            (
                "REVENUE_INTELLIGENCE_SPRINT_SERVICE.md",
                "خدمة Revenue Intelligence Sprint",
                "B2B سعودي ببيانات حسابات فوضوية → أولويات + مسودات + Proof.",
                ["No scraping", "No cold WhatsApp", "No guaranteed sales"],
            ),
            (
                "DATA_READINESS_SPRINT_SERVICE.md",
                "خدمة جاهزية البيانات",
                "Source Passport + جودة + تطبيع قبل أي AI تشغيلي.",
                ["No Source Passport = no AI"],
            ),
            (
                "COMPANY_BRAIN_SPRINT_SERVICE.md",
                "خدمة Company Brain Sprint",
                "تجميع معرفة داخلية محكومة (بدون مصادر مجهولة).",
                ["Source clarity", "Governed excerpts"],
            ),
            (
                "AI_GOVERNANCE_REVIEW_SERVICE.md",
                "خدمة مراجعة حوكمة AI",
                "سياسات قنوات + موافقات + سجل قرارات.",
                ["Runtime governance alignment"],
            ),
            (
                "MONTHLY_REVOPS_OS_SERVICE.md",
                "خدمة RevOps شهرية",
                "Cadence + تقارير قيمة ملاحظة + فرص مرتبة.",
                ["يعتمد على Proof وAdoption"],
            ),
            (
                "MONTHLY_GOVERNANCE_OS_SERVICE.md",
                "خدمة حوكمة شهرية",
                "مراجعة سياسات + موافقات + مخاطر.",
                ["لا إرسال خارجي بدون أثر موافقة"],
            ),
            (
                "SERVICE_EXCLUSIONS.md",
                "استثناءات الخدمة",
                "قائمة موحدة لما لا نفعله في أي عرض.",
                ["Spam / automation outbound / fake proof"],
            ),
        ],
    ),
    (
        "27_delivery_playbooks",
        "Delivery Playbooks — تسليم كخطوات",
        [
            (
                "DELIVERY_PLAYBOOKS.md",
                "مكتبة Playbooks",
                "تحويل التسليم من اجتهاد إلى مسار قابل للتدريب.",
                ["Intake → Proof → Handoff"],
            ),
            (
                "REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md",
                "Playbook تسليم Revenue Intelligence",
                "Import → Score → Draft pack → Governance → QA → Proof → Retainer rec.",
                ["كل مرحلة لها مالك ومدخل ومخرج"],
            ),
            (
                "DATA_READINESS_DELIVERY_PLAYBOOK.md",
                "Playbook جاهزية البيانات",
                "Preview → PII → dedupe → passport → gate.",
                ["Cleanup قبل scoring عند الحاجة"],
            ),
            (
                "COMPANY_BRAIN_DELIVERY_PLAYBOOK.md",
                "Playbook Company Brain",
                "جمع مصادر داخلية + تلخيص محكوم.",
                ["No source-less answers"],
            ),
            (
                "GOVERNANCE_REVIEW_DELIVERY_PLAYBOOK.md",
                "Playbook مراجعة الحوكمة",
                "Policy registry + channel policy + claim safety.",
                ["قرارات مسجلة"],
            ),
            (
                "DELIVERY_QA_CHECKLIST.md",
                "QA للتسليم",
                "قبل تسليم العميل: اكتمال الأقسام + حوكمة + لغة آمنة.",
                ["Proof Pack completeness"],
            ),
            (
                "CLIENT_HANDOFF_CHECKLIST.md",
                "تسليم للعميل",
                "ما يُسلَّم وما يبقى داخليًا + خطوات الموافقة.",
                ["Draft-only posture"],
            ),
        ],
    ),
    (
        "28_change_requests",
        "Change Request System — منع scope creep",
        [
            (
                "CHANGE_REQUEST_SYSTEM.md",
                "نظام طلبات التغيير",
                "كل طلب جديد يُصنَّف: included / minor / add-on / sprint / backlog / rejected.",
                ["يحمي الهامش"],
            ),
            (
                "CHANGE_REQUEST_TYPES.md",
                "أنواع الطلبات",
                "تعريفات حتمية لتقليل الجدل.",
                ["Included vs add-on"],
            ),
            (
                "CHANGE_REQUEST_PRICING.md",
                "تسعير التغييرات",
                "ربط التصنيف بالسعر أو بالـ backlog.",
                ["لا خصم قبل تقليل النطاق"],
            ),
            (
                "RETAINER_BACKLOG_POLICY.md",
                "سياسة backlog للـRetainer",
                "ما يُؤجل للاشتراك الشهري.",
                ["شفافية مع العميل"],
            ),
            (
                "SCOPE_BOUNDARY_RULES.md",
                "حدود النطاق",
                "قواعد رفض أو إعادة صياغة.",
                ["Good revenue filter"],
            ),
        ],
    ),
    (
        "29_sales_os",
        "Sales OS — تأهيل وعروض واعتراضات",
        [
            (
                "SALES_QUALIFICATION.md",
                "تأهيل المبيعات",
                "أسئلة: ألم واضح؟ owner؟ بيانات؟ قبول حوكمة؟ ميزانية؟ proof path؟",
                ["قرارات: Accept / Diagnostic / Reframe / Reject / Refer"],
            ),
            (
                "ICP_SCORECARD.md",
                "بطاقة ICP",
                "قطاع + حجم + نضج بيانات + استعداد حوكمة.",
                ["يقلل العملاء المرهقين"],
            ),
            (
                "CLIENT_RISK_SCORECARD.md",
                "مخاطر العميل",
                "طلبات غير آمنة، ضغط وعود، بيانات ناقصة.",
                ["رفض مبكر"],
            ),
            (
                "GOOD_REVENUE_BAD_REVENUE.md",
                "إيراد جيد وسيئ",
                "يربط المبيعات بـCapital وProof.",
                ["Bad revenue = تآكل ثقة"],
            ),
            (
                "DISCOVERY_CALL_SCRIPT.md",
                "سكربت Discovery",
                "أسئلة عربية/إنجليزية بثقة منخفضة ادعاء.",
                ["يؤدي إلى Sprint محدد"],
            ),
            (
                "QUALIFICATION_DECISION_TREE.md",
                "شجرة قرار التأهيل",
                "ربط الإجابات بالمسار التالي.",
                ["حتمي قدر الإمكان"],
            ),
            (
                "PROPOSAL_OS.md",
                "نظام العروض",
                "هيكل موحد: Problem → Sprint → Scope → Governance → Proof → Timeline → Price.",
                [],
            ),
            (
                "PROPOSAL_TEMPLATE_REVENUE_INTELLIGENCE.md",
                "قالب عرض Revenue Intelligence",
                "جملة أساسية: لا نعد مبيعات؛ نبني قدرة محكومة وProof.",
                ["Exclusions واضحة"],
            ),
            (
                "PROPOSAL_TEMPLATE_DATA_READINESS.md",
                "قالب عرض جاهزية البيانات",
                "Passport + جودة + خطة تنظيف.",
                [],
            ),
            (
                "PROPOSAL_TEMPLATE_AI_GOVERNANCE.md",
                "قالب عرض حوكمة AI",
                "سياسات + موافقات + سجلات.",
                [],
            ),
            (
                "PROPOSAL_EXCLUSIONS.md",
                "استثناءات العرض",
                "نفس الممنوعات غير القابلة للتفاوض.",
                [],
            ),
            (
                "PROPOSAL_PROOF_METRICS.md",
                "مقاييس Proof في العرض",
                "ما سيُقاس بنهاية Sprint.",
                [],
            ),
            (
                "OBJECTION_HANDLING.md",
                "التعامل مع الاعتراضات",
                "تحويل الاعتراض إلى ثقة لا دفاع.",
                [],
            ),
            (
                "OBJECTION_NO_WHATSAPP_AUTOMATION.md",
                "اعتراض: واتساب آلي",
                "رد: لا spam؛ مسودات وموافقة بشرية.",
                [],
            ),
            (
                "OBJECTION_NO_SCRAPING.md",
                "اعتراض: scraping",
                "رد: بيانات بلا مصدر = لا outreach.",
                [],
            ),
            (
                "OBJECTION_NO_GUARANTEED_SALES.md",
                "اعتراض: ضمان مبيعات",
                "رد: Proof وقياس لا وعود.",
                [],
            ),
            (
                "OBJECTION_PRICE_TOO_HIGH.md",
                "اعتراض: السعر",
                "رد: تقليل النطاق قبل الخصم.",
                [],
            ),
            (
                "OBJECTION_WHY_PROOF_PACK.md",
                "اعتراض: لماذا Proof Pack",
                "رد: أصل مبيعات وحوكمة.",
                [],
            ),
            (
                "OBJECTION_WHY_APPROVALS.md",
                "اعتراض: الموافقات",
                "رد: حدود قانونية وتشغيلية.",
                [],
            ),
        ],
    ),
    (
        "30_pricing",
        "Pricing Architecture — قيمة ومخاطر",
        [
            ("PRICING_ARCHITECTURE.md", "هندسة التسعير", "قيمة + مخاطر + عمق حوكمة + تكرار.", []),
            ("DIAGNOSTIC_PRICING.md", "تسعير تشخيصي", "منخفض المخاطر، يؤهل للـSprint.", []),
            ("SPRINT_PRICING.md", "تسعير Sprint", "مرتبط بنطاق مخرجات محدد.", []),
            ("RETAINER_PRICING.md", "تسعير Retainer", "Cadence + تقارير + حوكمة.", []),
            ("ENTERPRISE_PRICING.md", "تسعير Enterprise", "حوكمة أعمق + أدلة + procurement.", []),
            ("PRICE_INCREASE_RULES.md", "قواعد رفع السعر", "عند زيادة النطاق أو العمق.", []),
            ("DISCOUNT_POLICY.md", "سياسة الخصم", "لا خصم قبل تقليل النطاق.", []),
        ],
    ),
    (
        "31_operating_finance",
        "Operating Finance — نموذج مالي ووحدة اقتصادية",
        [
            ("FINANCIAL_MODEL.md", "النموذج المالي", "عرض × هامش × تكلفة تسليم × AI.", []),
            ("OFFER_UNIT_ECONOMICS.md", "اقتصاديات وحدة العرض", "ساعات + QA + حوكمة.", []),
            ("GROSS_MARGIN_BY_OFFER.md", "هامش إجمالي لكل عرض", "قرارات رفع سعر أو إيقاف عرض.", []),
            ("RETAINER_ECONOMICS.md", "اقتصاديات Retainer", "MRR مقابل عبء التسليم.", []),
            ("DELIVERY_COST_MODEL.md", "نموذج تكلفة التسليم", "ساعات تشغيل بشرية.", []),
            ("AI_COST_MODEL.md", "نموذج تكلفة AI", "توجيه نماذج + حدود تكلفة.", []),
            ("AI_COST_ACCOUNTING.md", "محاسبة تكلفة AI", "لكل تشغيل / مسودة / Proof pack.", []),
            ("MODEL_ROUTING_COSTS.md", "تكاليف التوجيه", "رخيص للمعالجة الآمنة، مميز للعربية التنفيذية.", []),
            ("COST_PER_OUTPUT.md", "تكلفة لكل مخرج", "قابل للتتبع.", []),
            ("COST_PER_PROOF_PACK.md", "تكلفة لكل Proof Pack", "للمقارنة بين العملاء.", []),
            ("COST_GUARD_POLICY.md", "سياسة حماية التكلفة", "حدود قبل تشغيل نماذج باهظة.", []),
            ("MARGIN_PROTECTION.md", "حماية الهامش", "رفع سعر / تقليل نطاق / add-on.", []),
            ("LOW_MARGIN_DECISION_RULES.md", "قرارات هامش منخفض", "لا تكبر بخسارة.", []),
            ("SCOPE_REDUCTION_POLICY.md", "تقليل النطاق", "بديل للخصم.", []),
            ("REPRICE_POLICY.md", "إعادة تسعير", "عند تغير المخاطر.", []),
        ],
    ),
    (
        "32_enterprise_readiness",
        "Enterprise Readiness — أسئلة أمن وثقة",
        [
            ("SECURITY_QUESTIONNAIRE_PACK.md", "حزمة استبيان الأمن", "إجابات جاهزة: تخزين، وصول، logs، subprocessors.", []),
            ("DATA_HANDLING_SUMMARY.md", "ملخص التعامل مع البيانات", "PDPL-aware language.", []),
            ("MODEL_PROVIDER_SUMMARY.md", "ملخص مزودي النماذج", "شفافية.", []),
            ("INCIDENT_RESPONSE_SUMMARY.md", "الاستجابة للحوادث", "مختصر تشغيلي.", []),
            ("DELETION_PROCESS.md", "عملية الحذف", "Retention + حذف بعد المشروع.", []),
            ("SUBPROCESSOR_LIST.md", "قائمة subprocessors", "قابلة للتحديث.", []),
            ("ACCESS_CONTROL_SUMMARY.md", "التحكم بالوصول", "أدوار وموافقات.", []),
            (
                "ENTERPRISE_TRUST_DATA_ROOM.md",
                "غرفة أدلة الثقة",
                "مكان واحد: Trust Pack + تقارير + عينات Proof.",
                [],
            ),
            ("TRUST_PACK_INDEX.md", "فهرس Trust Pack", "روابط موحدة.", []),
            ("AUDIT_SUMMARIES.md", "ملخصات تدقيق", "قرارات وسياسات.", []),
            ("COMPLIANCE_REPORTS.md", "تقارير امتثال", "قوالب.", []),
            ("INCIDENT_LOG_TEMPLATE.md", "قالب سجل حوادث", "", []),
            ("APPROVAL_WORKFLOW_SUMMARY.md", "ملخص موافقات", "Human-in-the-loop.", []),
        ],
    ),
    (
        "33_enterprise_rollout",
        "Enterprise Rollout — Land → Institutionalize",
        [
            ("ENTERPRISE_ROLLOUT_MODEL.md", "نموذج التوسع", "Pilot محكوم ثم Expand.", []),
            ("LAND_PROVE_ADOPT_EXPAND.md", "مراحل Land…Expand", "بوابات واضحة.", []),
            ("DEPARTMENT_ROLLOUT_MODEL.md", "توسع أقسام", "واحد تلو الآخر.", []),
            ("ENTERPRISE_GATES.md", "بوابات Enterprise", "Sponsor / Data / Workflow / Governance / Proof / Adoption / Retainer.", []),
            ("PLATFORM_PULL_SIGNALS.md", "إشارات سحب المنصة", "متى يطلب العميل workspace أوسع.", []),
        ],
    ),
    (
        "34_ai_estate",
        "AI Estate — جرد واستخدامات",
        [
            ("AI_ESTATE_MAPPING.md", "خريطة AI Estate", "نماذج + وكلاء + RAG + أدواء + بشر.", []),
            ("AI_INVENTORY.md", "جرد AI", "مالك لكل أصل.", []),
            ("SHADOW_AI_REVIEW.md", "مراجعة Shadow AI", "اكتشاف استخدام خارج الحوكمة.", []),
            ("USE_CASE_PORTFOLIO.md", "محفظة use cases", "أولويات وتكرار.", []),
            ("AI_ESTATE_RISK_MAP.md", "خريطة مخاطر", "ربط بالأدلة.", []),
        ],
    ),
    (
        "35_agent_iam",
        "Agent IAM — هوية وصلاحيات الوكيل",
        [
            ("AGENT_IAM.md", "هوية وصول الوكلاء", "No identity = no agent.", []),
            ("AGENT_IDENTITY_MODEL.md", "نموذج الهوية", "بطاقة وكيل + مالك.", []),
            ("AGENT_ACCESS_MODEL.md", "نموذج الوصول", "حدود أدوات وبيانات.", []),
            ("AGENT_SESSION_CONTROL.md", "جلسات", "نطاق جلسة قبل tools.", []),
            ("AGENT_CHAIN_CONTROL.md", "سلاسل sub-agents", "مساءلة السلسلة.", []),
            ("AGENT_PERMISSION_REVIEW.md", "مراجعة صلاحيات", "دوريًا.", []),
        ],
    ),
    (
        "36_agent_runtime_security",
        "Agent Runtime Security — أربع حدود",
        [
            ("AGENT_RUNTIME_SECURITY.md", "أمان وقت التشغيل", "Runtime policy enforcement.", []),
            ("FOUR_BOUNDARY_PROTECTION.md", "أربع حدود", "Prompt / Tool / Data / Context.", []),
            ("PROMPT_INTEGRITY.md", "سلامة الـPrompt", "إصدارات وتسجيل.", []),
            ("TOOL_BOUNDARY.md", "حد الأداة", "Deny-list واضح.", []),
            ("DATA_BOUNDARY.md", "حد البيانات", "PII + passport.", []),
            ("CONTEXT_BOUNDARY.md", "حد السياق", "منع تسرّب سياق غير مصرح.", []),
            ("RUNTIME_POLICY_ENFORCEMENT.md", "فرض سياسات", "ليس مجرد guardrails احتمالية.", []),
        ],
    ),
    (
        "37_saudi_layer",
        "Saudi Layer — تميز محلي",
        [
            ("SAUDI_SECTOR_INTELLIGENCE.md", "ذكاء قطاعات سعودي", "سياق B2B.", []),
            ("SAUDI_SECTOR_TAXONOMY.md", "تصنيف قطاعات", "توحيد التسميات.", []),
            ("CITY_REGION_NORMALIZATION.md", "مدن ومناطق", "توحيد للـscoring.", []),
            ("SAUDI_B2B_CONTEXT.md", "سياق B2B", "لغة سوق.", []),
            ("SAUDI_OPEN_DATA_USAGE.md", "بيانات مفتوحة", "سياق فقط — ليس موافقة تواصل.", []),
            ("ARABIC_EXECUTIVE_QA.md", "QA عربي تنفيذي", "نبرة مديريات.", []),
            ("ARABIC_STYLE_GUIDE.md", "دليل أسلوب عربي", "وضوح دون مبالغة.", []),
            ("FORBIDDEN_ARABIC_CLAIMS.md", "ممنوعات لغوية", "نضمن/نتائج مؤكدة…", []),
            ("PROOF_SAFE_ARABIC_LANGUAGE.md", "عربي آمن للإثبات", "Proof-safe.", []),
            ("BILINGUAL_REPORTING.md", "تقارير ثنائية اللغة", "AR + EN عند الحاجة.", []),
        ],
    ),
    (
        "38_standards",
        "Dealix Standard — معيار التشغيل",
        [
            ("DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md", "المعيار الرئيسي", "Data→Workflow→AI→Governance→Proof→Cadence.", []),
            ("SOURCE_PASSPORT_STANDARD.md", "معيار جواز المصدر", "حقول دنيا.", []),
            ("RUNTIME_GOVERNANCE_STANDARD.md", "معيار حوكمة وقت التشغيل", "قرارات مسجلة.", []),
            ("PROOF_PACK_STANDARD.md", "معيار Proof Pack", "أقسام v2/v3.", []),
            ("AGENT_CONTROL_STANDARD.md", "معيار تحكم بالوكلاء", "IAM + runtime.", []),
            ("OPERATING_CADENCE_STANDARD.md", "معيار إيقاع تشغيل", "شهري/أسبوعي.", []),
        ],
    ),
    (
        "39_academy",
        "Academy — بعد تراكم Proof",
        [
            ("ACADEMY_STRATEGY.md", "استراتيجية الأكاديمية", "لا تبدأ قبل 10+ مشاريع و3+ أصول Proof.", []),
            ("AI_OPS_EXECUTIVE_TRACK.md", "مسار تنفيذيين", "", []),
            ("REVENUE_AI_OPERATOR_TRACK.md", "مسار مشغل إيراد", "", []),
            ("AI_GOVERNANCE_LEAD_TRACK.md", "مسار قيادة حوكمة", "", []),
            ("DEALIX_CERTIFIED_PARTNER_TRACK.md", "شريك معتمد", "Partner covenant.", []),
        ],
    ),
    (
        "40_partners",
        "Partner Ecosystem",
        [
            ("PARTNER_ECOSYSTEM.md", "نظام الشركاء", "توسع بلا فقدان سيطرة.", []),
            ("PARTNER_COVENANT.md", "عهد الشريك", "No unsafe automation; Proof required.", []),
            ("PARTNER_SCORE.md", "تسجيل شريك", "جودة امتثال.", []),
            ("PARTNER_ENABLEMENT_KIT.md", "عدة تمكين", "قوالب + QA.", []),
            ("PARTNER_SUSPENSION_POLICY.md", "تعليق شريك", "عند كسر العهد.", []),
        ],
    ),
    (
        "41_benchmarks",
        "Benchmark Engine",
        [
            ("BENCHMARK_ENGINE.md", "محرك Benchmark", "Aggregated + anonymized + methodology.", []),
            ("SAUDI_AI_OPERATIONS_READINESS_REPORT.md", "تقرير جاهزية", "سوق سعودي.", []),
            ("SAUDI_B2B_REVENUE_READINESS_BENCHMARK.md", "Benchmark إيراد", "", []),
            ("AI_GOVERNANCE_GAP_REPORT.md", "فجوات حوكمة", "", []),
            ("ARABIC_AI_OUTPUT_QUALITY_REPORT.md", "جودة مخرجات عربية", "", []),
        ],
    ),
    (
        "42_market_power",
        "Market Power OS",
        [
            ("MARKET_POWER_OS.md", "قوة السوق", "اللغة والفئة.", []),
            ("CATEGORY_METRICS.md", "مقاييس الفئة", "بحث عن Proof pack / governance.", []),
            ("LANGUAGE_TRACKING.md", "تتبع لغة", "هل السوق ينسخ لغتك.", []),
            ("COMPETITOR_COPY_SIGNALS.md", "إشارات نسخ", "بحذر ومنهجية.", []),
            ("INBOUND_QUALITY_METRICS.md", "جودة inbound", "تأهيل أعلى.", []),
        ],
    ),
    (
        "43_business_units",
        "Business Unit Architecture",
        [
            ("BUSINESS_UNIT_ARCHITECTURE.md", "هندسة الوحدات", "Revenue / Brain / Governance / Ops / Academy / Ventures.", []),
            ("DEALIX_REVENUE.md", "وحدة الإيراد", "", []),
            ("DEALIX_BRAIN.md", "وحدة المعرفة", "", []),
            ("DEALIX_GOVERNANCE.md", "وحدة الحوكمة", "", []),
            ("DEALIX_OPERATIONS.md", "وحدة التشغيل", "", []),
            ("DEALIX_ACADEMY.md", "وحدة الأكاديمية", "", []),
            ("DEALIX_VENTURES.md", "وحدة المشاريع الاستثمارية", "", []),
        ],
    ),
    (
        "44_ventures",
        "Venture Gate — مسار القابضة",
        [
            ("VENTURE_OS.md", "نظام المشاريع", "Spinout منضبط.", []),
            ("VENTURE_GATE.md", "بوابة Venture", "عملاء + retainers + proof scores.", []),
            ("SPINOUT_CRITERIA.md", "معايير Spinout", "", []),
            ("HOLDING_COMPANY_PATH.md", "مسار القابضة", "انظر أيضًا docs/25_ventures/.", []),
        ],
    ),
]


def main() -> None:
    for folder, folder_title, files in SPECS:
        d = REPO / "docs" / folder
        d.mkdir(parents=True, exist_ok=True)
        rows = []
        for fname, title, role, bullets in files:
            (d / fname).write_text(md(title, role, bullets), encoding="utf-8")
            rows.append(f"| [{fname}]({fname}) | {title} |")
        readme = (
            textwrap.dedent(
                f"""# {folder_title}

| ملف | موضوع |
|------|--------|
{chr(10).join(rows)}

## ملاحظة

هذه الطبقة جزء من مسار التوسع من MVP إلى شركة تشغيل؛ راجع الموجات في
[DEALIX_EXECUTION_WAVES_AR.md](../strategic/DEALIX_EXECUTION_WAVES_AR.md).
""",
            ).strip()
            + "\n"
        )
        (d / "README.md").write_text(readme, encoding="utf-8")
        print(f"wrote {folder} ({len(files)} files)")


if __name__ == "__main__":
    main()
