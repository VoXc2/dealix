# العربية

## البيئات — الطبقة الأولى (النشر)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة بيئات Dealix الثلاث وكيف تُفصَل، بحيث لا يؤثر تغيير في التطوير على الإنتاج ولا تتسرّب بيانات الإنتاج للتطوير.

### البيئات الثلاث

| البيئة | الغرض | البيانات |
|---|---|---|
| التطوير (dev) | بناء واختبار الميزات | بيانات تجريبية فقط، لا بيانات إنتاج |
| التجهيز (staging) | محاكاة الإنتاج قبل الإصدار | بيانات تجريبية ممثِّلة، اختبار دخان |
| الإنتاج (prod) | خدمة المستأجرين الحقيقيين | بيانات المستأجرين الحقيقية |

### مبدأ الفصل

- لكل بيئة أسرارها ومتغيرات بيئتها المنفصلة (`platform/security/secrets.md`).
- لا تشارك بيانات إنتاج مع التطوير أو التجهيز.
- ترقية الكود تتدرّج: تطوير ثم تجهيز ثم إنتاج.
- اختبار الدخان على التجهيز عبر `.github/workflows/staging-smoke.yml` قبل الإنتاج.

### قواعد الحوكمة

- لا نشر مباشر للإنتاج دون مرور بالتجهيز.
- النشر للإنتاج يتطلب نجاح التكامل المستمر `.github/workflows/ci.yml`.
- نشر الإنتاج إجراء بتصنيف A2 على الأقل ويُسجَّل.
- لا تُستخدم بيانات مستأجر حقيقية خارج بيئة الإنتاج.

### المقاييس

- عدد عمليات النشر للإنتاج التي مرّت بالتجهيز: 100%.
- زمن ترقية إصدار من التجهيز للإنتاج.
- عدد حوادث تسرّب بيانات إنتاج لبيئة أدنى: هدف صفر.

### المراقبة

- فحص صحة لكل بيئة عبر `.github/workflows/scheduled_healthcheck.yml`.
- قيد تدقيق لكل نشر مع البيئة والإصدار.
- اختبار دخان بعد كل نشر للتجهيز.

### إجراء التراجع

1. عند فشل نشر إنتاج: التراجع لآخر إصدار مستقر وفق `platform/deployment/rollback_plan.md`.
2. عند فشل اختبار الدخان على التجهيز: حجب الترقية للإنتاج.
3. تسجيل التراجع كقيد تدقيق وإبلاغ قائد المنصة.

### الروابط ذات الصلة

- `platform/deployment/ci_cd.md`
- `platform/deployment/rollback_plan.md`
- `platform/security/secrets.md`

# English

## Environments — Layer 1 (Deployment)

Owner: Platform Lead

### Purpose

This document describes the three Dealix environments and how they are separated, so that a change in dev does not affect prod and prod data does not leak into dev.

### The three environments

| Environment | Purpose | Data |
|---|---|---|
| Development (dev) | Build and test features | Test data only, no production data |
| Staging | Simulate production before release | Representative test data, smoke testing |
| Production (prod) | Serve real tenants | Real tenant data |

### Separation principle

- Each environment has its own separated secrets and environment variables (`platform/security/secrets.md`).
- Production data is never shared with dev or staging.
- Code promotion is staged: dev, then staging, then prod.
- Smoke testing on staging via `.github/workflows/staging-smoke.yml` before production.

### Governance rules

- No direct production deploy without passing through staging.
- A production deploy requires passing CI `.github/workflows/ci.yml`.
- A production deploy is an A2-class action at minimum and is recorded.
- Real tenant data is never used outside the production environment.

### Metrics

- Ratio of production deploys that passed through staging: 100%.
- Time to promote a release from staging to production.
- Count of production-data leaks to a lower environment: target zero.

### Observability

- A healthcheck per environment via `.github/workflows/scheduled_healthcheck.yml`.
- An audit entry for every deploy with the environment and release.
- A smoke test after every staging deploy.

### Rollback procedure

1. On a failed production deploy: roll back to the last stable release per `platform/deployment/rollback_plan.md`.
2. On a failed staging smoke test: block promotion to production.
3. Record the rollback as an audit entry and notify the Platform Lead.

### Related docs

- `platform/deployment/ci_cd.md`
- `platform/deployment/rollback_plan.md`
- `platform/security/secrets.md`
