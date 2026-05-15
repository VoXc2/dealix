# العربية

## صلاحيات وكيل العمليات

**Owner:** قائد عمليات التسليم (`delivery_ops_lead`).

## مستوى الاستقلالية

`L4_internal_automation_only` وفق `AutonomyLevel` في `auto_client_acquisition/agent_governance/schemas.py`. الوكيل ينفّذ أتمتة داخلية فقط؛ أي إجراء خارجي مرفوع أو ممنوع.

## ما هو مسموح آلياً

- قراءة وتحليل حالة العمليات ضمن `ops_memory`.
- إنشاء وتحديث مسودات المهام والتقارير الداخلية.
- تجميع مسودات حزم الأدلة.

## ما يحتاج موافقة

- أي إرسال بريد خارجي.
- أي التزام مع مورّد أو تغيير تخصيص موارد.
- المُوافِق: `delivery_ops_lead`، عبر `auto_client_acquisition/governance_os/approval_policy.py`.

## ما هو ممنوع

الكشط، أتمتة LinkedIn، WhatsApp البارد، إرسال WhatsApp، تصدير PII بالجملة. مرفوضة عبر `auto_client_acquisition/governance_os/forbidden_actions.py`.

## حدود الذاكرة

`ops_memory` و`product_knowledge` فقط. لا وصول إلى `customer_memory` المباشر للعميل ولا `executive_memory`.

---

# English

## Ops agent permissions

**Owner:** Delivery Ops Lead (`delivery_ops_lead`).

## Autonomy level

`L4_internal_automation_only` per `AutonomyLevel` in `auto_client_acquisition/agent_governance/schemas.py`. The agent runs internal automation only; any external action is raised or forbidden.

## What is auto-permitted

- Read and analyze operations status within `ops_memory`.
- Create and update draft tasks and internal reports.
- Assemble evidence pack drafts.

## What requires approval

- Any external email send.
- Any vendor commitment or resource allocation change.
- Approver: `delivery_ops_lead`, via `auto_client_acquisition/governance_os/approval_policy.py`.

## What is forbidden

Scraping, LinkedIn automation, cold WhatsApp, WhatsApp send, bulk PII export. Rejected via `auto_client_acquisition/governance_os/forbidden_actions.py`.

## Memory bounds

`ops_memory` and `product_knowledge` only. No direct access to customer-facing `customer_memory` or `executive_memory`.
