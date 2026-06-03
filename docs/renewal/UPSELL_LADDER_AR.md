# سلّم الترقية — Upsell Ladder

> **السكيمة:** `schemas/upsell_opportunity.schema.json` | **الكتالوج:** `data/catalog/product_catalog.json` | **الموافقة:** مطلوبة لكل UPS-*

---

## مبدأ السلّم

سلّم الترقية هو **مسار طبيعي لنمو العلاقة** مع العميل، لا مسار ترويجي. كل خطوة تُفتح فقط بعد إثبات قيمة الخطوة السابقة (`evidence_level ∈ {client_data, measured, verified}`). لا قفز، لا ضغط، لا تخطي خطوات.

---

## 1. السلّم الكامل — الترتيب والأسعار

مستمد من `data/catalog/product_catalog.json`:

| # | product_id | الاسم | billing | السعر (SAR) | sku_ref | القادم |
|---|---|---|---|---|---|---|
| 1 | `readiness_scan` | فحص الجاهزية | one_time | مجاني | — | revenue_leakage_diagnostic |
| 2 | `revenue_leakage_diagnostic` | تشخيص تسرب الإيراد | one_time | 2,500–5,000 | PROP-P1 | followup_recovery_workflow |
| 3 | `followup_recovery_workflow` | ورشة استرجاع المتابعة | one_time | 2,500–6,000 | — | ai_revenue_ops_starter |
| 4 | `ai_revenue_ops_starter` | باقة عمليات الإيراد — مبتدئ | monthly | 3,000 | PROP-P2-SMALL | full_revenue_os |
| 5 | `full_revenue_os` | نظام تشغيل الإيراد الكامل | monthly | 8,000 | PROP-P2-MEDIUM | monthly_optimization |
| 6 | `monthly_optimization` | تحسين شهري (إضافة) | monthly | 1,500–4,000 | — | custom_company_os |
| 7 | `custom_company_os` | نظام تشغيل المؤسسة المخصص | monthly | 20,000 | PROP-P2-ENTERPRISE | multi_department_rollout |
| 8 | `multi_department_rollout` | تعميم متعدد الإدارات | custom | 20,000–100,000+ | — | (قمة السلّم) |

---

## 2. تفاصيل كل خطوة

### الخطوة 1 — فحص الجاهزية (readiness_scan)
**ما هو:** تشخيص أولي مجاني يقيس جاهزية الإيراد ويحدد أكبر نقطة تسرب.
**الجمهور:** عميل جديد أو محتمل.
**مخرَج التسليم:** تقرير جاهزية + توصية بأول خطوة مدفوعة.
**شرط الترقية للخطوة 2:** العميل رأى قيمة في التشخيص وأراد الخطوة التالية.

---

### الخطوة 2 — تشخيص تسرب الإيراد (revenue_leakage_diagnostic)
**ما هو:** Sprint 5 أيام: خريطة تسرب الإيراد + Proof Pack + خطة 30 يوم.
**السعر:** 2,500–5,000 SAR (one-time) | `sku_ref: PROP-P1`
**مخرَج التسليم:** خريطة فجوات مُفصَّلة + baseline + Proof Pack.
**شرط الترقية للخطوة 3:** `evidence_level: measured` على خريطة الفجوات.

---

### الخطوة 3 — ورشة استرجاع المتابعة (followup_recovery_workflow)
**ما هو:** بناء أول workflow متابعة فعلي يوقف أكبر نقطة تسرب.
**السعر:** 2,500–6,000 SAR (one-time)
**مخرَج التسليم:** Workflow جاهز للتشغيل + تدريب الفريق.
**شرط الترقية للخطوة 4:** `value_proof = true` من Workflow بعد أسبوع على الأقل من التشغيل.

---

### الخطوة 4 — باقة مبتدئ (ai_revenue_ops_starter)
**ما هو:** غرفة حرب أسبوعية + تتبع pipeline + تحسين الرسائل + تقرير شهري.
**السعر:** 3,000 SAR/شهر | `sku_ref: PROP-P2-SMALL`
**مخرَج التسليم:** تقارير أسبوعية WVR + تحسين مستمر.
**شرط الترقية للخطوة 5:** شهران+ من `evidence_level: measured` وطلب صريح من العميل.

---

### الخطوة 5 — نظام الإيراد الكامل (full_revenue_os)
**ما هو:** تشغيل كامل + A/B + ذكاء اعتراضات + تدريب أسبوعي + Proof Packs شهرية.
**السعر:** 8,000 SAR/شهر | `sku_ref: PROP-P2-MEDIUM`
**مخرَج التسليم:** نظام إيراد شامل مع مراجعات أسبوعية.
**شرط الترقية للخطوة 6:** العميل يريد تحسينًا مستمرًا فوق النظام الأساسي.

---

### الخطوة 6 — تحسين شهري (monthly_optimization)
**ما هو:** طبقة تحسين مستمرة تُضاف فوق أي باقة شهرية.
**السعر:** 1,500–4,000 SAR/شهر (إضافي)
**مخرَج التسليم:** A/B tests شهرية + تحسين رسائل + تقرير تحسين.
**شرط الترقية للخطوة 7:** العميل يريد نظامًا كاملًا لمؤسسته.

---

### الخطوة 7 — نظام المؤسسة المخصص (custom_company_os)
**ما هو:** تطبيق Revenue OS كامل + حوكمة مخصصة + مدير نجاح مخصص.
**السعر:** 20,000 SAR/شهر | `sku_ref: PROP-P2-ENTERPRISE`
**مخرَج التسليم:** نظام تشغيل مؤسسي مخصص + دعم 1-to-1.
**شرط الترقية للخطوة 8:** نجاح موثَّق في أكثر من إدارة.

---

### الخطوة 8 — تعميم متعدد الإدارات (multi_department_rollout)
**ما هو:** توسعة نظام الإيراد عبر أكثر من إدارة أو فرع.
**السعر:** 20,000–100,000+ SAR (مخصص) — موافقة المؤسس + تسليم بشري (L5)
**مخرَج التسليم:** خريطة تسليم لكل إدارة + فريق مخصص.
**ملاحظة:** هذه القمة — لا مرحلة بعدها على السلّم.

---

## 3. بنية سجل UPS-*

مستمدة من `upsell_opportunity.schema.json`:

| الحقل | القيمة | الوصف |
|---|---|---|
| `id` | `UPS-[...]` | معرّف فريد |
| `from_product_id` | المنتج الحالي | يجب أن ∈ الكتالوج |
| `to_product_id` | المنتج التالي | يجب أن يكون أعلى في السلّم |
| `ladder_step` | نفس `to_product_id` | من قائمة ladder_step المعتمدة |
| `cites_delivered_value` | مرجع WVR + رقم | non-empty إلزامي |
| `evidence_level` | client_data / measured / verified | لا قيمة أضعف |
| `suggested_next_step` | خطوة واحدة | بلا ضغط |
| `approval_required` | true (const) | دائمًا |
| `status` | draft → pending_approval → approved → sent_manually → won / declined | — |

---

## 4. قواعد تجاوز الخطوات

- **يُمنع القفز** من الخطوة 2 مباشرة للخطوة 5 مثلًا.
- الاستثناء الوحيد: إذا طلب العميل صراحةً خطوة أعلى وأثبتت بياناته جاهزيته — يُقيَّم بموافقة المؤسس.
- `to_product_id` يجب أن `ladder_order > from_product_id.ladder_order` في الكتالوج.

---

## 5. مثال حقيقي — UPS-1001

من `data/renewals/upsell_opportunities.jsonl`:

```json
{
  "id": "UPS-1001",
  "company": "Digital Rise Agency",
  "from_product_id": "revenue_leakage_diagnostic",   ← الخطوة 2
  "to_product_id": "ai_revenue_ops_starter",         ← الخطوة 4
  "ladder_step": "ai_revenue_ops_starter",
  "cites_delivered_value": ["WVR-1001: تحسّن نسبة المتابعة وزمن الرد (measured)"],
  "evidence_level": "measured",
  "suggested_next_step": "تجربة شهر واحد من باقة عمليات الإيراد المبتدئة لتثبيت النتائج.",
  "approval_required": true,
  "approved": false,
  "status": "draft"
}
```

> ملاحظة: الانتقال من 2 (revenue_leakage_diagnostic) مباشرة إلى 4 (ai_revenue_ops_starter) — هذا ممكن لأن الخطوة 3 (followup_recovery_workflow) أُدرجت ضمن تسليم الـ P1 Sprint. السلّم مرن ضمن قواعد الكتالوج بموافقة المؤسس.

---

## 6. ربط السلّم بالاقتصاديات

من `company_os/finance/unit_economics.md`:

| الباقة | السعر/شهر | هامش ربح تقريبي |
|---|---|---|
| ai_revenue_ops_starter | 3,000 SAR | ~75% |
| full_revenue_os | 8,000 SAR | ~80% |
| custom_company_os | 20,000 SAR | ~85% |

**قاعدة:** رفع المستوى على السلّم لا يعني فقط زيادة الإيراد — يعني زيادة القيمة المُسلَّمة بالتوازي.

---

*آخر تحديث: 2026-06-03 | الكتالوج: [product_catalog.json](../../data/catalog/product_catalog.json) | السكيمة: [upsell_opportunity.schema.json](../../schemas/upsell_opportunity.schema.json) | مرجع: [AGENTS.md](../../AGENTS.md)*
