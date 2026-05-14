# Dealix Sovereign Execution Blueprint — المخطط السيادي للتنفيذ

**الفكرة:** تحويل كل الطبقات السابقة إلى **نظام تشغيل نهائي** — بداية، قياس، حوكمة، ربح، توسع، و**إيقاف** ما يضر. Dealix لا تعتمد على العبقرية اللحظية؛ تعتمد على نظام يجعل **القرار الصحيح هو الافتراضي**.

---

## 1. النموذج النهائي

**Dealix = Governed Capability Company** — تبيع **قدرة تشغيلية محكومة قابلة للقياس**، لا «AI» كسلعة عامة.

تفاصيل الصياغة: [`../00_constitution/DEALIX_CONSTITUTION.md`](../00_constitution/DEALIX_CONSTITUTION.md).

---

## 2. لماذا الآن؟

استثمار واسع في AI مع فجوة **استراتيجية وROI** ومشاريع عالقة في pilot — انظر [IT Pro — enterprise AI adoption and FOMO](https://www.itpro.com/business/business-strategy/ai-adoption-projects-keep-failing-but-enterprise-fomo-means-investment-is-still-rising). في السعودية، استخدام GenAI واسع مع مخاوف خصوصية وحاجة لتدريب — [arXiv:2601.18234](https://arxiv.org/abs/2601.18234). محلياً، دراسات حديثة لمواقع التجارة الإلكترونية تشير إلى **فجوات امتثال/شفافية** في سياسات الخصوصية (مثال: نسب منخفضة لإعلان عناصر PDPL رئيسية في عينة) — [arXiv:2602.18616](https://arxiv.org/abs/2602.18616).

---

## 3. الاثنا عشر نظامًا مترابطًا

كل نظام يرفع مخرجات السابق:

| # | النظام | وظيفة مختصرة |
|---|--------|----------------|
| 1 | **Constitution** | من نحن وماذا لا نفعل |
| 2 | **Capability** | لغة «رفع القدرة» ومستويات 0–5 |
| 3 | **Offer** | عروض مُنتَجة بمسار proof وretainer |
| 4 | **Delivery** | تسليم متكرر بمراحل واضحة |
| 5 | **Governance** | runtime لا PDF فقط |
| 6 | **Proof** | اقتصاد الثقة · Proof Pack |
| 7 | **Capital** | أصول تتراكم لكل مشروع |
| 8 | **Productization** | من التكرار إلى module |
| 9 | **Intelligence** | قراءة ledgers → قرار |
| 10 | **Business Unit** | charter · KPIs · playbook |
| 11 | **Venture** | بوابة spinout |
| 12 | **Standards** | امتلاك الفئة عبر Method |

---

## 4. Capability System (مستويات 0–5)

**القدرات السبع:** Revenue · Customer · Operations · Knowledge · Data · Governance · Reporting.

لكل عميل: Current · Target · Transformation Gap · Best Starting Sprint · Expected Proof · Retainer Path.

| Level | معنى |
|-------|------|
| 0 | Absent |
| 1 | Manual |
| 2 | Structured |
| 3 | AI-Assisted |
| 4 | Governed Workflow |
| 5 | Optimized OS |

**مراجع:** [`../intelligence/CAPABILITY_INDEX.md`](../intelligence/CAPABILITY_INDEX.md) · [`../intelligence/CLIENT_CAPABILITY_REPORT.md`](../intelligence/CLIENT_CAPABILITY_REPORT.md).

---

## 5. Offer → Delivery → إكمال المشروع

**سلم العروض:** Diagnostic → Sprint → Pilot → Retainer → Enterprise.

**شروط العرض:** buyer · pain · outcome · scope · exclusions · price · QA · governance boundary · proof path · **next offer**. **أي عرض بلا Proof Path لا يُعرض.**

**دورة التسليم:** Intake → Scope → Data Request → Build → Governance Check → QA → Delivery → Handoff → **Proof** → Next Step.

**قاعدة الإكمال:** لا يُغلق المشروع حتى: deliverables · QA · governance نظيفة · **Proof Pack** · **capital asset** · **next offer** موصى به.

---

## 6. Governance System (Runtime)

كل مخرج يمر: source · PII · allowed_use · claims · channels · approval · audit · risk score.

**قرارات:** ALLOW · ALLOW_WITH_REVIEW · DRAFT_ONLY · REQUIRE_APPROVAL · REDACT · BLOCK · ESCALATE.

**لماذا runtime؟** سلوك الوكلاء **path-dependent**؛ تقييم السياسات أثناء التشغيل — [arXiv:2603.16586](https://arxiv.org/abs/2603.16586).

**الممنوعات:** [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).

---

## 7. Proof · Capital · Productization

**Proof Pack** يحتوي عناصر: Problem · Inputs · Work · Metrics · Before/After · AI Outputs · Governance Events · Value · Risks · Next Step.

**قاعدة:** No proof → no claim · no case study · no retainer push قوي.

**Capital:** Trust + (Product أو Knowledge) + Expansion Path — راجع [`../command/CAPITAL_CREATION_SCORE.md`](../command/CAPITAL_CREATION_SCORE.md).

**Productization path:** Manual → … → SaaS Module · **بنا من التكرار لا من الخيال** (3+ · مرتبط إيراد · وقت/خطر · اختبار · إعادة استخدام).

---

## 8. Intelligence · BU · Venture · Standards

- **Intelligence:** events/ledgers → Scale · Build · Pilot · Hold · Kill · … — [`../intelligence/STRATEGY_OFFICE.md`](../intelligence/STRATEGY_OFFICE.md) · `intelligence_os` / `command_os`.
- **BU:** problem · buyer · offers · module · proof type · KPIs · playbook · risk · owner — [`../group/BUSINESS_UNIT_MODEL.md`](../group/BUSINESS_UNIT_MODEL.md).
- **Venture Gate:** [`../ventures/VENTURE_GRADUATION_GATE.md`](../ventures/VENTURE_GRADUATION_GATE.md) · `enterprise_os/venture_factory.py`.
- **Standards:** Dealix Method + Data / Governance Runtime / Proof / QA / Capital / Capability — [`../standards/`](../standards/DEALIX_METHOD.md).

---

## 9. البنية التقنية (Modular Monolith)

**قاعدة:** ليست microservices الآن — **monolith وحدود واضحة**.

**توجيهات تنفيذية (الكود الحالي):**

- استدعاءات LLM عبر طبقة موحّدة (`llm_gateway` / نماذج موجودة حسب الريبو).
- الحوكمة عبر `governance_os` قبل المخرج الحساس.
- إغلاق مشروع بـ Proof عبر `reporting_os` / معايير Proof Pack.
- تكرار العمل يُسجّل في **Productization Ledger** (`docs/product/PRODUCTIZATION_LEDGER.md`).

**خرطة تفصيلية:** [`../architecture/MODULAR_MONOLITH.md`](../architecture/MODULAR_MONOLITH.md) · [`../architecture/CORE_OS.md`](../architecture/CORE_OS.md).

---

## 10. Event-driven spine (أحداث مرجعية)

أمثلة: `project_created` · `client_intake_completed` · `data_quality_scored` · `governance_checked` · `ai_run_completed` · `approval_granted` · `proof_event_created` · `capital_asset_created` · `retainer_recommended` · `venture_signal_detected` — تبني audit · ledgers · Command Center · Client Timeline.

**مرجع:** [`../architecture/EVENT_MODEL.md`](../architecture/EVENT_MODEL.md).

---

## 11. Scorecards

مراجع جاهزة: [`../scorecards/`](../scorecards/CLIENT_SCORECARD.md) · حقول `auto_client_acquisition/scorecards/`.

---

## 12. Kill Criteria

**القوة في الإيقاف:** [`../command/KILL_PROTOCOL.md`](../command/KILL_PROTOCOL.md) · `command_os/kill_criteria.py` · `kill_protocol.py`.

---

## 13. Endgame

**Saudi/MENA Governed AI Operations Holding** — Core OS · خدمات مُنتَجة · Proof Economy · Capital Ledger · BU · Standards · Academy · Partners · Ventures.

**فلايويل مختصر:** Services ↔ Cloud · Proof ↔ Sales · Academy ↔ Partners · Labs ↔ Ventures · Standards ↔ Category.

---

## 14. السلسلة التنفيذية الختامية

`Constitution → Capability → Offers مُنتَجة → Delivery متكرر → Governance runtime → Proof → Capital → Productization → Intelligence → BU → Ventures → Standards → Academy/Partners → Holding`

**الجملة:** من شركة «تنفّذ AI» إلى **نظام سيادي** يبني قدرات محكومة، يثبت أثرها، يحوّلها لأصول، ثم يُخرج منتجات ووحدات وventures تحت **Core OS واحد**.

---

## 15. مداخل سريعة

| موضوع | مسار |
|--------|------|
| دستور + ممنوعات + مبادئ قرار | [`../00_constitution/`](../00_constitution/DEALIX_CONSTITUTION.md) |
| Meta-OS (9 أنظمة فرعية سابقة) | [`../meta/META_OPERATING_SYSTEM.md`](../meta/META_OPERATING_SYSTEM.md) |
| تنفيذ عالمي | [`../command/COMMAND_SYSTEM.md`](../command/COMMAND_SYSTEM.md) |
| طبقة استثمارية وموثوقية (thesis · PMF · trust) | [`../investment/INVESTMENT_THESIS.md`](../investment/INVESTMENT_THESIS.md) · [`../trust/ENTERPRISE_TRUST_PACK.md`](../trust/ENTERPRISE_TRUST_PACK.md) |
| طبقة التوسع السيادي | [`../scale/SCALE_MODEL.md`](../scale/SCALE_MODEL.md) · [`../scale/SCALE_GATES.md`](../scale/SCALE_GATES.md) |
| طبقة الفئة والقابضة | [`../category/CATEGORY_DOMINANCE.md`](../category/CATEGORY_DOMINANCE.md) · [`../holding/HOLDING_PLAYBOOK.md`](../holding/HOLDING_PLAYBOOK.md) · [`../saudi/SAUDI_ADVANTAGE.md`](../saudi/SAUDI_ADVANTAGE.md) |
| طبقة القوة السوقية (لغة · توزيع · benchmarks) | [`../market_power/MARKET_POWER_SYSTEM.md`](../market_power/MARKET_POWER_SYSTEM.md) |
| خريطة الهيمنة التنفيذية | [`../dominance/DOMINANCE_EXECUTION_MAP.md`](../dominance/DOMINANCE_EXECUTION_MAP.md) |
| مخطط الإمبراطورية التشغيلية | [`../operating_empire/OPERATING_EMPIRE_BLUEPRINT.md`](../operating_empire/OPERATING_EMPIRE_BLUEPRINT.md) |
| علوية التنفيذ (cadence · gates · scorecards · قرار) | [`../execution/EXECUTION_SUPREMACY_SYSTEM.md`](../execution/EXECUTION_SUPREMACY_SYSTEM.md) |
| الخندق التشغيلي الاستراتيجي (moat مركب) | [`../moat/STRATEGIC_OPERATING_MOAT.md`](../moat/STRATEGIC_OPERATING_MOAT.md) |
| عقيدة التشغيل النهائية (holding + سلسلة مقدسة) | [`../endgame/ENDGAME_OPERATING_DOCTRINE.md`](../endgame/ENDGAME_OPERATING_DOCTRINE.md) |
| النموذج العالمي المؤسسي (trust + DCI + سلم جاهزية) | [`../global_grade/GLOBAL_GRADE_OPERATING_MODEL.md`](../global_grade/GLOBAL_GRADE_OPERATING_MODEL.md) |
| السيادة التشغيلية (model/data/commercial/distribution) | [`../sovereignty/OPERATING_SOVEREIGNTY.md`](../sovereignty/OPERATING_SOVEREIGNTY.md) |
| الدليل التشغيلي النهائي (جمع الطبقات) | [`../ultimate_manual/ULTIMATE_OPERATING_MANUAL.md`](../ultimate_manual/ULTIMATE_OPERATING_MANUAL.md) |
| الحوكمة المؤسسية (تحكم · تدقيق · Proof) | [`../institutional_control/INSTITUTIONAL_GOVERNANCE.md`](../institutional_control/INSTITUTIONAL_GOVERNANCE.md) |
| عقيدة التوسع المؤسسي (سلم · flywheel · metrics) | [`../institutional_scaling/INSTITUTIONAL_SCALING_DOCTRINE.md`](../institutional_scaling/INSTITUTIONAL_SCALING_DOCTRINE.md) |
| البنية الجاهزة للمجلس / المستثمر | [`../board_ready/BOARD_LEVEL_THESIS.md`](../board_ready/BOARD_LEVEL_THESIS.md) |
| عمود فقري للقيمة والإثبات (Proof & Value) | [`../proof_architecture/ENTERPRISE_PROOF_ARCHITECTURE.md`](../proof_architecture/ENTERPRISE_PROOF_ARCHITECTURE.md) |
| تمويل تشغيلي وتخصيص رأس مال | [`../operating_finance/OPERATING_FINANCE_SYSTEM.md`](../operating_finance/OPERATING_FINANCE_SYSTEM.md) |
| خريطة المجلدات 00–13 | [`../meta/META_REPOSITORY_MAP.md`](../meta/META_REPOSITORY_MAP.md) |
