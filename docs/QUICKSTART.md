<div dir="rtl">

# دليل البدء السريع للمطورين — Dealix Developer Quickstart

> هذا الدليل يُساعدك على تشغيل بيئة Dealix المحلية خلال أقل من 10 دقائق.

---

## 1. المتطلبات الأساسية

<div dir="ltr">

| Tool | Min Version | Check |
|------|-------------|-------|
| Docker | 24+ | `docker --version` |
| Docker Compose | v2.0+ | `docker compose version` |
| Git | 2.x | `git --version` |
| Python | 3.12+ | `python3 --version` (للتطوير بدون Docker) |
| Node.js | 22+ | `node --version` (للتطوير بدون Docker) |

</div>

---

## 2. استنساخ المستودع

<div dir="ltr">

```bash
git clone https://github.com/VoXc2/dealix.git
cd dealix
```

</div>

---

## 3. إعداد متغيرات البيئة

<div dir="ltr">

```bash
# نسخ الملف الأساسي
cp .env.example .env

# نسخ ملف Frontend
cp frontend/.env.example frontend/.env.local
```

</div>

افتح `.env` وأضف القيم التالية كحد أدنى:

<div dir="ltr">

```env
# Database
DATABASE_URL=postgresql+asyncpg://salesflow:salesflow_secret_2024@db:5432/salesflow

# Redis
REDIS_URL=redis://redis:6379/0

# LLM Keys (مطلوب واحد على الأقل)
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here   # Fallback

# JWT
SECRET_KEY=your_random_secret_key_min_32_chars

# WhatsApp (اختياري للتطوير المحلي)
ULTRAMSG_INSTANCE_ID=
ULTRAMSG_TOKEN=
```

</div>

> **تحذير:** لا تُضِف `.env` إلى Git أبداً — إنه مُدرَج في `.gitignore` بالفعل.

---

## 4. تشغيل المكدس الكامل (Docker)

<div dir="ltr">

```bash
# بناء الصور وتشغيل الخدمات
docker-compose up --build -d

# متابعة السجلات
docker-compose logs -f

# تطبيق مخططات قاعدة البيانات
docker-compose exec backend alembic upgrade head
```

</div>

### التحقق من الخدمات

<div dir="ltr">

```bash
# Backend API
curl -sSf http://localhost:8000/api/v1/health
# المتوقع: {"status": "ok"}

# Frontend
curl -sSf http://localhost:3000
# المتوقع: HTML للوحة التحكم
```

</div>

| Service | URL |
|---------|-----|
| Backend API Docs | http://localhost:8000/docs |
| Frontend Dashboard | http://localhost:3000 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

## 5. التشغيل بدون Docker (وضع التطوير)

### Backend

<div dir="ltr">

```bash
cd backend

# إنشاء بيئة Python افتراضية
python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS
# أو: .venv\Scripts\activate       # Windows

# تثبيت التبعيات
pip install -r requirements.txt

# تشغيل الخادم
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

</div>

### Frontend

<div dir="ltr">

```bash
cd frontend

# تثبيت التبعيات
npm ci

# تشغيل بيئة التطوير
npm run dev
```

</div>

### Celery Worker

<div dir="ltr">

```bash
cd backend
celery -A app.celery_app worker --loglevel=info --concurrency=4
```

</div>

---

## 6. إدارة قاعدة البيانات

<div dir="ltr">

```bash
# تطبيق جميع الترحيلات
PYTHONPATH=$(pwd) alembic upgrade head

# إنشاء ترحيل جديد بعد تغيير النماذج
PYTHONPATH=$(pwd) alembic revision --autogenerate -m "وصف التغيير"

# التراجع عن آخر ترحيل
PYTHONPATH=$(pwd) alembic downgrade -1

# عرض حالة الترحيلات
PYTHONPATH=$(pwd) alembic current
```

</div>

---

## 7. الاختبارات

<div dir="ltr">

```bash
cd backend

# تشغيل جميع الاختبارات
pytest -v

# مع تغطية الكود
pytest --cov=app --cov-report=html --cov-report=term-missing

# اختبار ملف واحد
pytest tests/test_agents.py -v

# اختبارات E2E (Frontend)
cd ../frontend
npx playwright install chromium    # مرة واحدة فقط
npm run test:e2e
```

</div>

---

## 8. أوامر Make المفيدة

<div dir="ltr">

```bash
# من جذر المستودع
make migrate      # تطبيق ترحيلات قاعدة البيانات
make seed         # تحميل البيانات الأولية
make test         # تشغيل الاختبارات
make lint         # فحص جودة الكود
make build        # بناء صور Docker
```

</div>

---

## 9. هيكل الوكلاء — مرجع سريع

<div dir="ltr">

```
backend/app/services/agents/
├── orchestrator.py    # يُدير سير العمل بين الوكلاء
├── researcher.py      # جمع بيانات العملاء المحتملين
├── qualifier.py       # تقييم BANT للعميل
├── outreach.py        # إرسال رسائل المبيعات
├── closer.py          # إعداد العروض وإغلاق الصفقات
├── compliance.py      # مراجعة الامتثال (ZATCA/PDPL)
├── analytics.py       # تقارير KPIs وحزم الأدلة
├── whatsapp.py        # إدارة محادثات واتساب
└── router.py          # توجيه الأحداث إلى الوكيل المناسب
```

</div>

---

## 10. نقاط API الأساسية

<div dir="ltr">

```
GET  /api/v1/health                          Health check
POST /api/v1/auth/login                      تسجيل الدخول
GET  /api/v1/leads/                          قائمة العملاء المحتملين
POST /api/v1/leads/                          إضافة عميل محتمل
GET  /api/v1/executive-room/snapshot         لوحة تحكم المدير التنفيذي
GET  /api/v1/compliance/matrix/              مصفوفة الامتثال السعودي
GET  /api/v1/evidence-packs/                 حزم الأدلة
GET  /api/v1/model-routing/dashboard         لوحة توجيه LLM
GET  /api/v1/forecast-control/unified        الفعلي مقابل التنبؤات
```

</div>

الوثائق الكاملة التفاعلية: `http://localhost:8000/docs`

---

## 11. استكشاف الأخطاء الشائعة

**المشكلة:** `Connection refused` على المنفذ 8000 أو 3000
**الحل:** تأكد من أن الخدمات تعمل: `docker-compose ps`

**المشكلة:** خطأ في ترحيل قاعدة البيانات
**الحل:** تأكد أن `db` تعمل: `docker-compose exec db pg_isready -U salesflow`

**المشكلة:** خطأ `GROQ_API_KEY not set`
**الحل:** راجع ملف `.env` وتأكد من وجود المفتاح وعدم وجود مسافات زائدة

**المشكلة:** RTL لا يعمل في Frontend
**الحل:** تأكد أن `NEXT_PUBLIC_API_URL` في `frontend/.env.local` يشير إلى الـ Backend الصحيح

---

## 12. روابط مفيدة

- [README الرئيسي](../README.md)
- [بنية النظام](./ARCHITECTURE.md)
- [قائمة التشغيل](./LAUNCH_CHECKLIST.md)
- [دليل البيئة المرحلية](./STAGING_ENV_CHECKLIST.md)
- [دليل المساهمة](../CONTRIBUTING.md)
- [سياسة الأمان](../SECURITY.md)

---

<div dir="ltr">

*Dealix Developer Quickstart · Arabic-First B2B Sales AI · منصة المبيعات الذكية للسوق السعودي*

</div>

</div>
