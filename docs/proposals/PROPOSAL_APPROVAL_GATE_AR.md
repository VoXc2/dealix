# Proposal Approval Gate — بوابة اعتماد العروض

> لا يخرج أي عرض للعميل دون **اعتماد بشري**. هذه البوابة تحمي السمعة والتسعير والالتزامات.

---

## 1. شرط العبور (Pass Conditions)

يُسمح للعرض بالانتقال إلى `approved` فقط إذا:

| # | الشرط |
|---|-------|
| 1 | `starter_price_sar` موجود و > 0 |
| 2 | `deliverables` ≥ 3 عناصر |
| 3 | `timeline` محدد |
| 4 | `required_inputs` ≥ 1 |
| 5 | `expected_first_proof` موجود |
| 6 | `approval_required = true` و`approved_by` مُعبّأ من بشري |
| 7 | لا يوجد أي ادعاء مضمون في النص |

---

## 2. شرط الرفض (Hard Fail)

```
- لا يوجد starter_price
- لا يوجد deliverables كافية
- لا يوجد timeline
- لا يوجد required_inputs
- approval_required ليست true
- يوجد claim مضمون (نضمن / 10x / مضمون)
```

---

## 3. مسار الاعتماد (Workflow)

```
draft → approval_queue → (Founder review)
   → approve → approved → (Founder send) → sent → won/lost
   → reject → نعود للصياغة أو نُسقط العرض
```

> يتسق هذا مع مصفوفة الصلاحيات في `company_os/governance/agent_permissions.md`:
> «Human approves all pricing and proposals» و«AI never makes pricing decisions».

---

## 4. سجل الاعتماد (Audit)

كل اعتماد/رفض يُسجَّل (الوقت، المعتمِد، النتيجة) ضمن أثر الحوكمة
(`company_os/governance/ai_action_ledger.jsonl`). لا اعتماد صامت.

---

## 5. الحالة الحالية

جميع عروض العيّنة الخمسة في `draft` بانتظار الاعتماد. الطابور:
`reports/proposals/PROPOSAL_APPROVAL_QUEUE.md`.

---

*Proposal Approval Gate | الإصدار 1.0 | آخر تحديث: 2026-06-03*
