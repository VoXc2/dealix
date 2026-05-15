# العربية

## الاستجابة للحوادث — الطبقة الأولى (الأمن)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه الوثيقة كيف تكتشف Dealix الحوادث الأمنية وتستجيب لها وتتعافى منها، مع الالتزام بمتطلبات الإبلاغ النظامية.

### تصنيف الحوادث

| المستوى | المثال |
|---|---|
| حرج | تسرّب بيانات بين المستأجرين، كشف سرّ إنتاجي |
| عالٍ | اشتباه سرقة رمز، وصول غير مصرّح به |
| متوسط | فجوة في تغطية قيود التدقيق، فشل فحص صحة متكرر |
| منخفض | محاولة وصول مرفوضة معزولة |

### دورة الاستجابة

1. الاكتشاف: عبر تنبيهات `dealix/observability/sentry.py`، فحوص `dealix/trust/audit.py`، وفحص الصحة.
2. الاحتواء: تجميد المسار أو الجلسة أو المفتاح المتأثر فورًا.
3. التقييم: تحديد نطاق التأثير من قيود التدقيق وتتبّعات `dealix/observability/otel.py`.
4. المعالجة: تطبيق التراجع وفق `platform/foundation/rollback.md` أو تدوير الأسرار.
5. الإبلاغ: عند مساس ببيانات شخصية تُطبَّق خطة `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
6. التعافي: استرجاع من نسخة احتياطية عند اللزوم، التحقق من سلامة عزل المستأجرين.
7. المراجعة: تحليل ما بعد الحادث وتحديث الضوابط.

### قواعد الحوكمة

- كل حادث يُسجَّل كقيد تدقيق غير قابل للتعديل.
- الحوادث الحرجة تُصعَّد فورًا لقائد المنصة.
- الإبلاغ عن خرق البيانات الشخصية يتبع نظام حماية البيانات الشخصية (المادتان 20/21) عبر `auto_client_acquisition/compliance_os/`.
- لا إخفاء حادث؛ الشفافية الداخلية إلزامية.

### المقاييس

- زمن الاكتشاف (من الحدث إلى التنبيه).
- زمن الاحتواء (من التنبيه إلى التجميد).
- زمن التعافي الكامل.
- عدد الحوادث المُبلَّغ عنها وفق المهلة النظامية.

### المراقبة

- تنبيهات مدمجة من Sentry وفحص الصحة وانحراف الأساس (`watchdog_drift.yml`).
- قيد تدقيق لكل مرحلة استجابة.

### إجراء التراجع

1. عكس أي تغيير طارئ غير ضروري بعد انتهاء الحادث.
2. استرجاع البيانات المتأثرة من آخر لقطة يومية ضمن نافذة RPO.
3. التحقق من فحص الصحة وعزل المستأجرين وتسجيل إغلاق الحادث.

### درجة الجاهزية الحالية

تُقاس ضمن مجمل جاهزية الأمن في `platform/security/readiness.md`.

### الروابط ذات الصلة

- `platform/security/readiness.md`
- `docs/SECURITY_RUNBOOK.md`
- `docs/PDPL_BREACH_RESPONSE_PLAN.md`

# English

## Incident Response — Layer 1 (Security)

Owner: Platform Lead

### Purpose

This document defines how Dealix detects, responds to, and recovers from security incidents, while meeting statutory reporting requirements.

### Incident classification

| Level | Example |
|---|---|
| Critical | Cross-tenant data leakage, production secret exposure |
| High | Suspected token theft, unauthorized access |
| Medium | Audit-coverage gap, repeated healthcheck failure |
| Low | An isolated rejected access attempt |

### Response cycle

1. Detection: via `dealix/observability/sentry.py` alerts, `dealix/trust/audit.py` checks, and the healthcheck.
2. Containment: immediately freeze the affected path, session, or key.
3. Assessment: determine the impact scope from audit entries and `dealix/observability/otel.py` traces.
4. Remediation: apply rollback per `platform/foundation/rollback.md` or rotate secrets.
5. Reporting: on impact to personal data, apply the `docs/PDPL_BREACH_RESPONSE_PLAN.md` plan.
6. Recovery: restore from a backup if needed, verify tenant-isolation integrity.
7. Review: post-incident analysis and control updates.

### Governance rules

- Every incident is recorded as an immutable audit entry.
- Critical incidents are escalated immediately to the Platform Lead.
- Personal-data breach reporting follows PDPL (Articles 20/21) via `auto_client_acquisition/compliance_os/`.
- No incident concealment; internal transparency is mandatory.

### Metrics

- Detection time (event to alert).
- Containment time (alert to freeze).
- Full recovery time.
- Count of incidents reported within the statutory window.

### Observability

- Combined alerts from Sentry, the healthcheck, and baseline drift (`watchdog_drift.yml`).
- An audit entry for every response stage.

### Rollback procedure

1. Reverse any unnecessary emergency change after the incident closes.
2. Restore affected data from the last daily snapshot within the RPO window.
3. Verify the healthcheck and tenant isolation, and record the incident closure.

### Current readiness score

Measured within the overall security readiness in `platform/security/readiness.md`.

### Related docs

- `platform/security/readiness.md`
- `docs/SECURITY_RUNBOOK.md`
- `docs/PDPL_BREACH_RESPONSE_PLAN.md`
