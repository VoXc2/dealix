# العربية

**Owner:** المالك القانوني (Legal Owner) — بالتنسيق مع مالك طبقة الحوكمة.

## قواعد الموافقة — الشؤون القانونية

تحدّد هذه الوثيقة من يوافق على الإجراءات ذات الأثر القانوني أو التنظيمي وكيف. تُطبَّق عبر `auto_client_acquisition/approval_center/approval_policy.py` وتراعي متطلبات PDPL في `auto_client_acquisition/compliance_os/`.

### القاعدة الحاكمة

كل إجراء يُنشئ التزاماً قانونياً أو يمسّ بيانات شخصية أو يتعلق بطلب صاحب بيانات يتطلب موافقة قانونية موثَّقة. الذكاء الاصطناعي لا يلتزم نيابة عن Dealix أو العميل.

### جدول القواعد

| الإجراء | التصنيف | المُوافِق |
|---|---|---|
| صياغة مسوّدة بند تعاقدي | A0 | لا موافقة (مسوّدة فقط) |
| إرسال مستند تعاقدي لعميل | A3 | المالك القانوني + المالك التجاري |
| الرد على طلب صاحب بيانات (PDPL) | A2 | المالك القانوني |
| حذف بيانات شخصية بناءً على طلب | A3 | المالك القانوني + مالك الحوكمة |
| إخطار خرق بيانات لـ SDAIA | A3 | المالك القانوني + قائد الأمن |
| إقرار علاقة مراقب/معالج لتكامل جديد | A2 | المالك القانوني |

### قيود غير قابلة للتفاوض

- لا التزام تعاقدي يصدر آلياً؛ كل مستند تعاقدي يُراجَع بشرياً.
- طلبات أصحاب البيانات تُعالَج وفق `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.
- إخطار الخرق خلال 72 ساعة وفق PDPL.
- لا ادعاء امتثال لم يُتحقَّق منه؛ المصدر سجل `dealix/registers/compliance_saudi.yaml`.

### الآلية

1. يُعدّ النظام مسوّدة الإجراء القانوني.
2. يُقيّمه محرّك السياسات ومحرّك الامتثال.
3. يُرفع للمُوافِق وفق الجدول؛ A3 موافقة مزدوجة.
4. عند الموافقة فقط يُنفَّذ؛ كل خطوة قيد تدقيق.

### قائمة الجاهزية

- [x] كل التزام قانوني خارجي يتطلب موافقة موثَّقة.
- [x] طلبات أصحاب البيانات لها مسار موافقة محدد.
- [ ] قائمة تحقق إخطار الخرق مدمجة في مسار الموافقة (مُخطَّط).

### الحوكمة والتراجع

- لا تفويض ذاتي.
- التراجع عن إجراء قانوني يتطلب مراجعة قانونية موثَّقة وقيد تدقيق.

انظر أيضاً: `governance/compliance/pdpl_readiness.md`، `governance/compliance/data_deletion.md`.

---

# English

**Owner:** Legal Owner — in coordination with the Governance Platform Lead.

## Approval Rules — Legal

This document defines who approves actions with legal or regulatory impact and how. Enforced via `auto_client_acquisition/approval_center/approval_policy.py` and observes PDPL requirements in `auto_client_acquisition/compliance_os/`.

### Governing rule

Every action that creates a legal commitment, touches personal data, or concerns a data subject request requires a documented legal approval. The AI does not commit on behalf of Dealix or the customer.

### Rule table

| Action | Classification | Approver |
|---|---|---|
| Draft a contractual clause | A0 | No approval (draft-only) |
| Send a contractual document to a customer | A3 | Legal owner + commercial owner |
| Respond to a data subject request (PDPL) | A2 | Legal owner |
| Delete personal data on request | A3 | Legal owner + governance owner |
| Notify SDAIA of a data breach | A3 | Legal owner + security lead |
| Affirm a controller/processor relationship for a new integration | A2 | Legal owner |

### Non-negotiable constraints

- No contractual commitment is issued automatically; every contractual document is human-reviewed.
- Data subject requests are handled per `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.
- Breach notification within 72 hours per PDPL.
- No claiming of unverified compliance; the source is the register `dealix/registers/compliance_saudi.yaml`.

### Mechanism

1. The system prepares the draft legal action.
2. The Policy Engine and Compliance Engine evaluate it.
3. It is raised to the approver per the table; A3 is dual approval.
4. Only on approval does it execute; every step is an audit entry.

### Readiness checklist

- [x] Every external legal commitment requires a documented approval.
- [x] Data subject requests have a defined approval path.
- [ ] Breach-notification checklist embedded in the approval path (planned).

### Governance and rollback

- No self-approval.
- Rolling back a legal action requires a documented legal review and an audit entry.

See also: `governance/compliance/pdpl_readiness.md`, `governance/compliance/data_deletion.md`.
