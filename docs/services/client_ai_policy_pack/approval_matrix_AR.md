# حزمة سياسة الذكاء الاصطناعي للعميل — مصفوفة الاعتمادات

**الطبقة:** L5 · الحوكمة المؤسسية
**المالك:** قائد الحوكمة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [approval_matrix.md](./approval_matrix.md)

## السياق
تحوّل مصفوفة الاعتمادات السياسة إلى قرارات تشغيلية: لأيّ إجراء، *مَن* يعتمد و*متى*. بدونها يصير الاعتماد افتراضيًا للأعلى رتبة، مما يخلق عنق زجاجة ومخاطرة. يوحّد هذا الملف المعتمِدين ويتسق مع `./policy_template.md` و`./employee_guide.md` و`./tool_usage_rules.md`، وكذلك مع `docs/DPA_DEALIX_FULL.md` و`docs/DATA_RETENTION_POLICY.md` و`docs/ops/PDPL_RETENTION_POLICY.md`.

## أدوار المعتمِدين
- **المدير** — المدير المباشر للطالب.
- **مراجع الحوكمة** — مالك الحوكمة لدى العميل (غالبًا الامتثال أو المخاطر أو COO).
- **مالك البيانات** — المالك المُسمّى لمجموعة البيانات.
- **الراعي التنفيذي** — راعٍ من C-Level لقرارات برنامج الذكاء الاصطناعي.

## المصفوفة الافتراضية
المصفوفة الافتراضية تربط صنف الإجراء (متسق مع `docs/governance/AI_ACTION_CONTROL.md`) بالمعتمِدين:

| Action Class | Description | Approver(s) | Audit Required |
|---|---|---|---|
| A | Internal insight, summary, classification | None (logged) | Yes |
| B | Client-facing draft / report | Manager + Governance Reviewer for new categories | Yes |
| C | Internal system change (CRM update, task create) | Manager | Yes |
| D | External communication (email, message, post) | Manager + Data Owner; Executive Sponsor for high-stakes channels | Yes |
| E | Autonomous external action | Blocked by default; Executive Sponsor + Governance Reviewer for any exception | Yes |

## طبقة فئة البيانات
كذلك تربط المصفوفة فئة البيانات بالمعتمِد المطلوب للوصول إليها:

| Dataset Class | Examples | Approver(s) |
|---|---|---|
| Public | Marketing site, public knowledge | None |
| Internal | Internal docs, non-sensitive analytics | Manager |
| Confidential | Customer data, deal data | Data Owner |
| Restricted | PII, regulated data, M&A, HR exits | Data Owner + Governance Reviewer |
| Special | Health, financial regulated, government | Data Owner + Governance Reviewer + Executive Sponsor |

عند تعدد الفئات، تحكم الأشد.

## كيف تُسجَّل الاعتمادات
- تُسجَّل بـ: اسم المعتمِد، الدور، صنف الإجراء، فئة البيانات، الطابع الزمني، النطاق، تاريخ الانتهاء.
- تُربط بأصل التشغيل (`docs/product/AI_RUN_PROVENANCE.md`).
- الاعتمادات الدائمة محدودة المدة وتُسجَّل مرة واحدة.

## التصعيد
- يُصعَّد الطلب الذي لم يُحسَم خلال SLA (افتراضي 48 ساعة عمل) إلى مدير المعتمِد.
- نمط التصعيد يحرّك مراجعة من الحوكمة للمصفوفة.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| صنف الإجراء + فئة البيانات | قائمة المعتمِدين | مراجع الحوكمة | لكل طلب |
| قرارات الاعتماد | رموز اعتماد مُسجَّلة | المعتمِدون | لكل طلب |
| التصعيدات | محفّز مراجعة المجلس | الحوكمة | حسب الحاجة |

## المقاييس
- Matrix Coverage — نسبة الإجراءات الخاضعة فعلًا للمصفوفة.
- Approval-Within-SLA Rate — نسبة الاعتمادات خلال 48 ساعة عمل.
- Standing-Approval Hygiene — نسبة الاعتمادات الدائمة ذات تاريخ انتهاء.
- Escalation Rate — تصعيدات لكل 100 طلب اعتماد.

## ذات صلة
- `docs/DPA_DEALIX_FULL.md` — اتفاقية معالجة البيانات
- `docs/DATA_RETENTION_POLICY.md` — قواعد الاحتفاظ
- `docs/ops/PDPL_RETENTION_POLICY.md` — توافق PDPL
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — سياق الشهادات
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
