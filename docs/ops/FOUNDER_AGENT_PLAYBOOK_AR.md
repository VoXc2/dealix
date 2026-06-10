# كتاب تشغيل وكلاء المؤسس — مبيعات / ربط / دعم

> للمؤسس فقط · Cursor subagents + وكلاء in-repo (draft-only خارجياً)

## نمط Prompt موحّد

```text
السياق: مؤسس Dealix، بيع السلم Diagnostic→Sprint→Retainer.
المرجع: docs/commercial/ops_client_pack + docs/COMMERCIAL_WIRING_MAP.md
المهمة: [اكتب المهمة هنا]
القيود: لا أرقام CRM مخترعة؛ لا إرسال خارجي؛ is_estimate للتجريبي.
المخرجات: checklist + أوامر shell + مسارات docs فقط.
```

---

## جدول المهام → الوكيل

| المهمة | وكيل Cursor | مرجع |
| --- | --- | --- |
| مسودة عرض Diagnostic | dealix-sales | [FOUNDER_SELL_MOTION_AR.md](FOUNDER_SELL_MOTION_AR.md) |
| qualify + اختيار عرض من السلم | dealix-sales | [COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md) |
| warm outreach مسودة | dealix-sales | [WARM_LIST_WORKFLOW.md](../sales-kit/WARM_LIST_WORKFLOW.md) |
| خطة Sprint 7 أيام | dealix-delivery | [FOUNDER_DELIVERY_LADDER_AR.md](FOUNDER_DELIVERY_LADDER_AR.md) |
| Proof Pack checklist | dealix-delivery | [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) |
| فشل pytest / endpoint | dealix-engineer | `scripts/founder_go_live_verify.sh` |
| «ما التالي أسبوعياً؟» | dealix-pm | `bash scripts/run_executive_weekly_checklist.sh` |
| مراجعة أقوى خطة (134 مهمة) + سلك YAML | dealix-pm | `python scripts/founder_strongest_plan_status.py` · [FOUNDER_STRONGEST_PLAN_AR.md](../commercial/FOUNDER_STRONGEST_PLAN_AR.md) |
| حلقة أسبوعية موحّدة (تحققات) | dealix-engineer | `bash scripts/founder_weekly_loop.sh` |
| رد دعم عميل | dealix-sales + delivery | [support_faq_en.md](../knowledge-base/support_faq_en.md) |

---

## Prompts جاهزة

### مبيعات — عرض Diagnostic

```text
اكتب Diagnostic Scope بالعربية لعميل [القطاع] في [المدينة].
الميزانية التقريبية [X]. المخرجات من ops runbook.
السعر 4999-9999 SAR. لا ضمان إيراد. لا إرسال تلقائي.
```

### مبيعات — اعتراض «غالي»

```text
صياغة رد عربي قصير: Diagnostic أسبوعان vs توظيف BDR.
مرجع VALUE_CAPTURE_LADDER. بدون أرقام مخترعة.
```

### تسليم — Sprint يوم 1

```text
checklist يوم 1 من CUSTOMER_ONBOARDING_DAY_BY_DAY لعميل [اسم].
engagement_id جديد. قنوات: واتساب مسودة+موافقة فقط.
```

### هندسة — فشل verify

```text
شغّل founder_go_live_verify.sh وحلّل أول FAIL.
لا features جديدة — إصلاح minimal فقط.
```

### PM — أسبوع المؤسس

```text
من business_now_cache و commercial-strategy: ما focus و next_best_actions؟
3 قرارات فقط للأسبوع القادم.
```

---

## وكلاء المنتج (ديمو)

| Agent | دور | مستوى |
| --- | --- | --- |
| SalesStrategistAgent | مسودة استراتيجية | draft |
| DeliveryAgent | خطة تسليم | draft |
| ComplianceGuardAgent | veto | approval |
| ProofAgent | برهان مخفّف | analyze |

مرجع: [AI_WORKFORCE_OPERATING_MODEL.md](../product/AI_WORKFORCE_OPERATING_MODEL.md)

---

## منهج 7 أيام

| يوم | تمرين |
| --- | --- |
| 1 | ديمو `/business-now#strategy` + 3 screenshots |
| 2 | `founder_go_live_verify.sh` + تحديث YAML |
| 3 | POST /leads + commercial-map + qualify وهمي |
| 4 | 3 مهام dealix-sales |
| 5 | محاكاة sprint مع dealix-delivery |
| 6 | FAQ دعم + مسودات Support OS |
| 7 | run_business_now + KPI + قرار أول عميل مدفوع |
