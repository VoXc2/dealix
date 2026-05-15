# العربية

## النسخ الاحتياطي والاسترجاع — الطبقة الأولى (النشر)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف تُنسَخ بيانات Dealix احتياطيًا وتُسترجَع، بحيث يمكن التعافي من فقدان البيانات دون أثر على عزل المستأجرين.

### النسخ الاحتياطي

- لقطات يومية آلية عبر `.github/workflows/daily_snapshot.yml`.
- تشمل اللقطة: قاعدة البيانات، حالة الهجرات، الملفات.
- النسخ الاحتياطية مشفّرة في مكان التخزين (`platform/security/encryption.md`).

### أهداف التعافي

| المؤشر | الهدف |
|---|---|
| نقطة الاسترجاع المستهدفة (RPO) | 24 ساعة |
| زمن الاسترجاع المستهدف (RTO) | 60 دقيقة |

### إجراء الاسترجاع

1. تحديد اللقطة المستهدفة من سجل اللقطات اليومية.
2. استرجاع اللقطة إلى بيئة معزولة أولًا، لا مباشرة للإنتاج.
3. التحقق من اكتمال البيانات وسلامة حدود `tenant_id`.
4. عند الاسترجاع الجزئي (مستأجر واحد): استخراج بيانات `tenant_id` المستهدف فقط.
5. إعادة الربط بالإنتاج بعد التحقق.
6. تسجيل الاسترجاع كقيد تدقيق عبر `dealix/trust/audit.py`.

### قواعد الحوكمة

- استرجاع بيانات إنتاج إجراء بتصنيف A2 على الأقل ويُسجَّل.
- لا استرجاع يكتب فوق بيانات مستأجرين سليمين دون موافقة.
- النسخ الاحتياطية تخضع لنفس ضوابط التشفير والوصول كبيانات الإنتاج.

### المقاييس

- نسبة نجاح اللقطة اليومية: هدف 100%.
- زمن الاسترجاع الفعلي مقابل RTO.
- عمر آخر لقطة صالحة مقابل RPO.
- عدد تمارين الاسترجاع الموثَّقة ربع سنويًا.

### المراقبة

- تنبيه على فشل لقطة يومية عبر `.github/workflows/daily_snapshot.yml`.
- قيد تدقيق لكل عملية استرجاع.

### إجراء التراجع

1. إن أفسد استرجاع حالة الإنتاج: العودة لآخر حالة سليمة من لقطة أحدث.
2. التحقق من عزل المستأجرين وفحص الصحة.
3. تسجيل الحادث كقيد تدقيق وإبلاغ قائد المنصة.

### درجة الجاهزية الحالية

تُقاس ضمن مجمل جاهزية النشر في `platform/deployment/readiness.md`. تمرين الاسترجاع الموثَّق ربع سنويًا فجوة جاهزية معروفة.

### الروابط ذات الصلة

- `platform/deployment/rollback_plan.md`
- `platform/multi_tenant/tenant_deletion.md`
- `platform/foundation/readiness.md`

# English

## Backup and Restore — Layer 1 (Deployment)

Owner: Platform Lead

### Purpose

This document describes how Dealix data is backed up and restored, so that data loss can be recovered with no impact on tenant isolation.

### Backup

- Automated daily snapshots via `.github/workflows/daily_snapshot.yml`.
- A snapshot covers: the database, migration state, and files.
- Backups are encrypted in their storage location (`platform/security/encryption.md`).

### Recovery objectives

| Objective | Target |
|---|---|
| Recovery Point Objective (RPO) | 24 hours |
| Recovery Time Objective (RTO) | 60 minutes |

### Restore procedure

1. Identify the target snapshot from the daily snapshot log.
2. Restore the snapshot into an isolated environment first, not directly to production.
3. Verify data completeness and the integrity of `tenant_id` boundaries.
4. For a partial restore (single tenant): extract only the target `tenant_id` data.
5. Re-link to production after verification.
6. Record the restore as an audit entry via `dealix/trust/audit.py`.

### Governance rules

- Restoring production data is an A2-class action at minimum and is recorded.
- No restore overwrites intact tenants' data without an approval.
- Backups are subject to the same encryption and access controls as production data.

### Metrics

- Daily snapshot success rate: target 100%.
- Actual restore time versus RTO.
- Age of the last valid snapshot versus RPO.
- Count of documented quarterly restore drills.

### Observability

- Alert on a failed daily snapshot via `.github/workflows/daily_snapshot.yml`.
- An audit entry for every restore operation.

### Rollback procedure

1. If a restore corrupts the production state: return to the last intact state from a newer snapshot.
2. Verify tenant isolation and the healthcheck.
3. Record the incident as an audit entry and notify the Platform Lead.

### Current readiness score

Measured within the overall deployment readiness in `platform/deployment/readiness.md`. A documented quarterly restore drill is a known readiness gap.

### Related docs

- `platform/deployment/rollback_plan.md`
- `platform/multi_tenant/tenant_deletion.md`
- `platform/foundation/readiness.md`
