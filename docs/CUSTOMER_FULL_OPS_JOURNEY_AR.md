# Dealix — رحلة العميل الكاملة (Full Ops)

هذا الملف يشرح **للعميل وللفريق** كيف يمرّ lead من أول لمسة حتى Proof Pack، وما الذي يجب أن يكون جاهزاً في كل جانب. التنفيذ التقني للـ API منفصل عن تشغيل Google Workspace (Level 1).

---

## 1) من هو العميل في هذه المرحلة؟

- **وكالة تسويق/نمو** (wedge أول) أو **شركة خدمات B2B** صغيرة ومتوسطة في السعودية.
- يدخل من: **نموذج (Form)**، **واتساب inbound** (رابط `wa.me`)، أو **إحالة**.

التموضع والنجم الشمالي: [strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md](strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md) · [strategic/NORTH_STAR_AR.md](strategic/NORTH_STAR_AR.md)

---

## 2) الرحلة من طرف العميل (ماذا يرى؟)

| الخطوة | ماذا يحدث للعميل | ماذا يحدث داخلياً |
|--------|-------------------|-------------------|
| 1 | يفتح رابط نموذج أو واتساب ويملأ بياناته و**الموافقة** | رد يظهر في `Form Responses 1` أو تسجيل يدوي في اللوحة |
| 2 | يستلم تأكيداً أو رسالة متابعة قصيرة (حسب إعدادكم) | Apps Script يضيف صفاً في `02_Operating_Board` ويولّد `diagnostic_card` ويُرسل تنبيهاً للمالك إن فُعّل |
| 3 | يستلم **Mini Diagnostic** (عربي، مخصّص بعد مراجعة بشرية) | تحديث `diagnostic_status` إلى `sent` |
| 4 | يتلقى عرض **Pilot** (مثلاً 499 ر.س / 7 أيام) عند الاهتمام | `pilot_status = offered` ثم `accepted` / `paid` |
| 5 | يستلم التسليم ثم **Proof Pack** | `proof_pack_status = delivered` + ملء تبويب `04_Proof_Pack` |

تفاصيل الحقول والتبويبات: [ops/full_ops_pack/GOOGLE_SHEET_MODEL_AR.md](ops/full_ops_pack/GOOGLE_SHEET_MODEL_AR.md)

---

## 3) الجوانب التي يجب أن تكون «جاهزة» قبل وصول العملاء

### أ) المنتج والوعد (لا تبالغ)

- سلم العروض: [OFFER_LADDER.md](OFFER_LADDER.md)
- لا وعود ضمان مبيعات؛ موافقة أولاً للقنوات الحساسة: [WHATSAPP_OPERATOR_FLOW.md](WHATSAPP_OPERATOR_FLOW.md)

### ب) الامتثال والثقة

- PDPL ومسارات البيانات: [PRIVACY_PDPL_READINESS.md](PRIVACY_PDPL_READINESS.md)
- سياسة الخصوصية وشروط الاستخدام: ضمن [PUBLIC_LAUNCH_CHECKLIST.md](PUBLIC_LAUNCH_CHECKLIST.md) قبل الإطلاق العام

### ج) التقني (ما يراه من يفحص المنتج)

- صفحة رئيسية / تسعير عام إن وُجدت في نشركم؛ API: `/health`، تسعير: `/api/v1/business/pricing`
- فحص محلي من الريبو: `python3 scripts/smoke_inprocess.py` يجب أن يطبع `SMOKE_INPROCESS_OK`
- Staging: `STAGING_BASE_URL=... python3 scripts/launch_readiness_check.py`

### د) التشغيل (Full Ops Level 1)

- تشغيل كامل: [ops/TURN_ON_FULL_OPS_AR.md](ops/TURN_ON_FULL_OPS_AR.md)
- قبول مع أدلة: [ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md)

### هـ) المبيعات والتسليم

- يوم أول وتوجيه وكالات: [ops/LAUNCH_DAY_ONE_KIT.md](ops/LAUNCH_DAY_ONE_KIT.md) · [ops/full_ops_pack/FIRST_10_AGENCIES_OUTREACH_AR.md](ops/full_ops_pack/FIRST_10_AGENCIES_OUTREACH_AR.md)
- فاتورة يدوية عند الحاجة: [ops/MANUAL_PAYMENT_SOP.md](ops/MANUAL_PAYMENT_SOP.md) · [BILLING_MOYASAR_RUNBOOK.md](BILLING_MOYASAR_RUNBOOK.md)

### و) القياس والنجم الشمالي

- يومياً: [ops/full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md](ops/full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md)
- أسبوعياً: [strategic/NORTH_STAR_AR.md](strategic/NORTH_STAR_AR.md)

### ز) ما بعد أول عميل

- [ops/POST_LAUNCH_BACKLOG.md](ops/POST_LAUNCH_BACKLOG.md)
- رحلات أدوار إضافية (CEO، وكالة، تقني): [CUSTOMER_JOURNEYS.md](CUSTOMER_JOURNEYS.md)

---

## 4) خريطة «وثيقة واحدة لكل سؤال»

| السؤال | الملف |
|--------|--------|
| أين خطة التدشين الكاملة؟ | [LAUNCH_MASTER_PLAN_AR.md](LAUNCH_MASTER_PLAN_AR.md) |
| كيف أشغّل النموذج واللوحة؟ | [ops/full_ops_pack/DEALIX_FULL_OPS_SETUP.md](ops/full_ops_pack/DEALIX_FULL_OPS_SETUP.md) |
| ماذا أنفّذ اليوم بالترتيب؟ | [ops/EXECUTE_NOW_AR.md](ops/EXECUTE_NOW_AR.md) |
| هل البنية التقنية جاهزة للإعلان؟ | [LAUNCH_GATES.md](LAUNCH_GATES.md) |

---

## 5) حدود صريحة

- **لا** يُنشَر إرسال واتساب بارد أو أتمتة live للواتساب/البريد الخارجي بدون بوابات موافقة من المنتج.
- **لا** تُخزَّن أسرار في الـ Sheet أو في نص السكربت العام؛ استخدم Script Properties حيث يلزم.
- ربط الفورم بالـ API (إن أردت) يبقى في [POST_LAUNCH_BACKLOG.md](ops/POST_LAUNCH_BACKLOG.md) حتى يثبت Level 1 يدوياً.

---

## 6) للدعم الداخلي بعد الدخول

- تشغيل وإغلاق أسبوع: [prompts/PROMPT_5_LAUNCH_CLOSURE_OPERATOR.md](prompts/PROMPT_5_LAUNCH_CLOSURE_OPERATOR.md)
