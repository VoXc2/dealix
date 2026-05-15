# العربية

## ملف مخاطر وكيل الدعم

**مستوى المخاطر:** متوسط (`medium`).

## مصادر المخاطر

- **إرسال خارجي:** ردود تصل العملاء. التخفيف: كل إرسال خارجي تحت `requires_approval_for`.
- **معلومة خاطئة:** رد غير دقيق. التخفيف: الردود مبنية على `knowledge.search_internal` فقط؛ التصعيد عند غياب الأساس.
- **التزام مالي:** عرض استرداد. التخفيف: موافقة `customer_success_lead` إلزامية.
- **بيانات شخصية:** بيانات العميل في التذكرة. التخفيف: نطاق `customer_memory` مقيّد بـ `tenant_id`.

## ضوابط التخفيف

- كل رد خارجي يبدأ كمسودة عبر `auto_client_acquisition/governance_os/draft_gate.py`.
- الإجراءات الممنوعة مرفوضة عبر `forbidden_actions.py`.
- إيقاف فوري عبر مفتاح الإيقاف.

## المخاطر المتبقية

احتمال صياغة رد بنبرة غير ملائمة — يخفّفه التحقق البشري عند الموافقة.

## درجة الجاهزية الحالية

**74 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Support agent risk profile

**Risk level:** medium.

## Risk sources

- **External send:** replies reach customers. Mitigation: every external send is under `requires_approval_for`.
- **Wrong information:** an inaccurate reply. Mitigation: replies are grounded only in `knowledge.search_internal`; escalation when a basis is missing.
- **Financial commitment:** a refund offer. Mitigation: `customer_success_lead` approval is mandatory.
- **Personal data:** customer data in the ticket. Mitigation: `customer_memory` scope bound by `tenant_id`.

## Mitigation controls

- Every external reply starts as a draft via `auto_client_acquisition/governance_os/draft_gate.py`.
- Forbidden actions are rejected via `forbidden_actions.py`.
- Instant stop via the kill switch.

## Residual risk

A possibility of drafting a reply with an unsuitable tone — mitigated by human verification at approval.

## Current readiness score

**74 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
