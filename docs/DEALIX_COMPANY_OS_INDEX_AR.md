# فهرس نظام Dealix التشغيلي الشامل — DEALIX_COMPANY_OS_INDEX_AR

> **هذا هو الفهرس الرئيسي لنظام Dealix التشغيلي** (Company OS). كل نظام فرعي مرتبط هنا بملف الدخول الخاص به. كل نظام إما **جديد** (بُني في الموجة 29-33) أو **قائم** (legacy).
>
> **آخر تحديث:** 2026-06-03
> **المالك:** المؤسس (Founder)
> **اللغة الأساسية:** العربية
> **الإصدار:** v1.0
> **agent-context:** Agent #35 — Final Integration

---

## 1. كيف تقرأ هذا الفهرس

| الرمز | المعنى |
|-------|--------|
| **جديد** | أُنشئ في الموجة الأخيرة (Agents 29-33). له وثائق + مخططات + بيانات + تقارير. |
| **قائم** | وُجد قبل الموجة الأخيرة. هو البنية الأساسية لـ Dealix. |
| **بوابة** | ملف الـ OS الرئيسي الذي يجب قراءته أولاً لكل نظام. |
| **FR** | ملف التقرير النهائي للنظام في `reports/<system>/`. |

> **القاعدة الذهبية:** عند البحث عن ملف، ابدأ بهذا الفهرس → اضغط على البوابة → ثم ادخل إلى الـ OS الفرعي.

---

## 2. الأنظمة الجديدة (Wave 29-33) — NEW

| # | النظام | الوصف (سطران) | البوابة (اقرأ أولاً) | عدد الملفات |
|---|--------|----------------|---------------------|-------------|
| 1 | **Enterprise Sales OS** (Agent 29) | نظام مبيعات المؤسسات (ABM) — اختيار الحسابات، خريطة المشترين، Discovery، Mutual Action Plan، إدارة المخاطر الأسبوعية، Pilot → Expansion. | [`docs/enterprise_sales/ENTERPRISE_SALES_OS_AR.md`](enterprise_sales/ENTERPRISE_SALES_OS_AR.md) | 11 doc + 4 data + 4 report + 7 schema = **26 ملف** |
| 2 | **AI Agent Governance OS** (Agent 30) | نظام حوكمة وكلاء الذكاء الاصطناعي — تسجيل الوكلاء، مستويات الاستقلالية A0-A5، دورة حياة الصلاحيات، الحوادث، التقييم الأسبوعي. | [`docs/ai_governance/AI_AGENT_GOVERNANCE_OS_AR.md`](ai_governance/AI_AGENT_GOVERNANCE_OS_AR.md) | 9 doc + 4 data + 4 report + 4 schema = **21 ملف** |
| 3 | **Data Products OS** (Agent 31) | نظام منتجات البيانات — معايير القطاع، مكتبة أداء الرسائل، استخبارات الاعتراضات، نموذج أداء العروض، أنماط التسليم، إشارات التجديد، حساسية التسعير. | [`docs/data_products/DATA_PRODUCTS_OS_AR.md`](data_products/DATA_PRODUCTS_OS_AR.md) | 8 doc + 6 data + 3 report + 9 schema = **26 ملف** |
| 4 | **Offer Landing Page System** (Agent 33) | نظام صفحات العروض الموحّد — 6 صفحات عروض جاهزة (Diagnostic, Followup, AI Starter, Full OS, Monthly, Custom) + مكتبة FAQ + مكتبة CTA. | [`docs/offers/OFFER_LANDING_PAGE_SYSTEM_AR.md`](offers/OFFER_LANDING_PAGE_SYSTEM_AR.md) | 9 doc + 0 data + 2 report + 2 schema = **13 ملف** |

> **المجموع:** 4 أنظمة جديدة × (docs + data + reports + schemas) = **86 ملف** موثّق، **Arabic-first**، JSONL مملوء بـ placeholders موافقة للمؤسس.

---

## 3. الأنظمة القائمة (Legacy) — حافظ على المرجعية

### 3.1 السوق والمبيعات التجارية (Commercial)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Commercial OS | الحركة التجارية الكاملة — Lead → Proposal → Pilot → Payment → Upsell | [`docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md`](commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| Sales (legacy) | سكريبتات، صفحات، بروبوزل، follow-up | [`docs/sales/SALES_PLAYBOOK.md`](sales/SALES_PLAYBOOK.md) |

### 3.2 المؤسسات والإطلاق المؤسسي (Enterprise + Rollout)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Enterprise Readiness | الجاهزية المؤسسية (security, privacy, procurement, support) | [`docs/enterprise/ENTERPRISE_READINESS_OS_AR.md`](enterprise/ENTERPRISE_READINESS_OS_AR.md) |
| Enterprise Rollout | استراتيجية دخول المؤسسات ودوران الفِرَق | [`docs/enterprise_rollout/ENTERPRISE_ROLLOUT_PLAYBOOK.md`](enterprise_rollout/ENTERPRISE_ROLLOUT_PLAYBOOK.md) |
| Trust Pack | رزمة الثقة المؤسسية | [`docs/enterprise_trust/ENTERPRISE_TRUST_DATA_ROOM.md`](enterprise_trust/ENTERPRISE_TRUST_DATA_ROOM.md) |

### 3.3 العمليات والتسليم (Operations + Delivery)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Operations | التشغيل اليومي للمؤسس | [`docs/operations/DEALIX_READINESS.md`](operations/DEALIX_READINESS.md) |
| Delivery | تسليم العملاء — معايير SOW، SLA، handoff | [`docs/delivery/DELIVERY_LIFECYCLE.md`](delivery/DELIVERY_LIFECYCLE.md) |
| Client OS / CS | نظام العميل + Customer Success | [`docs/client_os/`](client_os/) · [`docs/customer_success/CUSTOMER_SUCCESS_FINAL_REPORT.md`](../reports/customer_success/CUSTOMER_SUCCESS_FINAL_REPORT.md) |
| Phase-E / Launch | طقم الإطلاق + أوامر الفوتر | [`docs/phase-e/`](phase-e/) · [`docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md`](launch/DEALIX_LAUNCH_NOW_BUNDLE.md) |

### 3.4 الحوكمة والأمان (Governance + Security + Responsible AI)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Governance | حوكمة النظام الكاملة — A0-A5، approval matrix | [`docs/governance/GOVERNANCE_DECISION.md`](governance/GOVERNANCE_DECISION.md) |
| Security | الأمن السيبراني، prompt injection، keys | [`docs/security/INCIDENT_RESPONSE_RUNBOOK_AR.md`](security/INCIDENT_RESPONSE_RUNBOOK_AR.md) |
| Responsible AI | معايير الذكاء الاصطناعي المسؤول | [`docs/responsible_ai/RESPONSIBLE_AI_OPERATING_STANDARD.md`](responsible_ai/RESPONSIBLE_AI_OPERATING_STANDARD.md) |
| Legal | العقود، DPA، MSA، PDPL | [`docs/legal/`](legal/) |

### 3.5 البيانات (Data Governance + Data Products legacy)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Data Governance | جودة البيانات، الاحتفاظ، PII redaction | [`docs/data_governance/DATA_GOVERNANCE_OS_AR.md`](data_governance/DATA_GOVERNANCE_OS_AR.md) |
| Data (top) | المخططات والـ data tiers | [`docs/data/`](data/) |

### 3.6 المالية والسوق والمنتج

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Finance | اقتصاد الوحدة، تسعير، CAC | [`docs/finance/COMMERCIAL_UNIT_ECONOMICS_AR.md`](finance/COMMERCIAL_UNIT_ECONOMICS_AR.md) |
| Market | أبحاث السوق + المنافسين | [`docs/market/AI_OPS_MARKET_INTELLIGENCE.md`](market/AI_OPS_MARKET_INTELLIGENCE.md) |
| Partnerships | نظام الشراكات | [`docs/partnerships/PARTNERSHIP_OS_AR.md`](partnerships/PARTNERSHIP_OS_AR.md) |
| Product | خريطة المنتج، الجودة، evals | [`docs/product/MASTER_CODE_MAP.md`](product/MASTER_CODE_MAP.md) |
| Forecasting | التنبؤ والـ pipeline | [`docs/forecasting/`](forecasting/) |
| Agentic Ops / Agent Definitions | تعريفات الوكلاء الداخليين | [`docs/agentic_operations/`](agentic_operations/) · [`docs/agent_definitions/`](agent_definitions/) |

### 3.7 البنية المعمارية (Enterprise Architecture)

| النظام | الوصف | البوابة |
|--------|-------|---------|
| Enterprise Architecture (legacy) | خرائط الـ OS الكاملة (Brain OS, Data OS, Trust OS, إلخ) | [`docs/enterprise_architecture/SYSTEM_MAP.md`](enterprise_architecture/SYSTEM_MAP.md) |
| Meta | ميتا-نظام: خريطة المستودع | [`docs/meta/META_REPOSITORY_MAP.md`](meta/META_REPOSITORY_MAP.md) |
| Strategy | الاستراتيجية، الـ 12-month roadmap | [`docs/strategy/90_DAY_PLAN.md`](strategy/90_DAY_PLAN.md) |
| Institutional | الدستور المؤسسي | [`docs/institutional/DEALIX_CONSTITUTION.md`](institutional/DEALIX_CONSTITUTION.md) |

---

## 4. كيف ترتبط الأنظمة الجديدة بالقائمة

```
┌─────────────────────────────────────────────────────────────────────┐
│  OFFER PAGES (Agent 33)  ──→  تُغذّي Sales/Commercial pipeline      │
│           │                       (CTA → WhatsApp → Calendly)        │
│           ▼                                                             │
│  ENTERPRISE SALES (Agent 29)  ──→  تكتب Stakeholders, MAPs, Risks    │
│           │                       (تنشئ Pilot contract)               │
│           ▼                                                             │
│  DELIVERY (legacy) + CLIENT OS  ──→  تُسلّم Pilot + تكتب Proof Pack  │
│           │                                                              │
│           ▼                                                             │
│  DATA PRODUCTS (Agent 31)  ──→  تستهلك Proof Packs + Outbound data   │
│           │                       → benchmarks, objection library      │
│           ▼                                                             │
│  AI GOVERNANCE (Agent 30)  ──→  تراقب كل عميل (Sales/Delivery)       │
│                                  → external_action_capability        │
│                                  → incident_response                  │
└─────────────────────────────────────────────────────────────────────┘
```

> **القاعدة:** كل نظام جديد (29-33) **يعتمد على** legacy، ولا **يكرر** legacy. التفاصيل في [`docs/DEALIX_COMPANY_OS_MAP_AR.md`](DEALIX_COMPANY_OS_MAP_AR.md).

---

## 5. أين تجد المخرجات (Reports)

| النظام | مجلد التقارير | التقرير النهائي |
|--------|---------------|-----------------|
| Enterprise Sales | `reports/enterprise_sales/` | [`ENTERPRISE_SALES_FINAL_REPORT.md`](../reports/enterprise_sales/ENTERPRISE_SALES_FINAL_REPORT.md) |
| AI Governance | `reports/ai_governance/` | [`AI_GOVERNANCE_FINAL_REPORT.md`](../reports/ai_governance/AI_GOVERNANCE_FINAL_REPORT.md) |
| Data Products | `reports/data_products/` | [`DATA_PRODUCTS_FINAL_REPORT.md`](../reports/data_products/DATA_PRODUCTS_FINAL_REPORT.md) |
| Offers | `reports/offers/` | [`OFFER_MICRO_PRODUCTS_FINAL_REPORT.md`](../reports/offers/OFFER_MICRO_PRODUCTS_FINAL_REPORT.md) |
| **Final Integration** | `reports/final/` | [`DEALIX_COMPANY_OS_FINAL_REPORT.md`](../reports/final/DEALIX_COMPANY_OS_FINAL_REPORT.md) |

---

## 6. كيف تبدأ كمؤسس

1. **افتح** [`docs/FOUNDER_START_HERE_AR.md`](FOUNDER_START_HERE_AR.md) — هذا هو ملف البداية الوحيد.
2. **اتبع** ترتيب القراءة المحدد هناك (5 أقسام).
3. **شغّل** الأوامر اليومية في [`docs/DAILY_OPERATING_GUIDE_AR.md`](DAILY_OPERATING_GUIDE_AR.md).
4. **راجع** الـ priority roadmap في [`docs/PRIORITY_ROADMAP_AR.md`](PRIORITY_ROADMAP_AR.md).

---

## 7. منع التكرار (Anti-Duplication)

- **القاعدة:** قبل كتابة ملف جديد، افتح [`docs/ANTI_DUPLICATION_POLICY.md`](ANTI_DUPLICATION_POLICY.md) و [`docs/FILE_OWNERSHIP_MAP.md`](FILE_OWNERSHIP_MAP.md).
- **التدقيق:** [`reports/final/DUPLICATION_AND_CONFLICT_REVIEW.md`](../reports/final/DUPLICATION_AND_CONFLICT_REVIEW.md) — يحتوي 12+ نتيجة موثّقة.
- **حدود الأنظمة:** [`docs/SYSTEM_BOUNDARIES.md`](SYSTEM_BOUNDARIES.md).

---

## Open Questions for Founder

1. هل تريد أن يكون هذا الفهرس (`DEALIX_COMPANY_OS_INDEX_AR.md`) **هو** الـ `README.ar.md` للنظام التشغيلي، أم يبقى منفصلاً؟
2. هل الأنظمة الـ 4 الجديدة تستحق **مجلد فرعي** في الـ repo (مثل `dealix-os/v1/`) لتقليل التشتيت البصري، أم الإبقاء على `docs/enterprise_sales/` + `docs/ai_governance/` + `docs/data_products/` + `docs/offers/` كما هي؟
3. هل يتم استبدال **الفهارس القديمة** (مثل `docs/institutional/MASTER_REPOSITORY_AND_CODE_MAP.md` و `docs/meta/META_REPOSITORY_MAP.md`) بهذا الفهرس، أم يبقى كل فهرس لـ "طبقة" مختلفة (تشغيلي vs تقني)؟
