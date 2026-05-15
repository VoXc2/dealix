# العربية

**Owner:** المالك المالي (Finance Owner) — بالتنسيق مع مالك طبقة الحوكمة.

## قواعد الموافقة — المالية

تحدّد هذه الوثيقة من يوافق على الإجراءات المالية وكيف. تُطبَّق عبر `auto_client_acquisition/approval_center/approval_policy.py` ومصفوفة `auto_client_acquisition/governance_os/approval_matrix.py`، وتراعي متطلبات فوترة ZATCA المرحلة الثانية في `auto_client_acquisition/compliance_os/`.

### القاعدة الحاكمة

كل إجراء مالي ذي أثر خارجي أو غير عكوس يتطلب موافقة بشرية موثَّقة. الذكاء الاصطناعي يُعدّ مسوّدة الحساب أو الفاتورة؛ الإنسان يبتّ.

### جدول القواعد

| الإجراء | التصنيف | المُوافِق |
|---|---|---|
| إعداد مسوّدة فاتورة | A0 | لا موافقة (مسوّدة فقط) |
| إصدار فاتورة ZATCA | A2 | المالك المالي |
| تعديل بند تسعير معتمد | A2 | المالك المالي |
| استرداد مبلغ لعميل | A3 | المالك المالي + المالك التجاري |
| تسوية مبلغ متنازَع عليه | A3 | المالك المالي + الشؤون القانونية |
| تصدير سجلات مالية تحوي بيانات S3 | A3 | المالك المالي + مالك الحوكمة |

### قيود غير قابلة للتفاوض

- لا إصدار فاتورة دون استيفاء متطلبات ZATCA المرحلة الثانية.
- لا أرقام مالية في مخرجات موجّهة للعميل بلا مصدر موثَّق.
- السجلات المالية تُحفظ سبع سنوات وفق `dealix/registers/compliance_saudi.yaml`.
- لا بيانات مالية شخصية خام في السجلات (`no_pii_in_logs`).

### الآلية

1. يُعدّ النظام مسوّدة الإجراء المالي.
2. يُقيّمه محرّك السياسات ومحرّك الامتثال.
3. يُرفع للمُوافِق وفق الجدول؛ A3 موافقة مزدوجة.
4. عند الموافقة فقط يُنفَّذ؛ كل خطوة قيد تدقيق.

### قائمة الجاهزية

- [x] كل إجراء مالي خارجي يتطلب موافقة موثَّقة.
- [x] إصدار الفاتورة مرتبط بفحص امتثال ZATCA.
- [ ] ربط آلي بين قيد التدقيق المالي والفاتورة المُصدَرة (مُخطَّط).

### الحوكمة والتراجع

- لا تفويض ذاتي.
- التراجع المالي يتم بقيد معاكس موثَّق لا بحذف؛ يُسجَّل كقيد تدقيق.

انظر أيضاً: `governance/audit/audit_retention.md`، `governance/risk_models/action_risk_matrix.md`.

---

# English

**Owner:** Finance Owner — in coordination with the Governance Platform Lead.

## Approval Rules — Finance

This document defines who approves financial actions and how. Enforced via `auto_client_acquisition/approval_center/approval_policy.py` and the matrix `auto_client_acquisition/governance_os/approval_matrix.py`, and observes ZATCA Phase 2 invoicing requirements in `auto_client_acquisition/compliance_os/`.

### Governing rule

Every financial action with external or irreversible impact requires a documented human approval. The AI prepares the draft account or invoice; the human decides.

### Rule table

| Action | Classification | Approver |
|---|---|---|
| Prepare a draft invoice | A0 | No approval (draft-only) |
| Issue a ZATCA invoice | A2 | Finance owner |
| Change an approved pricing line | A2 | Finance owner |
| Refund a customer | A3 | Finance owner + commercial owner |
| Settle a disputed amount | A3 | Finance owner + legal |
| Export financial records containing S3 data | A3 | Finance owner + governance owner |

### Non-negotiable constraints

- No invoice is issued without meeting ZATCA Phase 2 requirements.
- No financial figures in customer-facing output without a documented source.
- Financial records are retained seven years per `dealix/registers/compliance_saudi.yaml`.
- No raw personal financial data in logs (`no_pii_in_logs`).

### Mechanism

1. The system prepares the draft financial action.
2. The Policy Engine and Compliance Engine evaluate it.
3. It is raised to the approver per the table; A3 is dual approval.
4. Only on approval does it execute; every step is an audit entry.

### Readiness checklist

- [x] Every external financial action requires a documented approval.
- [x] Invoice issuance is tied to a ZATCA compliance check.
- [ ] Automatic linkage between the financial audit entry and the issued invoice (planned).

### Governance and rollback

- No self-approval.
- A financial rollback is done by a documented compensating entry, not a deletion; it is recorded as an audit entry.

See also: `governance/audit/audit_retention.md`, `governance/risk_models/action_risk_matrix.md`.
