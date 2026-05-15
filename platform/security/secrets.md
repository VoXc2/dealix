# العربية

## الأسرار — الطبقة الأولى (الأمن)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف تُخزَّن أسرار Dealix وتُستخدم وتُدوَّر، بحيث لا يتسرّب أي مفتاح أو كلمة مرور إنتاجية.

### أنواع الأسرار

- مفاتيح وصول قاعدة البيانات.
- مفاتيح توقيع JWT (`api/security/jwt.py`).
- مفاتيح API للخدمات (`api/security/api_key.py`).
- أسرار توقيع الويب هوك (`api/security/webhook_signatures.py`).
- مفاتيح مزوّدي الخدمات الخارجيين.

### مبدأ التخزين

- كل الأسرار في متغيرات بيئة، لا في الكود ولا في المستودع.
- فصل تام بين أسرار بيئات التطوير والتجهيز والإنتاج.
- لا سرّ مشترك بين البيئات.

### التدوير

| الحدث | الإجراء |
|---|---|
| تدوير دوري | استبدال الأسرار وفق جدول محدّد |
| اشتباه تسرّب | تدوير فوري وإبطال السرّ القديم |
| مغادرة عضو فريق | تدوير الأسرار التي كان يصل إليها |

### قواعد الحوكمة

- لا يُكتب أي سرّ في السجلات (قاعدة `no_pii_in_logs`).
- فحص الكود الثابت عبر `.github/workflows/codeql.yml` يكشف الأسرار المُسرَّبة في الكود.
- الوصول لأسرار الإنتاج مقصور على أدوار محدّدة ويُسجَّل.
- إضافة أو تغيير سرّ إنتاجي إجراء بتصنيف A2 على الأقل.

### المقاييس

- عدد الأسرار المُسرَّبة في الكود المكتشَفة: هدف صفر.
- نسبة الأسرار المُدوَّرة ضمن الجدول.
- زمن التدوير عند اشتباه تسرّب: أقل من ساعة.

### المراقبة

- تنبيه على أي اكتشاف لسرّ في الكود أو السجلات.
- قيد تدقيق لكل إضافة أو تغيير سرّ إنتاجي.

### إجراء التراجع

1. عند تسرّب سرّ: تدوير فوري وإبطال السرّ القديم.
2. مراجعة قيود التدقيق لتحديد نطاق الوصول بالسرّ المُسرَّب.
3. إن لزم: تطبيق التراجع وفق `platform/foundation/rollback.md`.
4. تسجيل الحادث وفق `docs/SECURITY_RUNBOOK.md`.

### الروابط ذات الصلة

- `platform/security/encryption.md`
- `platform/security/access_control.md`
- `docs/SECURITY_RUNBOOK.md`

# English

## Secrets — Layer 1 (Security)

Owner: Platform Lead

### Purpose

This document describes how Dealix secrets are stored, used, and rotated, so that no production key or password leaks.

### Secret types

- Database access credentials.
- JWT signing keys (`api/security/jwt.py`).
- Service API keys (`api/security/api_key.py`).
- Webhook signing secrets (`api/security/webhook_signatures.py`).
- External provider keys.

### Storage principle

- All secrets live in environment variables, not in code or the repository.
- Full separation between dev, staging, and production secrets.
- No secret shared across environments.

### Rotation

| Event | Action |
|---|---|
| Periodic rotation | Replace secrets on a defined schedule |
| Suspected leak | Immediate rotation and revocation of the old secret |
| Team member departure | Rotate the secrets they had access to |

### Governance rules

- No secret is written to logs (`no_pii_in_logs` rule).
- Static code scanning via `.github/workflows/codeql.yml` detects secrets leaked in code.
- Access to production secrets is restricted to specific roles and logged.
- Adding or changing a production secret is an A2-class action at minimum.

### Metrics

- Count of secrets detected leaked in code: target zero.
- Ratio of secrets rotated on schedule.
- Rotation time on suspected leak: under one hour.

### Observability

- Alert on any detection of a secret in code or logs.
- An audit entry for every production secret addition or change.

### Rollback procedure

1. On a leaked secret: immediate rotation and revocation of the old secret.
2. Review audit entries to determine the access scope of the leaked secret.
3. If needed: apply rollback per `platform/foundation/rollback.md`.
4. Record the incident per `docs/SECURITY_RUNBOOK.md`.

### Related docs

- `platform/security/encryption.md`
- `platform/security/access_control.md`
- `docs/SECURITY_RUNBOOK.md`
