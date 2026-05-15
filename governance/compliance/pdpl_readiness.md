# العربية

**Owner:** قائد الخصوصية والثقة (Privacy & Trust Plane Lead).

## جاهزية الامتثال لنظام حماية البيانات الشخصية (PDPL)

تلخّص هذه الوثيقة وضع Dealix تجاه نظام حماية البيانات الشخصية السعودي. المصدر الرسمي الوحيد للحالة هو سجل `dealix/registers/compliance_saudi.yaml`؛ هذه الوثيقة عرض مقروء له ولا تُصدّر ادعاء امتثال لم يُتحقَّق منه.

### المواد المشمولة

- **المادة 5 — الأساس النظامي:** كل غرض معالجة لبيانات S3 يجب أن يُسجَّل له أساس نظامي (موافقة / عقد / التزام نظامي / مصلحة مشروعة). الإجراءات S3 تستوجب تحقق الأساس قبل التنفيذ.
- **المادة 13 — الإشعار والشفافية:** إشعار خصوصية عند جمع البيانات حيث الأساس موافقة.
- **المادة 14 — الموافقة:** التقاط الموافقة وإيصالها حيث يكون الأساس موافقة.
- **المادة 18 — حقوق صاحب البيانات:** الوصول والتصحيح والحذف ونقل البيانات.
- **المادة 21 — الاحتفاظ:** فترات احتفاظ محددة لكل صنف بيانات وحذف بعدها.

### الحالة الحالية (عرض من السجل)

| الضابط | الحالة | المرحلة |
|---|---|---|
| جرد البيانات | مُخطَّط | المرحلة 0 |
| سجل الأسس النظامية | مُخطَّط | المرحلة 0 |
| جدول الاحتفاظ | جزئي | المرحلة 1 |
| الاستجابة للخرق | مُخطَّط | المرحلة 1 |
| الموافقة والإشعار | جزئي | — |
| حقوق أصحاب البيانات | مُخطَّط | المرحلة 1 |
| النقل عبر الحدود | جزئي | — |

### الضوابط المُنفَّذة في الكود

- تصنيف الحساسية S0–S3 في `dealix/classifications/__init__.py`.
- معالجة طلبات أصحاب البيانات في `auto_client_acquisition/compliance_os/data_subject_requests.py`.
- سجل الموافقات `auto_client_acquisition/compliance_os/consent_ledger.py`.
- سجل أنشطة المعالجة `auto_client_acquisition/compliance_os/ropa.py`.
- منع البيانات الشخصية في السجلات عبر قاعدة `no_pii_in_logs`.
- بيانات S3 لا تُرسَل لمزوّدي النماذج الخارجيين قبل وجود اتفاقية معالجة بيانات.

### الفجوات المعروفة

- إصدار إيصال الموافقة غير مُنفَّذ بعد.
- الاحتفاظ غير مُطبَّق آلياً في قاعدة البيانات؛ يحتاج هجرة ومهمة مجدوَلة.
- التقييم الرسمي للنقل عبر الحدود وفق المادة 29 معلّق.

### قائمة الجاهزية

- [x] تصنيف الحساسية مُنفَّذ ويحكم مسار الإجراء.
- [x] معالجة طلبات أصحاب البيانات لها مسار كود ومسار موافقة.
- [x] قاعدة منع البيانات الشخصية في السجلات مفعّلة.
- [ ] جدول الاحتفاظ مُطبَّق آلياً (مُخطَّط).
- [ ] إيصال الموافقة (مُخطَّط).
- [ ] التقييم الرسمي للنقل عبر الحدود (مُخطَّط).

### المقاييس

- نسبة أغراض معالجة S3 ذات أساس نظامي مُسجَّل: هدف 100%.
- زمن الاستجابة لطلب صاحب بيانات.
- عدد الضوابط بحالة "مُنفَّذ" مقابل "مُخطَّط" في السجل.

### الحوكمة والتراجع

- مراجعة الوضع ربع سنوية وبعد أي حادث أو تحديث تنظيمي.
- لا تُصدَّر ادعاءات امتثال خارج ما يؤكده السجل.
- تعيين مسؤول حماية بيانات مسمّى قبل أول عميل إنتاجي ببيانات S3.

انظر أيضاً: `governance/compliance/data_deletion.md`، `governance/policies/data_handling_policy.md`، `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.

---

# English

**Owner:** Privacy & Trust Plane Lead.

## PDPL Compliance Readiness

This document summarizes Dealix's posture toward the Saudi Personal Data Protection Law. The single authoritative source of status is the register `dealix/registers/compliance_saudi.yaml`; this document is a readable view of it and issues no unverified compliance claim.

### Articles covered

- **Article 5 — lawful basis:** every processing purpose for S3 data must have a lawful basis recorded (consent / contract / legal obligation / legitimate interest). S3 actions require basis verification before execution.
- **Article 13 — notice and transparency:** a privacy notice at data collection where the basis is consent.
- **Article 14 — consent:** consent capture and a receipt where the basis is consent.
- **Article 18 — data subject rights:** access, correction, deletion, and portability.
- **Article 21 — retention:** defined retention periods per data class and deletion thereafter.

### Current status (view from the register)

| Control | Status | Phase |
|---|---|---|
| Data inventory | Planned | Phase 0 |
| Lawful basis register | Planned | Phase 0 |
| Retention schedule | Partial | Phase 1 |
| Breach response | Planned | Phase 1 |
| Consent and notice | Partial | — |
| Data subject rights | Planned | Phase 1 |
| Cross-border transfers | Partial | — |

### Controls implemented in code

- Sensitivity classification S0–S3 in `dealix/classifications/__init__.py`.
- Data subject request handling in `auto_client_acquisition/compliance_os/data_subject_requests.py`.
- Consent ledger `auto_client_acquisition/compliance_os/consent_ledger.py`.
- Records of processing activities `auto_client_acquisition/compliance_os/ropa.py`.
- Prevention of personal data in logs via the `no_pii_in_logs` rule.
- S3 data is not sent to external model providers before a Data Processing Agreement is in place.

### Known gaps

- Consent receipt emission is not yet implemented.
- Retention is not yet automatically enforced in the database; it needs a migration and a scheduled job.
- The formal cross-border transfer assessment per Article 29 is pending.

### Readiness checklist

- [x] Sensitivity classification is implemented and governs the action path.
- [x] Data subject request handling has a code path and an approval path.
- [x] The no-personal-data-in-logs rule is active.
- [ ] Retention schedule enforced automatically (planned).
- [ ] Consent receipt (planned).
- [ ] Formal cross-border transfer assessment (planned).

### Metrics

- Share of S3 processing purposes with a recorded lawful basis: target 100%.
- Response time for a data subject request.
- Count of controls in "implemented" vs "planned" status in the register.

### Governance and rollback

- The posture is reviewed quarterly and after any incident or regulatory update.
- No compliance claims are issued beyond what the register confirms.
- A named Data Protection Officer is appointed before the first production customer with S3 data.

See also: `governance/compliance/data_deletion.md`, `governance/policies/data_handling_policy.md`, `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.
