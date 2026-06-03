# بوابات قبول التسليم (Delivery Acceptance Gates)

> لكل انتقال حالة معنوي في الـ pipeline بوابة (Gate) بمعايير صريحة وحالة (open/passed/failed).
> تُسجَّل البوابات وفق `schemas/delivery_acceptance_gate.schema.json`، وتُراجَع نتائجها في
> `reports/delivery/DELIVERY_ACCEPTANCE_REVIEW.md`. المرجع الموحّد للمصطلحات: `/home/user/dealix/AGENTS.md`.

الجمهور: **Delivery Operator** + **Founder** (لبوابات الموافقة).

---

## 1. القواعد الحاكمة

```txt
- بوابة delivery_started لا تُمرَّر إلا إذا required_inputs_received = true (لا يبدأ العمل قبلها).
- بوابة proposal_sent تتطلب موافقة founder صراحةً.
- لا تُمرَّر أي بوابة بناءً على ادعاء إيراد مضمون.
- البيانات الحساسة تُستلم عبر بوابة آمنة لا عبر واتساب.
```

كل سجل بوابة يحمل الحقول الإلزامية من الـ schema: `id` (نمط `GATE-[0-9]{3,}`)، `company`، `recommended_system`، `state`، `criteria[]` (عنصر واحد على الأقل)، `status` (`open`/`passed`/`failed`). وحقول اختيارية: `evidence_level` (`L0..L4`)، `reviewed_by`.

> ملاحظة: قيمة `state` في البوابة لا تشمل `interested` ولا `payment_handoff` ولا الحالات النهائية — البوابات تغطّي الانتقالات المعنوية فقط كما في الـ schema.

---

## 2. جدول البوابات والمعايير

| البوابة (state) | المعايير (criteria) | من يراجع | evidence_level متوقّع |
|---|---|---|---|
| `qualified` | ألم واضح + نظام مناسب | Outreach Operator / Founder | L2–L3 |
| `mini_proposal_ready` | system + deliverables + starter_price جاهزة | Dealix AI Agents (تجهيز) | L2 |
| `proposal_sent` | **موافقة founder** | Founder | — |
| `won` | اتفاق أو دفع | Founder | L4 |
| `intake_required` | نحتاج required_inputs (القائمة محدّدة ومُرسلة) | Delivery Operator | — |
| `delivery_started` | **استلمنا required_inputs** (`required_inputs_received=true`) | Delivery Operator | L4 |
| `first_output_ready` | خرج أول مخرج مطابق للقالب | Delivery Operator | L4 |
| `client_review` | أُرسل للمراجعة للعميل | Delivery Operator | — |
| `accepted` | العميل وافق على المخرج | العميل + Delivery Operator | L4 |
| `weekly_value_report` | صدر تقرير قيمة (قيمة ملاحَظة لا موعودة) | Delivery Operator | L4 |
| `renewal_candidate` | يوجد دليل قيمة أو توسّع محتمل | Founder | L3–L4 |

---

## 3. تفصيل المعايير لكل بوابة (Checklist تشغيلي)

### بوابة `qualified`
- [ ] يوجد ألم واضح موثّق لدى العميل.
- [ ] النظام المرشّح مناسب لهذا الألم (أحد الأنظمة الخمسة).

### بوابة `mini_proposal_ready`
- [ ] `system` محدّد.
- [ ] `deliverables` محدّدة.
- [ ] `starter_price` جاهز.

### بوابة `proposal_sent`
- [ ] **موافقة founder** مسجّلة قبل أي إرسال.

### بوابة `won`
- [ ] يوجد اتفاق أو دفع موثّق.

### بوابة `intake_required`
- [ ] قائمة `required_inputs` للنظام محدّدة ومُرسلة للعميل.

### بوابة `delivery_started` (البوابة الحرجة)
- [ ] كل عناصر `required_inputs` مُستلمة.
- [ ] البيانات anonymized حيث أمكن (PDPL-aligned).
- [ ] لم تُطلب/تُستلم أي بيانات حساسة عبر واتساب.
- [ ] `required_inputs_received = true`.

### بوابة `first_output_ready`
- [ ] أول مخرج جاهز ومطابق لقالب النظام.
- [ ] لا توجد بيانات عميل حساسة مكشوفة في المخرج.

### بوابة `client_review`
- [ ] المخرج أُرسل للعميل للمراجعة.

### بوابة `accepted`
- [ ] العميل وافق صراحةً على المخرج (أو طلب تعديلات محدّدة عولجت).

### بوابة `weekly_value_report`
- [ ] صدر تقرير قيمة يصف قيمة **ملاحَظة** فقط، بلا أي وعد/ضمان.

### بوابة `renewal_candidate`
- [ ] يوجد دليل قيمة ملموس أو فرصة توسّع محتملة.

---

## 4. مفهوم سجل بوابة (Example GATE record concept)

```txt
id:               GATE-014
company:          مؤسسة ركائز العقارية (synthetic)
recommended_system: whatsapp_client_os
state:            delivery_started
criteria:
  - استلمنا أنواع المحادثات الشائعة
  - استلمنا سياسة الخصوصية الحالية
  - حُدّد من يستلم التصعيد (human handoff)
  - الأنظمة المرتبطة موصوفة (بدون مفاتيح API)
status:           passed
evidence_level:   L4
reviewed_by:      Delivery Operator
```

تفسير: البوابة `delivery_started` مُرّرت لأن كل `required_inputs` لنظام `whatsapp_client_os` استُلمت
(بدون أي مفاتيح API وبدون طلب أسرار داخل واتساب)، فأصبح `required_inputs_received = true` ويبدأ العمل.

> الأسماء أعلاه تركيبية (synthetic) بنمط سعودي، بلا PII ولا أرقام جوال ولا أسرار.

---

## 5. تدفّق المراجعة

```txt
افتح البوابة (status=open) → راجع المعايير بندًا بندًا
   ├─ كل المعايير محقّقة → status=passed → اسمح بالانتقال
   └─ معيار ناقص        → status=failed → سجّل السبب في blockers[] وابقَ في الحالة الحالية
```

تُجمَّع نتائج كل البوابات في `reports/delivery/DELIVERY_ACCEPTANCE_REVIEW.md` لمتابعة Founder.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
