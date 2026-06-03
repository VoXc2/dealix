# Mini Proposal Factory — مصنع العروض المصغّرة

كل اهتمام يتحول إلى **Mini Proposal من صفحة واحدة** جاهز للمراجعة، لا يُرسل إلا بعد اعتماد المؤسس.

---

## 1. الحقول (العقد)

المرجع: `schemas/mini_proposal.schema.json`.

```
proposal_id · pack_id · company_name · title
recommended_system · public_signal · likely_pain · why_this_system
first_sprint · deliverables(≥3) · timeline · starter_price_sar
required_inputs · expected_first_proof · risks_assumptions
next_step · approval_required(=true دائمًا) · status · generated_at
```

---

## 2. القالب (مخرج لكل اهتمام)

```
العنوان: Mini Proposal — [النظام] لـ[الشركة]

الإشارة العامة: [signal عام أو صياغة قطاعية محترمة]
الألم المحتمل:   [لغة احتمالية إن كان الدليل L0/L1]
لماذا هذا النظام: [سبب مختصر مرتبط بالقطاع]

أول Sprint: [Entry Sprint]
المخرجات:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3] (وقد تزيد)

المدة:        3 إلى 5 أيام عمل
السعر الافتتاحي: [starter_price] ريال
المطلوب منكم: [required inputs]
أول إثبات متوقع: [proof angle]

المخاطر/الافتراضات:
- النتائج تعتمد على جودة المدخلات.
- Sprint تشخيصي أولًا — لا وعود بأرقام مضمونة.

الخطوة التالية: مراجعة المؤسس واعتماد الإرسال، ثم جلسة مدخلات قصيرة.
```

---

## 3. التوليد

`scripts/generate_account_packs.py` ينتج عرضًا مصغّرًا لكل Pack في `data/proposals/mini_proposals.jsonl`.
التقارير: `reports/proposals/MINI_PROPOSAL_QUEUE.md` و`PROPOSAL_APPROVAL_QUEUE.md`.

الحالة الافتراضية: العروض ذات Account Score ≥ 75 تدخل `approval_queue`، والبقية `draft`.

---

## 4. القاعدة الذهبية

> **لا إرسال بلا اعتماد.** `approval_required = true` ثابت لا يتغيّر.
> ولا ادعاء مضمون في أي حقل.

---

*Version 1.0 — يقرأ مع PROPOSAL_APPROVAL_GATE_AR*
