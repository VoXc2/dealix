# نظام تشغيل منتجات البيانات — Data Products OS

> **الإطار الموحّد لمنتجات البيانات الداخلية في Dealix.** يحوّل عمليات
> Dealix اليومية إلى أصول تعلّم قابلة لإعادة الاستخدام، ومعايير قياسية
> (benchmarks)، وذكاء أعمال ملكي — **بدون انتهاك الخصوصية**.

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0

---

## 1. الرسالة (Mission)

بناء **flywheel تعلّم** يربط بين:

1. بيانات التشغيل (funnel events, client health, outreach).
2. منتجات البيانات (benchmarks + message + objection + delivery + renewal + pricing).
3. قرارات العمل (sales motion, delivery plan, marketing calendar, product roadmap).

الهدف: **decision advantage** — كل قرار في Dealix يستند إلى دليل مُوسَم
بـ `evidence_level`، مع تمييز صريح بين **assumption** و**measured**.

---

## 2. ميثاق الخصوصية (Privacy Charter)

| المبدأ | التطبيق |
| --- | --- |
| **لا PII خام** | ممنوع: أسماء أشخاص، أرقام هواتف شخصية، إيميلات حقيقية. |
| **لا أسرار** | ممنوع: قيم عقود، خروقات SLA، أرقام تحويلات حقيقية. |
| **تجميع دائماً** | البيانات على مستوى قطاع/قطاع فرعي، ليس على مستوى شركة. |
| **موافقة المؤسس** | أي سجل يُعرّف عميلاً بوضوح يحتاج موافقة المؤسس خطياً قبل النشر. |
| **إخفاء الهوية** | استخدام `client_id` مُشفّر، أو alias منطقي فقط. |
| **مستوى الدليل (evidence_level)** | كل صف يحمل `assumption` / `observed` / `validated` / `measured`. |
| **التدقيق** | كل تغيير في البيانات الموثوقة (validated/measured) يحتاج PR مع tag `data-change`. |

---

## 3. خريطة المنتجات (Map of 8 docs)

| # | الوثيقة | الغرض |
| - | --- | --- |
| 1 | `DATA_PRODUCTS_OS_AR.md` | هذا الملف — الإطار |
| 2 | `SECTOR_BENCHMARKS_AR.md` | معايير قياسية حسب القطاع السعودي |
| 3 | `MESSAGE_PERFORMANCE_LIBRARY_AR.md` | مكتبة أداء الرسائل (5 قوالب) |
| 4 | `OBJECTION_INTELLIGENCE_AR.md` | استخبارات الاعتراضات (Top 10 سعودي) |
| 5 | `OFFER_PERFORMANCE_MODEL_AR.md` | نموذج أداء العروض (6 خدمات أساسية) |
| 6 | `DELIVERY_PATTERN_LIBRARY_AR.md` | مكتبة أنماط التسليم (5 مراحل) |
| 7 | `RENEWAL_TRIGGER_LIBRARY_AR.md` | مكتبة إشارات التجديد (8 إشارات) |
| 8 | `PRICING_SENSITIVITY_LIBRARY_AR.md` | مكتبة حساسية التسعير |

---

## 4. كتالوج منتجات البيانات (Catalog)

| المنتج (Data Product) | الموقع | يجيب على السؤال |
| --- | --- | --- |
| **Sector Benchmark** | `data/data_products/sector_benchmarks.jsonl` | "ما المتوقع من قطاع معيّن؟" |
| **Message Performance** | `data/data_products/message_performance.jsonl` | "أي رسالة تعمل في أي قطاع؟" |
| **Objection Pattern** | `data/data_products/objection_patterns.jsonl` | "كيف أردّ على هذا الاعتراض؟" |
| **Delivery Pattern** | `data/data_products/delivery_patterns.jsonl` | "كم تستمر هذه المرحلة؟ وأين تفشل؟" |
| **Renewal Trigger** | `data/data_products/renewal_triggers.jsonl` | "هل هذا العميل في خطر؟ ومتى نتدخّل؟" |
| **Pricing Sensitivity** | `data/data_products/pricing_sensitivity.jsonl` | "ما حساسية السعر لهذا العرض؟" |

---

## 5. الربط مع الأنظمة القائمة

- **`data/commercial/`** → مدخلات الأرقام (objections.yaml, pricing_rules.yaml, product_catalog.yaml).
- **`data/analytics/`** → funnel_events, experiments, founder_decisions.
- **`data/customer_success/`** → client_health (مدخل لإشارات التجديد).
- **`learning_flywheel/`** → A/B testing + performance tracker + auto rollback.
- **`evals/`** → تقييم جودة المخرجات (Arabic quality, governance, outreach quality).
- **`reports/`** → مخرجات الإدارة العليا (DATA_PRODUCTS_REVIEW, LEARNING_LOOP_REVIEW).

---

## 6. إيقاع التحديث (Update Cadence)

| الإيقاع | المهمة | المالك |
| --- | --- | --- |
| **أسبوعي** | تجميع funnel events → تجديد message performance sample | Sales Lead |
| **شهري** | إعادة احتساب sector_benchmarks + delivery_patterns | Founder + Ops |
| **ربعي** | مراجعة learning loop (DATA_PRODUCTS_REVIEW + LEARNING_LOOP_REVIEW) | Founder |

عند تغيّر المصدر بنسبة > 10% في المؤشرات الأساسية (reply_rate, close_rate, renewal)، يُرفع رقم الإصدار `v0.x → v1.x`.

---

## 7. الحوكمة (Governance)

1. **Single source of truth**: كل منتج بيانات في `data/data_products/*.jsonl` هو المرجع.
2. **Schema-enforced**: كل صف يخضع لـ `schemas/<name>.schema.json`.
3. **Append-only**: لا يُحذف صف validated/measured. التصحيح عبر إصدار جديد.
4. **PR review**: أي إضافة لصفوف `validated` أو `measured` تحتاج مراجعة المؤسس.
5. **Changelog**: يُحدَّث `CHANGELOG.md` في كل إصدار رئيسي.

---

## 8. مخاطر (Risks)

1. **Privacy leak** عبر قصة عميل موضّحة → حل: review قبل النشر.
2. **Sample size صغير** → وضع `evidence_level: assumption` بوضوح.
3. **Benchmark drift** → bump version + تجميد الاقتباس من إصدار قديم.
4. **Bias في القطاع الواحد** → تجميع ≥ 3 مصادر (outreach + sales + delivery).

---

## 9. المراجع (References)

- `schemas/` — JSON Schema Draft 2020-12.
- `data/data_products/` — ملفات البيانات.
- `learning_flywheel/` — مكونات التعلّم.
- `evals/` — تقييم الجودة.
- `reports/data_products/` — المراجعات.
- `docs/PRIVACY_PDPL_READINESS.md` — أساس الخصوصية.
- `docs/DATA_RETENTION_POLICY.md` — سياسة الاحتفاظ.
