# Mini Proposal Factory — مصنع العروض المختصرة

*عرض من صفحة واحدة لكل حساب مهتم. دائمًا بسعر افتتاحي ودائمًا يحتاج موافقة.*
*المرجع الآلي: `schemas/mini_proposal.schema.json` · البيانات: `data/proposals/mini_proposals.jsonl`.*
*آخر تحديث: 2026-06-03*

---

## الحقول الملزِمة

```txt
title · company · recommended_system · why_this_system · public_signal ·
likely_pain · first_sprint · deliverables · timeline_days · starter_price_sar ·
required_inputs · expected_first_proof · next_step · approval_required (=true)
```

> قاعدتان لا تتغيّران (يفرضهما المدقّق):
> 1. **`starter_price_sar` موجود** (> 0).
> 2. **`approval_required = true`** — العرض مسودة حتى يوافق المؤسس.

---

## القالب (Template)

```txt
Title:           [First Sprint] for [Company]
Company:         [Company]
Recommended:     [System]
Why this system: [سبب مرتبط بالألم والدليل العام]
Public signal:   [إشارة عامة إن وُجدت]
Likely pain:     [بلغة احتمالية في L0/L1]
First Sprint:    [اسم الـ Sprint]
Deliverables:    - … - … - …
Timeline:        [أيام]
Starter price:   [SAR]
Required inputs: - … - … - …
Expected first proof: [أول مخرج ملموس]
Next step:       [مكالمة قصيرة / تأكيد المدخلات]
Approval:        required ✅
```

---

## مثال (من البيانات الحالية)

```txt
Title: 7-Day Follow-up Recovery Sprint for [Company]
Why: [Company] تعمل في قطاع تؤثر فيه جودة المتابعة مباشرة على التحويل.
First Sprint: بناء قائمة متابعة، نموذج حالة، ومجموعة رسائل.
Deliverables:
- Follow-up Queue
- Status Model
- Message Set
- Weekly Recovery Report
Timeline: 7 days
Starter price: 3,500 SAR
Required inputs:
- lead list or sample inquiries
- current follow-up messages
- communication channels
Approval required: yes
```

---

## قواعد الجودة

```txt
- نظام واحد فقط لكل عرض.
- لا ضمانات (نضمن/مضمون/100%/guarantee) — يرفضها المدقّق.
- لغة احتمالية عند ضعف الدليل.
- السعر افتتاحي وواضح.
- خطوة تالية واحدة بسيطة.
```

---

## دورة الحياة

```txt
draft → approved → sent → accepted / declined
```

العروض الجاهزة تظهر في `reports/proposals/MINI_PROPOSAL_QUEUE.md`.
التشغيل الحالي: **3 عروض** بحالة `draft` (Digital Rise · TrainMe · LegalEdge).
