# العربية

## صلاحيات وكيل الحوكمة

**Owner:** قائد الحوكمة (`governance_lead`).

## مستوى الاستقلالية

`L0_read_only` وفق `AutonomyLevel` في `auto_client_acquisition/agent_governance/schemas.py`. وكيل الحوكمة يقرأ ويقيّم ويصعّد فقط؛ لا ينفّذ ولا يرسل.

## ما هو مسموح آلياً

- قراءة وتحليل طلبات الإجراءات من الوكلاء الآخرين.
- تقييم الطلبات مقابل قواعد السياسة.
- توجيه التصعيدات للمُوافِق الصحيح.
- تسجيل آثار القرارات.

## ما يحتاج موافقة

- تغيير أي قاعدة سياسة.
- تغيير مصفوفة الموافقات.
- تغيير صلاحية أي وكيل.
- المُوافِق: `governance_lead`، عبر `auto_client_acquisition/governance_os/approval_policy.py`.

## ما هو ممنوع

كل أدوات الإرسال الخارجي، الكشط، أتمتة LinkedIn، WhatsApp البارد، تصدير PII بالجملة. وكيل الحوكمة لا يملك أداة إرسال خارجي إطلاقاً — هذا فصل صلاحيات مقصود.

## حدود الذاكرة

`governance_memory` و`product_knowledge` فقط. يقرأ بيانات وصفية عن إجراءات الوكلاء الآخرين، لا محتوى `customer_memory` الخام.

---

# English

## Governance agent permissions

**Owner:** Governance Lead (`governance_lead`).

## Autonomy level

`L0_read_only` per `AutonomyLevel` in `auto_client_acquisition/agent_governance/schemas.py`. The governance agent reads, evaluates, and escalates only; it does not execute and does not send.

## What is auto-permitted

- Read and analyze action requests from other agents.
- Evaluate requests against policy rules.
- Route escalations to the correct approver.
- Record decision traces.

## What requires approval

- Changing any policy rule.
- Changing the approval matrix.
- Changing any agent permission.
- Approver: `governance_lead`, via `auto_client_acquisition/governance_os/approval_policy.py`.

## What is forbidden

All external-send tools, scraping, LinkedIn automation, cold WhatsApp, bulk PII export. The governance agent holds no external-send tool at all — this is a deliberate separation of duties.

## Memory bounds

`governance_memory` and `product_knowledge` only. It reads metadata about other agents' actions, not raw `customer_memory` content.
