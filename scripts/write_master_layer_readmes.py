#!/usr/bin/env python3
"""One-shot generator for docs/NN_*/README.md master layer constitution files."""

from __future__ import annotations

import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"

# (relative_dir, title_ar, body_md) — body is dedented markdown after title block.
LAYERS: list[tuple[str, str, str]] = [
    (
        "00_constitution",
        "الطبقة 0 — الأطروحة العليا (Dealix Master Thesis)",
        """
        ## الفكرة الحاكمة

        **AI tools are easy to buy. AI value is hard to operate. Dealix turns AI into governed operating capabilities.**

        بالعربي: شراء أدوات AI سهل؛ تشغيل AI بقيمة حقيقية صعب؛ Dealix يحوّل الذكاء إلى **قدرات تشغيلية محكومة**.

        ## الأعمدة السبعة (إن نقص أحدها يتحول المشروع إلى demo أو مخاطرة)

        1. **Data** — وضوح المصدر وجواز الاستخدام.
        2. **Workflow** — ملكية وتسلسل عمل مُدار.
        3. **AI** — مساعدة عبر بوابة نماذج، لا صندوق أسود.
        4. **Human Approval** — مسارات موافقة صريحة للمخرجات الحساسة والخارجية.
        5. **Governance** — قرار وقت تشغيل (ALLOW / DRAFT_ONLY / BLOCK …).
        6. **Proof** — Proof Pack ودرجة إثبات تربط القيمة بالأدلة.
        7. **Operating Cadence** — إيقاع تشغيل شهري/أسبوعي يحافظ على الجودة.

        ## العدو الاستراتيجي

        **AI بلا انضباط تشغيلي**: Shadow AI، بيانات بلا مصدر، وكلاء بلا هوية، تواصل بلا موافقة، ادّعاءات بلا Proof، لوحات بلا أثر.

        ## وثائق مرتبطة

        - `DEALIX_CONSTITUTION.md`، `DEALIX_LAWS.md`، `NON_NEGOTIABLES.md`، `DECISION_PRINCIPLES.md` في هذا المجلد.
        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "01_category_creation",
        "الطبقة 1 — صناعة الفئة (Category Creation)",
        """
        ## اسم الفئة

        **Governed AI Operations** — تشغيل الذكاء الاصطناعي المحكوم.

        ## التعريف

        تحويل AI من أدوات متفرقة إلى **workflows داخل العمل** مبنية على: مصادر واضحة، موافقة بشرية، حوكمة وقت التشغيل، سجلات تدقيق، Proof للقيمة، وإيقاع تشغيل شهري.

        ## لغة الفئة (مفردات Dealix)

        Capability Score، Transformation Gap، Source Passport، Governance Runtime، AI Run Ledger، Proof Pack، Value Ledger، Evidence Control Plane، Client Workspace، Operating Cadence، Capital Ledger، Dealix Method.

        ## وعد الفئة

        **From AI experiments to governed operating capabilities.**  
        من تجارب AI إلى قدرات تشغيلية محكومة.

        ## روابط

        - `docs/category/` و`docs/enterprise/` للتوسع في السرد التسويقي.
        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "02_strategy",
        "الطبقة 1 (هوية) — الاستراتيجية: من نحن؟",
        """
        ## Dealix Identity

        **Saudi Governed AI Operations Company** — أو: **AI Operating Capability Builder**.

        ## ما لسنا عليه

        لسنا وكالة أتمتة عشوائية، ولا مكينة سكرابينغ، ولا بائع chatbot عام، ولا SaaS جامع ميزات بلا حوكمة.

        ## الرسالة

        نساعد الشركات السعودية والخليجية على **تشغيل AI داخل أعمالها** بأمان، حوكمة، قياس، وProof.

        ## الروابط

        - `docs/company/` و`docs/investment/` للرسالة الطويلة والـ thesis المالي.
        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "03_saudi_positioning",
        "التموضع السعودي",
        """
        ## التموضع

        السعودية تبني بنية تحتية للذكاء الاصطناعي؛ Dealix تبني **طبقة التشغيل** التي تمكّن الشركات من استخدام AI **بأمان وقياس** دون منافسة البنية السحابية/النماذج الأساسية.

        ## إشارات سوقية (تعليمية)

        فعاليات مثل LEAP وDeepFest تعكس حركة سوق قوية نحو AI — Dealix يترجم الحركة إلى **تشغيل محكوم** لا إلى فوضى أدوات.

        ## مصادر ذكاء مسموحة

        Saudi Open Data والقطاع العام والمزودون المرخّصون وبيانات العميل المرفوعة والإحالات — **من دون** خلط بيانات العميل الخاصة مع استخدامات غير مصرّحة.

        ## طبقة الجودة العربية والسعودية

        نبرة تنفيذية، عدم مبالغة، عدم وعود مبيعات، وعناية بـ PDPL وواتساب (علاقة/موافقة). راجع أيضًا `docs/saudi/` و`docs/intelligence_compounding/ARABIC_SAUDI_INTELLIGENCE_LAYER.md`.

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "04_product_strategy",
        "استراتيجية المنتج التجاري",
        """
        ## الـ Wedge الأول

        **Revenue Intelligence Sprint** — قريب من المال، سهل الفهم، ينتج Proof سريعًا، يفتح Retainer، يبني Data OS + Governance OS + Proof OS.

        ## العروض الأساسية

        Capability Diagnostic، Revenue Intelligence Sprint، Company Brain Sprint، AI Governance Review، AI Quick Win Sprint، Data Readiness Sprint.

        ## العروض الشهرية

        Monthly RevOps OS، Monthly Company Brain، Monthly Governance، Monthly AI Ops، Monthly Value Reporting.

        ## Enterprise لاحقًا

        AI Control Plane، Evidence Control Plane، Audit Exports، Agent Registry، Policy Registry، Executive AI Value Dashboard، Enterprise Trust Program.

        ## Ecosystem لاحقًا

        Academy، Certification، Partner Portal، Benchmark Reports، Vertical Playbooks.

        ## روابط

        - `docs/company/OFFER_LADDER.md`، `docs/dominance/`، [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "05_client_os",
        "نظام تشغيل العميل (Client OS)",
        """
        ## Client Workspace

        يعرض: Capability Score، Data Readiness، Governance Status، Draft Packs، Approvals، Proof Timeline، Value Dashboard، Next Actions.

        ## Client Health Score

        مالك واضح، جاهزية بيانات، مشاركة أصحاب المصلحة، قوة الإثبات، محاذاة حوكمة، حاجة workflow شهرية، إمكان توسع.

        ## Client Adoption Score

        راعٍ تنفيذي، مالك workflow، تفاعل، موافقات مكتملة، رؤية Proof، cadence شهرية، سحب توسعي.

        ## Retainer Readiness

        لا تعرض Retainer إلا إذا: Proof Score عالٍ، Adoption كافٍ، workflow متكرر، مالك موجود، قيمة شهرية واضحة، مخاطر حوكمة مسيطر عليها.

        ## نضج العميل (سلم التحوّل)

        تفاصيل السلم والمحرك: `docs/client_maturity/` و`auto_client_acquisition/client_maturity_os/`.

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "06_data_os",
        "طبقة البيانات (Data OS)",
        """
        ## Source Passport

        لكل مصدر: نوع، مالك، سياق الجمع، allowed use، حالة PII، حساسية، احتفاظ، هل AI مسموح، هل الاستخدام الخارجي مسموح.

        ## Data Readiness Score

        وضوح المصدر، اكتمال، تكرارات، حقول ناقصة، جودة صيغة، تصنيف PII، وضوح allowed use.

        ## قواعد

        - No Source Passport = no AI use.
        - No allowed use = internal analysis only.
        - Unknown source = no outreach.
        - PII + external use = approval required.

        ## Saudi Data Layer

        تصنيف قطاعات، تطبيع مدن/مناطق، حقول شركات عربية، لغة PDPL-aware، حالة علاقة/موافقة لواتساب.

        ## تنفيذ

        - `auto_client_acquisition/data_os/`، `docs/architecture/SOURCE_PASSPORT.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "07_governance",
        "طبقة الحوكمة (Governance OS)",
        """
        ## Governance Runtime

        قرارات مثل: ALLOW، ALLOW_WITH_REVIEW، DRAFT_ONLY، REQUIRE_APPROVAL، REDACT، BLOCK، ESCALATE.

        ## Policy Registry

        no_scraping، no_cold_whatsapp، no_linkedin_automation، no_guaranteed_claims، external_action_requires_approval، pii_requires_review، no_source_less_answers.

        ## Channel Policy

        Email: draft حتى الموافقة. WhatsApp: لا أتمتة باردة. LinkedIn: مسودة فقط بدون أتمتة. جهات مجهولة المصدر: لا outreach.

        ## Claim Safety

        No proof, no claim. No guaranteed sales. Estimated ≠ Verified.

        ## تنفيذ

        - `auto_client_acquisition/governance_os/`، `auto_client_acquisition/compliance_trust_os/`، `docs/governance/GOVERNANCE_RUNTIME.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "08_responsible_ai",
        "Responsible AI (D-RAIOS)",
        """
        ## الأعمدة التشغيلية

        Data Sovereignty، Human Oversight، Runtime Governance، Explainability & Auditability، Proof of Value، Operating Cadence، Continuous Improvement.

        ## AI Use Case Risk Classifier

        Low / Medium / High / Forbidden.

        ## AI Inventory

        use case، قسم، مالك، مصادر بيانات، agent/model، مستوى مخاطرة، مسار موافقة، حالة تدقيق، مقياس proof، حالة.

        ## وثائق وتنفيذ

        - `docs/responsible_ai/`، `auto_client_acquisition/responsible_ai_os/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "09_llm_gateway",
        "طبقة LLM Gateway",
        """
        ## كل استدعاء AI يمر عبر

        model router، prompt registry، schema validator، redaction، cost guard، eval hook، AI run ledger.

        ## Model Routing

        حسب: نوع المهمة، المخاطر، PII، جودة عربية، ميزانية تكلفة، زمن استجابة، صرامة المخطط.

        ## قواعد

        - No AI call outside LLM Gateway.
        - No prompt outside Prompt Registry.
        - No client output without schema + governance + QA.

        ## تنفيذ

        - `auto_client_acquisition/llm_gateway_v10/`، `docs/enterprise_architecture/LLM_GATEWAY.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "10_agents",
        "الوكلاء (Agentic Operations)",
        """
        ## الهوية والصلاحيات

        كل agent: agent_id، owner، purpose، business_unit، risk tier، بيئة، حالة. صلاحيات: مدخلات مسموحة، أدوات مسموحة/ممنوعة، متطلبات موافقة، مستوى استقلالية.

        ## مستويات الاستقلالية (مثال تشغيلي Dealix)

        في المنتج الموثّق لـ MVP راجع `docs/agentic_operations/AGENT_OPERATING_LEVELS.md` — المبدأ: **لا صلاحيات وكيلة بدون حوكمة وكيلة**.

        ## MVP

        إعداد وتحليل ومسودات وطوابير موافقة؛ **لا تنفيذ تواصل خارجي** في MVP الافتراضي.

        ## تنفيذ

        - `docs/agentic_operations/`، `auto_client_acquisition/agentic_operations_os/`، `auto_client_acquisition/ai_workforce/`، `auto_client_acquisition/agent_governance/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "11_secure_runtime",
        "Secure Agent Runtime + Kill Switch",
        """
        ## Runtime Assurance Loop

        Observe → Classify → Check Policy → Decide → Execute/Block/Escalate → Log Evidence → Update State.

        ## أربع حدود

        Prompt Boundary، Tool Boundary، Data Boundary، Context Boundary.

        ## حالات التشغيل

        SAFE، WATCH، RESTRICTED، ESCALATED، PAUSED، KILLED.

        ## Kill Switch

        Soft Kill، Tool Kill، Client Kill، Agent Kill، Fleet Kill — أي أداة يجب أن تكون قابلة للإيقاف الفوري مع أثر مسجّل.

        ## حلقات النشر (Rings)

        من sandbox محلي إلى عميل retainer بموافقات — لا قفزات بدون أدلة تغطية.

        ## تنفيذ

        - `auto_client_acquisition/tool_guardrail_gateway/`، `auto_client_acquisition/safe_send_gateway/`، وثائق `docs/institutional_control/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "12_auditability",
        "Auditability & Accountability",
        """
        ## Evidence Chain

        Source، Input، Policy، AI Run، Human Review، Approval، Output، Proof، Value.

        ## Accountability Model

        AI generated → Human approved → System logged → Company accountable.

        ## Policy Checkability

        rules checked، matched rules، decision، شرح بشري مقروء.

        ## Lifecycle Coverage

        created / approved / modified / executed / reviewed / incident / decommissioned.

        ## تنفيذ

        - `auto_client_acquisition/compliance_trust_os/audit_trail.py`، `docs/evidence_control_plane/`، `auto_client_acquisition/evidence_control_plane_os/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "13_evidence_control_plane",
        "Evidence Control Plane",
        """
        ## Evidence Graph

        يربط: Source، AI Run، Policy Check، Governance Decision، Human Review، Approval، Output، Proof Event، Value Event، Risk Event، Decision.

        ## Evidence Object

        evidence_id، type، client/project، actor، human owner، source IDs، artifacts، summary، confidence، timestamp.

        ## Evidence Gap Rules

        Missing Source Passport → block AI use. Missing Governance Decision → block delivery. Missing Approval → incident. Missing Proof → remove claim. Missing Agent Card → no production agent.

        ## وثائق وتنفيذ

        - `docs/evidence_control_plane/`، `auto_client_acquisition/evidence_control_plane_os/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "14_proof",
        "Proof OS",
        """
        ## Proof Pack

        Executive Summary، Problem، Inputs، Source Passports، Work Completed، Outputs، Quality Scores، Governance Decisions، Blocked Risks، Value Metrics، Limitations، Recommended Next Step، Capital Assets Created.

        ## Proof Score

        نطاقات تقييم جودة الإثبات لاستخدامات داخلية/مبيعات/تعلم (راجع `docs/proof_architecture/`).

        ## أنواع الإثبات

        Revenue، Time، Quality، Risk، Knowledge.

        ## قواعد

        No proof, no claim. No proof, no retainer push. No proof, no case study.

        ## تنفيذ

        - `auto_client_acquisition/proof_architecture_os/`، `docs/enterprise_architecture/PROOF_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "15_value",
        "Value OS",
        """
        ## Value Ledger

        value event، metric، before/after، confidence، evidence، limitations.

        ## أنواع القيمة

        Estimated Value، Observed Value، Verified Value.

        ## قاعدة

        لا تستخدم Estimated كدعاية؛ **Verified** فقط كأساس case study خارجي.

        ## تنفيذ

        - `auto_client_acquisition/value_capture_os/`، `auto_client_acquisition/proof_architecture_os/value_ledger.py` (إن وُجد)، `docs/enterprise_architecture/VALUE_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "16_capital",
        "Capital OS",
        """
        ## Capital Ledger

        كل مشروع يخلق أصلًا: Service/Product/Knowledge/Trust/Market/Standard/Partner/Venture capital.

        ## الحد الأدنى

        1 Trust Asset + 1 Product or Knowledge Asset + 1 Expansion Path.

        ## Productization Gate

        تكرار خطوة يدوية ≥ 3، تكلفة وقت ≥ ساعتين/مشروع، مرتبط بعرض مدفوع، يقلل مخاطر أو يحسن هامش، قابل للاختبار، قابل لإعادة الاستخدام.

        ## تنفيذ

        - `docs/enterprise/CAPITAL_LEDGER_V2.md`، `auto_client_acquisition/operating_finance_os/`، `auto_client_acquisition/board_decision_os/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "17_revenue_os",
        "Revenue OS",
        """
        ## Revenue Intelligence

        يدخل: حسابات مرفوعة، جوازات مصدر، قطاع/مدينة، حالة علاقة/موافقة. يخرج: جودة بيانات، تنظيف، ترتيب، فرص، Draft Pack، مسار مصغّر، Revenue Proof Pack.

        ## ممنوع

        scraping engine، cold WhatsApp automation، LinkedIn automation، ادّعاءات مبيعات مضمونة.

        ## Draft Pack

        مسودات بريد، سكربت مكالمة، خطة متابعة، LinkedIn draft-only، WhatsApp draft-only مع علاقة/موافقة.

        ## تنفيذ

        - `auto_client_acquisition/revenue_os/`، `docs/enterprise_architecture/REVENUE_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "18_brain_os",
        "Brain OS (Company Brain)",
        """
        ## المكونات

        source registry، فهرسة مستندات، retrieval، إجابات باستشهاد، وضع نقص أدلة، فجوات معرفة، knowledge proof.

        ## القواعد

        No source-less answer. Insufficient evidence إجابة صالحة. Knowledge gaps تصبح مهام.

        ## تنفيذ

        - `auto_client_acquisition/knowledge_os/`، `docs/enterprise_architecture/BRAIN_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "19_workflow_os",
        "Workflow OS",
        """
        ## تعريف Workflow

        owner، inputs، outputs، خطوات AI-assisted، approval path، QA rubric، proof metric، cadence.

        ## قواعد

        No workflow without owner. No retainer without cadence. No cadence without proof metric.

        ## تنفيذ

        - `auto_client_acquisition/delivery_os/`، `docs/product/WORKFLOW_REGISTRY.md`، `docs/enterprise_architecture/WORKFLOW_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "20_adoption",
        "Client Adoption",
        """
        ## Adoption Model

        Awareness → Trust → First Use → Repeated Use → Operating Cadence → Managerial Reliance → Retainer → Platform Pull.

        ## Adoption Review

        هل استُخدمت المخرجات؟ من؟ هل اكتملت الموافقات؟ هل عاد للنظام؟ ما الاحتكاك؟

        ## Friction Log

        data friction، approval friction، user confusion، workflow ambiguity، trust concern، Arabic quality، integration، pricing.

        ## تنفيذ

        - `auto_client_acquisition/adoption_os/` (إن وُجد)، وثائق `docs/client/` و`docs/scorecards/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "21_operating_rhythm",
        "Operating Rhythm",
        """
        ## Daily CEO Check

        أعلى فرصة إيراد، أعلى خطر تسليم، أعلى خطر حوكمة، أي proof يحتاج تحسين، ماذا نتجاهل.

        ## Weekly Operating Meeting

        قرارات، Pipeline، تسليم، Proof، حوكمة، Adoption، Productization، تخصيص رأس مال، Stop list.

        ## Monthly Board Memo

        جودة إيراد، Proof & Value، حوكمة، Adoption، Productization، أصول سوقية، مخاطر، رهانات قادمة.

        ## Quarterly Strategic Review

        ماذا نوسّع، نقتل، نبني، نرفع سعره، نرّوج له سرديًا.

        ## وثائق وتنفيذ

        - `docs/operating_rhythm/`، `auto_client_acquisition/operating_rhythm_os/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "22_board_decision",
        "Board Decision System",
        """
        ## أنواع القرارات

        Scale، Build، Pilot، Hold، Kill، Raise Price، Offer Retainer، Reject Revenue، Create Playbook/Benchmark/BU/Venture candidate.

        ## CEO Command Center

        Top 5 decisions، جودة إيراد، قوة Proof، فرص Retainer، مخاطر عملاء، طابور Productization، مخاطر حوكمة، إيراد سيئ مرفوض، نضج وحدات، إشارات Venture.

        ## تنفيذ

        - `auto_client_acquisition/board_decision_os/`، `docs/command/`، `docs/enterprise_architecture/COMMAND_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "23_intelligence",
        "Intelligence Compounding",
        """
        ## أنواع الذكاء

        Market، Client، Data، Workflow، Governance، Product، Arabic/Saudi.

        ## من إشارة إلى قرار

        sales call → market signal؛ friction → product signal؛ governance event → rule؛ proof event → benchmark؛ human edit → QA.

        ## Decision Engine

        Signal → Score → Decision → Action → Proof → Learning.

        ## تنفيذ

        - `auto_client_acquisition/intelligence_os/`، `auto_client_acquisition/intelligence_compounding_os/`، `docs/intelligence_compounding/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "24_risk_resilience",
        "Risk & Resilience",
        """
        ## Risk Taxonomy

        Data، Privacy، AI Output، Agent Autonomy، Channel، Claim، Client، Delivery، Partner، Financial، Market، Strategic Drift.

        ## Incident-to-Asset

        كل حادثة تنتج: rule، test، checklist، owner، prevention metric.

        ## Resilience Score

        تغطية حوكمة، جوازات مصدر، تسجيل AI runs، اكتمال Proof Pack، جودة استجابة حوادث، رفض إيراد سيئ، تكرار تسليم، امتثال شركاء.

        ## تنفيذ

        - `auto_client_acquisition/risk_resilience_os/`، `docs/enterprise_architecture/RISK_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "25_compliance_trust",
        "Compliance & Trust Ops",
        """
        ## Trust Operations Model

        Discover → Classify → Govern → Approve → Execute → Log → Prove → Review → Improve.

        ## Compliance Report

        مصادر، جوازات، PII، redactions، AI runs، قرارات حوكمة، موافقات، حوادث، توصيات.

        ## Trust Pack (Enterprise)

        ما تفعله Dealix وما ترفضه، معالجة بيانات، Source Passport، AI run ledger، governance runtime، agent control، human oversight، approvals، audit trail، proof standard، incident response، مسؤوليات العميل.

        ## تنفيذ

        - `auto_client_acquisition/compliance_trust_os/`، `docs/compliance_trust_ops/`، `docs/trust/`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "26_human_amplified",
        "Human-Amplified Organization",
        """
        ## المبدأ

        AI prepares → Humans approve → System logs → Proof validates → Governance improves.

        ## أدوار Dealix

        CEO/Strategic Operator، Revenue، Delivery، Governance، Proof، Product، Client Success، Finance/Capital.

        ## Human Review as Product Signal

        كل تعديل بشري يكشف: QA gap، prompt weakness، governance issue، نبرة عربية، سوء فهم عميل، فرصة ميزة.

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "27_value_capture",
        "Value Capture & Monetization",
        """
        ## Revenue Ladder

        Education → Paid Diagnostic → Sprint → Pilot → Retainer → Managed Platform → Enterprise → Academy → Partners → Ventures.

        ## Pricing Philosophy

        سعّر: capability، proof، governance، risk reduction، cadence، business impact — لا تسعر ساعات فقط.

        ## Revenue Quality Score

        هامش، تكرار، retainer potential، proof strength، governance safety، productization signal.

        ## Bad Revenue Filter

        رفض: scraping، cold WhatsApp، مبيعات مضمونة، مصدر غير واضح، نطاق مفتوح، هامش منخفض، لا مسار proof.

        ## تنفيذ

        - `auto_client_acquisition/value_capture_os/`، `docs/company/PRICING_ENGINE.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "28_operating_finance",
        "Operating Finance",
        """
        ## Investment Buckets

        Revenue Capture، Delivery Efficiency، Governance & Trust، Proof & Value، Productization، Distribution، Talent & Enablement، Venture Optionality.

        ## Capital Allocation Score

        أثر إيراد، تكرار، تحسين هامش، قيمة حوكمة، قوة proof، productization، خندق استراتيجي، سرعة تعلم.

        ## Spend Rules

        No product before signal. No growth before offer clarity. No hiring before playbook. No academy before proof. No venture before retainers.

        ## تنفيذ

        - `auto_client_acquisition/operating_finance_os/`، `docs/company/COST_GOVERNANCE.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "29_enterprise_rollout",
        "Enterprise Rollout",
        """
        ## Rollout Model

        Land → Prove → Adopt → Operate → Expand → Standardize → Institutionalize.

        ## Enterprise Entry

        AI Governance & Readiness Review؛ Governed AI Workflow Pilot.

        ## Department Rollout

        Sales → Revenue Intelligence؛ Operations → AI Quick Win؛ Knowledge → Company Brain؛ Governance/IT → AI Governance Review؛ Executive Office → Value Dashboard.

        ## Enterprise Gates

        Sponsor، Data، Workflow، Governance، Proof، Adoption، Retainer.

        ## تنفيذ

        - `auto_client_acquisition/enterprise_rollout_os/`، `docs/enterprise/ROAD_TO_ENTERPRISE.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "30_standards",
        "Standards (Dealix Governed AI Operations Standard)",
        """
        ## المكوّنات

        Capability Diagnostic Standard، Data Readiness، Source Passport، Runtime Governance، Agent Control، AI Output QA، Proof Pack، Operating Cadence، Capital Creation.

        ## تنفيذ

        - `docs/standards/`، `auto_client_acquisition/standards_os/`، `docs/enterprise_architecture/STANDARDS_OS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "31_certification",
        "Certification",
        """
        ## مستويات

        Dealix Aware → Operator → Implementer → Certified Partner → Strategic Partner.

        ## الامتحان

        knowledge test، case simulation، governance test، QA review.

        ## تنفيذ

        - `docs/academy/CERTIFICATION_TRACKS.md`، `docs/institutional/STANDARDS_ACADEMY_PARTNERS.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "32_ecosystem",
        "Ecosystem",
        """
        ## Flywheel

        Services → Proof → Retainers → Workspace → Product Modules → Standards → Academy → Partners → Benchmarks → More Clients.

        ## Partner Ladder

        Referral → Advisory → Implementation → Certified → Strategic → White-label.

        ## Academy Tracks

        AI Ops Executive، Revenue AI Operator، Company Brain Builder، AI Governance Lead، Certified Partner.

        ## Benchmark Engine

        تقارير جاهزية/بيانات/حوكمة/جودة عربية/Company Brain readiness (تعليمية، بمصادر مسموحة).

        ## تنفيذ

        - `auto_client_acquisition/ecosystem_os/`، `docs/growth/ACADEMY.md`، `docs/enterprise/PARTNER_OPERATING_SYSTEM.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "33_ventures",
        "Venture Factory",
        """
        ## Venture Gate (مثال)

        عملاء مدفوعون متعددون، retainers، مكتبة Proof، تكرار تسليم، مالك، هامش صحي، اعتماد على Core OS.

        ## Venture Candidates

        Revenue OS، Governance Cloud، Company Brain، Clinics OS، Logistics OS — عند نضج السوق والتكرار.

        ## قواعد

        No venture without proof library. No spinout without owner. No product without repeated paid workflow.

        ## تنفيذ

        - `docs/ventures/`، `docs/enterprise/VENTURE_FACTORY.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "34_market_power",
        "Market Power + Strategic Resilience",
        """
        ## Market Power Metrics

        تبنّي لغة الفئة، inbound diagnostics، طلبات Proof Pack، استفسارات Enterprise trust، إحالات شركاء، تنزيلات benchmarks، waitlist أكاديمية، إشارات نسخ منافسين.

        ## Strategic Resilience (Anti-fragile)

        ضغط → إشارة → تشخيص → rule → test → playbook → تحسين منتج → proof → خندق أقوى.

        ## Strategic Drift Detector

        كثرة custom، لا proof packs، لا أصول رأسمالية، ميزات بلا استخدام، طلبات عميل غير آمنة، اختناق مؤسس.

        ## تنفيذ

        - `auto_client_acquisition/market_power_os/`، `docs/market_power/`، `auto_client_acquisition/risk_resilience_os/strategic_drift.py`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "35_tests",
        "Tests & Guardrails",
        """
        ## فلسفة

        الحوكمة لا تكون حقيقية بدون اختبارات عقدية تمنع الانحدار.

        ## أمثلة أسماء ملفات (مرجعية)

        `test_no_source_passport_no_ai.py`، `test_pii_external_requires_approval.py`، `test_no_cold_whatsapp.py`، `test_no_linkedin_automation.py`، `test_no_scraping_engine.py`، `test_no_guaranteed_claims.py`، `test_output_requires_governance_status.py`، `test_proof_pack_required.py`، `test_agent_autonomy_mvp_limit.py`، `test_case_study_requires_verified_value.py` — إضافة إلى اختبارات الوكلاء في `tests/test_agentic_operations_os.py`.

        ## وثائق

        - `docs/testing/DEALIX_REQUIRED_TESTS.md`، `docs/enterprise_architecture/TESTS_REQUIRED.md`

        ## روابط

        - [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
    (
        "36_architecture",
        "Architecture — الحزم وحدود API وأولوية MVP",
        """
        ## شجرة الحزم (مرجعية)

        الهدف التنظيمي: `core_os`، `data_os`، `governance_os`، `llm_gateway`، `agent_os`، `workflow_os`، `revenue_os`، `brain_os`، `proof_os`، `value_os`، `capital_os`، `client_os`، `intelligence_os`، `command_os`، `trust_os`، `risk_os`، `standards_os`، `ecosystem_os`، `saudi_layer` — **التعيين الفعلي للمسارات** في `docs/enterprise_architecture/SYSTEM_MAP.md`.

        ## حدود API (ممنوع)

        - `revenue_os` لا يرسل رسائل خارجية مباشرة.
        - `agent_os` لا يتجاوز `governance_os`.
        - `brain_os` لا يجيب بلا source registry.
        - `client_os` لا يعرض مخرجات بلا governance status.
        - `proof_os` لا ينشئ case بلا proof score.

        ## أولوية تنفيذ MVP (مراحل)

        1. Core + Trust MVP: data/governance/llm/revenue/proof/value.  
        2. Commercial MVP: diagnostic، sprint، draft pack، proof، client summary، trust pack.  
        3. Retainer MVP: monthly value report، health، proof timeline، cadence، adoption review.  
        4. Agent-safe MVP: identity، permissions، auditability card، runtime policy، kill switch، agent tests.  
        5. Enterprise MVP: AI run ledger، evidence graph، approval engine، compliance report، trust dashboard، audit export.

        ## روابط

        - [SYSTEM_MAP.md](../enterprise_architecture/SYSTEM_MAP.md)، [API_BOUNDARIES.md](../enterprise_architecture/API_BOUNDARIES.md)، [MVP_BUILD_ORDER.md](../enterprise_architecture/MVP_BUILD_ORDER.md)، [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
        """,
    ),
]


def main() -> None:
    for rel, title, body in LAYERS:
        body_clean = textwrap.dedent(body).strip()
        path = DOCS / rel / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        text = f"# {title}\n\n{body_clean}\n"
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(REPO))


if __name__ == "__main__":
    main()
