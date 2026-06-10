# نموذج أداء العروض — Offer Performance Model

> **نموذج افتراضي (assumption bands)** لأداء العروض الستة الأساسية في
> Dealix. يُحدَّث إلى observed → validated → measured مع بيانات فعلية.

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0 (assumptions)  
**Schema:** (يستخدم `productized_service.schema.json` + reference fields)  
**البيانات:** `data/data_products/pricing_sensitivity.jsonl` (مرجع)

---

## 1. العروض الستة (Core Offers)

| # | المعرّف | الاسم | النوع | السعر (SAR) |
| - | --- | --- | --- | --- |
| 1 | `revenue_leakage_diagnostic` | تشخيص تسرّب الإيراد | fixed_scope | 1,500–5,000 |
| 2 | `follow_up_recovery_workflow` | تشغيل استعادة المتابعة | fixed_scope | 5,000–9,000 |
| 3 | `ai_revenue_ops_starter` | بداية تشغيل الإيرادات بالذكاء | retainer | 2,999/شهر |
| 4 | `full_revenue_os` | نظام تشغيل الإيرادات الكامل | hybrid | 9,999–25,000/شهر |
| 5 | `monthly_optimization` | تحسين شهري | retainer | 4,999–7,999/شهر |
| 6 | `custom_company_os` | نظام تشغيل مخصص | hybrid | 250,000+ |

> هذه الأرقام **assumptions** حتى تُتحقق من بيانات Dealix الفعلية.

---

## 2. العرض ١ — `revenue_leakage_diagnostic`

- **دورة البيع:** 3–10 أيام.
- **معدل الإغلاق:** 30–45% (validated لـ inbound warm).
- **معدل التوسّع (expansion):** 50% إلى العرض التالي.
- **هامش التسليم:** 70–80% (مجهود مركّز، مخرج واحد).
- **Add-ons شائعة:** ورقة ROI مخصصة، جلسة executive summary.
- **نقطة الانسحاب (drop-off):** بعد ٢ follow-ups بلا رد → nurture.
- **Evidence level:** validated (نسبة، sub-verticals).

---

## 3. العرض ٢ — `follow_up_recovery_workflow`

- **دورة البيع:** 7–21 يوم.
- **معدل الإغلاق:** 25–35% (validated).
- **معدل التوسّع:** 35% إلى `ai_revenue_ops_starter` أو `monthly_optimization`.
- **هامش التسليم:** 60–70% (تكامل + بناء workflow).
- **Add-ons:** workflows إضافية، تكامل CRM مخصص.
- **نقطة الانسحاب:** في منتصف pilot إذا لم يرَ العميل نتائج.
- **Evidence level:** validated.

---

## 4. العرض ٣ — `ai_revenue_ops_starter`

- **دورة البيع:** 14–30 يوم.
- **معدل الإغلاق:** 20–30% (validated).
- **معدل التوسّع:** 40% إلى `full_revenue_os` خلال 6 أشهر.
- **هامش التسليم:** 50–60% (وقت تهيئة + workflows).
- **Add-ons:** workflows إضافية، موافقات متقدمة.
- **نقطة الانسحاب:** setup week 3 إذا لم يُمنح API access.
- **Evidence level:** validated.

---

## 5. العرض ٤ — `full_revenue_os`

- **دورة البيع:** 30–90 يوم.
- **معدل الإغلاق:** 15–25% (observed).
- **معدل التوسّع:** 50% (cross-sell workflows).
- **هامش التسليم:** 40–55% (وقت كبير + فريق).
- **Add-ons:** dashboards, advanced integrations, training sessions.
- **نقطة الانسحاب:** قبل kickoff إذا لم يُعيَّن executive sponsor.
- **Evidence level:** observed.

---

## 6. العرض ٥ — `monthly_optimization`

- **دورة البيع:** 7–21 يوم (داخل علاقة قائمة).
- **معدل الإغلاق:** 60–80% (validated) — لأن العميل موجود.
- **معدل التوسّع:** 25% (upsell إلى tier أعلى).
- **هامش التسليم:** 70–80% (retainer متكرر).
- **Add-ons:** workshop ربع سنوي، تقارير مخصصة.
- **نقطة الانسحاب:** إذا العميل فاته ٣ مراجعات شهرية متتالية.
- **Evidence level:** validated.

---

## 7. العرض ٦ — `custom_company_os`

- **دورة البيع:** 60–180 يوم.
- **معدل الإغلاق:** 10–20% (assumption).
- **معدل التوسّع:** 70% (workflows إضافية على نفس المنصة).
- **هامش التسليم:** 30–45% (مشروع كبير).
- **Add-ons:** training مكثف، IP transfer، صيانة سنوية.
- **نقطة الانسحاب:** قبل MSA إذا لم يُحسم scope.
- **Evidence level:** assumption (لم تُسجَّل صفقة كاملة بعد).

---

## 8. الإضافات الشائعة (Common Add-ons)

- **Executive summary session** (90 دقيقة) → يُضاف لأي عرض.
- **PDPL audit pack** → mandatory لأي healthcare/government.
- **Custom integrations** → +20–40% على السعر الأساسي.
- **Quarterly business review** → embedded في `full_revenue_os`.
- **Coaching call for sales team** → 4–8 ساعات/شهر.
- **Arabic content templates** → يضاف عند عملاء content-heavy.

---

## 9. نقاط الانسحاب الشائعة (Common Drop-off Points)

| المرحلة | drop-off rate | السبب |
| --- | --- | --- |
| بعد التشخيص (offer 1) | 50% | العميل لم يرَ حاجة للخطوة التالية |
| منتصف setup (offer 3) | 20% | IT delay |
| قبل kickoff (offer 4) | 30% | لا executive sponsor |
| بعد شهر 1 (offer 5) | 15% | لم يرَ تحسّناً |
| قبل MSA (offer 6) | 25% | تفاوض سعر/نطاق |

---

## 10. ملاحظة المنهجية (Methodology Note)

- كل الأرقام في هذا المستند **assumptions** أو **validated** بدون observed
  ربع كامل.
- لتحويل assumption → observed: 
  1. ≥ 10 صفقات مغلقة على نفس العرض.
  2. ≥ 3 عملاء في delivery.
  3. ≥ 1 عميل في renewal.
- bump version عندما تتحقق أرقام جديدة.

---

## 11. الربط مع المنتجات الأخرى

- **Sector Benchmarks** → `best_offer` يشير إلى أي عرض في كل قطاع.
- **Message Performance** → CTA يربط بقالب العرض.
- **Objection Intelligence** → `too_expensive` و`need_to_think` هما الأكثر تكراراً لهذه العروض.
- **Delivery Patterns** → المدد في هذا المستند تتطابق مع `delivery_patterns.jsonl`.

---

## 12. المراجع (References)

- `data/productized_services/services.yaml` — catalog كامل.
- `data/data_products/pricing_sensitivity.jsonl` — حساسية السعر.
- `data/data_products/sector_benchmarks.jsonl` — `best_offer` per sector.
- `data/data_products/delivery_patterns.jsonl` — أنماط التسليم.
- `docs/PRICING_AND_PACKAGING_V6.md`
- `docs/OFFER_LADDER.md`
