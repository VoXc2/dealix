# Dealix — Founder A-to-Z Launch Runbook

هذا المستند هو مسار التشغيل النهائي من الصفر إلى إنتاج مستقر. الهدف: أي خدمة تفشل في Railway أو GitHub Actions يكون سببها واضحًا وقابلًا للإصلاح بدون تخمين.

## 0) قاعدة التشغيل

- لا تحفظ أسرار حقيقية داخل الريبو.
- لا تستخدم أي متغير يبدأ بـ `NEXT_PUBLIC_` لمفاتيح Admin أو API خاصة.
- API فقط هو الذي يشغل migrations/predeploy.
- الواجهات تستخدم `/healthz` فقط كفحص سريع.

## 1) خريطة الخدمات

| الخدمة | Root Directory | Dockerfile | Railway config | Healthcheck |
|---|---|---|---|---|
| API | `.` | `Dockerfile` | `railway.json` | `/healthz` |
| Frontend | `frontend` | `Dockerfile` | `frontend/railway.json` | `/healthz` |
| Apps web | `apps/web` | `Dockerfile` | `apps/web/railway.json` | `/healthz` |

المصدر الآلي لهذه الخريطة: `dealix/config/railway_services.json`.

## 2) إعداد متغيرات الإنتاج

### API

إلزامي:

```text
APP_ENV=production
APP_SECRET_KEY=<64-byte hex>
JWT_SECRET_KEY=<64-byte hex or strong secret>
API_KEYS=<comma-separated private keys>
ADMIN_API_KEYS=<comma-separated admin-only keys>
```

مهم عند الربط الفعلي:

```text
DATABASE_URL=<Railway Postgres URL>
REDIS_URL=<Railway Redis URL>
SENTRY_DSN=<Sentry DSN>
ANTHROPIC_API_KEY=<optional>
OPENAI_API_KEY=<optional>
GROQ_API_KEY=<optional>
GOOGLE_API_KEY=<optional>
```

### Frontend

```text
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1
DEALIX_OPS_PROXY_SECRET=<server-only if needed>
```

### Apps web

```text
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
```

## 3) قبل النشر

شغّل محليًا أو داخل Codespaces:

```bash
python scripts/founder_launch_final_check.py
python scripts/verify_railway_surfaces.py
```

للتأكد من Docker:

```bash
docker build -t dealix-api .
docker build -t dealix-frontend frontend
docker build -t dealix-apps-web apps/web
```

## 4) النشر على Railway

1. افتح كل خدمة.
2. تأكد من Root Directory حسب الجدول.
3. تأكد من Dockerfile path = `Dockerfile`.
4. تأكد من Healthcheck path = `/healthz`.
5. أعد النشر.
6. راقب أول build error حقيقي، وليس تنبيه البريد فقط.

## 5) بعد النشر

API:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
```

واجهة واحدة أو أكثر:

```bash
curl -fsS https://dealix.me/healthz
```

فحص موحد:

```bash
python scripts/founder_launch_final_check.py --live \
  --api-base https://api.dealix.me \
  --web-base https://dealix.me
```

أو من GitHub Actions شغّل `CI` يدويًا عبر `workflow_dispatch` وأدخل روابط الخدمات.

## 6) GitHub Actions المطلوبة

- CI
- Security
- Production Smoke

لا تعتبر الإطلاق مكتملًا إلا بعد مرور CI أو توثيق سبب الفشل كـ Issue واضح.

## 7) نظام الأعطال

| العرض | السبب المرجح | الإجراء |
|---|---|---|
| Build failed في frontend | Root Directory خطأ أو Dockerfile غير مستخدم | اضبط Root Directory = `frontend` |
| Build failed في apps/web | Root Directory خطأ | اضبط Root Directory = `apps/web` |
| Deploy failed بعد build | Healthcheck path غير موجود | استخدم `/healthz` |
| API يفشل startup | أسرار production ناقصة | راجع `APP_SECRET_KEY`, `JWT_SECRET_KEY`, `API_KEYS`, `ADMIN_API_KEYS` |
| preDeploy يفشل في واجهة | خدمة واجهة تستخدم config الجذر | استخدم `frontend/railway.json` أو `apps/web/railway.json` |
| deep health degraded | DB/Redis/LLM/Sentry ناقص أو غير متاح | افحص `/healthz?deep=1` وRailway variables |

## 8) معايير الإطلاق النهائي

- كل خدمة Railway deployed وhealthcheck أخضر.
- `/healthz` يعمل للـ API والواجهة.
- `/ready` يعمل للـ API.
- CI أخضر أو فشل موثق بسبب خارجي.
- لا يوجد Admin key داخل `NEXT_PUBLIC_*`.
- أسرار الإنتاج موجودة في Railway/GitHub Secrets فقط.
- DNS/TLS يعمل على الدومينات النهائية.

## 9) أمر المؤسس النهائي

```bash
python scripts/founder_launch_final_check.py --live
```

إذا طبع:

```text
FOUNDER_LAUNCH_FINAL_CHECK=ok
```

فحالة الإطلاق من جانب الريبو والأسطح العامة جاهزة.
