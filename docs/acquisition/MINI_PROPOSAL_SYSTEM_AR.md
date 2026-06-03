# Mini Proposal System — دليل التشغيل (AR)

> عرض من **صفحة واحدة** يُجهَّز بعد ظهور اهتمام العميل. **يتطلب موافقة founder قبل الإرسال** (`approval_required = true`). بلا أي نتائج مضمونة.
> مرجع الحقول: `schemas/mini_proposal.schema.json`. مرجع المصطلحات: `AGENTS.md`.

---

## 1. الغرض والقاعدة الصارمة

الـ Mini Proposal يحوّل الاهتمام إلى خطوة ملموسة صغيرة: Sprint محدّد، مخرجات واضحة، سعر افتتاحي، ومدخلات مطلوبة. الهدف **إثبات أول مخرج** لا بيع مشروع كبير.

```txt
HARD RULES:
- approval_required = true دائمًا. لا إرسال قبل موافقة founder.
- لا نتائج مضمونة (لا "مضمون" / "نضاعف" / "guarantee").
- السعر النهائي خارج السعر الافتتاحي يحتاج موافقة founder.
- delivery لا يبدأ قبل استلام required_inputs (حالة delivery_started).
```

تسلسل الحالات: `draft → pending_approval → approved → sent → accepted/declined`.

---

## 2. القالب (Template) — الحقول الـ 13

| # | الحقل | الشرح |
|---|---|---|
| 1 | `title` | عنوان العرض (مثال: 7-Day Follow-up Recovery Sprint). |
| 2 | `company` | اسم الشركة. |
| 3 | `recommended_system` | أحد الأنظمة الخمسة. |
| 4 | `why_this_system` | لماذا هذا النظام لهذه الشركة. |
| 5 | `current_likely_pain` | الألم المحتمل الحالي (صياغة احتمالية عند L0/L1). |
| 6 | `first_sprint` | وصف أول Sprint عملي. |
| 7 | `deliverables` | قائمة المخرجات الملموسة (≥ 1). |
| 8 | `timeline` | المدة (مثال: 7 days). |
| 9 | `starter_price` | كائن: `amount` (عدد) + `currency` (`SAR`) + `display` (مثال: "ابتداءً من 3,500 SAR"). |
| 10 | `required_inputs` | المدخلات المطلوبة من العميل قبل البدء (≥ 1). |
| 11 | `expected_first_proof` | أول إثبات متوقع (بلا ضمان نتيجة مالية). |
| 12 | `next_step` | الخطوة التالية الواضحة. |
| 13 | `approval_required` | `true` دائمًا. |

> حقول إضافية: `id` (نمط `MP-###`)، `status`، `created_at`.

```txt
=== MINI PROPOSAL ===
Title:                 [عنوان Sprint]
Company:               [الشركة]
System:                [recommended_system]
Why this system:       [سبب مرتبط بالشركة]
Current likely pain:   [ألم محتمل — صياغة احتمالية]
First sprint:          [وصف أول Sprint]
Deliverables:          [قائمة مخرجات]
Timeline:              [مدة]
Starter price:         ابتداءً من [X] SAR
Required inputs:       [مدخلات مطلوبة من العميل]
Expected first proof:  [أول إثبات متوقع — بلا ضمان نتيجة مالية]
Next step:             [خطوة واضحة]
Approval required:     true
=====================
```

---

## 3. أول Sprint + السعر الافتتاحي لكل نظام

> الأسعار **افتتاحية** بصيغة "ابتداءً من X SAR" ضمن مدى معقول 3,500–7,500 SAR. لا نتائج مضمونة. السعر النهائي خارج هذا يحتاج موافقة founder.

| النظام | أول Sprint | مخرجات نموذجية | سعر افتتاحي |
|---|---|---|---|
| `revenue_os` | بناء lead status model + next action لكل فرصة مفتوحة | Lead Status Model, Next-Action List, Weekly Opportunity Report | ابتداءً من 5,000 SAR |
| `executive_command_os` | تعريف أهم تقرير يومي + ربطه بقرار تالٍ صريح | Daily Command View, Decision-Trigger Map, Weekly Exec Summary | ابتداءً من 6,500 SAR |
| `followup_recovery_os` | بناء follow-up queue + رسائل متابعة حسب حالة العميل | Follow-up Queue, Lead Status Model, Message Set, Weekly Recovery Report | ابتداءً من 3,500 SAR |
| `whatsapp_client_os` | تصنيف الطلبات + flow + action cards + قاعدة handoff لإنسان | Request Taxonomy, WhatsApp Flow, Action Cards, Handoff Rules | ابتداءً من 5,500 SAR |
| `proposal_proof_os` | قالب عرض فيه scope + proof + سعر افتتاحي | Proposal Template, Proof Block, Scope Sheet, Objection Notes | ابتداءً من 4,500 SAR |

---

## 4. مثال عملي كامل — `followup_recovery_os`

```txt
=== MINI PROPOSAL ===
id:                    MP-101
Title:                 7-Day Follow-up Recovery Sprint
Company:               شركة تدريب في الرياض
System:                followup_recovery_os
Why this system:       الشركة لديها برامج متعددة وقناة واتساب ظاهرة، وهذا غالبًا يعني وجود
                       استفسارات تحتاج متابعة منظمة.
Current likely pain:   استفسارات التسجيل غالبًا تضيع أو لا تُتابع بنفس الجودة عبر القنوات.
First sprint:          نبني follow-up queue ونجهّز رسائل متابعة حسب حالة العميل.
Deliverables:
  - Follow-up Queue
  - Lead Status Model
  - Message Set
  - Weekly Recovery Report
Timeline:              7 days
Starter price:         Starts at 3,500 SAR
Required inputs:
  - قائمة الاستفسارات الأخيرة (من مصادر عامة/بيانات يقدّمها العميل، بلا PII غير لازم)
  - حالات المسجّل المعتادة (استفسر / سجّل مبدئيًا / لم يكمل)
  - من يتابع حاليًا وعبر أي قناة
Expected first proof:  تقرير أسبوعي يوضح كم استفسارًا أُعيد تفعيله بمتابعة منظمة (مؤشر تشغيلي، لا ضمان إيراد).
Next step:             مكالمة 20 دقيقة لفهم مصادر الاستفسارات.
Approval required:     true
status:                pending_approval
=====================
```

**ملاحظات الأمان في المثال:**
- `Expected first proof` مؤشر تشغيلي ("كم استفسارًا أُعيد تفعيله")، **لا** وعد بزيادة إيراد.
- `Required inputs` صريحة لأن العمل لا يبدأ قبل استلامها (`delivery_started`).
- `approval_required = true` والحالة `pending_approval` — لن يُرسل قبل موافقة founder.
- السعر افتتاحي بصيغة "Starts at 3,500 SAR".

---

## 5. التحقق

- التحقق: `schemas/mini_proposal.schema.json` (يفرض `approval_required = true` و`currency = SAR`).
- الفاحص: `scripts/acquisition_delivery_check.py` (`npm run os:check`).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
