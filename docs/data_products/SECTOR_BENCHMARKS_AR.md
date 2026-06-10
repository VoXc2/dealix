# معايير قياسية حسب القطاع السعودي — Sector Benchmarks

> **مرجع benchmark سري سعودي** — متوسط الرد، الاجتماع، الإغلاق، حجم الصفقة،
> الاعتراضات الشائعة، أفضل CTA، أفضل عرض، تعقيد التسليم، احتمال التجديد.

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0  
**Schema:** `schemas/sector_benchmark.schema.json`  
**البيانات:** `data/data_products/sector_benchmarks.jsonl`

---

## 1. القطاعات المغطّاة (8 قطاعات)

| # | القطاع | Sub-vertical | sample_size | evidence_level |
| - | --- | --- | --- | --- |
| 1 | `industrial` | manufacturing_plant | 42 | observed |
| 2 | `healthcare` | clinic_chain | 38 | observed |
| 3 | `retail` | ecommerce_d2c | 56 | observed |
| 4 | `professional_services` | marketing_agency | 31 | observed |
| 5 | `real_estate` | brokerage | 27 | observed |
| 6 | `fnb` | restaurant_group | 18 | observed |
| 7 | `logistics` | fleet_3pl | 22 | assumption |
| 8 | `education` | training_center | 14 | assumption |

> 6 قطاعات ببيانات observed، 2 بافتراضات. أي benchmark يُستخدم في عرض تجاري
> يجب أن يكون `observed` أو أعلى. `assumption` فقط للـ planning.

---

## 2. الأرقام حسب القطاع (Q1 2026 — anonymized)

### Industrial (manufacturing_plant)
- Reply rate: 18% · Positive reply: 7% · Meeting: 45% · Proposal: 55% · Close: 22%
- Deal size band: 25k–180k SAR (typical 75k)
- اعتراضات شائعة: too_expensive, we_already_have_vendor, need_to_think, send_proposal, no_budget
- أفضل CTA: `roi_calculator` · أفضل عرض: `full_revenue_os`
- تعقيد التسليم: **high** · احتمال التجديد: 55–70%

### Healthcare (clinic_chain)
- Reply rate: 27% · Positive reply: 12% · Meeting: 60% · Proposal: 65% · Close: 28%
- Deal size band: 8k–45k SAR (typical 18k)
- اعتراضات: send_to_procurement, we_tried_ai, privacy_concerns, need_to_think, no_time
- أفضل CTA: `diagnostic_offer` · أفضل عرض: `revenue_leakage_diagnostic`
- تعقيد التسليم: **medium** · احتمال التجديد: 60–78%

### Retail (ecommerce_d2c)
- Reply rate: 22% · Positive reply: 9% · Meeting: 50% · Proposal: 50% · Close: 18%
- Deal size band: 5k–35k SAR (typical 14k)
- اعتراضات: too_expensive, we_already_have_vendor, not_relevant, no_time, no_budget
- أفضل CTA: `short_audit_call` · أفضل عرض: `follow_up_recovery_workflow`
- تعقيد التسليم: **low** · احتمال التجديد: 50–70%

### Professional Services (marketing_agency)
- Reply rate: 34% · Positive reply: 16% · Meeting: 70% · Proposal: 60% · Close: 32%
- Deal size band: 6k–50k SAR (typical 22k)
- اعتراضات: we_already_have_vendor, need_to_think, send_proposal, not_the_right_time, internal_team
- أفضل CTA: `case_study_link` · أفضل عرض: `ai_revenue_ops_starter`
- تعقيد التسليم: **medium** · احتمال التجديد: 65–82%

### Real Estate (brokerage)
- Reply rate: 19% · Positive reply: 8% · Meeting: 40% · Proposal: 45% · Close: 15%
- Deal size band: 10k–60k SAR (typical 28k)
- اعتراضات: not_the_right_time, no_time, too_expensive, we_already_have_vendor, need_to_think
- أفضل CTA: `sample_workflow` · أفضل عرض: `follow_up_recovery_workflow`
- تعقيد التسليم: **low** · احتمال التجديد: 45–65%

### F&B (restaurant_group)
- Reply rate: 21% · Positive reply: 8% · Meeting: 50% · Proposal: 55% · Close: 20%
- Deal size band: 4k–22k SAR (typical 9k)
- اعتراضات: no_budget, too_expensive, not_relevant, we_already_have_vendor, no_time
- أفضل CTA: `short_audit_call` · أفضل عرض: `revenue_leakage_diagnostic`
- تعقيد التسليم: **low** · احتمال التجديد: 40–60%

### Logistics (fleet_3pl) — `assumption`
- Reply rate: 17% · Positive reply: 6% · Meeting: 40% · Proposal: 50% · Close: 18%
- Deal size band: 15k–120k SAR (typical 50k)
- اعتراضات: we_already_have_vendor, send_to_procurement, too_expensive, need_to_think, no_time
- أفضل CTA: `roi_calculator` · أفضل عرض: `full_revenue_os`
- تعقيد التسليم: **high** · احتمال التجديد: 50–70%

### Education (training_center) — `assumption`
- Reply rate: 24% · Positive reply: 10% · Meeting: 55% · Proposal: 55% · Close: 22%
- Deal size band: 5k–30k SAR (typical 12k)
- اعتراضات: no_budget, not_relevant, send_proposal, need_to_think, no_time
- أفضل CTA: `executive_summary` · أفضل عرض: `ai_revenue_ops_starter`
- تعقيد التسليم: **medium** · احتمال التجديد: 55–72%

---

## 3. المنهجية (Method)

### كيف تُحسب
1. **مصدر**: funnel_events + client_health (مجهول الهوية).
2. **تجميع**: ربع سنوي، مرتّب حسب sub-vertical.
3. **مؤشرات**: reply / positive_reply / meeting / proposal / close / deal_size / renewal.
4. **مستوى الدليل**: 
   - `assumption` = رأي خبير بدون بيانات.
   - `observed` = سجل Dealix الفعلي.
   - `validated` = cross-checked مع شريك أو customer.
   - `measured` = statistically significant (n > 30, p < 0.05).

### عينة ذات معنى
- n < 10 → **لا تنشر**، ضع assumption.
- 10–29 → `observed`، ناقص للقرار الحاسم.
- ≥ 30 → `observed`، صالح لـ sales motion.
- validated + n ≥ 30 → صالح لـ public benchmark.
- measured → صالح لـ investment case.

---

## 4. الإصدارات (Versioning)

- `v0.x` → assumption أو sample صغير.
- `v1.0` → observed، 6+ قطاعات، review.
- `v1.1+` → bump عند تغيّر أي رقم رئيسي > 10% في ربع.
- الترميز: `v<major>.<minor>`. كسر major = تغيير منهجية، كسر minor = drift.

عند bump: يُحدَّث `CHANGELOG.md` + `reports/data_products/DATA_PRODUCTS_REVIEW.md`.

---

## 5. قيود (Limitations)

- **Real estate seasonality**: Q1 ضعيف، Q2 قوي.
- **Government-related**: غير مغطى (يحتاج فصل خاص PDPL).
- **Logistics / Education**: لا يزال assumption، Q2 سيُحدَّث.
- **Sub-vertical granularity**: حالياً ≤ 3 لكل قطاع. سيُوسَّع.

---

## 6. المراجع (References)

- `schemas/sector_benchmark.schema.json`
- `data/data_products/sector_benchmarks.jsonl`
- `data/analytics/funnel_events.jsonl`
- `data/commercial/product_catalog.yaml`
- `docs/OBJECTION_INTELLIGENCE_AR.md`
- `docs/OFFER_PERFORMANCE_MODEL_AR.md`
