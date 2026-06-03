# Proposal Approval Queue
*Date: 2026-06-03*

> العروض بانتظار **اعتماد بشري**. لا يخرج أي عرض للعميل قبل الاعتماد والإرسال اليدوي.

---

## 1. بانتظار الاعتماد

| العرض | الشركة | السعر (SAR) | الشرط المُتحقّق | بانتظار |
|------|--------|------:|-----------------|---------|
| MP-004 | Rased | 3,000 | كل الشروط ✅ | اعتماد + إرسال يدوي |
| MP-001 | Madar | 4,500 | كل الشروط ✅ | اعتماد + إرسال يدوي |
| MP-002 | Tadreeb Plus | 3,500 | كل الشروط ✅ | اعتماد + إرسال يدوي |
| MP-005 | BinaaPro | 3,000 | كل الشروط ✅ | اعتماد + إرسال يدوي |
| MP-003 | Noor Clinics | 4,500 | كل الشروط ✅ | اعتماد + إرسال يدوي |

---

## 2. شروط العبور (مرجع)

```
1. starter_price_sar > 0
2. deliverables ≥ 3
3. timeline محدد
4. required_inputs ≥ 1
5. expected_first_proof موجود
6. approval_required = true + approved_by بشري
7. لا ادعاء مضمون
```

المرجع: `docs/proposals/PROPOSAL_APPROVAL_GATE_AR.md`.

---

## 3. مسار الاعتماد

```
draft → approval_queue → (Founder) approve/reject
   → approved → (Founder) send → sent → won/lost
```

كل قرار يُسجَّل في أثر الحوكمة (`company_os/governance/ai_action_ledger.jsonl`).

---

## 4. ملاحظة حوكمة

يتسق هذا مع `company_os/governance/agent_permissions.md`:
«Human approves all pricing and proposals» — التسعير قرار بشري حصرًا، والوكيل لا يرسل بلا اعتماد.

---

*Proposal Approval Queue | Generated: 2026-06-03 | بانتظار الاعتماد البشري*
