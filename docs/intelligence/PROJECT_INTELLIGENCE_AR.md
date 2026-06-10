# ذكاء المشروع (Project Intelligence) — عربي

**الوظيفة:** تمكين Dealix (والوكلاء والبشر) من **فهم المستودع والوثائق كمنظومة تشغيل واحدة** — ليس مجرد بحث نصي، بل ربط بين **الكود، المعايير، الحوكمة، الإثبات، والتمويل التشغيلي** بحيث يصبح المشروع **قابلاً للشرح والتدقيق** كما في طبقات المؤسسة الأخيرة.

**الفرق عن «طبقة الذكاء التشغيلي»:**  
- **Project Intelligence** = **ماذا يوجد في الريبو وكيف يُرتب ويُفهرس ويُستعلم عنه** (خريطة، فهرسة، RAG محلي، أسئلة على الهيكل).  
- **`docs/intelligence/` (Intelligence Layer)** = **كيف تتخذ Dealix قرارات تشغيلية** (أحداث، ledgers، مؤشرات، SCALE/KILL، venture signals) — راجع [`INTELLIGENCE_LAYER.md`](INTELLIGENCE_LAYER.md).  
- **`docs/intelligence_compounding/`** = **كيف يتراكم التعلم الآمن عبر العملاء** (سوق، عميل، بيانات، workflow، حوكمة، منتج، benchmarks، عربية) — راجع [`../intelligence_compounding/INTELLIGENCE_COMPOUNDING_SYSTEM.md`](../intelligence_compounding/INTELLIGENCE_COMPOUNDING_SYSTEM.md) مقابل `intelligence_os` الأوسع في الكود.  
- **`docs/board_decision_system/`** = **كيف تُحوَّل الإشارات إلى قرارات CEO/Board** (scorecards، memo، رهانات، بوابة وكلاء، مخاطر، تخصيص رأس مال لوحي) — راجع [`../board_decision_system/STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md`](../board_decision_system/STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md) و`board_decision_os`.  
- **`docs/risk_resilience/`** = **مخاطر استراتيجية، امتثال، وصمود** (taxonomy، قنوات، وكلاء، شركاء، انحراف، سجل، لوحة، طبقة سعودية) — راجع [`../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md`](../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md) و`risk_resilience_os`.  
- **`docs/compliance_trust_ops/`** = **امتثال-by-design وتشغيل ثقة** (Passport، قرارات حوكمة، audit، تقارير، ادعاءات، حوادث، طبقة سعودية، لوحة) — راجع [`../compliance_trust_ops/COMPLIANCE_BY_DESIGN.md`](../compliance_trust_ops/COMPLIANCE_BY_DESIGN.md) و`compliance_trust_os`.

---

## 1) المكونات التقنية المحلية (كما في قرار الـ AI Stack)

- **فهرسة محلية:** `scripts/index_project_memory.py` — يغذي ذاكرة مشروع محلية (`scan_project`, `chunk_text`, `naive_search` — راجع [`../AI_STACK_DECISIONS.md`](../AI_STACK_DECISIONS.md)).
- **واجهة API والتشغيل الآمن:** `api/` مع أنماط موافقة وحوكمة (لا إرسال خارجي صامت).
- **ذاكرة استراتيجية/مشروع:** مسارات Supabase/Postgres/pgvector حسب إعداد البيئة — لا تخلط بيانات عميل إنتاج مع فهرسة الريبو المحلية.

**قاعدة:** أي إجابة من «ذكاء المشروع» عن المستودع يجب أن تبقى **قابلة للتتبع** إلى ملف أو مسار (مسار وثيقة، أو رمز، أو اختبار).

---

## 2) خريطة الطبقات المؤسسية الحديثة (وثائق + كود)

هذه الطبقات **تغذي** ذكاء المشروع لأنها تضيف **مسارات ثابتة الاسم** يتعلمها السوق داخل الريبو:

| الطبقة | وثائق | كود مساند (حيث يوجد) |
|--------|--------|------------------------|
| حوكمة مؤسسية | [`../institutional_control/`](../institutional_control/INSTITUTIONAL_GOVERNANCE.md) | `auto_client_acquisition/institutional_control_os/` |
| توسع مؤسسي | [`../institutional_scaling/`](../institutional_scaling/INSTITUTIONAL_SCALING_DOCTRINE.md) | `auto_client_acquisition/institutional_scaling_os/` |
| جاهزية مجلس / مستثمر | [`../board_ready/`](../board_ready/BOARD_LEVEL_THESIS.md) | `auto_client_acquisition/board_ready_os/` |
| إثبات وقيمة | [`../proof_architecture/`](../proof_architecture/ENTERPRISE_PROOF_ARCHITECTURE.md) | `auto_client_acquisition/proof_architecture_os/` |
| التقاط قيمة وتسعير | [`../value_capture/`](../value_capture/VALUE_CAPTURE_ARCHITECTURE.md) | `auto_client_acquisition/value_capture_os/` |
| نظام تشغيل العميل | [`../client_os/`](../client_os/CLIENT_OPERATING_SYSTEM.md) | `auto_client_acquisition/client_os/` |
| منظومة ecosystem | [`../ecosystem/`](../ecosystem/ECOSYSTEM_EXPANSION_SYSTEM.md) | `auto_client_acquisition/ecosystem_os/` |
| معايير وشهادات (D-GAOS) | [`../standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md`](../standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) · [`../certification/CERTIFICATION_SYSTEM.md`](../certification/CERTIFICATION_SYSTEM.md) | `auto_client_acquisition/standards_os/` |
| تبني مؤسسي وتغيير | [`../adoption/`](../adoption/ENTERPRISE_ADOPTION_SYSTEM.md) | `auto_client_acquisition/adoption_os/` |
| Rollout enterprise | [`../enterprise_rollout/`](../enterprise_rollout/ENTERPRISE_ROLLOUT_PLAYBOOK.md) | `auto_client_acquisition/enterprise_rollout_os/` |
| تمويل تشغيلي ورأس مال | [`../operating_finance/`](../operating_finance/OPERATING_FINANCE_SYSTEM.md) | `auto_client_acquisition/operating_finance_os/` |
| تعلم مركّب (Data & Intelligence Compounding) | [`../intelligence_compounding/INTELLIGENCE_COMPOUNDING_SYSTEM.md`](../intelligence_compounding/INTELLIGENCE_COMPOUNDING_SYSTEM.md) | `auto_client_acquisition/intelligence_compounding_os/` |
| ذكاء استراتيجي وقرارات Board | [`../board_decision_system/STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md`](../board_decision_system/STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md) | `auto_client_acquisition/board_decision_os/` |
| مخاطر ومرونة وحوكمة | [`../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md`](../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md) | `auto_client_acquisition/risk_resilience_os/` |
| امتثال وتشغيل ثقة (Compliance-by-Design) | [`../compliance_trust_ops/COMPLIANCE_BY_DESIGN.md`](../compliance_trust_ops/COMPLIANCE_BY_DESIGN.md) | `auto_client_acquisition/compliance_trust_os/` |

**علاقة الذكاء التشغيلي:** قرارات مثل «هل نوسّع؟» أو «هل نستثمر في ميزة؟» يجب أن تلتقي مع:
- أدوات **`proof_architecture_os`** (مستويات Proof 1–5، Proof Score، مقاييس القيمة حسب العرض، بوابة retainer، venture gate)، و  
- أدوات **`value_capture_os`** (جودة الإيراد والعميل، سلالم التوسع، upsell من إشارات Proof، تصنيف تغيير النطاق، أرضيات الهامش)، و  
- أدوات **`client_os`** (صحة العميل، لوحات الجاهزية/الحوكمة/الـtimeline، تقرير القيمة الشهري، توسع من إشارات الـworkspace، شفافية الوكلاء)، و  
- أدوات **`ecosystem_os`** (جودة الشريك، بوابة الشريك، شهادات، benchmarks آمنة، تسلسل الإطلاق، venture gate)، و  
- أدوات **`standards_os`** (D-GAOS: جواز مصدر، حوكمة وقت التشغيل، حدود وكيل MVP، Proof Pack v2، اختبار شهادة، بوابة عهد الشريك)، و  
- أدوات **`adoption_os`** (Adoption Score، kit التمكين، مراجعة التبني، احتكاك→منتج، جاهزية retainer من الاستخدام، لوحة التبني)، و  
- أدوات **`enterprise_rollout_os`** (مراحل Land→Institutionalize، بوابات الاعتماد السبع، kit التسليم، إشارات سحب المنصة، لوحة rollout)، و  
- **`operating_finance_os`** (تخصيص رأس مال، فلتر إيراد سيء، مراجعة رأس مال)،  
إضافة إلى وثائق [`CAPITAL_ALLOCATION_SCORE.md`](CAPITAL_ALLOCATION_SCORE.md) و[`DECISION_ENGINE.md`](DECISION_ENGINE.md) داخل نفس مجلد الذكاء.

---

## 3) ماذا يجب أن «يعرفه» فهر المشروع؟

### أ) هيكل الريبو ذي الصلة بالتشغيل

- **`docs/company/`** — POSITIONING، خدمات، جاهزية.  
- **`docs/product/`** — سجل وكلاء، provenance، حوكمة مخرجات.  
- **`docs/governance/`** — موافقات، سياسات، retention، PII.  
- **`docs/trust/`** — Enterprise Trust Pack (canonical).  
- **`docs/strategy/`**، **`docs/saudi/`** — سياق سوقي وسعودي.  
- **`auto_client_acquisition/*_os/`** — بوابات رقمية محضة (scores، flags) تُختبر بـ `tests/test_*_os.py`.

### ب) نقاط تحقق الجاهزية

- **`scripts/verify_company_ready.py`** — تجميع وجود ملفات شركة + حزمة اختبارات سريعة (`DEALIX_COMPANY_READY`).  
- **`AGENTS.md`** — كيفية تشغيل الخدمات والاختبارات السريعة.

---

## 4) سلوك الوكيل عند الإجابة عن «ماذا بنينا؟»

1. **اربط الادعاء بمسار:** `docs/...` أو `auto_client_acquisition/...` أو `tests/...`.  
2. **اميز وثيقة إطار من تنفيذ كود:** الوثيقة تصف السياسة؛ الكود يطبّق **بوابات** فقط حيث وُجد.  
3. **لا تخلط** بين `docs/intelligence/CAPITAL_ALLOCATION_SCORE.md` (إطار قرار في طبقة الذكاء) وبين **`operating_finance_os`** (حسابات/قوائم تحقق في الكود) — كلاهما مكمل.  
4. للـ**Trust / PDPL / منع واتساب البارد:** ابدأ من [`../trust/ENTERPRISE_TRUST_PACK.md`](../trust/ENTERPRISE_TRUST_PACK.md) و[`../institutional_control/`](../institutional_control/INSTITUTIONAL_GOVERNANCE.md).

---

## 5) الصعود السريع

| موضوع | مسار |
|--------|------|
| مخطط التنفيذ السيادي | [`../blueprint/SOVEREIGN_EXECUTION_BLUEPRINT.md`](../blueprint/SOVEREIGN_EXECUTION_BLUEPRINT.md) |
| فهرس المستودع | [`../company/MASTER_REPOSITORY_INDEX.md`](../company/MASTER_REPOSITORY_INDEX.md) |
| ذكاء التشغيل (فهرس) | [`README.md`](README.md) |
| قرار مكدس AI | [`../AI_STACK_DECISIONS.md`](../AI_STACK_DECISIONS.md) |

---

## الخلاصة

> **Project Intelligence** يجعل المستند ليس «مجلد ملفات» بل **ذاكرة تشغيلية مرتبة**: تعرف أين المعيار، أين الحوكمة، أين الإثبات، أين تخصيص رأس المال، وأين الاختبارات التي تثبت أن البوابات تعمل — وهذا يدعم بالضبط ما تبنيه Dealix كـ **Revenue OS محكوم** وليس كـ وكالة تنفذ مهامًا.
