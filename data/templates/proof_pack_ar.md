# قالب طقم الإثبات — Proof Pack Template
# Dealix L1-L3 Proof Pack Format (AR+EN)
# الاستخدام: يُملأ بعد 7 أيام من التسليم — يتطلب موافقة الفاوندر

---

# طقم إثبات Dealix — {{company_name}}
**Dealix Proof Pack — {{company_name}}**

المعرف: `{{pack_id}}` | المستوى: **{{proof_level}}** | التاريخ: {{date}}

---

## 1. الملخص التنفيذي / Executive Summary

**{{executive_summary_ar}}**

*{{executive_summary_en}}*

الأحداث الموثقة: **{{event_count}}** | متوسط التحسن: **{{avg_improvement}}%**

---

## 2. المشكلة / The Problem

**ما كانت تعاني منه {{company_name}} قبل Dealix:**

{{problem_ar}}

*What {{company_name}} faced before Dealix:*

*{{problem_en}}*

---

## 3. الإجراءات المتخذة / Actions Taken

| اليوم | الإجراء | النتيجة |
|-------|---------|---------|
{{#each actions}}
| {{day}} | {{action_ar}} | {{result_ar}} |
{{/each}}

---

## 4. النتائج القابلة للقياس / Measurable Results

{{#each results}}
- **{{metric_ar}}**: من {{before}} إلى {{after}} (+{{delta}}%)
{{/each}}

**إجمالي الوقت المُوفَّر**: {{total_hours_saved}} ساعة/أسبوع

**القيمة التقديرية**: {{estimated_value_sar}} ريال/شهر

---

## 5. الأدلة / Evidence

{{#each evidence}}
**{{index}}. {{title_ar}}**
{{description_ar}}
{{#if screenshot_url}}[لقطة الشاشة]({{screenshot_url}}){{/if}}

{{/each}}

---

## 6. شهادة العميل / Customer Testimonial

{{#if customer_consent}}
> "{{quote_ar}}"
> — {{contact_name}}، {{company_name}}

> *"{{quote_en}}"*
> *— {{contact_name}}, {{company_name}}*
{{else}}
> ⏳ في انتظار موافقة العميل على النشر
{{/if}}

---

## 7. الخطوة التالية / Next Step

**{{next_step_ar}}**

*{{next_step_en}}*

{{#if upsell_eligible}}
### عرض Managed Ops

بناءً على النتائج أعلاه، تستحق {{company_name}} برنامجاً شهرياً مستمراً:

- **Managed Ops الأساسي**: 2,999 ريال/شهر (8 جلسات + KPI dashboard)
- **Managed Ops المتقدم**: 4,999 ريال/شهر (16 جلسة + أولوية الدعم)

[رابط العرض: يُضاف بعد موافقة الفاوندر]
{{/if}}

---

## 8. إشعار PDPL / PDPL Notice

تمت معالجة جميع البيانات في هذا الطقم وفق **نظام حماية البيانات الشخصية السعودي (PDPL)**. البيانات مستخدمة فقط لأغراض التحليل الداخلي وطقم الإثبات. يحق لك طلب حذفها في أي وقت.

*All data processed under Saudi PDPL. Used solely for internal analysis and proof documentation.*

---

*Dealix — نظام التشغيل الذكي للشركات السعودية B2B*
*معرّف الطقم: {{pack_id}} | تاريخ الإصدار: {{date}}*

---

> **للمؤسس**: هذا الطقم يتطلب مراجعتك قبل التسليم للعميل.
> تحقق من: (1) صحة الأرقام، (2) موافقة العميل على الشهادة، (3) مستوى الإثبات مناسب.
