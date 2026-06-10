# نظام تشغيل الخدمات القابلة للبيع — Dealix Productized Services OS

> **الإطار الموحّد لكل خدمة Dealix قابلة للبيع.** كل خدمة جديدة تُسجَّل
> في `data/productized_services/services.yaml`، لها playbook منفصل، لها
> acceptance criteria في `acceptance_criteria.jsonl`، ولها deliverables في
> `deliverables.jsonl`.

**الحالة:** مسودة — Phase 1 من Agent #15
**التاريخ:** 2026-06-03

---

## 1. المبادئ (Principles)

1. **Service = Product, not Project.** كل خدمة لها سعر ثابت (أو مدى
   ضيق)، زمن تسليم ثابت، deliverables محددة مسبقاً، acceptance
   criteria قابلة للقياس.
2. **Scope is Law.** ما هو خارج الـ scope لا يُسلَّم بدون change
   request (see `docs/delivery/SCOPE_CONTROL.md`).
3. **Acceptance in writing.** لا يُعتبر deliverable "مُسلَّم" إلا بعد
   موافقة العميل على acceptance criteria.
4. **Renewal path is built-in.** كل خدمة لها خطة renewal/upsell
   معرّفة في catalog.
5. **No fake urgency.** مواعيد التسليم حقيقية، لا تنتهي "غداً".

## 2. قالب الخدمة (Service Template)

كل خدمة يجب أن تحدد:

| الحقل | الوصف | إلزامي |
| --- | --- | --- |
| `id` | معرّف فريد (snake_case) | ✅ |
| `name_ar` / `name_en` | الاسم بالعربية والإنجليزية | ✅ |
| `icp` | قائمة شروط العميل المثالي | ✅ |
| `problem_solved` | المشكلة المحددة | ✅ |
| `price_range_sar` | مدى السعر (min, max) | ✅ |
| `timeline_days` | زمن التسليم (min, max) | ✅ |
| `required_access` | ما يحتاجه Dealix من العميل | ✅ |
| `client_responsibilities` | ما يفعله العميل | ✅ |
| `dealix_responsibilities` | ما يفعله Dealix | ✅ |
| `deliverables` | قائمة outputs الملموسة | ✅ |
| `out_of_scope` | ما لا يشمله السعر | ✅ |
| `acceptance_criteria` | شروط القبول | ✅ |
| `risks` | مخاطر + mitigation | ✅ |
| `first_7_days` | خطة الأسبوع الأول | ✅ |
| `weekly_reporting` | شكل التقرير الأسبوعي | ✅ |
| `renewal_path` | إلى أين يذهب العميل بعدها | ✅ |

## 3. الـ 6 خدمات الأساسية (Core Services)

| # | المعرّف | الاسم | السعر (SAR) | المدة |
| - | --- | --- | --- | --- |
| 1 | `revenue_leakage_diagnostic` | فحص تسرب الإيرادات | 1,500–3,000 | 5–7 أيام |
| 2 | `followup_recovery_workflow` | تشغيل استعادة المتابعة | 5,000–9,000 | 10–14 يوم |
| 3 | `ai_revenue_ops_starter` | بداية تشغيل الإيرادات بالذكاء الاصطناعي | 2,999/شهر | 14–21 يوم |
| 4 | `full_revenue_os` | نظام تشغيل الإيرادات الكامل | 9,999–25,000/شهر | 30–45 يوم |
| 5 | `monthly_optimization_retainer` | تحسين شهري | 4,999–7,999/شهر | شهري |
| 6 | `custom_company_os` | نظام تشغيل مخصص للشركة | 250,000+ | 60–180 يوم |

الكامل في `data/productized_services/services.yaml`.

## 4. مسار الترقية (Service Upgrade Path)

```
[Free Diagnostic]
       ↓
[Revenue Leakage Diagnostic] (1,500-3,000 SAR)
       ↓
[Follow-up Recovery Workflow] (5,000-9,000 SAR)
       ↓
[AI Revenue Ops Starter] (2,999 SAR/شهر)
       ↓
[Full Revenue OS] (9,999-25,000 SAR/شهر)
       ↓
[Custom Company OS] (250,000+ SAR)
       ↑
[Monthly Optimization Retainer] (تشعب من أي مستوى)
```

## 5. Acceptance Criteria — المكتبة

`data/productized_services/acceptance_criteria.jsonl` يحتوي على
`acceptance_id`, `service_id`, `deliverable_ref`, `criterion`,
`measurement`, `owner`. مثال:

```json
{
  "acceptance_id": "acc_2026_rld_01",
  "service_id": "revenue_leakage_diagnostic",
  "deliverable_ref": "proof_pack",
  "criterion": "Proof Pack يعرض ≥ 3 leaks محددة بأرقام",
  "measurement": "manual review by founder + client",
  "owner": "founder"
}
```

## 6. Deliverables — المكتبة

`data/productized_services/deliverables.jsonl` يحتوي على
`deliverable_id`, `service_id`, `name`, `format`, `template_ref`,
`due_offset_days`. مثال:

```json
{
  "deliverable_id": "del_2026_rld_01",
  "service_id": "revenue_leakage_diagnostic",
  "name": "Proof Pack PDF",
  "format": "pdf",
  "template_ref": "data/templates/proof_pack_ar.md",
  "due_offset_days": 5
}
```

## 7. الحوكمة (Governance)

- أي تغيير على catalog (إضافة/حذف/تعديل خدمة) يحتاج:
  1. PR مع tag `services-change`.
  2. مراجعة من المؤسس.
  3. تحديث `CHANGELOG.md`.
- لا agent يغيّر السعر بدون موافقة المؤسس + Decision Pack §S1.
- `services.yaml` هو المصدر الوحيد للحقيقة (لا hardcode في الكود).

## 8. الربط مع agents أخرى

- **Agent #13 (Legal):** كل named case study ⇒ `case_study_permissions.jsonl`.
- **Agent #14 (Localization):** كل deliverable عربي ⇒
  `docs/localization/TERMINOLOGY_GLOSSARY_AR.md` compliance.
- **Agent #16 (Data Room):** "Custom Company OS" example = section في
  data room.
- **Agent #17 (Procurement):** tool costs per service تُحدَّث شهرياً.

## 9. مخاطر

1. **Scope creep** في Custom Company OS ⇒ SCOPE_CONTROL.md + change
   request process.
2. **Misaligned ICP** ⇒ founder يرفض بأدب قبل البدء.
3. **Overpromise on delivery time** ⇒ لا تعد بـ timeline أقل من
   timeline_days.max.
4. **Acceptance drift** ⇒ كل deliverable له acceptance مكتوب مسبقاً.

## 10. المراجع

- `data/productized_services/services.yaml` — catalog
- `data/productized_services/deliverables.jsonl` — deliverables
- `data/productized_services/acceptance_criteria.jsonl` — criteria
- `schemas/productized_service.schema.json` — schema
- `docs/PRICING_AND_PACKAGING_V6.md` — pricing rules
- `docs/OFFER_LADDER.md` — offer ladder
- `docs/delivery/SCOPE_CONTROL.md` — scope control
- `docs/delivery/DELIVERY_LIFECYCLE.md` — delivery lifecycle
- `docs/legal/LEGAL_REVIEW_POLICY_AR.md` — legal review triggers
- `docs/localization/ARABIC_BRAND_VOICE_AR.md` — voice for client copy
