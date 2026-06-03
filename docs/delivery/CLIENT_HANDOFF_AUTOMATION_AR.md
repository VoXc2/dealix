# أتمتة تسليم العميل (Client Handoff Automation) — من الموقع إلى التسليم

> هذه الوثيقة تشرح كيف يتحوّل lead قادم من صفحة نظام في الموقع إلى حزمة تسليم كاملة، ضمن قواعد PDPL
> وقواعد Dealix الصارمة. المرجع الموحّد: `/home/user/dealix/AGENTS.md`. استلام البيانات يتبع
> `company_os/governance/data_handling_checklist.md`.

الجمهور: **Delivery Operator**.

---

## 1. القواعد الحاكمة

```txt
- العمل لا يبدأ قبل استلام required_inputs (delivery_started يتطلب required_inputs_received=true).
- لا تُطلب بيانات حساسة أو مفاتيح API داخل واتساب إطلاقًا — تُستلم عبر بوابة آمنة.
- البيانات anonymized حيث أمكن (PDPL-aligned).
- الحالات الحساسة → human handoff.
- لا ادعاءات بإيرادات مضمونة في أي مخرج تسليم.
```

---

## 2. المبدأ: كل صفحة نظام تولّد حزمة تسليم

عندما يدخل lead من صفحة نظام معيّن (landing page)، يولّد النظام آليًا أربعة عناصر مترابطة:

```txt
Landing page (نظام محدّد)
   → intake (مدخلات النظام)
   → mini proposal (بالنظام والمخرجات والسعر الافتتاحي)
   → delivery pack (حزمة تسليم النظام)
   → weekly report (قالب تقرير القيمة الأسبوعي)
```

> ملاحظة: mini proposal تبقى draft حتى **موافقة founder** قبل أي إرسال (قاعدة صارمة).

---

## 3. مثالان للتوليد حسب الصفحة

### مثال 1 — lead دخل من صفحة `revenue_os`

```txt
lead من صفحة revenue_os →
   1) Revenue OS intake
   2) Revenue Mini Proposal
   3) Revenue Delivery Pack
   4) Revenue Weekly Report
```

| العنصر المُولَّد | المحتوى |
|---|---|
| Revenue OS intake | نموذج مدخلات revenue_os (انظر `SYSTEM_REQUIRED_INPUTS_AR.md`) |
| Revenue Mini Proposal | عرض مصغّر: النظام + المخرجات + starter price (draft حتى موافقة founder) |
| Revenue Delivery Pack | حزمة تسليم revenue_os (انظر `SYSTEM_DELIVERY_CHECKLISTS_AR.md`) |
| Revenue Weekly Report | قالب تقرير قيمة أسبوعي (قيمة ملاحَظة فقط) |

### مثال 2 — lead دخل من صفحة `whatsapp_client_os`

```txt
lead من صفحة whatsapp_client_os →
   1) WhatsApp intake
   2) WhatsApp flow checklist
   3) WhatsApp action card template
   4) WhatsApp handoff policy
```

| العنصر المُولَّد | المحتوى |
|---|---|
| WhatsApp intake | نموذج مدخلات whatsapp_client_os (بدون مفاتيح API) |
| WhatsApp flow checklist | قائمة تدفّقات لكل نوع محادثة |
| WhatsApp action card template | قالب بطاقات إجراء للردود الشائعة (بلا طلب أسرار) |
| WhatsApp handoff policy | سياسة تحويل الحالات الحساسة إلى human handoff |

---

## 4. قائمة Intake (Intake checklist) + بوابة required_inputs

```txt
استلام lead → جهّز intake النظام → أرسل required_inputs list →
   استلم المدخلات (بوابة آمنة) → anonymize → required_inputs_received=true → delivery_started
```

قائمة تحقق Intake:

- [ ] حُدّد `recommended_system` للـ lead (من الصفحة التي دخل منها).
- [ ] أُنشئ نموذج intake الخاص بالنظام.
- [ ] أُرسلت `required_inputs list` للعميل عبر قناة مناسبة.
- [ ] أكّد العميل ملكيته للبيانات وحقّه في مشاركتها.
- [ ] لا توجد PII لأطراف ثالثة ضمن البيانات.
- [ ] استُلمت البيانات الحساسة عبر **بوابة آمنة** (ليس واتساب، ليس بريد شخصي، ليس مشاركة عامة).
- [ ] أُجري anonymize حيث أمكن.
- [ ] حُدّدت فترة الاحتفاظ (افتراضي 90 يومًا) وآلية الحذف.
- [ ] ضُبط `required_inputs_received = true` بعد التحقق الفعلي.

> البوابة الحرجة: لا انتقال إلى `delivery_started` قبل أن تكتمل القائمة أعلاه ويصبح `required_inputs_received = true`.

---

## 5. استلام البيانات وفق PDPL

يتبع الاستلام `company_os/governance/data_handling_checklist.md`. أهم النقاط للـ Delivery Operator:

- [ ] التحويل عبر وسيلة آمنة (encrypted email / secure drive). لا بريد شخصي ولا مشاركة عامة.
- [ ] فحص البيانات بحثًا عن PII حساسة قبل التحليل.
- [ ] anonymize / masking للأسماء والمعرّفات حيث أمكن.
- [ ] عدم لصق بيانات العميل في أدوات AI عامة.
- [ ] التخزين في مجلد خاص بالعميل.
- [ ] حذف البيانات الخام بعد 90 يومًا وتأكيد الحذف مع العميل.

> المرجع الكامل لمتطلبات SDAIA PDPL في وثيقة الحوكمة المذكورة أعلاه.

---

## 6. البوابة الآمنة للبيانات الحساسة (Secure Portal) — لا واتساب أبدًا

```txt
بيانات حساسة / مفاتيح / تصدير CRM →  بوابة آمنة فقط
                                  ✗  واتساب (ممنوع طلب أو استلام أسرار)
                                  ✗  بريد شخصي / مشاركة عامة
```

- أي طلب بيانات حساسة أو مفاتيح API يحتاج موافقة (قاعدة صارمة) ويتم عبر البوابة الآمنة.
- في `whatsapp_client_os`: استخدم **Secure Portal Handoff Guide** لتوجيه العميل للبوابة بدل واتساب.
- الحالات الحساسة (شكوى، بيانات شخصية، نزاع) → **human handoff** فورًا.

---

## 7. تدفّق الحالة بعد الـ handoff

```txt
won → (auto-create حزمة التسليم) → intake_required
   → (استلام required_inputs عبر بوابة آمنة + anonymize)
   → required_inputs_received=true → delivery_started
   → first_output_ready → client_review → accepted
   → weekly_value_report → renewal_candidate
```

تُتابع حالة كل عميل في `reports/delivery/DELIVERY_PIPELINE_STATUS.md` وفق `schemas/delivery_pipeline.schema.json`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
