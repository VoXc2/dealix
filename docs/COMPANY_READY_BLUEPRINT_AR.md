# خطة جاهزية Dealix لخدمة الشركات (Backend + Frontend + Operations + Workflow)

هذا المستند يحوّل النظام إلى تشغيل مؤسسي واضح: **جاهزية تقنية + جاهزية تشغيل + جاهزية تجربة عميل**.

## 1) الهدف التنفيذي

- تشغيل مستقر يومي لمنصّة Dealix للشركات.
- تقليل الأعطال عبر فحوصات جاهزية قبل وأثناء التشغيل.
- توحيد رحلة العميل من Lead إلى Delivery داخل Workflow قابل للقياس.

## 2) معايير القبول (Definition of Ready)

نعتبر البيئة "جاهزة للشركات" عند تحقق التالي:

1. الخدمات الأساسية تعمل (Postgres + Redis + API + Frontend).
2. فحوصات الـ Backend السريعة تنجح.
3. فحوصات Revenue OS الأساسية تنجح.
4. فحوصات Frontend (lint + typecheck + build) تنجح.
5. ملف البيئة `.env` مضبوط بما يلائم البيئة الحالية.
6. وجود مسار تشغيل يومي موثّق (Morning / Midday / EOD).

## 3) تدفق التشغيل القياسي

### A) تشغيل البنية التحتية

```bash
docker compose up -d postgres redis
```

### B) تشغيل الـ Backend

```bash
APP_ENV=development uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### C) تشغيل الـ Frontend

```bash
cd frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## 4) طبقة التحقق السريع (Quick Regression Gate)

- Backend quick tests:

```bash
pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py -q --no-cov
```

- Revenue OS hard verification:

```bash
bash scripts/revenue_os_master_verify.sh
```

- Frontend quality:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

## 5) Workflow موحّد من العميل إلى التنفيذ

1. **Lead Intake** عبر `POST /api/v1/leads`.
2. **Qualification + Decision Passport** تلقائياً.
3. **Plan/Offer Selection** حسب readiness والأدلة.
4. **Execution Tasks** مع Anti-waste guardrails.
5. **Weekly Learning Loop** عبر template التعلّم الأسبوعي.

## 6) حوكمة عمليات يومية (Ops Cadence)

### Morning (15–25 دقيقة)
- التأكد من حالة الخدمات.
- تشغيل فحوصات الجاهزية السريعة.
- مراجعة أخطاء اليوم السابق.

### Midday (10–15 دقيقة)
- مراجعة queue/latency/failed jobs.
- متابعة العملاء المعلّقين في pipeline.

### End of Day (15–20 دقيقة)
- تثبيت حالة الصفقات.
- توثيق تعلّمات اليوم.
- تجهيز أولويات الغد.

## 7) نموذج مسؤوليات (RACI مختصر)

- **Tech Lead**: سلامة API/DB/Deploy وقرارات الترقيات.
- **Frontend Owner**: تجربة المستخدم، الأداء، انضباط الـ build.
- **Ops Owner**: SLA، المتابعة اليومية، الحوادث.
- **Growth/Revenue Owner**: تحويل الإشارات إلى فرص ومبيعات.

## 8) مؤشرات الأداء الأساسية

- API success rate (>= 99%).
- P95 latency لأهم endpoints.
- Conversion من lead -> qualified -> proposal -> closed.
- Time-to-first-value للعميل الجديد.
- نسبة الإجراءات التي تتوافق مع Decision Passport.

## 9) مخاطر معروفة يجب احترامها

- وجود رؤوس Alembic متعددة (two heads) يتطلب حذر في الترقية.
- `PostgresEventStore` غير آمن مع sync callers في المسارات المعروفة.
- lint drift تاريخي لا يُستخدم وحده كدليل على صحة API.

## 10) طريقة التشغيل الموصى بها

استخدم سكربت التهيئة التالي لتوحيد فحوصات الجاهزية محلياً:

```bash
bash scripts/company_enterprise_ready.sh
```

السكربت ينفذ checks متسلسلة ويعطي تقرير PASS/FAIL واضح لكل طبقة.
