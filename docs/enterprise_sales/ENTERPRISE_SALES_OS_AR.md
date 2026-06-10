# Enterprise Sales OS — نظام مبيعات المؤسسات

> **Agent 29 — Dealix Enterprise Sales Motion & ABM**
> **الإصدار:** v0.1 (Design Draft)
> **التاريخ:** 2026-06-03
> **المالك:** المؤسس (Founder) مع Sales Lead و Customer Success
> **اللغة الأساسية:** العربية — مع المصطلحات التقنية بالإنجليزية عند الحاجة

---

## 1. الرؤية المؤسسية (Mission)

**نظام Enterprise Sales OS** هو الإطار التشغيلي الذي يربط حركة المبيعات الموجّهة للحسابات الكبيرة (Account-Based Selling — ABM) في السوق السعودي بمنظومة Dealix الكاملة. يغطّي OS هذا:

- **اختيار الحسابات الاستراتيجية** (Tier-1 / Tier-2 / Tier-3) بدلًا من الـ spray-and-pray.
- **رسم خريطة كاملة للمشترين** (Buying Committee) ضمن المؤسسات الكبيرة.
- **تشغيل دورة بيع طويلة** تمتد من الاكتشاف (Discovery) إلى التوسّع بعد التسليم.
- **العمل مع Procurement** و **الأمن/الخصوصية** و **الشؤون القانونية** دون انزلاقات.
- **التحكّم بالمخاطر** (Deal Risk) على أساس أسبوعي.
- **التكامل الرأسي** مع `docs/commercial/` و `docs/enterprise/` و `docs/enterprise_rollout/` و `docs/governance/` دون تكرار.

**الرسالة المؤسسية (Mission Statement):**

> «نبيع للمؤسسات السعودية الكبيرة عبر شراكة مبنية على الأدلة، وليس عبر عروض شرائح (slide decks). كل حساب مؤسسي = خطة عمل مشتركة (Mutual Action Plan) قابلة للقياس، ومخاطر مُدارة، وتوسّع مُصمَّم من اليوم الأول.»

---

## 2. لماذا الآن (Why Now)

1. **نضج السوق المؤسسي السعودي:** رؤية 2030 دفعت الشركات الكبيرة (صناعية، رعاية صحية، اتصالات، خدمات مالية، عقار) نحو تبنّي AI كأولوية استراتيجية. KPMG وTechRadar يذكران قلق %60 من المؤسسات من بيانات/خصوصية AI.
2. **ارتفاع متوسط حجم الصفقة (ACV):** المؤسسات الكبيرة تدفع مقابل **حوكمة + تنفيذ + قياس**، وليس فقط مقابل «منتج». هذا يفتح شريحة سعرية مختلفة عن SMB/Commercial.
3. **تعقيد دورة البيع:** multi-stakeholder (6–10 صنّاع قرار)، دورات 3–9 أشهر، متطلبات Security/Privacy/Procurement مكثّفة. لا يمكن إدارة هذا بـ Sales Playbook الحالي وحده.
4. **الفرصة في ABM:** 80% من التأثير في B2B يأتي من 20% من الحسابات. ABM يحرّك الموارد حيث العائد.
5. **الفجوة في Dealix:** لدينا Enterprise Readiness OS (`docs/enterprise/`) و Enterprise Rollout (`docs/enterprise_rollout/`) و Commercial (`docs/commercial/`)، لكن لا يوجد حتى الآن **Enterprise Sales Motion** موحّد يربطهم في **حركة واحدة** من ABM → Discovery → Pilot → Expansion.

> **الـ OS هذا يُغطّي الفجوة بين التسويق والمبيعات وبين التسليم وتجديد العقد.**

---

## 3. خريطة النظام (Map of the OS)

ملفات النظام مرقّمة وفق الترتيب التشغيلي الطبيعي:

| # | الملف | الغرض | المالك |
|---|-------|--------|--------|
| 1 | [`ENTERPRISE_SALES_OS_AR.md`](ENTERPRISE_SALES_OS_AR.md) | هذا الملف — الفهرس والرؤية | المؤسس |
| 2 | [`ACCOUNT_BASED_SELLING_AR.md`](ACCOUNT_BASED_SELLING_AR.md) | تعريف ABM، اختيار الحسابات، النشاط، القياس | Sales Lead |
| 3 | [`TARGET_ACCOUNT_PROFILE_AR.md`](TARGET_ACCOUNT_PROFILE_AR.md) | TAP — قالب وملف الحساب بـ 14 حقلًا | Sales Lead |
| 4 | [`STAKEHOLDER_MAPPING_AR.md`](STAKEHOLDER_MAPPING_AR.md) | خريطة 10 أدوار للمشترين + رسائل | Sales Lead |
| 5 | [`BUYING_COMMITTEE_PLAYBOOK_AR.md`](BUYING_COMMITTEE_PLAYBOOK_AR.md) | ورشة، Power vs Interest، بناء coalition | Sales Lead |
| 6 | [`ENTERPRISE_DISCOVERY_AR.md`](ENTERPRISE_DISCOVERY_AR.md) | اجتماع اكتشاف 90 دقيقة، بنك أسئلة | Sales Lead |
| 7 | [`MUTUAL_ACTION_PLAN_AR.md`](MUTUAL_ACTION_PLAN_AR.md) | 10 مراحل من الاكتشاف إلى التوسّع | Sales Lead + Customer Success |
| 8 | [`EXECUTIVE_BUSINESS_CASE_AR.md`](EXECUTIVE_BUSINESS_CASE_AR.md) | صفحة واحدة لصانع القرار التنفيذي | المؤسس + Sales Lead |
| 9 | [`PILOT_TO_EXPANSION_PLAYBOOK_AR.md`](PILOT_TO_EXPANSION_PLAYBOOK_AR.md) | تصميم Pilot، 4 نماذج، سلّم التوسّع | Customer Success + Sales Lead |
| 10 | [`PROCUREMENT_SALES_PLAYBOOK_AR.md`](PROCUREMENT_SALES_PLAYBOOK_AR.md) | المشتريات، RFP/RFI، بنود (placeholders) | المؤسس + Sales Lead |
| 11 | [`ENTERPRISE_DEAL_RISK_REVIEW_AR.md`](ENTERPRISE_DEAL_RISK_REVIEW_AR.md) | 9 فئات مخاطر + مراجعة أسبوعية | Sales Lead |

---

## 4. ملكية الملفات (File Ownership)

| الملف | مالك أساسي | مالك ثانوي | تكرار المراجعة |
|-------|-----------|-----------|----------------|
| ENTERPRISE_SALES_OS_AR | المؤسس | Sales Lead | ربع سنوي |
| ACCOUNT_BASED_SELLING_AR | Sales Lead | المؤسس | ربع سنوي |
| TARGET_ACCOUNT_PROFILE_AR | Sales Lead | Marketing | ربع سنوي |
| STAKEHOLDER_MAPPING_AR | Sales Lead | CS Lead | نصف سنوي |
| BUYING_COMMITTEE_PLAYBOOK_AR | Sales Lead | CS Lead | نصف سنوي |
| ENTERPRISE_DISCOVERY_AR | Sales Lead | — | ربع سنوي |
| MUTUAL_ACTION_PLAN_AR | Sales Lead | CS Lead | نصف سنوي |
| EXECUTIVE_BUSINESS_CASE_AR | المؤسس | Sales Lead | نصف سنوي |
| PILOT_TO_EXPANSION_PLAYBOOK_AR | CS Lead | Sales Lead | نصف سنوي |
| PROCUREMENT_SALES_PLAYBOOK_AR | المؤسس | Sales Lead | نصف سنوي |
| ENTERPRISE_DEAL_RISK_REVIEW_AR | Sales Lead | المؤسس | ربع سنوي |

> **القاعدة:** أي تعديل على أكثر من ملفَين يتطلب نسخة جديدة (`version`) في الـ Change Log أسفل.

---

## 5. الربط مع الأنظمة القائمة (Linkage to Existing Systems)

| النظام القائم | ماذا نأخذ منه | ماذا لا نأخذ |
|--------------|---------------|----------------|
| `docs/commercial/` | `SALES_PLAYBOOK.md` (الـ inbound flow)، `OBJECTION_HANDLING_V6.md`، `OFFER_LADDER_AND_PRICING.md` | لا نكرر حركة SMB. الـ Enterprise layer يركب فوقها. |
| `docs/enterprise/` | `ENTERPRISE_READINESS_OS_AR.md`، `VENDOR_PROFILE_AR.md`، `SECURITY_OVERVIEW_AR.md`، `PRIVACY_OVERVIEW_AR.md`، `SLA_SLO_DRAFT_AR.md`، `PROCUREMENT_FAQ_AR.md`، `ENTERPRISE_OBJECTION_BANK_AR.md` | لا نكرر وثائق الـ Readiness. نربطها من ABM → Procurement. |
| `docs/enterprise_rollout/` | `ENTERPRISE_ENTRY_STRATEGY.md`، `ENTERPRISE_EXPANSION_PATH.md`، `DEPARTMENT_ROLLOUT_MODEL.md`، `ENTERPRISE_ROLES.md` | لا نكرر rollout model. الـ Sales OS يجهز العميل لـ rollout. |
| `docs/governance/` | `AI_CONTROL_PLANE.md`، `CONTROLS_MATRIX.md`، `ENTERPRISE_GOVERNANCE_LAYER.md` | لا نكرر governance. نستخدمها كـ proof artifact في الـ Business Case. |
| `docs/legal/` | `LEGAL_FOUNDER_SELF_EXECUTION.md`، `PARTNER_LEGAL_AGREEMENT.md`، `DPA_DEALIX_FULL.md` | الـ Sales OS يستشهد فقط، لا ينشئ عقود. |
| `docs/security/` | `SECURITY_GUIDE.md`، `SECURITY_RUNBOOK.md`، `PDPL_*` | نفس المبدأ. |
| `data/enterprise/` | `questionnaires.jsonl`، `risks.jsonl` (نمط schema) | الـ `enterprise_sales/` يستخدم نفس `$schema` key ونفس نمط JSONL. |

### تدفّق الربط (Cross-system Flow)

```
Marketing Qualified Account (MQA)
        │
        ▼
[Enterprise Sales OS — هذا الـ OS]
        │  ABM → TAP → Stakeholder Map → MAP
        ▼
Procurement & Security Review
        │  يستخدم docs/enterprise/ (DPA, SLA, Vendor Profile)
        ▼
Closed-Won → Pilot Delivery
        │  يستخدم docs/enterprise_rollout/ (Roles, Department Model)
        ▼
Expansion → Account Growth
        │  يستخدم docs/commercial/ upsell motion
        ▼
Renewal & Multi-department Rollout
```

---

## 6. حدود النظام (System Boundaries)

### ما هو داخل النطاق (In Scope)

- **ABM** لاختيار الحسابات المؤسسية وتحديد Tier-1/2/3.
- **TAP** كوثيقة رسمية لكل حساب مؤسسي.
- **Stakeholder Map** لـ 10 أدوار معيارية في Buying Committee.
- **Buying Committee Playbook** (ورشة + coalition + neutralization).
- **Enterprise Discovery** متعدد-الأصحاب-المصلحة (90 دقيقة).
- **Mutual Action Plan (MAP)** بـ 10 مراحل.
- **Executive Business Case** صفحة واحدة بالعربية.
- **Pilot-to-Expansion Playbook** بـ 4 نماذج Pilots + سلّم توسّع.
- **Procurement Sales Playbook** للسوق السعودي (RFP/RFI/RFQ + بنود placeholders).
- **Enterprise Deal Risk Review** بـ 9 فئات مخاطر ومراجعة أسبوعية.
- **Schemas + JSONL Data** لكل عنصر (Account, Stakeholder, MAP, Deal Risk).
- **3 تقارير مراجعة** (Pipeline, Account Plan, Deal Risk).
- **Final Report** يربط كل شيء.

### ما هو خارج النطاق (Out of Scope — لا يُغطّى هنا)

- **إنشاء العقود** (contracts) أو مراجعتها قانونيًا — هذا في `docs/legal/`.
- **كتابة DPA / MSA / SOW** كوثائق عميل — نُشير إلى `docs/enterprise/DPA_DEALIX_FULL.md` فقط.
- **إرسال أي تواصل خارجي** (Email/WhatsApp/Call) — ممنوع تمامًا في هذا الـ OS.
- **تحديد أسعار نهائية** بأرقام ثابتة — placeholders فقط، النطاقات السعريّة تتطلب تأكيد المؤسس (`founder-confirmed`).
- **حركة SMB / Commercial** — لها OS خاص في `docs/commercial/`.
- **Product roadmap** — في `docs/strategic/` و `roadmap_item.schema.json`.
- **Marketing site / content production** — في `docs/marketing/` و `GEO_CONTENT_CALENDAR.md`.
- **توليد Case Studies** — في `PROOF_AND_CASE_STUDY_SYSTEM.md`.
- **إدارة الـ Legal Entity / Tax / ZATCA** — في `docs/legal/` و `docs/compliance/`.

---

## 7. علامات الجاهزية (READY / PARTIAL / NEEDS_REVIEW)

> كل ملف وكل بند في هذا الـ OS يجب أن يحمل علامة جاهزية واحدة.

| العلامة | المعنى | الإجراء |
|---------|--------|---------|
| **READY** | مكتمل، مملوك، قابل للتنفيذ، ومراجَع ذاتيًا | لا يلزم إجراء |
| **PARTIAL** | مكتمل بنيويًا، لكن يحتاج تأكيد المؤسس (مثل الأسعار، الأسماء، النطاقات) | يحتاج مراجعة Founder قبل الاستخدام في عرض حقيقي |
| **NEEDS_REVIEW** | مسودة، أو به فجوات معرفية، أو يحتاج Owner ثانوي ليُكمل | يوضع في `reports/enterprise_sales/ENTERPRISE_SALES_FINAL_REPORT.md` كـ Open Question |

### كيف نضع العلامة

في رأس كل ملف من ملفات الـ 11:
```markdown
> **Status:** READY | PARTIAL | NEEDS_REVIEW
> **Evidence Level:** assumption | observed | validated | measured
> **Owner:** [Name / Role]
```

`evidence_level` يجب أن يُحدّد لكل صف في JSONL، وكذلك لكل قسم في الـ docs (assumption كقاعدة design-time).

---

## 8. مؤشرات الأداء (KPIs) — على مستوى OS

> لا توجد أرقام فعلية حتى الآن. النطاقات هنا placeholders للأهداف المستقبلية.

| المؤشر | الهدف (placeholder) | تكرار القياس |
|--------|---------------------|--------------|
| عدد الحسابات Tier-1 النشطة | 3–5 | شهري |
| Pipeline Coverage (3× ACV المستهدف) | مُحقَّق | شهري |
| Multi-threading Index (≥4 stakeholders/account) | ≥80% | شهري |
| متوسط دورة البيع Tier-1 | founder-confirmed range | ربع سنوي |
| نسبة Pilot-to-Close (closed-won) | founder-confirmed range | ربع سنوي |
| نسبة التوسّع في السنة الأولى | founder-confirmed range | سنوي |
| نقاط مخاطر مغلقة/أسبوع | tracked only | أسبوعي |

> **لا توجد أرقام فعلية مُقاسَة** في هذه النسخة. مؤشرات القياس تحتاج أول Closed-Won لتُعاير.

---

## 9. Change Log

| التاريخ | الإصدار | المؤلف | التغيير |
|---------|---------|--------|---------|
| 2026-06-03 | v0.1 (Design Draft) | Agent 29 — Enterprise Sales & ABM | إنشاء أولي لإطار Enterprise Sales OS، 11 ملف + 4 schemas + 4 data + 3 reports + final report |

---

## 10. Open Questions (للمراجعة من المؤسس)

1. **قائمة Tier-1 الفعلية** — ما هي الحسابات السعودية الـ 5 الأولى التي سنستهدفها في الـ 12 شهرًا القادمة؟ (مجهولة الهوية حتى الآن).
2. **نطاق السعرة** — ما هي النطاقات المعتمدة لـ Pilot، Annual Contract، Multi-department Rollout؟ (placeholders فقط في هذا الـ OS).
3. **تشكيل فريق ABM** — هل سيتم تعيين ABM Specialist أم سيُدار من قِبل Sales Lead + المؤسس؟
4. **Procurement Templates** — هل لدينا MSA / SOW / NDA فعلية معتمدة من المستشار القانوني؟ (الـ OS يفترض وجودها في `docs/enterprise/`).
5. **CRM** — ما الحقل الذي سيخزّن `account_id` و `stakeholder_id`؟ (HubSpot أم حل محلي؟).
6. **Security Review SLA** — ما هو الزمن المستهدف لإجابة استبيان Security؟ (مؤسسيًا 5–10 أيام عمل).

---

> **آخر تحديث:** 2026-06-03
> **حالة OS:** Design Draft — READY (structure) / PARTIAL (numerical content) / NEEDS_REVIEW (Tier-1 list, pricing, ABM team shape)
