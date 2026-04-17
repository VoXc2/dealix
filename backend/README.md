# Dealix Backend

خدمة API الخلفية لمنصة **Dealix** — نظام تشغيل الصفقات والنمو والالتزام.  
مبنية على **FastAPI + SQLAlchemy 2 (async) + PostgreSQL + LangGraph + CrewAI**.

للاطلاع على الصورة الكاملة للمشروع راجع [README الرئيسي](../README.md)  
وللبنية المعمارية راجع [ARCHITECTURE.md](../ARCHITECTURE.md).

---

## المتطلبات

| الأداة | الإصدار |
|--------|---------|
| Python | ≥ 3.12, < 3.13 |
| PostgreSQL | ≥ 15 |
| Redis | ≥ 7 |
| pgvector | ≥ 0.7 |

---

## التثبيت

```bash
# استنسخ المستودع
git clone <repo-url>
cd dealix-clean/backend

# أنشئ بيئة افتراضية
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# أو: .venv\Scripts\activate       # Windows

# ثبّت الاعتمادات
make install

# أعد ملف البيئة
cp .env.example .env
# ثم عدّل .env بقيمك الحقيقية
```

---

## التشغيل المحلي

```bash
# شغّل قاعدة البيانات و Redis عبر Docker (مستحسن)
docker compose up -d db redis

# نفّذ ترحيلات قاعدة البيانات
alembic upgrade head

# ابدأ الخادم
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

الـ API يعمل على `http://localhost:8000`  
وثائق Swagger: `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

---

## Tests

```bash
# تشغيل كل الاختبارات
make test

# مع تقرير التغطية
pytest tests -q --cov=app --cov-report=term-missing

# اختبارات محددة فقط
pytest tests/api/ -q
pytest -m "not slow" -q      # تجاهل الاختبارات البطيئة
```

---

## Linting والفحص

```bash
# فحص الأسلوب (ruff)
make lint

# تنسيق الكود (black + ruff --fix)
make format

# فحص شامل: ruff + mypy
make check

# فحص الأمان (bandit)
make security
```

### الأدوات المستخدمة

| الأداة | الغرض |
|--------|--------|
| **ruff** | Linter سريع (يغطي E/F/W/I/N/UP/B/C4/S/A/RET/SIM/TCH) |
| **black** | تنسيق الكود |
| **mypy** | فحص الأنواع الساكنة |
| **bandit** | فحص الثغرات الأمنية |
| **pytest** | إطار الاختبارات مع دعم async |

إعدادات الأدوات موجودة في `pyproject.toml`.

---

## هيكل المشروع

```
backend/
├── app/
│   ├── agents/        # وكلاء LangGraph و CrewAI
│   ├── ai/            # منطق LLM والمحادثات
│   ├── api/           # نقاط نهاية FastAPI
│   ├── integrations/  # تكاملات خارجية (WhatsApp، Email...)
│   ├── models/        # نماذج SQLAlchemy
│   ├── schemas/       # مخططات Pydantic
│   ├── services/      # منطق الأعمال
│   └── main.py        # نقطة الدخول
├── tests/             # الاختبارات
├── alembic/           # ترحيلات قاعدة البيانات
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Makefile
└── .env.example
```

---

## متغيرات البيئة

انسخ `.env.example` إلى `.env` وعدّل القيم:

| المتغير | الوصف |
|---------|--------|
| `DATABASE_URL` | رابط اتصال PostgreSQL |
| `REDIS_URL` | رابط اتصال Redis |
| `GROQ_API_KEY` | مفتاح Groq API |
| `OPENAI_API_KEY` | مفتاح OpenAI API |
| `JWT_SECRET` | مفتاح توقيع JWT (≥ 32 حرف) |
| `ENVIRONMENT` | `development` أو `production` |
| `LOG_LEVEL` | مستوى التسجيل (`INFO`, `DEBUG`...) |
