# العربية

## صلاحيات وكيل المبيعات

**Owner:** قائد Revenue OS (`revenue_os_lead`).

## مستوى الاستقلالية

`L2_approval_required` وفق `AutonomyLevel` في `auto_client_acquisition/agent_governance/schemas.py`. الوكيل يصيغ ويوصي؛ التنفيذ الخارجي يحتاج موافقة بشرية.

## ما هو مسموح آلياً

- قراءة وتحليل بيانات العميل ضمن `customer_memory` (مقيّدة بـ `tenant_id`).
- إنشاء مسودات: عملاء محتملون، حسابات، عروض، رسائل.
- طلب حجز اجتماع.

## ما يحتاج موافقة

- أي إرسال خارجي (WhatsApp، بريد).
- أي خصم أو التزام تعاقدي أو مالي.
- المُوافِق: `revenue_os_lead`، عبر `auto_client_acquisition/governance_os/approval_policy.py`.

## ما هو ممنوع

الكشط، أتمتة LinkedIn، WhatsApp البارد، تصدير PII بالجملة. مرفوضة عبر `auto_client_acquisition/governance_os/forbidden_actions.py`.

## حدود الذاكرة

`customer_memory` و`product_knowledge` فقط. لا وصول إلى `governance_memory` أو `executive_memory`.

---

# English

## Sales agent permissions

**Owner:** Revenue OS Lead (`revenue_os_lead`).

## Autonomy level

`L2_approval_required` per `AutonomyLevel` in `auto_client_acquisition/agent_governance/schemas.py`. The agent drafts and recommends; external execution needs human approval.

## What is auto-permitted

- Read and analyze customer data within `customer_memory` (bound by `tenant_id`).
- Create drafts: leads, accounts, proposals, messages.
- Request a meeting booking.

## What requires approval

- Any external send (WhatsApp, email).
- Any discount, contractual, or financial commitment.
- Approver: `revenue_os_lead`, via `auto_client_acquisition/governance_os/approval_policy.py`.

## What is forbidden

Scraping, LinkedIn automation, cold WhatsApp, bulk PII export. Rejected via `auto_client_acquisition/governance_os/forbidden_actions.py`.

## Memory bounds

`customer_memory` and `product_knowledge` only. No access to `governance_memory` or `executive_memory`.
