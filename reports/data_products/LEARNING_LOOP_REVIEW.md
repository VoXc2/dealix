# مراجعة حلقة التعلّم — Learning Loop Review

> **كيف تُغذّي منتجات البيانات الستة أنظمة Dealix** (sales, delivery,
> product, marketing) عبر إيقاع أسبوعي → شهري → ربعي.

**التاريخ:** 2026-06-03  
**الإصدار:** v1.0

---

## 1. الإطار (Framework)

```
[Run] → [Capture] → [Aggregate] → [Decide] → [Act] → [Measure] → [Run]
```

| المرحلة | المالك | الإيقاع |
| --- | --- | --- |
| Capture | Sales/CSM | مستمر |
| Aggregate | Ops | أسبوعي |
| Decide | Founder + Leads | شهري |
| Act | Sales/CSM/Product | أسبوعي (تعديلات) / ربع سنوي (إصلاحات كبيرة) |
| Measure | Analytics | أسبوعي |

---

## 2. المنتج ١ — `sector_benchmarks`

### كيف يُغذّي Sales
- **Weekly:** يعرف sales_lead التوقعات لكل قطاع (reply, close, deal size).
- **Monthly:** تعديل quota + ICP fit per sector.
- **Quarterly:** إعادة تخصيص موارد sales حسب أعلى-عائد قطاع.

### كيف يُغذّي Marketing
- **Monthly:** تخصيص ميزانية acquisition حسب `best_cta` لكل قطاع.
- **Quarterly:** تخطيط content calendar حسب `common_objections` (للمعالجة المسبقة).

### كيف يُغذّي Product
- **Quarterly:** sub-verticals عالية close_rate = أولوية product focus.

### كيف يُغذّي Delivery
- **Monthly:** توقعات `complexity` و`renewal_probability` تُستخدم في staffing.

---

## 3. المنتج ٢ — `message_performance`

### Sales
- **Weekly:** outbound يختار archetype الأنسب للقطاع المستهدف.
- **Monthly:** A/B test على hook patterns.

### Marketing
- **Monthly:** أعلى-أداء subject patterns تدخل في nurture sequence.
- **Quarterly:** تحديث email/LinkedIn copy.

### Product
- **Quarterly:** in-app messaging يستخدم نفس الـ patterns.

### Delivery
- **Monthly:** في onboarding emails.

---

## 4. المنتج ٣ — `objection_patterns`

### Sales
- **Weekly:** استخدام playbook لكل اعتراض مُسجَّل في funnel.
- **Monthly:** تقييم جديد variants مع team.

### Marketing
- **Monthly:** website copy يعالج `common_objections` كـ FAQ.
- **Quarterly:** landing pages تستخدم counter-frames.

### Product
- **Quarterly:** UI changes تعالج `privacy_concerns` (PDPL banner).

### Delivery
- **Monthly:** csm يستخدم escalation paths.

---

## 5. المنتج ٤ — `delivery_patterns`

### Delivery
- **Weekly:** kickoff/setup يستخدمان نفس الـ templates.
- **Monthly:** review complexity scores.
- **Quarterly:** rebalance weights حسب `complexity_score` الفعلي.

### Sales
- **Monthly:** setting expectations in proposal phase.

### Product
- **Quarterly:** feedback على features المطلوبة من delivery.

### Marketing
- **Quarterly:** case studies تستند إلى success_criteria المُحقّقة.

---

## 6. المنتج ٥ — `renewal_triggers`

### CSM (Delivery)
- **Weekly:** monitor signals عبر client_health.
- **Monthly:** review save_rate.

### Sales
- **Monthly:** pipeline of renewals.
- **Quarterly:** upsell opportunities من scope_creep.

### Product
- **Monthly:** feedback من competitor_mention.

### Marketing
- **Quarterly:** reference stories من low_nps → recovered.

---

## 7. المنتج ٦ — `pricing_sensitivity`

### Sales
- **Weekly:** يستخدم anchor techniques حسب sensitivity_band.
- **Monthly:** discount log review.
- **Quarterly:** price increase at renewal.

### Product
- **Quarterly:** pricing experiments.

### Marketing
- **Monthly:** landing page copy يعكس framing techniques.

### Delivery
- **Quarterly:** margin review.

---

## 8. الإيقاع الكامل (Cadence Map)

| الإيقاع | المهمة | المدخلات | المخرجات | المالك |
| --- | --- | --- | --- | --- |
| **يومي** | تسجيل funnel events | outreach + sales | funnel_events | auto |
| **أسبوعي** | تحديث message performance sample | outreach notes | message_performance v0.x | sales_lead |
| **أسبوعي** | تجميع usage signals | product_usage | client_health update | csm |
| **شهري** | إعادة احتساب sector_benchmarks | funnel + delivery | sector_benchmarks v0.x | ops |
| **شهري** | مراجعة objection frequency | funnel_events | objection_patterns updated | sales_lead |
| **شهري** | margin review | delivery | pricing_sensitivity update | founder |
| **ربعي** | review learning loop | كل المنتجات | DATA_PRODUCTS_REVIEW.md | founder |
| **ربعي** | OKR refresh | DATA_PRODUCTS_REVIEW | OKR_AR updated | founder |

---

## 9. نقاط التحويل (Conversion Points)

| من | إلى | كيف |
| --- | --- | --- |
| funnel_events | sector_benchmarks | aggregation script |
| sector_benchmarks | sales playbook | monthly review |
| message_performance | templates | auto-rotation |
| objection_patterns | crm scripts | versioned JSON |
| delivery_patterns | kickoff deck | template_ref |
| renewal_triggers | csm dashboard | signal detector |
| pricing_sensitivity | proposal template | anchor bank |

---

## 10. المخاطر (Risks)

1. **Loop decay** — إذا لم يُحدَّث data، تنتهي صلاحية المنتجات.
   حل: PR gate.
2. **Single source of truth drift** — إذا قُرأت الأرقام من CRM يدوياً.
   حل: ETL.
3. **Mis-attribution** — خطأ في ربط رسالة بنتيجة.
   حل: UTM + cohort_id.
4. **Feedback lag** — Q-end reviews متأخرة.
   حل: monthly mini-review.

---

## 11. KPIs للـ Loop

- **Loop latency:** أيام من capture إلى decision.
- **Re-use rate:** % من decision يستخدم data_product.
- **Version freshness:** % من المنتجات v0.x vs v1.x.
- **Action-to-data ratio:** # of actions per data point.

---

## 12. Sign-off

- **Author:** Agent #31 (general)
- **Reviewer:** founder
- **Next review:** 2026-07-01

---

## 13. المراجع (References)

- `docs/data_products/DATA_PRODUCTS_OS_AR.md`
- `data/data_products/*.jsonl`
- `data/analytics/funnel_events.jsonl`
- `data/customer_success/client_health.jsonl`
- `learning_flywheel/` (A/B testing, performance tracker, auto rollback)
- `evals/` (Arabic quality, governance, outreach quality)
- `reports/data_products/DATA_PRODUCTS_REVIEW.md`
