# العربية

## صلاحيات وكيل الدعم

**Owner:** قائد نجاح العملاء (`customer_success_lead`).

## مستوى الاستقلالية

`L2_approval_required` وفق `AutonomyLevel` في `auto_client_acquisition/agent_governance/schemas.py`. الوكيل يصيغ الردود ويوصي؛ التنفيذ الخارجي يحتاج موافقة بشرية.

## ما هو مسموح آلياً

- قراءة وتحليل التذاكر ضمن `customer_memory` (مقيّدة بـ `tenant_id`).
- البحث في المعرفة الداخلية.
- إنشاء وتحديث مسودات التذاكر والردود.

## ما يحتاج موافقة

- أي إرسال خارجي (WhatsApp، بريد).
- أي عرض استرداد أو التزام SLA.
- المُوافِق: `customer_success_lead`، عبر `auto_client_acquisition/governance_os/approval_policy.py`.

## ما هو ممنوع

الكشط، أتمتة LinkedIn، WhatsApp البارد، تصدير PII بالجملة. مرفوضة عبر `auto_client_acquisition/governance_os/forbidden_actions.py`.

## حدود الذاكرة

`customer_memory` و`product_knowledge` فقط. لا وصول إلى `governance_memory` أو `executive_memory`.

---

# English

## Support agent permissions

**Owner:** Customer Success Lead (`customer_success_lead`).

## Autonomy level

`L2_approval_required` per `AutonomyLevel` in `auto_client_acquisition/agent_governance/schemas.py`. The agent drafts replies and recommends; external execution needs human approval.

## What is auto-permitted

- Read and analyze tickets within `customer_memory` (bound by `tenant_id`).
- Search internal knowledge.
- Create and update draft tickets and replies.

## What requires approval

- Any external send (WhatsApp, email).
- Any refund offer or SLA commitment.
- Approver: `customer_success_lead`, via `auto_client_acquisition/governance_os/approval_policy.py`.

## What is forbidden

Scraping, LinkedIn automation, cold WhatsApp, bulk PII export. Rejected via `auto_client_acquisition/governance_os/forbidden_actions.py`.

## Memory bounds

`customer_memory` and `product_knowledge` only. No access to `governance_memory` or `executive_memory`.
