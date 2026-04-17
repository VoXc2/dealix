<div dir="rtl">

# Dealix — منصة المبيعات الذكية للسوق السعودي

<div dir="ltr">

> **Arabic-first B2B Sales AI Platform** — من الرصاص إلى العميل الموقِّع | From Lead to Signed Deal

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![Node](https://img.shields.io/badge/Node-22+-339933.svg)](https://nodejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![CI](https://img.shields.io/github/actions/workflow/status/VoXc2/dealix/dealix-ci.yml?label=CI)](https://github.com/VoXc2/dealix/actions)

</div>

---

## 📋 نظرة عامة

**Dealix** هي منصة ذكاء اصطناعي للمبيعات B2B مصمَّمة للسوق السعودي. تجمع المنصة بين إدارة العملاء المحتملين، وأتمتة المبيعات، وجدولة الاجتماعات، وتتبع الصفقات، ومعالجة العمولات — في نظام تشغيل واحد مدفوع بثمانية وكلاء ذكاء اصطناعي متخصصين.

**السعر:** 1,499 ريال سعودي / شهر لكل مستأجر (Multi-tenant SaaS)

**السوق المستهدف:** الشركات الصغيرة والمتوسطة السعودية في قطاعات العقارات، الرعاية الصحية، التجزئة، المقاولات، والتعليم.

---

## ✨ الميزات الرئيسية — وكلاء الذكاء الاصطناعي الثمانية

<div dir="ltr">

| Agent | Arabic Name | Role |
|-------|-------------|------|
| **Orchestrator** | المُنسِّق | يدير سير عمل الوكلاء، يوزّع المهام، ويضمن تسلسل العمليات وتجانسها |
| **Researcher** | الباحث | يجمع بيانات الشركات والمعلومات التجارية من المصادر العامة ويُعِدّ ملفات الاستهداف |
| **Qualifier** | المُؤهِّل | يُقيِّم جاهزية العملاء المحتملين وفق معايير BANT ويُصدر بطاقات تقييم مُهيكلة |
| **Outreach** | التواصل | يصيغ رسائل المبيعات بالعربية ويُرسلها عبر البريد الإلكتروني وواتساب بعد التحقق من موافقة PDPL |
| **Closer** | المُغلِق | يُعِدّ العروض والمقترحات ويتابع مراحل إغلاق الصفقات حتى التوقيع |
| **Compliance** | الامتثال | يراجع كل إجراء مقابل متطلبات ZATCA وPDPL وSDAIA وNCA قبل تنفيذه |
| **Analytics** | التحليلات | يرصد KPIs، ويُولِّد تقارير الأداء الفعلي مقابل التنبؤات، ويُدير حزم الأدلة |
| **WhatsApp** | واتساب | يُدير محادثات واتساب للأعمال عبر UltraMsg مع قواعد الاستجابة وأتمتة المتابعة |

</div>

---

## 🏗️ البنية التقنية

### مكدس التقنيات — Stack Versions

<div dir="ltr">

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Framework** | FastAPI | 0.115 |
| **Runtime** | Python | 3.12 |
| **Database** | PostgreSQL | 16 |
| **Cache / Message Broker** | Redis | 7 |
| **Task Queue** | Celery | 5.x |
| **ORM** | SQLAlchemy (async) | 2.0 |
| **Migrations** | Alembic | latest |
| **Auth** | PyJWT | latest |
| **Frontend Framework** | Next.js (App Router) | 15 |
| **UI Library** | React | 19 |
| **Language** | TypeScript | 5.7 |
| **Styling** | Tailwind CSS (RTL) | 3.4 |
| **Reverse Proxy** | Nginx | stable |
| **Containerization** | Docker Compose | v3.8 |
| **LLM Primary** | Groq (llama-3.1-70b) | — |
| **LLM Fallback** | OpenAI GPT-4o-mini | — |
| **WhatsApp API** | UltraMsg | — |

</div>

### رسم البنية المعمارية

<div dir="ltr">

```
┌─────────────────────────────────────────────────────────────────┐
│                        DEALIX PLATFORM                          │
│                     منصة Dealix للمبيعات                        │
└─────────────────────────────────────────────────────────────────┘

 ┌────────────────┐      ┌────────────────────────────────────────┐
 │   Next.js 15   │      │           FastAPI 0.115               │
 │  React 19 + TS │◄────►│         Python 3.12 / Uvicorn         │
 │  Tailwind RTL  │      │         /api/v1/* (REST)              │
 └────────────────┘      └──────────────┬─────────────────────────┘
        │                               │
        │ HTTPS (Nginx)                 │
        │                    ┌──────────▼──────────┐
        │                    │   Agent Orchestrator │
        │                    │      (router.py)     │
        │                    └──┬──┬──┬──┬──┬──┬───┘
        │                       │  │  │  │  │  │
        │            ┌──────────┘  │  │  │  │  └──────────┐
        │            │  ┌──────────┘  │  │  └──────────┐  │
        │            │  │  ┌──────────┘  └──────────┐  │  │
        │            ▼  ▼  ▼                         ▼  ▼  ▼
        │       ┌─────────────────────────────────────────────┐
        │       │  Researcher │ Qualifier │ Outreach │ Closer  │
        │       │  Compliance │ Analytics │ WhatsApp          │
        │       └──────────────────────┬──────────────────────┘
        │                              │
        │                    ┌─────────▼──────────┐
        │                    │   Groq (primary)   │
        │                    │   OpenAI (fallback) │
        │                    └────────────────────┘
        │
        │    ┌──────────────────────────────────────────────┐
        │    │            Infrastructure Layer              │
        │    │                                              │
        │    │  ┌──────────────┐   ┌──────────────────┐    │
        │    │  │ PostgreSQL 16│   │    Redis 7        │    │
        │    │  │  (primary DB)│   │ (cache + broker)  │    │
        │    │  └──────────────┘   └──────────────────┘    │
        │    │                                              │
        │    │  ┌──────────────────────────────────────┐   │
        │    │  │    Celery Workers (async tasks)       │   │
        │    │  └──────────────────────────────────────┘   │
        │    └──────────────────────────────────────────────┘
        │
        │    ┌──────────────────────────────────────────────┐
        │    │            Compliance Layer                  │
        │    │  ZATCA │ PDPL │ SDAIA │ NCA │ Truth Registry │
        │    └──────────────────────────────────────────────┘
```

</div>

---

## 🚀 البدء السريع

### المتطلبات

<div dir="ltr">

| Tool | Minimum Version |
|------|----------------|
| Docker | 24+ |
| Docker Compose | v2.0+ |
| Python | 3.12+ (للتطوير المحلي) |
| Node.js | 22+ (للتطوير المحلي) |
| Git | 2.x |

</div>

### التثبيت

<div dir="ltr">

```bash
# 1. استنساخ المستودع
git clone https://github.com/VoXc2/dealix.git
cd dealix

# 2. إعداد متغيرات البيئة
cp .env.example .env
# افتح .env وأضف مفاتيح API المطلوبة:
#   GROQ_API_KEY, OPENAI_API_KEY, DATABASE_URL, REDIS_URL

# 3. تهيئة قاعدة البيانات وتشغيل الخدمات
docker-compose up --build -d

# 4. تطبيق مخططات قاعدة البيانات
docker-compose exec backend alembic upgrade head

# 5. تحميل البيانات الأولية (اختياري)
docker-compose exec backend python -m app.seeds.run
```

</div>

### التشغيل

<div dir="ltr">

```bash
# تشغيل الخدمات الكاملة
docker-compose up

# التحقق من الصحة
curl -sSf http://localhost:8000/api/v1/health

# الواجهات
# Backend API Docs:  http://localhost:8000/docs
# Frontend Dashboard: http://localhost:3000
```

</div>

#### التشغيل بدون Docker (للتطوير)

<div dir="ltr">

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (terminal منفصل)
cd frontend
npm ci
npm run dev

# Celery Worker (terminal منفصل)
cd backend
celery -A app.celery_app worker --loglevel=info
```

</div>

---

## 📁 هيكل المستودع

<div dir="ltr">

```
dealix/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/v1/            # API routes (REST endpoints)
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── agents/        # 8 AI agent implementations
│   │   │   ├── ai/            # LLM integration & model_router.py
│   │   │   └── ...
│   │   ├── core/              # Config, security, dependencies
│   │   └── main.py            # Application entry point
│   ├── alembic/               # Database migrations
│   ├── tests/                 # pytest test suite
│   └── requirements.txt
├── frontend/                   # Next.js 15 App Router
│   ├── app/                   # App directory (pages, layouts)
│   ├── components/            # Reusable React components (RTL-first)
│   ├── lib/                   # API client, utilities
│   └── public/                # Static assets
├── openclaw/                  # Governance & policy engine
│   └── policy.py             # Agent trust-plane: Class A/B/C actions
├── infra/                     # Infrastructure configs (Nginx, Docker)
├── scripts/                   # Utility scripts
├── docs/                      # Project documentation
│   ├── QUICKSTART.md
│   ├── ARCHITECTURE.md
│   └── ...
├── docker-compose.yml
├── .env.example
├── Makefile
├── AGENTS.md                  # AI agent coding conventions
├── SECURITY.md                # Security policy
├── CONTRIBUTING.md            # Contribution guide
└── LICENSE                    # Proprietary license
```

</div>

---

## 🔧 التطوير

### Backend — FastAPI

<div dir="ltr">

```bash
cd backend

# تشغيل الاختبارات
pytest -v

# تشغيل الاختبارات مع تغطية الكود
pytest --cov=app --cov-report=html

# فحص الكود
ruff check app/
mypy app/

# ترحيل قاعدة البيانات
PYTHONPATH=$(pwd) alembic upgrade head

# إنشاء ترحيل جديد
PYTHONPATH=$(pwd) alembic revision --autogenerate -m "description"
```

</div>

### Frontend — Next.js

<div dir="ltr">

```bash
cd frontend

# تثبيت التبعيات
npm ci

# تشغيل بيئة التطوير
npm run dev

# فحص الكود
npm run lint

# بناء الإنتاج
npm run build

# اختبارات E2E (Playwright)
npx playwright install chromium  # مرة واحدة فقط
npm run test:e2e
```

</div>

### Tests

<div dir="ltr">

```bash
# فحص بنية المشروع
python scripts/architecture_brief.py

# التحقق من الإطلاق
.\verify-launch.ps1 -HttpCheck -SoftReady   # Windows
# أو
bash deploy_server.sh                        # Linux/macOS
```

</div>

### Release Process

<div dir="ltr">

```
Feature Branch → PR → Code Review
       ↓
  Tests + Security Scan
       ↓
  Deploy to Staging
       ↓
  Smoke Test (AR + EN)
       ↓
  Canary Deploy (10%) → Monitor 30min
       ↓
  Full Production Rollout
```

</div>

---

## 🔐 الأمان والامتثال

تعمل Dealix وفق إطار امتثال متكامل للسوق السعودي:

### ZATCA — هيئة الزكاة والضريبة والجمارك
الفوترة الإلكترونية متوافقة مع متطلبات ZATCA المرحلة الثانية. جميع الفواتير تحمل UUID، وختم وقت، وتوقيعاً رقمياً وفق المواصفات المعتمدة.

### PDPL — نظام حماية البيانات الشخصية
لا تُرسَل أي رسالة تسويقية دون فحص موافقة PDPL مسبقاً عبر وكيل Compliance. جميع بيانات PII محظور تخزينها في السجلات.

### SDAIA / NCA
يلتزم النظام بتوجيهات الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA) والهيئة الوطنية للأمن السيبراني (NCA) فيما يخص حوكمة الذكاء الاصطناعي وحماية البيانات.

### Truth Registry — سجل الحقيقة

> **ثوابت لا تُخرَق — Non-Negotiable Invariants**

<div dir="ltr">

| Invariant | Rule |
|-----------|------|
| **No Unsupported Claims** | Any metric or performance claim must be backed by telemetry data in the evidence pack |
| **No Fabricated Attribution** | Agent-generated content must not attribute results to features not yet deployed |
| **No Silent Failures** | All agent errors must be logged and surfaced to the Orchestrator |
| **No PII in Logs** | Personal data must never appear in application logs |
| **No Raw SQL** | All database queries must go through SQLAlchemy ORM |
| **PDPL Gate** | Outreach messages require explicit consent verification before dispatch |
| **Tenant Isolation** | Cross-tenant data access is a Class C (Forbidden) action |

</div>

**ملاحظة:** لا تدّعي المنصة أي اعتمادات من قبيل "SOC 2" أو "ISO 27001" أو "100% accurate" أو "bank-grade" أو "military-grade". جميع ادعاءات الأداء مربوطة بقياسات فعلية موثّقة.

للإبلاغ عن ثغرة أمنية: راجع [./SECURITY.md](./SECURITY.md) أو راسل sami.assiri11@gmail.com مباشرةً.

---

## 🗓️ خارطة الطريق

تفاصيل خارطة الطريق اليومية وجداول التنفيذ متاحة في:

- [جدول التنفيذ اليومي — DAILY_EXECUTION_SCHEDULE_AR.md](./DAILY_EXECUTION_SCHEDULE_AR.md)
- [مخطط التنفيذ الشامل — DEALIX_EXECUTION_BLUEPRINT.md](./DEALIX_EXECUTION_BLUEPRINT.md)
- [مخطط المرحلة الثانية — DEALIX_PHASE2_BLUEPRINT.md](./DEALIX_PHASE2_BLUEPRINT.md)

---

## 🤝 المساهمة

نرحب بالمساهمات من الفريق الداخلي. يرجى مراجعة [دليل المساهمة — CONTRIBUTING.md](./CONTRIBUTING.md) قبل فتح أي Pull Request.

**القواعد الأساسية:**
- لا ترفع مباشرةً على `main` — استخدم feature branches دائماً
- كل PR يحتاج مراجعة من مراجع واحد على الأقل
- الاختبارات مطلوبة لأي تغيير وظيفي جديد
- جميع الواجهات المرئية يجب أن تدعم RTL والعربية

---

## 📜 الترخيص

هذا البرنامج **مملوك ملكية خاصة** وغير مرخَّص للاستخدام العام.

جميع الحقوق محفوظة لـ Sami Mohammed Assiri.
راجع [./LICENSE](./LICENSE) للتفاصيل الكاملة.

---

## 📞 التواصل

<div dir="ltr">

| Channel | Details |
|---------|---------|
| **Owner** | Sami Mohammed Assiri |
| **Email** | sami.assiri11@gmail.com |
| **Repository** | https://github.com/VoXc2/dealix (Private) |
| **Security Reports** | See [SECURITY.md](./SECURITY.md) — do not open public issues |

</div>

---

<div dir="ltr">

*Built for the Saudi Market · Arabic-First · B2B Sales AI · منصة المبيعات الذكية*

</div>

</div>
