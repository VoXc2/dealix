#!/usr/bin/env python3
"""Generate docs/00_foundation … docs/25_ventures layered execution plan (Arabic-first stubs).

Run: py -3 scripts/generate_layered_execution_docs.py
Links to master blueprint and existing deep docs; each file is an operational stub
for founders — expand in-place as the layer matures.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SEE_ALSO = """
## روابط مرجعية

- [DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md](../from_zero/DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md)
- [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
- `docs/enterprise_architecture/` — تعيين تقني ↔ ريبو
"""


def md(title_ar: str, role: str, bullets_ar: list[str], extra_en: str = "") -> str:
    b = "\n".join(f"- {x}" for x in bullets_ar)
    body = f"""# {title_ar}

## دور هذه الوثيقة في التنفيذ

{role}

## نقاط تشغيلية

{b}
{SEE_ALSO}
{extra_en}
"""
    return textwrap.dedent(body).strip() + "\n"


LAYERS: dict[str, list[tuple[str, str, str, list[str]]]] = {
    "00_foundation": [
        ("DEALIX_CONSTITUTION.md", "دستور Dealix", "طبقة Foundation — تحدد من نحن وماذا نرفض قبل أي توسع كود.", ["Saudi Governed AI Operations Company", "لا وكالة أتمتة عشوائية", "كل مخرج يمر بحوكمة وProof"]),
        ("NON_NEGOTIABLES.md", "غير قابل للتفاوض", "قائمة الحدود التي تبني الثقة وتمنع المخاطر التجارية.", ["No scraping / cold WhatsApp / LinkedIn automation", "No fake proof / guaranteed sales", "No PII in logs", "No external action without approval"]),
        ("DEALIX_POSITIONING.md", "التموضع", "لماذا Dealix ليست أداة AI عامة.", ["طبقة تشغيل محكومة", "قيمة قابلة للقياس", "Proof قبل الادّعاء"]),
        ("OPERATING_EQUATION.md", "معادلة التشغيل", "ربط البيانات + Workflow + AI + موافقة + حوكمة + Proof.", ["أي عمود ناقص = demo أو مخاطرة"]),
        ("WHAT_DEALIX_REFUSES.md", "ما نرفضه", "فلتر مبيعات وثقافة داخلية.", ["Spam وscraping ووعود مبيعات", "وكلاء بلا هوية"]),
        ("GOOD_REVENUE_BAD_REVENUE.md", "إيراد جيد وسيئ", "حماية التركيز والهامش.", ["Bad revenue = دين تركيز", "Good revenue = مسار Proof وRetainer"]),
        ("STRATEGIC_WEDGE.md", "الـ Wedge الاستراتيجي", "أول عرض يقود النظام.", ["Revenue Intelligence Sprint", "قريب من المال + Proof سريع"]),
    ],
    "01_category": [
        ("GOVERNED_AI_OPERATIONS.md", "Governed AI Operations", "تعريف الفئة التي تمتلكها Dealix.", ["من تجارب إلى قدرات تشغيلية محكومة"]),
        ("CATEGORY_POV.md", "وجهة نظر الفئة", "امتلاك تعريف المشكلة قبل الحل.", ["AI value is hard to operate"]),
        ("CATEGORY_ENEMY.md", "عدو الفئة", "AI بلا تشغيل ولا حوكمة.", ["Shadow AI", "بيانات بلا مصدر"]),
        ("CATEGORY_LANGUAGE.md", "لغة الفئة", "مفردات البيع والمنتج.", ["Capability Score", "Proof Pack", "Source Passport"]),
        ("CATEGORY_PROMISE.md", "وعد الفئة", "وعد قابل للإثبات.", ["From experiments to governed capabilities"]),
        ("SAUDI_CATEGORY_CONTEXT.md", "سياق سعودي للفئة", "لماذا الفئة تنطبق على السوق المحلي.", ["HUMAIN / بنية تحتية", "Dealix طبقة تشغيل"]),
        ("NO_UNSAFE_GROWTH.md", "لا نمو غير آمن", "رفض نمو يهدم الثقة.", ["لا أتمتة خارجية بلا موافقة"]),
    ],
    "02_saudi_positioning": [
        ("SAUDI_AI_OPERATIONS_THESIS.md", "أطروحة التشغيل السعودي", "Arabic-first + PDPL-aware.", ["واتساب حساس", "قطاعات سعودية"]),
        ("SAUDI_MARKET_CONTEXT.md", "سياق السوق", "LEAP / DeepFest / حركة سوق.", ["سوق واعٍ يحتاج تشغيلًا لا أدوات فقط"]),
        ("ARABIC_FIRST_STRATEGY.md", "عربي أولًا", "جودة تنفيذية لا ترجمة حرفية.", ["نبرة تنفيذية", "عدم مبالغة"]),
        ("SAUDI_SECTOR_TAXONOMY.md", "تصنيف قطاعات", "B2B services كـ wedge.", ["توسع عمودي لاحقًا"]),
        ("WHATSAPP_BOUNDARY.md", "حدود واتساب", "علاقة وموافقة.", ["لا بارد", "DRAFT_ONLY"]),
        ("PDPL_AWARE_LANGUAGE.md", "لغة PDPL", "وضوح الاستخدام والاحتفاظ.", ["مصطلحات آمنة للعميل"]),
    ],
    "03_commercial_mvp": [
        ("REVENUE_INTELLIGENCE_SPRINT.md", "Sprint الذكاء الإيرادي", "أول عرض تجاري.", ["بيانات مسموحة", "Top 10", "Proof Pack"]),
        ("SPRINT_SCOPE.md", "نطاق Sprint", "ما داخل وما خارجه.", ["لا إرسال خارجي تلقائي"]),
        ("SPRINT_INPUTS.md", "مدخلات", "حسابات + جواز مصدر.", ["Source Passport إلزامي"]),
        ("SPRINT_OUTPUTS.md", "مخرجات", "Data quality + drafts + proof.", ["Retainer recommendation"]),
        ("SPRINT_PRICING_LOGIC.md", "منطق التسعير", "قيمة وحوكمة لا ساعات فقط.", ["risk + proof depth"]),
        ("SPRINT_PROOF_METRICS.md", "مقاييس Proof", "ما يُقاس في نهاية Sprint.", ["Proof Score path"]),
        ("RETAINER_PATH.md", "مسار Retainer", "متى نعرض الشهري.", ["Proof + Adoption thresholds"]),
    ],
    "04_data_os": [
        ("DATA_OS.md", "Data OS", "قبل أي AI — وضوح المصدر.", ["Source Passport", "جودة وجرد"]),
        ("SOURCE_PASSPORT.md", "جواز المصدر", "عقد استخدام البيانات.", ["No passport = no AI use"]),
        ("DATA_IMPORT_PREVIEW.md", "معاينة استيراد", "dedupe + جودة.", ["استيراد آمن"]),
        ("DATA_QUALITY_SCORE.md", "درجة الجودة", "اكتمال + تكرار.", ["أرقام تنفيذية"]),
        ("PII_CLASSIFICATION.md", "تصنيف PII", "قنوات وموافقات.", ["PII + خارجي = موافقة"]),
        ("ALLOWED_USE_POLICY.md", "سياسة الاستخدام المسموح", "تحديد allowed_use.", ["داخلي vs خارجي"]),
        ("DATA_RETENTION_POLICY.md", "الاحتفاظ", "مدة وحذف.", ["project_duration"]),
        ("DATA_PROVENANCE.md", "أصل البيانات", "تتبع المصدر.", ["من جمع؟ متى؟"]),
    ],
    "05_governance_os": [
        ("GOVERNANCE_OS.md", "Governance OS", "الحارس التشغيلي.", ["Runtime decisions"]),
        ("RUNTIME_GOVERNANCE.md", "حوكمة وقت التشغيل", "ALLOW … ESCALATE.", ["كل مخرج له قرار"]),
        ("POLICY_REGISTRY.md", "سجل السياسات", "قواعد معروفة.", ["no_scraping"]),
        ("CHANNEL_POLICY.md", "سياسة القنوات", "Email/WhatsApp/LinkedIn.", ["DRAFT_ONLY defaults"]),
        ("CLAIM_SAFETY.md", "أمان الادّعاء", "No proof no claim.", ["Estimated ≠ verified promo"]),
        ("APPROVAL_POLICY.md", "الموافقات", "مسارات بشرية.", ["خارجي = موافقة"]),
        ("GOVERNANCE_DECISION_TYPES.md", "أنواع القرار", "مفردات موحّدة.", ["DRAFT_ONLY"]),
    ],
    "06_llm_gateway": [
        ("LLM_GATEWAY.md", "بوابة النماذج", "لا استدعاء عشوائي.", ["Model router"]),
        ("MODEL_ROUTING.md", "توجيه النماذج", "حسب المخاطر والعربية.", ["PII-aware route"]),
        ("PROMPT_REGISTRY.md", "سجل البرومبت", "إصدارات.", ["No prompt without version"]),
        ("SCHEMA_VALIDATION.md", "مخططات", "JSON/schema للمخرجات.", ["No schema no client output"]),
        ("REDACTION_POLICY.md", "إخفاء", "قبل وبعد النموذج.", ["PII redaction"]),
        ("AI_RUN_LEDGER.md", "سجل تشغيل AI", "تدقيق.", ["cost + id"]),
        ("COST_GUARD.md", "حراسة التكلفة", "حدود الميزانية.", ["per tenant"]),
    ],
    "07_proof_os": [
        ("PROOF_OS.md", "Proof OS", "محرك الثقة.", ["Proof Pack"]),
        ("PROOF_PACK_STANDARD.md", "معيار الحزمة", "14 قسمًا.", ["Capital assets"]),
        ("PROOF_SCORE.md", "درجة الإثبات", "شرائح البيع.", [">=85 case"]),
        ("PROOF_EVENTS.md", "أحداث إثبات", "زمنية.", ["append-only mindset"]),
        ("CASE_SAFE_SUMMARY.md", "ملخص آمن للحالة", "Verified فقط.", ["لا أرقام مخترعة"]),
        ("LIMITATIONS_POLICY.md", "القيود", "صراحة مع العميل.", ["limitations section"]),
    ],
    "08_value_os": [
        ("VALUE_OS.md", "Value OS", "Estimated / Observed / Verified.", ["لا Estimated كدعاية"]),
        ("VALUE_LEDGER.md", "دفتر القيمة", "أحداث قيمة.", ["قبل/بعد"]),
        ("ESTIMATED_OBSERVED_VERIFIED_VALUE.md", "أنواع القيمة", "تعريفات صارمة.", ["Verified للـ case"]),
        ("ROI_DISCIPLINE.md", "انضباط ROI", "ربط بـProof.", ["لا وعود"]),
        ("VALUE_DASHBOARD.md", "لوحة القيمة", "عرض للعميل لاحقًا.", ["monthly"]),
    ],
    "09_capital_os": [
        ("CAPITAL_OS.md", "Capital OS", "لا وكالة بلا أصول.", ["Trust + Product/Knowledge"]),
        ("CAPITAL_LEDGER.md", "دفتر رأس المال", "تسجيل الأصول لكل مشروع.", ["expansion path"]),
        ("CAPITAL_ASSET_TYPES.md", "أنواع الأصول", "8 أنواع.", ["Venture لاحقًا"]),
        ("PRODUCTIZATION_LEDGER.md", "تمييز كمنتج", "Gate التكرار.", [">=3 مرات"]),
        ("CAPITAL_REVIEW.md", "مراجعة رأس المال", "شهريًا.", ["ماذا تراكم؟"]),
    ],
    "10_tests": [
        ("TESTING_STRATEGY.md", "استراتيجية الاختبار", "عقد CI للحوكمة.", ["guardrails first"]),
        ("GOVERNANCE_TESTS.md", "اختبارات الحوكمة", "Doctrine + output.", ["403 paths"]),
        ("REVENUE_SAFETY_TESTS.md", "أمان الإيراد", "لا قنوات خطرة.", ["draft only"]),
        ("PROOF_TESTS.md", "اختبارات Proof", "scores + gates.", ["retainer gate"]),
        ("AGENT_TESTS.md", "اختبارات الوكلاء", "هوية وصلاحيات.", ["MVP levels"]),
    ],
    "11_client_os": [
        ("CLIENT_OS.md", "Client OS", "Workspace بدل ملف PDF فقط.", ["Capability + Proof timeline"]),
        ("CLIENT_WORKSPACE_MVP.md", "Workspace MVP", "لوحات أولية.", ["Draft packs"]),
        ("CLIENT_HEALTH_SCORE.md", "صحة العميل", "جاهزية تشغيل.", ["owner + data"]),
        ("CAPABILITY_DASHBOARD.md", "قدرات", "محاذاة Diagnostic.", ["6 axes"]),
        ("DATA_READINESS_PANEL.md", "لوحة بيانات", "Source + جودة.", ["passport coverage"]),
        ("GOVERNANCE_PANEL.md", "لوحة حوكمة", "قرارات.", ["DRAFT_ONLY ratio"]),
        ("PROOF_TIMELINE.md", "زمنية Proof", "أحداث.", ["pack versions"]),
        ("VALUE_DASHBOARD.md", "قيمة", "Verified فقط للعرض الخارجي.", ["monthly"]),
    ],
    "12_adoption_os": [
        ("ADOPTION_OS.md", "Adoption OS", "لا Retainer بلا اعتماد.", ["Adoption Score"]),
        ("ADOPTION_MODEL.md", "نموذج التبني", "مراحل الوعي → المنصة.", ["Friction"]),
        ("ADOPTION_SCORE.md", "درجة التبني", "راعٍ + تفاعل.", [">=70 retainer"]),
        ("ADOPTION_REVIEW.md", "مراجعة", "أسئلة تشغيلية.", ["من يستخدم؟"]),
        ("FRICTION_LOG.md", "سجل الاحتكاك", "تصنيف الاحتكاك.", ["موافقات"]),
        ("ADOPTION_TO_RETAINER_LOGIC.md", "من تبني إلى Retainer", "ربط Proof.", ["gates"]),
    ],
    "13_workflow_os": [
        ("WORKFLOW_OS.md", "Workflow OS", "AI داخل العمل اليومي.", ["owner"]),
        ("WORKFLOW_MODEL.md", "نموذج", "inputs/outputs/cadence.", ["proof metric"]),
        ("WORKFLOW_OWNER_RULES.md", "قواعد المالك", "No workflow without owner.", []),
        ("APPROVAL_FLOW.md", "تدفق موافقة", "مسارات.", ["human"]),
        ("OPERATING_CADENCE.md", "إيقاع تشغيل", "شهري/أسبوعي.", ["meetings"]),
        ("WORKFLOW_METRICS.md", "مقاييس", "جودة التسليم.", ["SLA hints"]),
    ],
    "14_trust_os": [
        ("TRUST_OS.md", "Trust OS", "الثقة كمنتج.", ["Trust Pack"]),
        ("TRUST_PACK.md", "حزمة ثقة", "Enterprise.", ["refusals"]),
        ("TRUST_ARTIFACTS.md", "أدلة ثقة", "Passport + ledger.", []),
        ("TRUST_DASHBOARD.md", "لوحة", "تغطية.", ["coverage scores"]),
        ("COMPLIANCE_REPORT.md", "تقرير امتثال", "تشغيلي.", ["PDPL"]),
    ],
    "15_evidence_control_plane": [
        ("EVIDENCE_CONTROL_PLANE.md", "سيطرة الأدلة", "Enterprise traceability.", ["Graph"]),
        ("EVIDENCE_GRAPH.md", "الرسم البياني للأدلة", "Source→Proof.", []),
        ("EVIDENCE_OBJECT_STANDARD.md", "كائن أدلة", "حقول موحدة.", []),
        ("EVIDENCE_DASHBOARD.md", "لوحة", "تغطية.", []),
        ("EVIDENCE_GAP_RULES.md", "قواعد الفجوات", "Missing=block.", []),
        ("EVIDENCE_TO_PROOF.md", "إلى Proof", "ربط.", []),
        ("EVIDENCE_TO_RISK.md", "إلى مخاطر", "إشارات.", []),
    ],
    "16_agents": [
        ("AGENT_OS.md", "Agent OS", "وكلاء محكومون.", ["Identity"]),
        ("AGENT_IDENTITY.md", "هوية", "بطاقة وكيل.", []),
        ("AGENT_PERMISSION_MODEL.md", "صلاحيات", "Least privilege.", []),
        ("AGENT_AUTONOMY_LEVELS.md", "مستويات", "MVP 0–3.", []),
        ("AGENT_AUDITABILITY_CARD.md", "تدقيق", "سجل.", []),
        ("AGENT_LIFECYCLE.md", "دورة حياة", "Deploy gates.", []),
    ],
    "17_secure_agent_runtime": [
        ("SECURE_AGENT_RUNTIME.md", "تشغيل آمن", "حدود أربعة.", ["Prompt/Tool/Data/Context"]),
        ("RUNTIME_ASSURANCE_LOOP.md", "حلقة ضمان", "Observe→Log.", []),
        ("RUNTIME_POLICY_ENGINE.md", "محرك سياسات", "وقت التشغيل.", []),
        ("STATEFUL_RISK_MEMORY.md", "ذاكرة مخاطر", "حالة الوكيل.", []),
        ("AGENT_RUNTIME_STATES.md", "حالات", "SAFE…KILLED.", []),
        ("KILL_SWITCH.md", "Kill switch", "أنواع.", []),
        ("DEPLOYMENT_RINGS.md", "حلقات نشر", "0→5.", []),
    ],
    "18_intelligence_os": [
        ("INTELLIGENCE_OS.md", "Intelligence OS", "إشارات مركبة.", ["Signal→Decision"]),
        ("MARKET_INTELLIGENCE.md", "سوق", "مكالمات مبيعات.", []),
        ("CLIENT_INTELLIGENCE.md", "عميل", "احتكاك.", []),
        ("DATA_INTELLIGENCE.md", "بيانات", "أنماط.", []),
        ("WORKFLOW_INTELLIGENCE.md", "سير عمل", "اختناقات.", []),
        ("GOVERNANCE_INTELLIGENCE.md", "حوكمة", "قواعد جديدة.", []),
        ("PRODUCT_INTELLIGENCE.md", "منتج", "فرص ميزات.", []),
        ("DECISION_ENGINE.md", "محرك قرار", "لوحة المؤسس.", []),
    ],
    "19_command_os": [
        ("COMMAND_OS.md", "Command OS", "قرارات CEO.", ["Top 5"]),
        ("CEO_COMMAND_CENTER.md", "مركز القيادة", "لقطات.", []),
        ("BOARD_DECISION_LOOP.md", "حلقة مجلس", "Scale/Kill.", []),
        ("DECISION_TYPES.md", "أنواع", "Pilot/Hold.", []),
        ("BOARD_SCORECARDS.md", "بطاقات أداء", "شهريًا.", []),
        ("MONTHLY_BOARD_MEMO.md", "مذكرة شهرية", "قالب.", []),
    ],
    "20_sales_os": [
        ("SALES_OS.md", "Sales OS", "بيع مضبوط.", ["qualification"]),
        ("SALES_QUALIFICATION.md", "تأهيل", "أسئلة.", []),
        ("OBJECTION_HANDLING.md", "اعتراضات", "مكتبة.", []),
        ("PROPOSAL_OS.md", "مقترحات", "قوالب.", []),
        ("BAD_REVENUE_FILTER.md", "فلتر إيراد سيئ", "رفض.", []),
        ("SALES_ASSET_LIBRARY.md", "مكتبة أصول", "رسائل.", []),
    ],
    "21_operating_finance": [
        ("OPERATING_FINANCE.md", "مالية تشغيل", "هامش وتكلفة.", []),
        ("CAPITAL_ALLOCATION_SCORE.md", "تخصيص", "أولويات.", []),
        ("FINANCIAL_MODEL.md", "نموذج", "وحدات.", []),
        ("MARGIN_PROTECTION.md", "حماية هامش", "قواعد.", []),
        ("AI_COST_ACCOUNTING.md", "تكلفة AI", "LLM.", []),
        ("DELIVERY_COST_ACCOUNTING.md", "تكلفة تسليم", "ساعات.", []),
    ],
    "22_enterprise_rollout": [
        ("ENTERPRISE_ROLLOUT.md", "دخول مؤسسات", "Land→…", []),
        ("ENTERPRISE_ENTRY_STRATEGY.md", "دخول", "Governance review.", []),
        ("DEPARTMENT_ROLLOUT_MODEL.md", "أقسام", "قالب.", []),
        ("ENTERPRISE_GATES.md", "بوابات", "Sponsor/Data/…", []),
        ("PROCUREMENT_READINESS.md", "مشتريات", "جاهزية.", []),
    ],
    "23_standards": [
        ("DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md", "المعيار العام", "Dealix Standard.", []),
        ("CAPABILITY_DIAGNOSTIC_STANDARD.md", "تشخيص", "محاور.", []),
        ("DATA_READINESS_STANDARD.md", "جاهزية بيانات", "حقول.", []),
        ("SOURCE_PASSPORT_STANDARD.md", "جواز", "JSON.", []),
        ("RUNTIME_GOVERNANCE_STANDARD.md", "حوكمة وقت تشغيل", "قرارات.", []),
        ("PROOF_PACK_STANDARD.md", "Proof", "14 قسمًا.", []),
        ("OPERATING_CADENCE_STANDARD.md", "إيقاع", "اجتماعات.", []),
        ("CAPITAL_CREATION_STANDARD.md", "رأس مال", "أصول.", []),
    ],
    "24_ecosystem": [
        ("ECOSYSTEM_OS.md", "نظام بيئي", "شركاء وأكاديمية.", []),
        ("ACADEMY_STRATEGY.md", "أكاديمية", "متى تُطلق.", ["10+ projects"]),
        ("CERTIFICATION_SYSTEM.md", "شهادات", "مسارات.", []),
        ("PARTNER_COVENANT.md", "عهد شركاء", "حوكمة.", []),
        ("PARTNER_GOVERNANCE.md", "حوكمة شركاء", "تدقيق.", []),
        ("BENCHMARK_ENGINE.md", "معايير", "تقارير مجمعة.", []),
    ],
    "25_ventures": [
        ("VENTURE_OS.md", "Venture OS", "مصنع وحدات.", []),
        ("VENTURE_GATE.md", "بوابة", "5 عملاء مدفوعين…", []),
        ("BUSINESS_UNIT_MATURITY.md", "نضج وحدة", "قياس.", []),
        ("SPINOUT_CRITERIA.md", "Spinout", "شروط.", []),
        ("HOLDING_COMPANY_PATH.md", "شركة قابضة", "رحلة.", []),
    ],
}


def main() -> None:
    for folder, files in LAYERS.items():
        base = REPO / "docs" / folder
        base.mkdir(parents=True, exist_ok=True)
        idx_lines = [f"# طبقة `{folder}` — فهرس", "", "| الملف | الموضوع |", "|--------|---------|"]
        for fname, title_ar, role, bullets in files:
            path = base / fname
            path.write_text(md(title_ar, role, bullets), encoding="utf-8")
            idx_lines.append(f"| [{fname}]({fname}) | {title_ar} |")
        idx_lines.append("")
        idx_lines.append("## ترتيب البناء المقترح")
        idx_lines.append("راجع [DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md](../from_zero/DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md) لرحلة الشركة القابضة.")
        (base / "README.md").write_text("\n".join(idx_lines) + "\n", encoding="utf-8")
        print("wrote", folder, len(files) + 1, "files")


if __name__ == "__main__":
    main()
