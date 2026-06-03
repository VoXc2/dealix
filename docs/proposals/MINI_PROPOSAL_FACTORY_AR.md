# Mini Proposal Factory — مصنع العروض المختصرة

> كل اهتمام يتحول إلى **Mini Proposal** من صفحة واحدة. العرض **لا يُرسل** حتى يعتمده المؤسس.

---

## 1. الحقول المطلوبة

المخطط: `schemas/mini_proposal.schema.json` — البيانات: `data/proposals/mini_proposals.jsonl`.

```
Title
Company
Recommended System
Public Signal
Likely Pain
Why this system
First Sprint
Deliverables (≥ 3)
Timeline
Starter Price (SAR)
Required Inputs (≥ 1)
Expected First Proof
Risks / Assumptions
Next Step
Approval Required  = true
```

---

## 2. الأسعار الافتتاحية (Catalog Defaults)

| النظام | السعر الافتتاحي (SAR) |
|--------|----------------------:|
| Executive Command OS | 5,500 |
| Revenue Operating System | 4,500 |
| WhatsApp Client OS | 4,500 |
| Follow-up Recovery OS | 3,500 |
| Proposal & Proof OS | 3,000 |

> السعر النهائي **قرار بشري**. هذه قيم الكتالوج الافتتاحية فقط، ويبقى التسعير ضمن صلاحيات المؤسس (راجع `company_os/governance/agent_permissions.md`).

---

## 3. قالب الصفحة الواحدة

```
العنوان: [Title]
الشركة: [Company]
النظام الموصى به: [Recommended System]
الإشارة العامة: [Public Signal — موثّقة أو "لا يوجد"]
الألم المحتمل: [Likely Pain]
لماذا هذا النظام: [Why this system]
أول Sprint: [First Sprint]
المخرجات:
  - [Deliverable 1]
  - [Deliverable 2]
  - [Deliverable 3]
المدة: [Timeline]
السعر الافتتاحي: [Starter Price] SAR
المطلوب منكم: [Required Inputs]
أول دليل قيمة متوقع: [Expected First Proof]
مخاطر وافتراضات: [Risks / Assumptions]
الخطوة التالية: [Next Step]
يتطلب اعتمادًا: نعم
```

---

## 4. العروض الجاهزة في العيّنة (5)

| العرض | الشركة | النظام | السعر | الحالة |
|------|--------|--------|------:|--------|
| `MP-001` | Madar | Revenue Operating System | 4,500 | draft |
| `MP-002` | Tadreeb Plus | Follow-up Recovery OS | 3,500 | draft |
| `MP-003` | Noor Clinics | WhatsApp Client OS | 4,500 | draft |
| `MP-004` | Rased | Proposal & Proof OS | 3,000 | draft |
| `MP-005` | BinaaPro | Proposal & Proof OS | 3,000 | draft |

كلها `approval_required = true` و`status = draft`. الطابور: `reports/proposals/MINI_PROPOSAL_QUEUE.md`.

---

## 5. بوابة الجودة

`scripts/account-factory-check.mjs` يرفض العرض إذا:
- لا يوجد `starter_price_sar` > 0
- `approval_required ≠ true`
- أقل من 3 `deliverables`
- لا يوجد `expected_first_proof`
- يحتوي ادعاءً مضمونًا

راجع أيضًا `docs/proposals/PROPOSAL_APPROVAL_GATE_AR.md`.

---

*Mini Proposal Factory | الإصدار 1.0 | آخر تحديث: 2026-06-03 | كل عرض مسودة*
