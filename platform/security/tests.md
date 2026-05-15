# العربية

## مواصفة الاختبار — الطبقة الأولى (الأمن)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات اختبار الأمن ومعايير قبولها. مواصفة مكتوبة بلا كود.

### حالات الاختبار

#### SEC-T1 — الأسرار خارج الكود

- خطوات: فحص المستودع والكود عبر `.github/workflows/codeql.yml`.
- القبول: لا يظهر أي سرّ إنتاجي في الكود؛ كل الأسرار في متغيرات بيئة.

#### SEC-T2 — التشفير أثناء النقل

- خطوات: محاولة اتصال بموجّه API عبر قناة غير مشفّرة.
- القبول: يُرفض الاتصال غير المشفّر.

#### SEC-T3 — تجزئة كلمة المرور

- خطوات: فحص تخزين كلمة المرور بعد إنشاء مستخدم.
- القبول: كلمة المرور مُجزَّأة، لا تظهر نصًّا.

#### SEC-T4 — عدم تسرّب السرّ في السجلات

- خطوات: تنفيذ إجراءات تستخدم أسرارًا وفحص السجلات.
- القبول: لا يظهر أي سرّ أو معرّف شخصي (قاعدة `no_pii_in_logs`).

#### SEC-T5 — حماية SSRF

- خطوات: محاولة دفع المنصة لطلب وجهة داخلية غير مصرّح بها.
- القبول: يُحجب الطلب عبر `api/security/ssrf_guard.py`.

#### SEC-T6 — محدّد معدّل الطلبات

- خطوات: تكرار الطلبات فوق العتبة على مسار محمي.
- القبول: تُحجب الطلبات الزائدة عبر `api/security/rate_limit.py`.

#### SEC-T7 — رفض الوصول غير المصرّح به

- خطوات: استدعاء مسار محمي بلا رمز أو برمز غير صالح.
- القبول: يُرفض الطلب ويُكتب قيد تدقيق رفض.

#### SEC-T8 — تدوير سرّ عند اشتباه تسرّب

- خطوات: محاكاة اشتباه تسرّب سرّ وتطبيق إجراء التدوير.
- القبول: يُبطَل السرّ القديم خلال أقل من ساعة ويُسجَّل الحادث.

#### SEC-T9 — مسار الاستجابة للحادث

- خطوات: محاكاة حادث حرج وتتبّع دورة الاستجابة.
- القبول: تكتمل مراحل الاكتشاف والاحتواء والتقييم والتسجيل وفق `incident_response.md`.

### معايير القبول الشاملة

- جميع حالات SEC-T1 إلى SEC-T9 ناجحة قبل النشر للإنتاج.
- التكامل المستمر يحجب الدمج عند فشل أي حالة.

### الروابط ذات الصلة

- `platform/security/readiness.md`
- `platform/security/incident_response.md`
- `platform/foundation/tests.md`

# English

## Test Specification — Layer 1 (Security)

Owner: Platform Lead

### Purpose

This specification defines security test cases and their acceptance criteria. It is a written spec with no code.

### Test cases

#### SEC-T1 — Secrets out of code

- Steps: scan the repository and code via `.github/workflows/codeql.yml`.
- Acceptance: no production secret appears in code; all secrets are in environment variables.

#### SEC-T2 — Encryption in transit

- Steps: attempt to connect to an API router over an unencrypted channel.
- Acceptance: the unencrypted connection is rejected.

#### SEC-T3 — Password hashing

- Steps: inspect password storage after creating a user.
- Acceptance: the password is hashed, never appears as plaintext.

#### SEC-T4 — No secret leak in logs

- Steps: run actions that use secrets and inspect logs.
- Acceptance: no secret or personal identifier appears (`no_pii_in_logs` rule).

#### SEC-T5 — SSRF protection

- Steps: attempt to push the platform to request an unauthorized internal destination.
- Acceptance: the request is blocked via `api/security/ssrf_guard.py`.

#### SEC-T6 — Request rate limit

- Steps: repeat requests above the threshold on a protected path.
- Acceptance: excess requests are blocked via `api/security/rate_limit.py`.

#### SEC-T7 — Unauthorized access denial

- Steps: call a protected path with no token or an invalid token.
- Acceptance: the request is rejected and a denial audit entry is written.

#### SEC-T8 — Secret rotation on suspected leak

- Steps: simulate a suspected secret leak and apply the rotation procedure.
- Acceptance: the old secret is revoked in under one hour and the incident is recorded.

#### SEC-T9 — Incident response path

- Steps: simulate a critical incident and follow the response cycle.
- Acceptance: detection, containment, assessment, and recording stages complete per `incident_response.md`.

### Overall acceptance criteria

- All cases SEC-T1 through SEC-T9 pass before a production deploy.
- CI blocks merge on any failing case.

### Related docs

- `platform/security/readiness.md`
- `platform/security/incident_response.md`
- `platform/foundation/tests.md`
