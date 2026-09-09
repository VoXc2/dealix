# قالب طقم الإثبات — Dealix Proof Pack Template
# Weekly / Final Evidence Format (AR+EN)
# الاستخدام: يُملأ أثناء أو في نهاية Revenue Command Pilot بعد التحقق من المصادر
# brand_version: V2.1_DRAFT
# template_version: proof_pack_ar_v2_1
# owner_agent: dealix-delivery
# support_agent: dealix-content

---

# طقم إثبات Dealix — {{company_or_handle}}
**Dealix Proof Pack — {{company_or_handle}}**

المعرف: `{{pack_id}}` | المستوى: **{{proof_level}}** | الفترة: {{period}} | التاريخ: {{date}}

> **حالة الإثبات:** {{proof_readiness}}
>
> `READY_FOR_VERIFICATION` لا تعني تلقائيًا Customer Value أو Publication Permission. الأدلة المفقودة أو القديمة أو الاصطناعية تبقى `UNKNOWN / BLOCKED`.

---

## 1. الملخص التنفيذي / Executive Summary

**{{executive_summary_ar}}**

*{{executive_summary_en}}*

- الأحداث الموثقة من مصادر معروفة: **{{verified_event_count}}**
- الأحداث غير المتحققة/المحجوبة: **{{unverified_event_count}}**
- النطاق الموافق عليه: **{{approved_scope_ref}}**
- baseline/source: **{{baseline_source_ref}}**

لا تُحسب نسبة تحسن أو قيمة مالية إلا إذا وُجد before/after قابل للمقارنة ومصدر وطريقة قياس موثقة.

---

## 2. المشكلة وBaseline / Problem & Baseline

**المشكلة المعتمدة:**

{{problem_ar}}

*Approved problem:*

*{{problem_en}}*

**Baseline:** {{baseline_value}}

**المصدر:** `{{baseline_source_ref}}`

**نافذة القياس:** {{measurement_window}}

إذا لم يوجد baseline صالح: `{{baseline_missing_reason}}`.

---

## 3. الإجراءات والتسليم / Actions & Delivery

| التاريخ/الفترة | الإجراء | الحالة | المصدر/الدليل |
|---|---|---|---|
{{#each actions}}
| {{when}} | {{action_ar}} | {{status}} | {{source_ref}} |
{{/each}}

> النشاط المنفذ لا يساوي تلقائيًا Customer Value أو Revenue.

---

## 4. النتائج القابلة للقياس / Measured Outcomes

{{#each results}}
- **{{metric_ar}}**
  - قبل: {{before}}
  - بعد: {{after}}
  - التغير: {{delta}}
  - المصدر: `{{source_ref}}`
  - الطريقة: {{method}}
  - الحالة: {{evidence_status}}
{{/each}}

**الوقت الموفر (إن كان مثبتًا):** {{verified_hours_saved}}

**القيمة الاقتصادية (إن كانت مثبتة):** {{verified_value_sar}}

إذا كانت القيمة تقديرية فقط، يجب وسمها `ESTIMATE` مع الافتراضات وعدم عرضها كCustomer Value محقق.

---

## 5. الأدلة / Evidence

{{#each evidence}}
**{{index}}. {{title_ar}}**

- الوصف: {{description_ar}}
- المصدر: `{{source_ref}}`
- المالك/الموافق: {{owner_or_approver}}
- الحالة: {{status}}
{{#if screenshot_url}}
- رابط لقطة/أصل داخلي: {{screenshot_url}}
{{/if}}

{{/each}}

---

## 6. فصل حالات الحقيقة / Truth-State Separation

| الحالة | القيمة | الدليل |
|---|---|---|
| Delivery | {{delivery_status}} | {{delivery_evidence_ref}} |
| Payment | {{payment_status}} | {{payment_evidence_ref}} |
| Revenue | {{revenue_status}} | {{revenue_evidence_ref}} |
| Customer Value | {{customer_value_status}} | {{customer_value_evidence_ref}} |
| Publication Permission | {{publication_status}} | {{publication_evidence_ref}} |

**قاعدة:**

```text
Activity ≠ Delivery ≠ Payment ≠ Revenue ≠ Customer Value ≠ Publication Permission
```

---

## 7. شهادة/صوت العميل — Publication Gate

{{#if publication_permission}}
> "{{quote_ar}}"
>
> *"{{quote_en}}"*

مرجع الإذن بالنشر: `{{publication_evidence_ref}}`
{{else}}
> **غير مسموح بالنشر.** وجود Feedback أو نتيجة مثبتة لا يمنح Publication Permission تلقائيًا.
{{/if}}

لا تعرض اسم شخص أو بيانات تواصل في النسخة العامة إلا إذا كان ذلك ضروريًا ومصرحًا به صراحة.

---

## 8. القرار التالي / Next Decision

**{{next_decision}}** — يجب أن تكون إحدى:

- `STOP`
- `EXPAND`
- `REDESIGN`

السبب والأدلة:

{{next_decision_rationale}}

إذا كان القرار `EXPAND`:

- لا يوجد Managed Ops price tier عام تلقائي.
- يلزم نطاق جديد معتمد، customer-specific quote، ومراجعة margin/capacity/data/approval gates.
- لا يُفترض Retainer أو Upsell من مجرد تحسن داخلي.

---

## 9. الخصوصية وحدود البيانات / Privacy & Data Boundary

- Approved data boundary: `{{approved_data_boundary_ref}}`
- Data classes used: {{data_classes_used}}
- Retention/deletion path: {{retention_deletion_ref}}
- Tenant/security reference: {{tenant_security_ref}}

هذا الطقم **لا يدّعي** PDPL certification أو Saudi data residency أو أي استنتاج قانوني عام. يجب أن يطابق كل Claim تدفق البيانات والضوابط والمستندات الفعلية للحالة المحددة.

---

## 10. مراجعة الإصدار / Release Review

قبل مشاركة أي Proof Pack خارج الفريق:

- [ ] كل رقم له source/method أو موسوم Unknown/Estimate.
- [ ] لا synthetic/demo/internal evidence ظاهر كCustomer Proof.
- [ ] Payment وRevenue وCustomer Value مفصولة.
- [ ] لا اسم/Logo/Testimonial بدون Publication Permission.
- [ ] لا compliance/residency/certification claim غير مثبت.
- [ ] لا fixed price أو automatic upsell من قالب Proof.
- [ ] approval المطلوب للمشاركة الخارجية موجود.
- [ ] `brand_version`, `template_version`, `proof_level`, `source_refs` ونسخة الـClaim محفوظة في سجل الأصل/الـrenderer عند الاستخدام.

---

*Dealix — AI Business Operating System · Revenue + Proof + Command*

*معرّف الطقم: {{pack_id}} | تاريخ الإصدار: {{date}}*

> **للمشغّل:** هذا قالب داخلي حتى يمر عبر مراجعة الأدلة والموافقة المناسبة. لا إرساله تلقائيًا.
