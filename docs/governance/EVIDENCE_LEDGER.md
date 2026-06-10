# Evidence Ledger — Dealix

**المرجع الاستراتيجي:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)

## الغرض

سجل **حديث قابل للتدقيق** يربط كل قرار أو إجراء **بمصدر** و**نتيجة سياسة** و**موافقة** عند الاقتضاء.

## أحداث أدلة مرجعية (أمثلة)

`lead_captured` · `message_prepared` · `message_approved` · `message_sent` · `reply_received` · `meeting_booked` · `meeting_done` · `scope_requested` · `scope_sent` · `invoice_sent` · `invoice_paid` · `onboarding_submitted` · `diagnostic_started` · `proof_pack_sent` · `value_confirmed` · `sprint_proposed` · `retainer_proposed` · `referral_requested`

## حقول مقترحة لكل حدث

- `event_type` · `timestamp` · `actor` (human | agent | system)  
- `subject` (lead_id / ticket_id / deal_id)  
- `sources[]` (مراجع ملفات، روابط داخلية، معرفات CRM — بدون أسرار)  
- `policy_result` (allowed | draft_only | blocked | approval_required)  
- `approval_id` إن وُجد  
- `payload_summary` (نص قصير غير حساس)

## قواعد جودة

- لا رقم **مباع** بلا مصدر أو بدون `is_estimate=true`  
- لا ادّعاء أمني/امتثال في مواد عميل بدون مصدر ومراجعة  
- اكتمال الأدلة لمسار العميل المدفوع ≥ عتبة تشغيلية (مثال 90% حسب تعريفك للـ«مكتمل»)

## API (هدف)

`POST /api/v1/evidence/events` — كما في الخطة المركزية؛ اربط تدريجياً بـ Revenue Memory / event store الحالي في المستودع.
