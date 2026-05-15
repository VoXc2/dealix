# العربية

## صلاحيات الوكيل التنفيذي

**Owner:** المؤسس (`founder`).

## مستوى الاستقلالية

`L1_draft_only` وفق `AutonomyLevel` في `auto_client_acquisition/agent_governance/schemas.py`. الوكيل يصيغ المذكّرات فقط؛ النشر والالتزام يحتاجان موافقة المؤسس.

## ما هو مسموح آلياً

- قراءة وتحليل المؤشرات المجمَّعة ضمن `executive_memory`.
- صياغة ملخصات تنفيذية ومذكّرات قرار (مسودة).
- تجميع المؤشرات بلا PII وبلا مؤشرات سرية.

## ما يحتاج موافقة

- نشر أي تقرير خارجياً.
- أي التزام استراتيجي.
- أي إرسال بريد خارجي.
- المُوافِق: `founder`، عبر `auto_client_acquisition/governance_os/approval_policy.py`.

## ما هو ممنوع

الكشط، أتمتة LinkedIn، WhatsApp البارد، إرسال WhatsApp، تصدير PII بالجملة. مرفوضة عبر `auto_client_acquisition/governance_os/forbidden_actions.py`.

## حدود الذاكرة

`executive_memory` و`product_knowledge` فقط. لا وصول إلى `customer_memory` الخام للعميل — المؤشرات تصل مجمَّعة فقط.

---

# English

## Executive agent permissions

**Owner:** Founder (`founder`).

## Autonomy level

`L1_draft_only` per `AutonomyLevel` in `auto_client_acquisition/agent_governance/schemas.py`. The agent drafts memos only; publishing and commitments need founder approval.

## What is auto-permitted

- Read and analyze aggregated metrics within `executive_memory`.
- Draft executive summaries and decision memos (draft state).
- Aggregate metrics with no PII and no confidential metrics.

## What requires approval

- Publishing any report externally.
- Any strategic commitment.
- Any external email send.
- Approver: `founder`, via `auto_client_acquisition/governance_os/approval_policy.py`.

## What is forbidden

Scraping, LinkedIn automation, cold WhatsApp, WhatsApp send, bulk PII export. Rejected via `auto_client_acquisition/governance_os/forbidden_actions.py`.

## Memory bounds

`executive_memory` and `product_knowledge` only. No access to raw customer `customer_memory` — metrics arrive aggregated only.
