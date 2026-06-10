# خطة استجابة فشل Railway — Dealix

هذه الخطة تختصر التعامل مع تنبيهات `Build failed` و `Deploy failed` حتى لا يتحول الفشل إلى تعطيل للنظام.

## 1) تحديد الخدمة المتأثرة

- خدمة API: تستخدم جذر الريبو، وتبني من `Dockerfile` في الجذر، وتتحقق من `/healthz`.
- خدمة `frontend`: تستخدم Root Directory = `frontend`، وتبني من `frontend/Dockerfile`، وتتحقق من `/healthz`.
- خدمة `apps/web`: تستخدم Root Directory = `apps/web`، وتبني من `apps/web/Dockerfile`، وتتحقق من `/healthz`.
- أي خدمة باسم `web` أو `cv` يجب ربطها بمسارها الحقيقي فقط. لا تربط خدمة واجهة بجذر الريبو إلا إذا كانت مقصودة كـ API.

## 2) إعدادات Railway الموصى بها

### API service

- Root Directory: فارغ / repo root
- Builder: Dockerfile
- Dockerfile path: `Dockerfile`
- Healthcheck path: `/healthz`
- Start command: اتركه فارغًا ليستخدم `CMD` من Dockerfile
- متغيرات إلزامية في الإنتاج:
  - `APP_ENV=production`
  - `APP_SECRET_KEY`
  - `JWT_SECRET_KEY`
  - `API_KEYS`
  - `ADMIN_API_KEYS`
  - `DATABASE_URL` عند استخدام Postgres

### Frontend service

- Root Directory: `frontend`
- Builder: Dockerfile
- Dockerfile path: `Dockerfile`
- Healthcheck path: `/healthz`
- Start command: اتركه فارغًا
- متغيرات عامة آمنة فقط:
  - `NEXT_PUBLIC_API_URL=https://api.dealix.me`
  - `NEXT_PUBLIC_SITE_URL=https://dealix.me`
  - `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1`

### Apps web service

- Root Directory: `apps/web`
- Builder: Dockerfile
- Dockerfile path: `Dockerfile`
- Healthcheck path: `/healthz`
- Start command: اتركه فارغًا
- متغيرات عامة آمنة فقط:
  - `NEXT_PUBLIC_API_URL=https://api.dealix.me`
  - `NEXT_PUBLIC_SITE_URL=https://dealix.me`

لا تضع مفاتيح Admin داخل متغيرات `NEXT_PUBLIC_*` لأنها تصبح جزءًا من حزمة المتصفح.

## 3) فحوصات بعد الإصلاح

API:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
```

Frontend أو apps/web:

```bash
curl -fsS https://dealix.me/healthz
```

فحص محلي سريع:

```bash
python scripts/verify_railway_surfaces.py
cd frontend && npm ci && npm run build
cd ../apps/web && npm ci && npm run build
```

فحص Docker محلي:

```bash
docker build -t dealix-api .
docker build -t dealix-frontend frontend
docker build -t dealix-apps-web apps/web
```

## 4) عند استمرار الفشل

انسخ أول خطأ حقيقي من Railway build logs، وليس عنوان الإيميل فقط. غالبًا يكون السبب واحدًا من:

- Root Directory غير صحيح.
- Railway يستخدم خدمة `apps/web` بينما Root Directory مضبوط على `frontend`، أو العكس.
- عدم وجود `output: 'standalone'` في Next.js مع Dockerfile يعتمد على `.next/standalone`.
- preDeploy migration من API يعمل داخل image واجهة.
- متغير إنتاج إلزامي مفقود يجعل API يفشل عند startup.
- Healthcheck مضبوط على مسار غير موجود.

## 5) سياسة حماية الإنتاج

- لا يتم تجاوز فشل الأسرار في الإنتاج. أصلح المتغيرات بدل تعطيل التحقق.
- شغّل migrations فقط عندما تكون قاعدة البيانات جاهزة: `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1`.
- أبقِ healthcheck سريعًا على `/healthz`، واستخدم الفحص العميق يدويًا بعد النشر.
- أي تعديل Deployment جديد يجب أن يمر عبر `scripts/verify_railway_surfaces.py` و Docker build في CI.
