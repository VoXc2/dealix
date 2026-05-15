# العربية

## ملف مخاطر وكيل المبيعات

**مستوى المخاطر:** متوسط (`medium`).

## مصادر المخاطر

- **إرسال خارجي:** الوكيل يصيغ رسائل قد تصل العملاء. التخفيف: كل إرسال خارجي تحت `requires_approval_for`.
- **التزام تجاري:** خصم أو عقد. التخفيف: موافقة `revenue_os_lead` إلزامية.
- **مبالغة في الادعاء:** وعود مبيعات. التخفيف: قاعدة `no_guaranteed_claims` في `auto_client_acquisition/governance_os/rules/no_guaranteed_claims.py`.
- **بيانات شخصية:** بيانات العميل المحتمل. التخفيف: نطاق `customer_memory` مقيّد بـ `tenant_id`.

## ضوابط التخفيف

- كل إرسال خارجي يبدأ كمسودة عبر `auto_client_acquisition/governance_os/draft_gate.py`.
- الإجراءات الممنوعة مرفوضة عبر `forbidden_actions.py`.
- إيقاف فوري عبر مفتاح الإيقاف.

## المخاطر المتبقية

احتمال صياغة عرض بسعر خاطئ — يخفّفه التحقق البشري عند الموافقة.

## درجة الجاهزية الحالية

**76 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Sales agent risk profile

**Risk level:** medium.

## Risk sources

- **External send:** the agent drafts messages that may reach customers. Mitigation: every external send is under `requires_approval_for`.
- **Commercial commitment:** discount or contract. Mitigation: `revenue_os_lead` approval is mandatory.
- **Overclaim:** sales promises. Mitigation: the `no_guaranteed_claims` rule in `auto_client_acquisition/governance_os/rules/no_guaranteed_claims.py`.
- **Personal data:** prospect data. Mitigation: `customer_memory` scope bound by `tenant_id`.

## Mitigation controls

- Every external send starts as a draft via `auto_client_acquisition/governance_os/draft_gate.py`.
- Forbidden actions are rejected via `forbidden_actions.py`.
- Instant stop via the kill switch.

## Residual risk

A possibility of drafting a proposal with a wrong price — mitigated by human verification at approval.

## Current readiness score

**76 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
