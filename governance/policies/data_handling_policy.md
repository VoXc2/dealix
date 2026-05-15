# العربية

**Owner:** قائد الخصوصية والثقة (Privacy & Trust Plane Lead).

## سياسة معالجة البيانات

تحدّد هذه السياسة كيف تُصنَّف بيانات Dealix وتُخزَّن وتُستخدم وتُحذَف، بما يتوافق مع نظام حماية البيانات الشخصية السعودي (PDPL).

**الإصدار:** 1.0 — **تاريخ السريان:** 2026-05-15 — **المراجعة التالية:** 2026-08-15.

### تصنيف البيانات

تُصنَّف كل بيانات حسب محور الحساسية في `dealix/classifications/__init__.py`:

- **S0 — عام:** بيانات غير سرّية يجوز نشرها.
- **S1 — داخلي:** بيانات تشغيلية داخلية.
- **S2 — سرّي:** بيانات تجارية حساسة (عروض، أسعار، خطط).
- **S3 — بيانات شخصية:** بيانات تخضع لـ PDPL، تستوجب أساساً نظامياً.

### الأساس النظامي

كل غرض معالجة لبيانات S3 يجب أن يُسجَّل له أساس نظامي في سجل الأسس بـ `dealix/registers/compliance_saudi.yaml`: موافقة، أو عقد، أو التزام نظامي، أو مصلحة مشروعة. لا معالجة لبيانات S3 بلا أساس مُسجَّل، ولا استخدام ثانوي دون إعادة تبرير.

### قواعد المعالجة

- بيانات S2/S3 لا تُكتب في السجلات؛ تُستخدم معرّفات مستعارة (قاعدة `no_pii_in_logs`).
- بيانات S3 لا تُرسَل لمزوّدي نماذج اللغة الخارجيين قبل وجود اتفاقية معالجة بيانات (DPA) ووضوح إقامة البيانات، وفق `compliance_saudi.yaml`.
- نقل البيانات عبر الحدود يخضع لتقييم وفق PDPL المادة 29.
- كل وصول لبيانات S2/S3 يُسجَّل كقيد تدقيق.

### الاحتفاظ والحذف

تُطبَّق فترات احتفاظ لكل صنف بيانات وفق الجدول في `compliance_saudi.yaml`:

| صنف البيانات | مدة الاحتفاظ |
|---|---|
| فرص S1 غير نشطة | 24 شهراً |
| فرص S2 مستبعَدة | 12 شهراً |
| بيانات شخصية S3 | حسب الغرض والأساس النظامي |
| عروض S2 | 7 سنوات (سجل تجاري) |
| قيود التدقيق | 7 سنوات |

تفاصيل الحذف في `governance/compliance/data_deletion.md`.

### حقوق صاحب البيانات

يُعالج طلب الوصول والتصحيح والحذف ونقل البيانات عبر `auto_client_acquisition/compliance_os/data_subject_requests.py` ووفق `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.

### الحوكمة

- إجراء يمسّ S3 يُصنَّف عالي المخاطر ويمر عبر الموافقة.
- تصدير بيانات S3 يتطلب موافقة A3 مزدوجة.
- مراجعة السياسة ربع سنوية وبعد أي حادث جوهري.

انظر أيضاً: `governance/compliance/pdpl_readiness.md`، `governance/compliance/data_deletion.md`.

---

# English

**Owner:** Privacy & Trust Plane Lead.

## Data Handling Policy

This policy defines how Dealix data is classified, stored, used, and deleted, in line with the Saudi Personal Data Protection Law (PDPL).

**Version:** 1.0 — **Effective:** 2026-05-15 — **Next review:** 2026-08-15.

### Data classification

All data is classified by the sensitivity axis in `dealix/classifications/__init__.py`:

- **S0 — public:** non-confidential data that may be published.
- **S1 — internal:** internal operational data.
- **S2 — confidential:** sensitive commercial data (proposals, prices, plans).
- **S3 — personal data:** data subject to PDPL, requiring a lawful basis.

### Lawful basis

Every processing purpose for S3 data must have a lawful basis recorded in the lawful-basis register in `dealix/registers/compliance_saudi.yaml`: consent, contract, legal obligation, or legitimate interest. There is no S3 processing without a recorded basis, and no secondary use without re-justification.

### Processing rules

- S2/S3 data is not written to logs; pseudonymous identifiers are used (`no_pii_in_logs` rule).
- S3 data is not sent to external LLM providers before a Data Processing Agreement (DPA) is in place and data residency is clear, per `compliance_saudi.yaml`.
- Cross-border transfers are subject to an assessment per PDPL Article 29.
- Every access to S2/S3 data is recorded as an audit entry.

### Retention and deletion

Retention periods are applied per data class per the schedule in `compliance_saudi.yaml`:

| Data class | Retention |
|---|---|
| S1 inactive leads | 24 months |
| S2 disqualified leads | 12 months |
| S3 personal data | per purpose and lawful basis |
| S2 proposals | 7 years (commercial record) |
| Audit entries | 7 years |

Deletion details are in `governance/compliance/data_deletion.md`.

### Data subject rights

Access, correction, deletion, and portability requests are handled via `auto_client_acquisition/compliance_os/data_subject_requests.py` and per `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.

### Governance

- An action touching S3 is classified high-risk and passes through approval.
- Exporting S3 data requires dual A3 approval.
- The policy is reviewed quarterly and after any material incident.

See also: `governance/compliance/pdpl_readiness.md`, `governance/compliance/data_deletion.md`.
