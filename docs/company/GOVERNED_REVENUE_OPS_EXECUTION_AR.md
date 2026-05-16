# Governed Revenue Ops Execution Blueprint (AR)

## التموضع التشغيلي

Dealix = **Governed Revenue & AI Operations**

القاعدة الحاكمة:
كل توصية أو متابعة أو قرار مبيعات يرتبط بـ:

- `source_ref`
- `approval`
- `evidence`
- `decision_passport`

## شاشات الفرونت إند الرئيسية

1. Founder Command Center
2. Service Catalog
3. Market Proof Console
4. Revenue Ops Console
5. Evidence Ledger
6. Billing / Invoices

### Revenue Ops Console (أولوية)

يعرض:

- clients
- pipeline files
- opportunities
- deal risks
- next actions
- follow-up drafts
- decision passports
- proof events

أزرار التشغيل:

- Create Diagnostic
- Upload CRM Export
- Generate Revenue Review
- Create Decision Passport
- Draft Follow-up
- Mark Approved
- Create Invoice Draft
- Generate Proof Pack

ممنوع افتراضيًا:

- Send automatically

## Backend domains المقترحة

- clients
- contacts
- market_proof
- revenue_ops
- diagnostics
- evidence
- approvals
- billing
- board_decision
- reports

## واجهات API التشغيلية

- `POST /api/v1/revenue-ops/diagnostics`
- `POST /api/v1/revenue-ops/upload`
- `POST /api/v1/revenue-ops/score`
- `GET  /api/v1/revenue-ops/{id}/decision-passport`
- `POST /api/v1/revenue-ops/{id}/follow-up-drafts`
- `POST /api/v1/evidence/events`
- `POST /api/v1/approvals`
- `POST /api/v1/invoices`

## Revenue Ops state machine

- `draft` = داخلي
- `approved` = تمت موافقة المؤسس
- `sent` = إرسال يدوي أو عبر قناة مصرح بها
- `used_in_meeting` = L5
- `scope_requested` = L6
- `invoice_sent` = L7 candidate
- `invoice_paid` = L7 confirmed

## مقاييس البداية (مختصرة)

- `sent_count`
- `reply_count`
- `meeting_count`
- `diagnostic_scope_requested`
- `invoice_sent`
- `invoice_paid`
- `proof_pack_created`
- `retainer_opportunity`
