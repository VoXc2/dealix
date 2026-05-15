# العربية

## التشفير — الطبقة الأولى (الأمن)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف تُشفَّر بيانات Dealix أثناء النقل والتخزين، بحيث تظل بيانات كل مستأجر محمية حتى عند الوصول غير المصرّح به للوسائط.

### التشفير أثناء النقل

- كل اتصال بموجّهات API الـ117 عبر قناة مشفّرة (TLS).
- استدعاءات مزوّدي الخدمات الخارجيين عبر قنوات مشفّرة فقط.
- توقيع الويب هوك للتحقق من السلامة عبر `api/security/webhook_signatures.py`.

### التشفير أثناء التخزين

- قاعدة البيانات: تشفير على مستوى التخزين لدى مزوّد قاعدة البيانات (`supabase/`).
- النسخ الاحتياطية واللقطات: مشفّرة في مكان التخزين.
- الملفات والمرفقات: مشفّرة على مستوى تخزين الكائنات.

### كلمات المرور والرموز

- كلمات المرور مُجزَّأة بخوارزمية تجزئة قوية، لا تُخزَّن نصًّا.
- رموز JWT موقَّعة عبر `api/security/jwt.py`.

### قواعد الحوكمة

- لا تُنقل بيانات أعمال عبر قناة غير مشفّرة.
- البيانات الحساسة المصنَّفة S2/S3 (`dealix/classifications/__init__.py`) تخضع لأعلى ضوابط التشفير.
- مفاتيح التشفير تُدار كأسرار وفق `platform/security/secrets.md`.

### المقاييس

- نسبة الاتصالات المشفّرة: 100%.
- نسبة النسخ الاحتياطية المشفّرة: 100%.
- عدد البيانات المخزَّنة غير المشفّرة المكتشَفة: هدف صفر.

### المراقبة

- تنبيه على أي اتصال يحاول قناة غير مشفّرة.
- قيد تدقيق لتغييرات إعدادات التشفير.

### إجراء التراجع

1. عند خلل في إعداد التشفير: التراجع لآخر إعداد آمن معروف وفق `platform/foundation/rollback.md`.
2. عند اشتباه كشف بيانات: تطبيق `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
3. تدوير المفاتيح المتأثرة وتسجيل الحادث كقيد تدقيق.

### الروابط ذات الصلة

- `platform/security/secrets.md`
- `platform/multi_tenant/data_boundaries.md`
- `docs/SECURITY_RUNBOOK.md`

# English

## Encryption — Layer 1 (Security)

Owner: Platform Lead

### Purpose

This document describes how Dealix data is encrypted in transit and at rest, so that each tenant's data stays protected even on unauthorized access to the media.

### Encryption in transit

- Every connection to the 117 API routers over an encrypted channel (TLS).
- External provider calls over encrypted channels only.
- Webhook signing for integrity verification via `api/security/webhook_signatures.py`.

### Encryption at rest

- Database: storage-level encryption at the database provider (`supabase/`).
- Backups and snapshots: encrypted in their storage location.
- Files and attachments: encrypted at the object-storage level.

### Passwords and tokens

- Passwords hashed with a strong hashing algorithm, never stored as plaintext.
- JWT tokens signed via `api/security/jwt.py`.

### Governance rules

- No business data is transmitted over an unencrypted channel.
- Sensitive data classified S2/S3 (`dealix/classifications/__init__.py`) is subject to the strictest encryption controls.
- Encryption keys are managed as secrets per `platform/security/secrets.md`.

### Metrics

- Ratio of encrypted connections: 100%.
- Ratio of encrypted backups: 100%.
- Count of unencrypted stored data detected: target zero.

### Observability

- Alert on any connection attempting an unencrypted channel.
- An audit entry for encryption-configuration changes.

### Rollback procedure

1. On an encryption-configuration fault: revert to the last known-good setting per `platform/foundation/rollback.md`.
2. On suspected data exposure: apply `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
3. Rotate affected keys and record the incident as an audit entry.

### Related docs

- `platform/security/secrets.md`
- `platform/multi_tenant/data_boundaries.md`
- `docs/SECURITY_RUNBOOK.md`
