# مصفوفة الضوابط — نموذج تشغيل القدرات

**الطبقة:** L2 · نموذج تشغيل القدرات
**المالك:** المؤسس / قائد الحوكمة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [CONTROLS_MATRIX.md](./CONTROLS_MATRIX.md)

## السياق
مشترو المؤسسات لا يشترون وعودًا؛ يشترون ضوابط. مصفوفة الضوابط هي
الصفحة الواحدة التي تربط كل ضابط من ضوابط Dealix بمن يحتاجه وأين
يُنفَّذ. هي إجابة Dealix لفِرَق المشتريات وأمن المعلومات والامتثال.
يرجع لها `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` و
`docs/DPA_DEALIX_FULL.md` و
`docs/legal/COMPLIANCE_CERTIFICATIONS.md`.

## المصفوفة

| Control | Description | Required For |
|---|---|---|
| RBAC | Role-based access control inside the platform | enterprise |
| SSO | Single sign-on integration | enterprise |
| Audit exports | Export of audit logs to client systems | enterprise |
| Data retention | Retention rules per dataset | sensitive clients |
| Approval workflows | Action approval routing | all |
| PII redaction | Detection and redaction of personal data | all |
| Model run logs | Traceability for every AI run | all |
| Eval reports | Quality evaluation results per service | production AI |
| Incident response | AI failures, PII exposure, mis-actions | enterprise |

## ملاحظات لكل ضابط
- **RBAC.** متوافق مع مطابقة الصلاحيات في
  `docs/governance/PERMISSION_MIRRORING.md`؛ كل طلب مربوط بـ ACL
  المستخدم.
- **SSO.** مطلوب للمؤسسات؛ يدعم مزودي SAML/OIDC الأكثر شيوعًا في
  مؤسسات السعودية.
- **Audit exports.** تصديرات إضافية فقط ومُوقَّعة؛ هيكلها من
  `docs/product/MANAGEMENT_API_SPEC.md`.
- **Data retention.** الجدول في `docs/DATA_RETENTION_POLICY.md` وجدول
  PDPL في `docs/ops/PDPL_RETENTION_POLICY.md`.
- **Approval workflows.** جزء من تصنيف الإجراءات في
  `docs/governance/AI_ACTION_TAXONOMY.md`.
- **PII redaction.** تُطبَّق على بوابة LLM؛ تُسجَّل مع إصدار سياسة
  الحجب.
- **Model run logs.** تُحفظ وفق `docs/ledgers/AI_RUN_LEDGER.md`.
- **Eval reports.** من `docs/product/EVALUATION_REGISTRY.md`.
- **Incident response.** راجع `docs/governance/INCIDENT_RESPONSE.md`.

## تعريف جاهزية المؤسسات
يصبح العميل "جاهز مؤسسات" داخل Dealix عندما:

- تُصدَّر سجلات التدقيق على الجدول.
- يُمكَّن RBAC و SSO لتلك المساحة.
- توقَّع وتُطبَّق سياسة احتفاظ.
- يُسمَّى ويُختَبر إجراء دعم وحوادث.
- تُوقَّع هذه المصفوفة.
- يكون runbook الاستجابة جاهزًا ومقبولًا.

بدون ذلك، تُعامَل المساحة كـ"شريحة نمو" ولا تُمكَّن إجراءات L5
خارجيًا.

## الاستخدام في البيع والتسليم
- **البيع:** المصفوفة ملحق كل عرض مؤسسات.
- **التسليم:** RACI كل مشروع مؤسسي يشير للمصفوفة لتخصيص ملكية الضوابط.
- **التدقيق:** المصفوفة فهرس لتحديد نطاق التدقيقات الخارجية.

## الواجهات
| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| أسئلة مشتريات المؤسسات | إجابات ضوابط معبَّأة وروابط أدلة | قائد الحوكمة | لكل صفقة |
| حالة تنفيذ الضوابط | أدلة لكل ضابط (سجلات، إعدادات) | قائد المنصة | مستمر |
| نتائج التدقيق | تحديثات المصفوفة | قائد الحوكمة | لكل تدقيق |

## المقاييس
- **تغطية الضوابط** — نسبة الضوابط "Required For: all" المُمكَّنة في
  الإنتاج (الهدف = 100%).
- **حداثة الأدلة** — نسبة الضوابط ذات الأدلة المحدَّثة خلال 90 يومًا
  (الهدف ≥ 95%).
- **تغطية المؤسسات** — نسبة المساحات المؤسسية بكل ضوابط المؤسسات
  مُمكَّنة (الهدف = 100%).
- **إغلاق نتائج التدقيق** — نسبة النتائج المغلقة في SLA المتفق
  (الهدف ≥ 90%).

## ذات صلة
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — حزمة الثقة المرتبطة.
- `docs/DPA_DEALIX_FULL.md` — اتفاقية معالجة البيانات.
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — سجل الشهادات.
- `docs/governance/INCIDENT_RESPONSE.md` — الملف الشقيق للحوادث.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
