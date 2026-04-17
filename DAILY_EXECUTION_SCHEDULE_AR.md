# Dealix — جدول التنفيذ اليومي (90 يوم حتى التدشين)

> **المنصة:** Dealix — B2B Sales AI للسوق السعودي  
> **المطوّر:** Sami Mohammed Assiri  
> **السعر:** 1,499 ريال/شهر  
> **المستودع:** https://github.com/VoXc2/dealix  
> **تاريخ البداية:** اليوم 1 من الآن  
> **الهدف:** تدشين المنتج للعملاء الأوائل خلال 90 يوماً

---

## نظرة عامة

| المرحلة | الأسابيع | المحور |
|---------|----------|--------|
| 1 — الأساسات | 1–2 | CI/CD، Docker، DB، Secrets |
| 2 — Backend Hardening | 3–5 | Auth، RBAC، Rate Limiting، Tests |
| 3 — AI Agents | 6–8 | LLM Router، 8 Agents، Token Tracking |
| 4 — Frontend & RTL | 9–10 | Arabic UI، Dashboards، Onboarding |
| 5 — Compliance & Legal | 11 | ZATCA، PDPL، Privacy Policy |
| 6 — Go-to-Market | 12 | Landing Page، Demo، Pilot Customers |
| 7 — التدشين | 13 | Soft Launch، Monitoring، First Customer |

> **قاعدة صارمة:** لا يُعلَن عن أي ميزة كـ"جاهزة للإنتاج" قبل **30 يوماً من telemetry** مستقرة.

---

## المعالم الرئيسية (Milestones)

| اليوم | المعلم |
|-------|--------|
| 7 | CI/CD أخضر بالكامل + Docker Compose يعمل محلياً |
| 14 | DB migrations كاملة + Secrets management + Truth Registry v1 |
| 21 | JWT Auth + RBAC + Rate Limiting جاهز |
| 28 | Idempotency keys + Hash chain audit logs |
| 35 | Test coverage ≥ 70% على Backend |
| 42 | LLM Router (Groq→OpenAI) جاهز + Orchestrator agent |
| 49 | 8 agents مكتملة + prompt caching |
| 56 | Token tracking dashboard + Arabic UI أساسي |
| 63 | Frontend كامل + Onboarding wizard |
| 70 | RTL accessibility WCAG AA |
| 77 | ZATCA + PDPL compliance كاملة |
| 84 | Landing page + Demo video + 3 pilot outreach |
| 90 | Soft launch + أول عميل مدفوع |

---

## المرحلة 1: الأساسات (أسبوع 1–2)

---

## الأسبوع 1 (أيام 1-7): CI/CD والبنية التحتية

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم CLI دائماً قبل MCP — `grep` قبل `read`، `git log --oneline` قبل فتح الملفات.

---

### اليوم 1 — تدقيق المستودع وإعداد البيئة

- [ ] نفّذ `git clone https://github.com/VoXc2/dealix && git log --oneline -20` وسجّل آخر 20 commit في ملف `docs/repo_audit.md`
- [ ] افحص الـ 67,105 LOC بـ `find . -name "*.py" | xargs wc -l | sort -rn | head -20` وحدّد أكبر 20 ملفاً
- [ ] أنشئ ملف `.env.example` يحتوي على جميع المتغيرات المطلوبة (DATABASE_URL، REDIS_URL، GROQ_API_KEY، OPENAI_API_KEY، JWT_SECRET، ZATCA_API_KEY)
- [ ] تحقق أن Python 3.12 و Node.js 20+ مثبّتان: `python3 --version && node --version && docker --version`
- [ ] أنشئ `docs/DAY1_BASELINE.md` بقائمة ما يعمل وما لا يعمل حالياً

---

### اليوم 2 — Docker Compose الأساسي

- [ ] راجع `docker-compose.yml` الموجود (إن كان موجوداً) بـ `cat docker-compose.yml` ثم افتحه فقط إذا احتجت تعديلاً
- [ ] تأكد أن services كالتالي: `api` (FastAPI)، `db` (PostgreSQL 16)، `redis` (Redis 7)، `celery_worker`، `frontend` (Next.js 15)
- [ ] أضف health checks لكل service في docker-compose: `pg_isready -U postgres`، `redis-cli ping`، `curl -f http://localhost:8000/health`
- [ ] نفّذ `docker compose up -d --build` وتحقق أن جميع containers تعمل بـ `docker compose ps`
- [ ] سجّل نتيجة الـ health checks في `docs/docker_status.md`

---

### اليوم 3 — GitHub Actions CI Pipeline

- [ ] أنشئ `.github/workflows/ci.yml` بـ pipeline يشمل: `pytest` + `ruff` + `mypy` + `next build`
- [ ] أضف cache لـ pip packages وـ npm packages في الـ workflow لتقليل وقت CI
- [ ] أضف خطوة `docker build --no-cache` كـ smoke test في CI
- [ ] أنشئ badge للـ CI status في `README.md`: `![CI](https://github.com/VoXc2/dealix/actions/workflows/ci.yml/badge.svg)`
- [ ] push التغييرات وتحقق أن الـ pipeline يمر بالكامل (لا يوجد خطأ أحمر)

---

### اليوم 4 — Pre-commit Hooks وCode Quality

- [ ] ثبّت `pre-commit`: `pip install pre-commit` وأنشئ `.pre-commit-config.yaml` يشمل: `ruff`, `black`, `mypy`, `trailing-whitespace`
- [ ] أضف hook لمنع commit الـ secrets: استخدم `detect-secrets` أو `gitleaks`
- [ ] نفّذ `pre-commit run --all-files` وأصلح أي أخطاء تظهر
- [ ] أضف `pyproject.toml` بإعدادات `ruff` و`black` موحّدة للمشروع
- [ ] تحقق أن الـ pre-commit hooks تعمل بـ commit تجريبي وإلغائه: `git commit --allow-empty -m "test"`

---

### اليوم 5 — Secrets Management

- [ ] أنشئ `config/settings.py` باستخدام `pydantic-settings` يقرأ من `.env` مع validation صارم لكل متغير مطلوب
- [ ] تأكد أن `.env` و`.env.local` مضافان في `.gitignore` — افحص بـ `git check-ignore -v .env`
- [ ] أضف Doppler أو GitHub Secrets كـ CI/CD secrets provider (وثّق الخطوات في `docs/secrets_setup.md`)
- [ ] اكتب test: `test_settings_validation.py` يتحقق أن التطبيق يرفض البدء بدون متغيرات إلزامية
- [ ] افحص أن لا secrets مكشوفة في git history: `git log --all --full-history -- "*.env"` يجب أن يعود فارغاً

---

### اليوم 6 — Database Migrations Setup

- [ ] تحقق أن Alembic مثبّت وأنشئ `alembic/env.py` يستخدم models من FastAPI
- [ ] نفّذ `alembic current` وتحقق من حالة migrations الموجودة
- [ ] أنشئ migration للـ baseline schema: `alembic revision --autogenerate -m "baseline_schema"`
- [ ] نفّذ `alembic upgrade head` وتحقق أن جميع tables أُنشئت بـ `psql -c "\dt"` أو `docker exec -it dealix_db psql -U postgres -c "\dt"`
- [ ] أضف `alembic upgrade head` في بداية docker-compose startup script

---

### اليوم 7 (الجمعة) — مراجعة الأسبوع الأول + Truth Registry v0

- [ ] **مراجعة أسبوعية:** افتح `docs/DAY1_BASELINE.md` وقارن الحالة الآن بالبداية — وثّق ما تحسّن
- [ ] **تحديث Truth Registry:** أنشئ `docs/TRUTH_REGISTRY.md` بالحالة الفعلية: ما يعمل ✅، ما لا يعمل ❌، ما غير محدد ⚠️
- [ ] تأكد أن CI pipeline أخضر بالكامل قبل نهاية اليوم
- [ ] أنشئ GitHub Milestone "Week 1 Complete" وأغلق الـ issues المرتبطة
- [ ] اكتب `docs/WEEK1_RETROSPECTIVE.md`: ما أنجزته، ما تعثّرت فيه، الخطوات القادمة

> **معلم الأسبوع 1:** CI/CD أخضر ✅ | Docker Compose يعمل ✅ | Secrets آمنة ✅ | DB migrations تعمل ✅

---

## الأسبوع 2 (أيام 8-14): البنية التحتية المتقدمة

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم `grep -n "pattern" file` لتحديد السطر قبل قراءة الملف — لا تقرأ ملفات أكبر من 500 سطر كاملاً دفعة واحدة.

---

### اليوم 8 — Logging والـ Observability

- [ ] أضف `structlog` للـ FastAPI application: كل request يسجّل `request_id`, `user_id`, `endpoint`, `duration_ms`, `status_code`
- [ ] أنشئ middleware `LoggingMiddleware` يضيف `X-Request-ID` header تلقائياً لكل response
- [ ] اضبط log levels: `DEBUG` في development، `INFO` في staging، `WARNING` في production
- [ ] أضف log rotation بـ `logging.handlers.RotatingFileHandler`: max 10MB، 5 backups
- [ ] تحقق أن logs تظهر بشكل صحيح في Docker: `docker compose logs -f api | head -50`

---

### اليوم 9 — Health Checks والـ Readiness Probes

- [ ] أنشئ endpoint `/health` يفحص: DB connection، Redis connection، وقت الاستجابة
- [ ] أنشئ endpoint `/ready` يفحص: DB migrations applied، required env vars loaded
- [ ] أنشئ endpoint `/metrics` بـ Prometheus format: request count، error rate، response time
- [ ] أضف الـ health checks في `docker-compose.yml` بـ `interval: 30s`, `timeout: 10s`, `retries: 3`
- [ ] اكتب tests: `test_health_endpoints.py` يتحقق من كل endpoint

---

### اليوم 10 — Redis Cache Layer

- [ ] أنشئ `core/cache.py` wrapper حول Redis يدعم: `get`, `set`, `delete`, `exists` مع TTL
- [ ] أضف type hints كاملة وـ docstrings بالعربي في ملف الـ cache
- [ ] أنشئ decorator `@cached(ttl=300)` يمكن تطبيقه على أي FastAPI endpoint
- [ ] اكتب `tests/test_cache.py` يتحقق من: cache hit، cache miss، TTL expiry، cache invalidation
- [ ] أضف metric: `cache_hits_total` و`cache_misses_total` في Prometheus

---

### اليوم 11 — Celery Task Queue

- [ ] تحقق أن Celery مهيّأ صح: `celery -A app.celery inspect active` يجب أن يعود بدون خطأ
- [ ] أنشئ مهمة نموذجية: `tasks/sample_task.py` بـ retry logic وـ error handling
- [ ] اضبط Celery beat schedule في `celery_config.py`: مهمة cleanup يومية كل صباح 03:00 Asia/Riyadh
- [ ] أضف Celery Flower dashboard على port 5555 في docker-compose (للمراقبة في dev فقط)
- [ ] اكتب test: `test_celery_tasks.py` يتحقق أن المهام تُنفَّذ بالترتيب الصحيح

---

### اليوم 12 — Multi-tenant Database Architecture

- [ ] أنشئ `tenant_id` column في كل table رئيسية مع `NOT NULL` constraint وـ index
- [ ] أنشئ Alembic migration: `add_tenant_id_to_all_tables`
- [ ] أنشئ `TenantMiddleware` يستخرج `tenant_id` من JWT token ويضيفه في request context
- [ ] تأكد أن جميع database queries تفلتر بـ `tenant_id` — ابحث بـ `grep -rn "db.query" app/` وراجع كل استعلام
- [ ] اكتب test: تأكد أن tenant A لا يمكنه رؤية بيانات tenant B

---

### اليوم 13 — Environment Parity (Dev/Staging/Prod)

- [ ] أنشئ `docker-compose.staging.yml` يستخدم نفس images لكن بـ staging environment variables
- [ ] وثّق الفرق بين environments في `docs/ENVIRONMENTS.md`: أي features موجودة في كل بيئة
- [ ] تأكد أن Staging يستخدم database منفصلة (لا يشارك production DB أبداً)
- [ ] أضف `ENVIRONMENT=staging` check في الكود — ميزات تجريبية فقط في staging وليس production
- [ ] اختبر full deployment على staging environment واحتفظ بالنتائج في `docs/staging_test_results.md`

---

### اليوم 14 (الجمعة) — مراجعة الأسبوع الثاني + Truth Registry v1

- [ ] **مراجعة أسبوعية:** مقارنة الـ CI metrics: وقت البناء هذا الأسبوع مقابل الأسبوع الماضي
- [ ] **تحديث Truth Registry:** حدّث `docs/TRUTH_REGISTRY.md` — أضف: Logging ✅، Cache ✅، Celery ✅، Multi-tenant ✅
- [ ] نفّذ `pytest --cov=app --cov-report=term-missing` وسجّل نسبة التغطية الحالية
- [ ] تأكد أن Docker Compose يبدأ من الصفر بنجاح: `docker compose down -v && docker compose up -d`
- [ ] أنشئ `docs/WEEK2_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 2 Complete"

> **معلم الأسبوع 2:** Logging ✅ | Redis Cache ✅ | Celery ✅ | Multi-tenant isolation ✅ | Truth Registry v1 ✅

---

## المرحلة 2: Backend Hardening (أسبوع 3–5)

---

## الأسبوع 3 (أيام 15-21): Authentication وRBAC

> **قاعدة Token Efficiency هذا الأسبوع:** اكتب tests أولاً (TDD) — فكّر في المخرجات قبل الكود. استخدم `pytest -k "test_name"` لتشغيل test محدد بدلاً من كل الـ suite.

---

### اليوم 15 — JWT Authentication

- [ ] أنشئ `auth/jwt.py`: إنشاء tokens بـ `python-jose`، access token (15 دقيقة)، refresh token (7 أيام)
- [ ] أنشئ endpoints: `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`
- [ ] أضف JWT في HTTP-only cookie وليس localStorage — أسلم من XSS
- [ ] اكتب `tests/test_auth.py`: login صحيح، login خاطئ، token منتهي، refresh token
- [ ] تأكد أن كل endpoint محمي بـ `Depends(get_current_user)` — `grep -rn "def " app/api/` وافحص الـ routes

---

### اليوم 16 — RBAC (Role-Based Access Control)

- [ ] أنشئ جدول `roles` وجدول `permissions` وجدول `role_permissions` في DB
- [ ] أنشئ roles: `super_admin`, `tenant_admin`, `sales_rep`, `viewer`
- [ ] أنشئ decorator `@require_permission("sales:create")` يُستخدم على الـ endpoints
- [ ] Seed الـ default permissions في Alembic migration
- [ ] اكتب tests: `test_rbac.py` — تأكد أن `viewer` لا يمكنه الكتابة وأن `sales_rep` لا يمكنه حذف tenants

---

### اليوم 17 — Password Security

- [ ] استخدم `bcrypt` لتشفير كلمات المرور — لا تستخدم MD5 أو SHA1 أبداً
- [ ] أضف password strength validation: 8+ أحرف، رقم واحد على الأقل، رمز خاص واحد
- [ ] أنشئ flow كامل لـ password reset عبر البريد الإلكتروني (token مؤقت 1 ساعة)
- [ ] أضف account lockout بعد 5 محاولات فاشلة (استخدم Redis counter)
- [ ] اكتب tests: `test_password_security.py` — brute force protection، password reset، lockout

---

### اليوم 18 — Rate Limiting

- [ ] أضف `slowapi` للـ FastAPI: `pip install slowapi`
- [ ] اضبط rate limits: `/auth/login` → 5 طلبات/دقيقة، `/api/*` → 100 طلبات/دقيقة لكل user
- [ ] خزّن rate limit counters في Redis مع TTL مناسب
- [ ] أضف headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- [ ] اكتب tests: تحقق أن الـ rate limit يُطبَّق فعلاً وأن الـ headers صحيحة

---

### اليوم 19 — Input Validation وSanitization

- [ ] افحص جميع Pydantic models: `grep -rn "class.*BaseModel" app/` وتأكد أن كل field يملك validation
- [ ] أضف SQL injection protection: تحقق أنك تستخدم SQLAlchemy ORM أو parameterized queries — لا raw SQL مع user input
- [ ] أضف XSS protection: كل string input يمر على `bleach.clean()` قبل التخزين
- [ ] أضف CORS configuration صارم في FastAPI: اسمح فقط بـ domains المعروفة
- [ ] اكتب `tests/test_input_validation.py`: SQL injection attempts، XSS attempts، oversized payloads

---

### اليوم 20 — API Versioning وDocumentation

- [ ] أنشئ structure: `/api/v1/` لجميع endpoints الحالية
- [ ] تأكد أن OpenAPI/Swagger docs تعمل: `http://localhost:8000/docs` يعرض كل endpoints
- [ ] أضف Arabic descriptions للـ endpoints الرئيسية في OpenAPI schema
- [ ] أنشئ `docs/API_REFERENCE.md` بقائمة جميع endpoints وطريقة استخدامها
- [ ] اختبر كل endpoint بـ `pytest` وتأكد أن الـ response schemas صحيحة

---

### اليوم 21 (الجمعة) — مراجعة الأسبوع الثالث + Truth Registry v2

- [ ] **مراجعة أسبوعية:** شغّل `pytest --cov` وسجّل نسبة التغطية — يجب أن تكون > 50% الآن
- [ ] **تحديث Truth Registry:** أضف: JWT ✅، RBAC ✅، Rate Limiting ✅، Input Validation ✅
- [ ] افعل security scan: `pip install bandit && bandit -r app/ -f txt -o docs/security_scan.txt`
- [ ] راجع جميع GitHub issues المفتوحة وأعد أولويتها
- [ ] أنشئ `docs/WEEK3_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 3 Complete"

> **معلم الأسبوع 3:** JWT Auth ✅ | RBAC ✅ | Rate Limiting ✅ | Input Validation ✅

---

## الأسبوع 4 (أيام 22-28): Audit Logs وIdempotency

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم `git diff HEAD~1 --stat` لرؤية ما تغيّر قبل قراءة الملفات. استخدم `wc -l` قبل فتح أي ملف كبير.

---

### اليوم 22 — Audit Log Foundation

- [ ] أنشئ جدول `audit_logs`: `id`, `tenant_id`, `user_id`, `action`, `entity_type`, `entity_id`, `old_value`, `new_value`, `timestamp`, `ip_address`, `hash`
- [ ] أنشئ Alembic migration لجدول الـ audit logs
- [ ] أنشئ `core/audit.py`: function `log_action(user_id, action, entity_type, entity_id, old, new)` تُسجّل في DB وتحسب hash
- [ ] تأكد أن الـ audit logs تُكتب في background task لا تبطّئ الـ request الأصلي
- [ ] اكتب `tests/test_audit.py`: تحقق أن الـ actions تُسجَّل بشكل صحيح

---

### اليوم 23 — Hash Chain للـ Audit Logs

- [ ] أنشئ نظام Hash Chain: كل audit log يحتوي على `previous_hash` من السجل السابق
- [ ] الـ hash يُحسَّب بـ SHA-256: `hash = sha256(previous_hash + timestamp + user_id + action + entity_id + data)`
- [ ] أنشئ function `verify_audit_chain(tenant_id)` تتحقق من سلامة كل السلسلة
- [ ] أضف endpoint `GET /admin/audit/verify` يعيد `{valid: true, chain_length: N}` أو يرفع خطأ
- [ ] اكتب test: إذا عدّلت سجل في المنتصف، `verify_audit_chain` يكتشف التلاعب

---

### اليوم 24 — Idempotency Keys

- [ ] أنشئ `IdempotencyMiddleware`: كل POST/PUT request يقبل header `Idempotency-Key`
- [ ] خزّن الـ idempotency keys في Redis مع TTL 24 ساعة
- [ ] إذا جاء request بنفس الـ key مرة ثانية، أعد نفس الـ response المخزّن دون تنفيذ العملية مجدداً
- [ ] طبّق على endpoints المهمة: `POST /contracts`, `POST /invoices`, `POST /deals`
- [ ] اكتب tests: تأكد أن نفس الـ request مرتين لا تنشئ سجلّين

---

### اليوم 25 — Database Connection Pooling وPerformance

- [ ] اضبط SQLAlchemy connection pool: `pool_size=10`, `max_overflow=20`, `pool_timeout=30`
- [ ] أضف `pool_pre_ping=True` لإعادة الاتصال التلقائي بعد انقطاع الشبكة
- [ ] أضف indexes على columns المستخدمة في `WHERE` clauses — افحص بـ `EXPLAIN ANALYZE` في PostgreSQL
- [ ] أنشئ script: `scripts/check_slow_queries.sql` يجد queries أبطأ من 1 ثانية في pg_stat_statements
- [ ] وثّق النتائج في `docs/DB_PERFORMANCE.md`

---

### اليوم 26 — Error Handling وGlobal Exception Handler

- [ ] أنشئ `core/exceptions.py` بـ exception classes محددة: `TenantNotFound`, `Unauthorized`, `ValidationError`, `ExternalAPIError`
- [ ] أنشئ `@app.exception_handler` لكل exception type يعيد response منسّق ومنظّم
- [ ] تأكد أن الـ error responses لا تكشف stack traces في production (فقط في debug mode)
- [ ] أضف error tracking: كل 5xx error يُسجَّل في audit log ويُرسَل alert
- [ ] اكتب `tests/test_error_handling.py`: تأكد أن errors تعيد الـ format الصحيح

---

### اليوم 27 — Background Jobs وScheduling

- [ ] أنشئ `tasks/cleanup_tasks.py`: حذف expired tokens، تنظيف cache قديم، أرشفة audit logs قديمة
- [ ] أنشئ `tasks/notification_tasks.py`: إرسال emails، إشعارات WhatsApp (skeleton فقط الآن)
- [ ] اضبط Celery Beat schedule في `celery_config.py`: cleanup يومي 03:00، health check كل 5 دقائق
- [ ] أضف retry logic لكل task: max 3 retries، exponential backoff
- [ ] تحقق من Celery Flower dashboard أن كل tasks تعمل بدون failed jobs

---

### اليوم 28 (الجمعة) — مراجعة الأسبوع الرابع + Truth Registry v3

- [ ] **مراجعة أسبوعية:** نفّذ `verify_audit_chain` على DB الـ development وتأكد أنها سليمة
- [ ] **تحديث Truth Registry:** أضف: Audit Logs ✅، Hash Chain ✅، Idempotency ✅، Connection Pooling ✅
- [ ] شغّل `pytest --cov` — يجب أن تكون التغطية > 60% الآن
- [ ] راجع performance: `docker stats` أثناء load test بسيط بـ `locust`
- [ ] أنشئ `docs/WEEK4_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 4 Complete"

> **معلم الأسبوع 4:** Audit Hash Chain ✅ | Idempotency ✅ | DB Performance ✅ | Error Handling ✅

---

## الأسبوع 5 (أيام 29-35): Test Coverage وIntegration Tests

> **قاعدة Token Efficiency هذا الأسبوع:** `pytest -x --tb=short` يوقف عند أول فشل ويظهر خطأ موجز — أسرع من قراءة كل الـ output.

---

### اليوم 29 — Test Infrastructure

- [ ] أنشئ `conftest.py` شامل: fixtures للـ test DB، Redis mock، authenticated test client
- [ ] أنشئ `tests/factories.py` بـ factory_boy: `UserFactory`, `TenantFactory`, `DealFactory`
- [ ] اضبط pytest config في `pyproject.toml`: `asyncio_mode = "auto"`, `testpaths = ["tests"]`
- [ ] أنشئ test database منفصلة: `dealix_test` — لا تشارك أبداً مع dev DB
- [ ] تحقق أن `pytest` يعمل من صفر بدون أي setup manual: `docker compose run api pytest`

---

### اليوم 30 — Unit Tests للـ Core Modules

- [ ] اكتب unit tests لـ `core/auth.py`: token generation، token validation، refresh logic
- [ ] اكتب unit tests لـ `core/cache.py`: set/get/delete/TTL expiry
- [ ] اكتب unit tests لـ `core/audit.py`: hash chain generation وverification
- [ ] اكتب unit tests لـ `core/settings.py`: validation على missing vars
- [ ] نفّذ `pytest tests/unit/ --cov=core` وتأكد أن coverage > 85% على الـ core modules

---

### اليوم 31 — Integration Tests للـ Auth Endpoints

- [ ] اكتب integration test: register → login → access protected endpoint → refresh → logout
- [ ] اكتب integration test: RBAC — كل role يصل لما يُسمَح له فقط
- [ ] اكتب integration test: rate limiting — 6 محاولات login تعطي 429
- [ ] اكتب integration test: tenant isolation — tenant A لا يرى بيانات tenant B
- [ ] اكتب integration test: idempotency — نفس الـ key مرتين يعيد نفس الـ response

---

### اليوم 32 — Integration Tests للـ Business Logic

- [ ] اكتب integration test لـ deal creation flow الكامل
- [ ] اكتب integration test لـ audit log: action تنشئ audit entry بـ hash صحيح
- [ ] اكتب integration test لـ Celery tasks: task تُرسَل وتُنفَّذ
- [ ] اكتب integration test لـ cache: miss → DB → cache → hit
- [ ] نفّذ `pytest tests/integration/ --cov=app` وسجّل النتيجة

---

### اليوم 33 — Load Testing أولي

- [ ] ثبّت `locust`: `pip install locust`
- [ ] أنشئ `tests/load/locustfile.py` بـ scenarios: login، create deal، list deals
- [ ] شغّل load test: 50 users، 10 minutes وسجّل النتائج
- [ ] حدّد bottlenecks: أي endpoint أبطأ من 500ms تحت load؟
- [ ] وثّق النتائج في `docs/LOAD_TEST_RESULTS.md` مع recommendations

---

### اليوم 34 — Bug Fixes من نتائج الـ Tests

- [ ] اصلح أي failures من اليومين الماضيين — ابدأ بـ `pytest -x --tb=long` لتفصيل الأخطاء
- [ ] راجع الـ bottlenecks من load testing وأضف indexes مفقودة أو cache للـ slow queries
- [ ] أضف `pytest-benchmark` وقيس performance الـ core functions
- [ ] تأكد أن `docker compose down -v && docker compose up -d && pytest` يعمل بالكامل (clean run)
- [ ] أغلق جميع GitHub issues المرتبطة بالـ bugs المكتشفة

---

### اليوم 35 (الجمعة) — مراجعة الأسبوع الخامس + Truth Registry v4

- [ ] **مراجعة أسبوعية:** نفّذ `pytest --cov=app --cov-report=html` وافتح `htmlcov/index.html` — يجب أن التغطية ≥ 70%
- [ ] **تحديث Truth Registry:** أضف: Test Coverage ≥ 70% ✅، Load Testing ✅، Integration Tests ✅
- [ ] إذا التغطية < 70% — حدّد أكثر 3 modules غير مغطاة وأضف tests لها قبل نهاية اليوم
- [ ] أنشئ `docs/WEEK5_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 5 Complete"
- [ ] احتفل — المرحلة 2 مكتملة! Backend hardened وready للـ AI Agents

> **معلم الأسبوع 5:** Test Coverage ≥ 70% ✅ | Load Testing ✅ | Integration Tests ✅ | Backend Hardened ✅

---

## المرحلة 3: AI Agents (أسبوع 6–8)

---

## الأسبوع 6 (أيام 36-42): LLM Router والـ Orchestrator

> **قاعدة Token Efficiency هذا الأسبوع:** كل LLM call يجب أن يمر عبر الـ Router — لا تستدعِ Groq أو OpenAI مباشرة من الـ agent code. استخدم prompt caching للـ system prompts الثابتة.

---

### اليوم 36 — LLM Router Architecture

- [ ] أنشئ `agents/llm_router.py`: class `LLMRouter` يقبل provider priority list
- [ ] Primary: Groq (llama-3.3-70b)، Fallback: OpenAI (gpt-4o-mini) — لا تستخدم gpt-4 لتوفير tokens
- [ ] أضف logic: إذا Groq أعاد error أو timeout > 10s، انتقل لـ OpenAI تلقائياً
- [ ] سجّل في كل LLM call: `provider`, `model`, `prompt_tokens`, `completion_tokens`, `cost_usd`, `latency_ms`
- [ ] اكتب `tests/test_llm_router.py`: test fallback logic مع mock للـ APIs

---

### اليوم 37 — Token Tracking وBudget Control

- [ ] أنشئ `agents/token_tracker.py`: يحسب token consumption لكل tenant يومياً وشهرياً
- [ ] خزّن token usage في Redis مع daily rollup في PostgreSQL
- [ ] أضف tenant budget limits: إذا تجاوز tenant الـ daily limit، أوقف LLM calls وأرسل alert
- [ ] أنشئ endpoint `GET /api/v1/usage/tokens` يعرض استهلاك tokens للـ tenant
- [ ] اكتب dashboard widget (JSON) يعرض: tokens هذا الشهر، التكلفة المتوقعة، النسبة من الـ budget

---

### اليوم 38 — Prompt Caching

- [ ] أنشئ `agents/prompt_cache.py`: يخزّن system prompts في Redis بـ hash key
- [ ] Cache key = `sha256(system_prompt + model_name)` — TTL 24 ساعة
- [ ] قبل كل LLM call: تحقق من الـ cache أولاً، إذا موجود أرسل `cache_control: {"type": "ephemeral"}` لـ Anthropic أو استخدم prefix caching في Groq
- [ ] Track cache hit rate: `prompt_cache_hits / total_llm_calls` — هدف > 40%
- [ ] اكتب `tests/test_prompt_cache.py`: تحقق أن system prompts لا تُرسَل كاملة مرتين

---

### اليوم 39 — Orchestrator Agent

- [ ] أنشئ `agents/orchestrator.py`: يستقبل task، يحدد أي agent يُستدعى، يعيد النتيجة
- [ ] أضف routing logic: بناءً على `task_type`، ابعث للـ agent الصحيح
- [ ] أضف circuit breaker: إذا agent فشل 3 مرات متتالية، disable مؤقتاً لـ 5 دقائق
- [ ] أنشئ state machine بسيطة للـ task lifecycle: `pending → in_progress → completed | failed`
- [ ] اكتب tests: Orchestrator يوجّه بشكل صحيح وينقل state بشكل صحيح

---

### اليوم 40 — Researcher Agent

- [ ] أنشئ `agents/researcher.py`: يبحث عن معلومات الشركة المستهدفة من مصادر متعددة
- [ ] أضف input validation: company name, website, LinkedIn URL
- [ ] أنشئ structured output schema (Pydantic): `CompanyProfile` بحقول: name, industry, size, location, pain_points
- [ ] أضف rate limiting لـ external API calls (لا تجاوز 10 requests/minute لأي source)
- [ ] اكتب tests: mock الـ external APIs وتحقق أن الـ output يطابق `CompanyProfile` schema

---

### اليوم 41 — Qualifier Agent

- [ ] أنشئ `agents/qualifier.py`: يقيّم مدى ملاءمة prospect للمنتج (fit score 0-100)
- [ ] Scoring criteria: company size، industry، budget signals، decision maker presence
- [ ] أنشئ structured output: `QualificationResult` مع score، reasoning بالعربي، recommended action
- [ ] أضف explanation للـ score — لا يكفي رقم، يجب تفسير سبب التقييم
- [ ] اكتب tests: حالات مختلفة (fit عالي، fit منخفض، بيانات ناقصة)

---

### اليوم 42 (الجمعة) — مراجعة الأسبوع السادس + Truth Registry v5

- [ ] **مراجعة أسبوعية:** قيس average token cost لكل agent call — سجّل في `docs/TOKEN_COSTS.md`
- [ ] **تحديث Truth Registry:** أضف: LLM Router ✅، Token Tracking ✅، Prompt Caching ✅، Orchestrator ✅، Researcher ✅، Qualifier ✅
- [ ] تحقق أن fallback من Groq لـ OpenAI يعمل فعلاً (اختبر بـ mock Groq timeout)
- [ ] أنشئ `docs/WEEK6_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 6 Complete"
- [ ] تأكد أن token budget control يعمل — لا تترك tenant يستنفد budget بدون warning

> **معلم الأسبوع 6:** LLM Router مع Fallback ✅ | Token Tracking ✅ | Orchestrator ✅ | 3 Agents جاهزة ✅

---

## الأسبوع 7 (أيام 43-49): باقي الـ Agents

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم structured outputs بدلاً من free-form text — تقلل hallucination وتقلل tokens اللازمة للـ parsing. اضبط `max_tokens` لكل agent call على أقل قيمة كافية.

---

### اليوم 43 — Outreach Agent

- [ ] أنشئ `agents/outreach.py`: يكتب رسائل تواصل مخصصة بالعربي لكل prospect
- [ ] Templates: LinkedIn message، WhatsApp message، Email — كل واحدة بـ max tokens مختلف
- [ ] أضف personalization tokens: `{company_name}`, `{pain_point}`, `{decision_maker_name}`
- [ ] أنشئ A/B variants: لكل prospect، أنشئ نسختين مختلفتين للمقارنة لاحقاً
- [ ] اكتب tests: تحقق أن الرسائل تحتوي على الـ personalization tokens المطلوبة

---

### اليوم 44 — Closer Agent

- [ ] أنشئ `agents/closer.py`: يحلل مرحلة الـ deal ويقترح الخطوة التالية لإغلاق البيع
- [ ] Input: deal history، prospect responses، current stage
- [ ] Output: recommended action، talking points بالعربي، objection handlers
- [ ] أضف deal stage detection: Awareness → Interest → Consideration → Decision → Closed
- [ ] اكتب tests: scenarios مختلفة من الـ sales funnel

---

### اليوم 45 — Compliance Agent

- [ ] أنشئ `agents/compliance.py`: يفحص كل outreach message للتوافق مع PDPL وـ NCA
- [ ] أضف rules: لا تُرسَل معلومات شخصية بدون موافقة، لا claims كاذبة، لا spam patterns
- [ ] أضف Arabic text analysis للكشف عن محتوى قد يكون sensitive
- [ ] Integration مع Outreach Agent: كل رسالة تمر على Compliance قبل الإرسال
- [ ] اكتب tests: رسائل تخالف القواعد يجب أن تُرفَض مع تفسير سبب الرفض

---

### اليوم 46 — Analytics Agent

- [ ] أنشئ `agents/analytics.py`: يحلل performance الـ sales pipeline ويقترح تحسينات
- [ ] Metrics: conversion rate per stage، average deal size، top performing segments
- [ ] Output: weekly analytics report بالعربي في format مناسب للـ dashboard
- [ ] أضف anomaly detection: إذا conversion rate انخفض > 20% هذا الأسبوع، أنشئ alert
- [ ] اكتب tests: mock data → تحقق أن الـ analytics صحيحة رياضياً

---

### اليوم 47 — WhatsApp Agent

- [ ] أنشئ `agents/whatsapp.py`: يدير conversation flow عبر WhatsApp Business API
- [ ] أضف message templates المعتمدة مسبقاً (WhatsApp يتطلب pre-approved templates للـ outbound)
- [ ] أضف conversation state machine: `initial_contact → responded → meeting_scheduled → deal_created`
- [ ] أضف opt-out handler: إذا أرسل العميل "لا" أو "توقف"، أوقف كل رسائل هذا الـ contact
- [ ] اكتب tests: conversation flow كامل مع mock WhatsApp API

---

### اليوم 48 — Agent Integration Tests

- [ ] اكتب integration test لـ full pipeline: Orchestrator → Researcher → Qualifier → Outreach → Compliance
- [ ] تحقق أن الـ circuit breaker يعمل: أوقف agent وتأكد أن الـ Orchestrator يتعامل معه صح
- [ ] قيس total tokens لـ full pipeline run — يجب أن لا يتجاوز 5,000 tokens لكل prospect
- [ ] تحقق أن كل agent يخزّن نتيجته في DB للـ audit trail
- [ ] وثّق average latency لكل agent في `docs/AGENT_PERFORMANCE.md`

---

### اليوم 49 (الجمعة) — مراجعة الأسبوع السابع + Truth Registry v6

- [ ] **مراجعة أسبوعية:** قيس end-to-end pipeline latency — target < 30 ثانية لكل prospect
- [ ] **تحديث Truth Registry:** أضف: Outreach ✅، Closer ✅، Compliance ✅، Analytics ✅، WhatsApp ✅
- [ ] تحقق أن جميع الـ 8 agents تعمل وتمر tests
- [ ] نفّذ `pytest tests/agents/ --cov=agents` — target > 70% coverage
- [ ] أنشئ `docs/WEEK7_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 7 Complete"

> **معلم الأسبوع 7:** جميع الـ 8 Agents جاهزة ✅ | Integration Tests ✅ | Token Budget < 5K/prospect ✅

---

## الأسبوع 8 (أيام 50-56): Agent Optimization وToken Efficiency

> **قاعدة Token Efficiency هذا الأسبوع:** profile كل agent بـ `cProfile` وحدد أين الوقت يُصرَف. استخدم `async` بالكامل للـ LLM calls المتوازية.

---

### اليوم 50 — Async Parallelization

- [ ] حوّل كل agent calls لـ `async def` إذا لم تكن كذلك
- [ ] استخدم `asyncio.gather()` لتشغيل Researcher وQualifier بالتوازي بدلاً من التسلسل
- [ ] قيس التحسن: `before_async_latency` vs `after_async_latency` في `docs/ASYNC_IMPROVEMENT.md`
- [ ] تأكد أن DB sessions thread-safe مع async: استخدم `AsyncSession` من SQLAlchemy
- [ ] اكتب test: تحقق أن التوازي لا يتسبب في race conditions

---

### اليوم 51 — Prompt Optimization

- [ ] راجع كل system prompt للـ 8 agents — احسب token count لكل prompt: `len(encoding.encode(prompt))`
- [ ] أزل الجمل الزائدة وكرر هذا: "هل هذه الجملة ضرورية؟" لكل سطر في الـ prompt
- [ ] هدف: قلّل كل system prompt بـ 20% دون تغيير الأداء — اختبر بـ same test cases
- [ ] وثّق token counts قبل وبعد في `docs/PROMPT_OPTIMIZATION.md`
- [ ] أضف `max_tokens` parameter لكل agent call: Qualifier → 500، Outreach → 300، Analytics → 1000

---

### اليوم 52 — Response Caching للـ Agents

- [ ] أنشئ `agents/agent_cache.py`: cache نتائج الـ agents بـ hash(input) كـ key
- [ ] Researcher: cache نتائج بحث الشركة لمدة 7 أيام (معلومات الشركة نادراً ما تتغير)
- [ ] Qualifier: cache score لمدة 24 ساعة لنفس بيانات الـ prospect
- [ ] أضف cache invalidation عند تحديث بيانات الـ prospect
- [ ] قيس cache hit rate بعد يوم كامل من الاستخدام — target > 30%

---

### اليوم 53 — Error Recovery وGraceful Degradation

- [ ] أنشئ `agents/fallback_responses.py`: ردود افتراضية عندما كل الـ LLMs تفشل
- [ ] أضف قائمة pre-written Arabic messages للـ Outreach Agent كـ fallback
- [ ] أنشئ user notification عندما agent يعمل بـ degraded mode: "يعمل بشكل محدود حالياً"
- [ ] اختبر: أوقف Groq وOpenAI معاً وتحقق أن التطبيق لا يكرش — يُظهر رسالة مناسبة
- [ ] اكتب test: `test_graceful_degradation.py` لكل سيناريو فشل

---

### اليوم 54 — Agent Monitoring Dashboard Data

- [ ] أنشئ endpoint `GET /api/v1/agents/status` يعرض: حالة كل agent، آخر run، success rate
- [ ] أنشئ endpoint `GET /api/v1/agents/metrics` يعرض: tokens/day، cost/day، avg latency
- [ ] خزّن metrics في time-series format في Redis: `agent:researcher:tokens:2024-01-15 = 15000`
- [ ] أنشئ aggregate endpoint: `GET /api/v1/agents/summary?period=7d` للـ weekly summary
- [ ] اكتب tests لجميع الـ metrics endpoints

---

### اليوم 55 — Webhook وReal-time Updates

- [ ] أنشئ WebSocket endpoint: `WS /ws/agent-updates/{tenant_id}` لإرسال updates فورية
- [ ] عندما ينتهي agent من task، أرسل update عبر WebSocket للـ frontend
- [ ] أضف authentication للـ WebSocket: تحقق من JWT token في connection headers
- [ ] أضف reconnection logic: إذا انقطع الاتصال، يعيد المحاولة كل 5 ثواني
- [ ] اكتب test: `test_websocket_updates.py` يتحقق أن messages تصل بشكل صحيح

---

### اليوم 56 (الجمعة) — مراجعة الأسبوع الثامن + Truth Registry v7

- [ ] **مراجعة أسبوعية:** قيس مقارنة tokens/prospect هذا الأسبوع vs الأسبوع 7 — يجب أن تنخفض
- [ ] **تحديث Truth Registry:** أضف: Async Parallelization ✅، Prompt Optimization ✅، Agent Caching ✅، Graceful Degradation ✅
- [ ] شغّل full pipeline end-to-end test وسجّل: latency، tokens، cost
- [ ] أنشئ `docs/WEEK8_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 8 Complete"
- [ ] احتفل — المرحلة 3 مكتملة! AI Agents جاهزة ومحسّنة

> **معلم الأسبوع 8:** Async Parallelization ✅ | Prompts محسّنة -20% tokens ✅ | Agent Monitoring ✅

---

## المرحلة 4: Frontend وRTL (أسبوع 9–10)

---

## الأسبوع 9 (أيام 57-63): Arabic-First UI

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم TypeScript strict mode — يوفّر debug time لاحقاً. استخدم `tsc --noEmit` للتحقق من الأخطاء بدون بناء كامل.

---

### اليوم 57 — Next.js RTL Setup

- [ ] تحقق أن `tailwind.config.ts` يدعم RTL: `dir: 'rtl'` في الـ config
- [ ] أضف `<html lang="ar" dir="rtl">` في `app/layout.tsx`
- [ ] اختر Arabic font مناسب: `IBM Plex Sans Arabic` أو `Noto Kufi Arabic` — أضف في `next/font`
- [ ] تحقق أن جميع الـ margins والـ paddings تنعكس صح في RTL: `ms-4` بدلاً من `ml-4`
- [ ] أنشئ `components/RTLProvider.tsx` يغلف التطبيق ويضبط direction تلقائياً

---

### اليوم 58 — Design System Components

- [ ] أنشئ `components/ui/Button.tsx` بـ variants: primary، secondary، ghost، danger — كل شيء RTL compatible
- [ ] أنشئ `components/ui/Input.tsx` يدعم Arabic text و placeholder بالعربي
- [ ] أنشئ `components/ui/Table.tsx` مع RTL-aware sorting icons
- [ ] أنشئ `components/ui/Modal.tsx` بـ close button في اليسار (RTL standard)
- [ ] أنشئ `components/ui/Alert.tsx` بـ variants: info، success، warning، error — مع أيقونات

---

### اليوم 59 — Authentication Pages

- [ ] أنشئ `app/(auth)/login/page.tsx`: نموذج تسجيل دخول بالعربي مع validation
- [ ] أنشئ `app/(auth)/register/page.tsx`: نموذج تسجيل بالعربي (اسم الشركة، الاسم، البريد، كلمة المرور)
- [ ] أنشئ `app/(auth)/forgot-password/page.tsx`: استعادة كلمة المرور
- [ ] أضف loading states لكل form submission
- [ ] تحقق أن الـ forms تعمل صح على الموبايل (responsive RTL)

---

### اليوم 60 — Dashboard الرئيسي

- [ ] أنشئ `app/(dashboard)/page.tsx`: لوحة تحكم رئيسية بـ KPI cards
- [ ] KPI Cards: عدد الـ deals، conversion rate، revenue هذا الشهر، active prospects
- [ ] أضف recent activity feed: آخر 10 actions في الـ pipeline
- [ ] أنشئ `components/dashboard/AgentStatusWidget.tsx`: حالة الـ 8 agents (green/yellow/red)
- [ ] تحقق أن البيانات تُجلَب من الـ API endpoints التي بنيتها في الأسبوع 8

---

### اليوم 61 — Sales Pipeline View

- [ ] أنشئ `app/(dashboard)/pipeline/page.tsx`: Kanban board بـ 5 stages
- [ ] كل card يعرض: اسم الشركة، القيمة المتوقعة، آخر activity، agent recommendation
- [ ] أضف drag-and-drop بين stages (استخدم `@dnd-kit/core`)
- [ ] أضف RTL-aware drag handling (drag من اليمين لليسار)
- [ ] أنشئ API call لتحديث stage عند drop: `PATCH /api/v1/deals/{id}/stage`

---

### اليوم 62 — Prospects Management

- [ ] أنشئ `app/(dashboard)/prospects/page.tsx`: قائمة prospects مع search وfilter
- [ ] أضف Arabic search: البحث يعمل بالأحرف العربية بدون مشاكل encoding
- [ ] أنشئ `app/(dashboard)/prospects/[id]/page.tsx`: تفاصيل prospect مع agent insights
- [ ] أضف "إضافة prospect" modal مع validation كامل
- [ ] أضف export: تصدير prospects كـ CSV بـ Arabic columns

---

### اليوم 63 (الجمعة) — مراجعة الأسبوع التاسع + Truth Registry v8

- [ ] **مراجعة أسبوعية:** اختبر كل page يدوياً على Chrome وSafari، موبايل وديسك توب
- [ ] **تحديث Truth Registry:** أضف: RTL Setup ✅، Auth Pages ✅، Dashboard ✅، Pipeline ✅، Prospects ✅
- [ ] شغّل `tsc --noEmit` — يجب أن لا يكون هناك TypeScript errors
- [ ] أنشئ `docs/WEEK9_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 9 Complete"
- [ ] خذ screenshots للـ dashboard وأضفها في `docs/screenshots/` للمرجع

> **معلم الأسبوع 9:** Arabic-First UI ✅ | RTL Layout ✅ | Dashboard ✅ | Pipeline View ✅

---

## الأسبوع 10 (أيام 64-70): Onboarding وAccessibility

> **قاعدة Token Efficiency هذا الأسبوع:** استخدم `next build && next start` لاختبار production build — يكشف مشاكل لا تظهر في dev mode.

---

### اليوم 64 — Onboarding Wizard

- [ ] أنشئ `app/(onboarding)/setup/page.tsx`: wizard من 5 خطوات
- [ ] الخطوة 1: معلومات الشركة (الاسم، القطاع، الحجم)
- [ ] الخطوة 2: إعداد الفريق (دعوة أعضاء)
- [ ] الخطوة 3: ربط WhatsApp Business API
- [ ] الخطوة 4: رفع أول قائمة prospects (CSV)
- [ ] الخطوة 5: تشغيل أول pipeline وعرض النتائج

---

### اليوم 65 — Token Usage Dashboard

- [ ] أنشئ `app/(dashboard)/usage/page.tsx`: لوحة استهلاك tokens
- [ ] Charts: tokens/day (آخر 30 يوم)، تكلفة هذا الشهر، breakdown بالـ agent
- [ ] أضف budget alerts: تحذير عند وصول 80% من الـ monthly budget
- [ ] استخدم `recharts` أو `chart.js` للـ charts — تأكد أنها RTL compatible
- [ ] أضف "تصدير التقرير" PDF functionality

---

### اليوم 66 — Settings وConfiguration

- [ ] أنشئ `app/(dashboard)/settings/page.tsx`: إعدادات الحساب والـ tenant
- [ ] قسم: معلومات الشركة، إعدادات الـ AI، حدود الـ budget، إعدادات الإشعارات
- [ ] أضف "تغيير كلمة المرور" flow كامل
- [ ] أضف "إدارة الأعضاء": دعوة، تغيير role، إلغاء وصول
- [ ] تأكد أن Settings يحتاج RBAC: فقط `tenant_admin` يمكنه تغيير الإعدادات

---

### اليوم 67 — Notifications وAlerts

- [ ] أنشئ `components/Notifications.tsx`: bell icon في الـ header بـ unread count
- [ ] أنشئ `app/(dashboard)/notifications/page.tsx`: قائمة الإشعارات كاملة
- [ ] أنواع الإشعارات: deal تقدّم، agent انتهى، budget alert، compliance warning
- [ ] أضف "تحديد الكل كمقروء" و"حذف الكل"
- [ ] أضف WebSocket connection للإشعارات الفورية (استخدم الـ WS endpoint من اليوم 55)

---

### اليوم 68 — Accessibility WCAG AA

- [ ] ثبّت `@axe-core/react` وأضفه في development mode فقط
- [ ] أصلح كل aria-label مفقودة: `npx axe http://localhost:3000 --dir docs/a11y_report`
- [ ] تأكد أن color contrast ratio ≥ 4.5:1 لكل النصوص (استخدم Chrome DevTools accessibility)
- [ ] تأكد أن keyboard navigation يعمل كامل: Tab، Enter، Escape، Arrow keys
- [ ] تحقق أن screen readers تقرأ العربية بشكل صحيح (اختبر بـ NVDA أو macOS VoiceOver)

---

### اليوم 69 — Mobile Responsiveness

- [ ] اختبر كل page على: 375px (iPhone SE)، 768px (iPad)، 1440px (Desktop)
- [ ] أصلح أي layout issues في RTL على الموبايل (خصوصاً navigation وtables)
- [ ] أضف `PWA` support: `next-pwa` package، manifest.json بالعربي
- [ ] اختبر offline mode: يجب أن تظهر رسالة واضحة "لا يوجد اتصال بالإنترنت"
- [ ] تحقق أن الـ touch targets كلها ≥ 44px × 44px (Apple Human Interface Guidelines)

---

### اليوم 70 (الجمعة) — مراجعة الأسبوع العاشر + Truth Registry v9

- [ ] **مراجعة أسبوعية:** شغّل `next build` — يجب أن يكتمل بدون errors أو warnings مهمة
- [ ] **تحديث Truth Registry:** أضف: Onboarding Wizard ✅، Accessibility WCAG AA ✅، Mobile Responsive ✅، PWA ✅
- [ ] شغّل Lighthouse audit: `npx lighthouse http://localhost:3000 --view` — target > 85 لكل scores
- [ ] أنشئ `docs/WEEK10_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 10 Complete"
- [ ] احتفل — المرحلة 4 مكتملة! Frontend جاهز بالكامل

> **معلم الأسبوع 10:** WCAG AA ✅ | Mobile RTL ✅ | Onboarding Wizard ✅ | Lighthouse > 85 ✅

---

## المرحلة 5: Compliance وLegal (أسبوع 11)

---

## الأسبوع 11 (أيام 71-77): ZATCA وPDPL وSDAIA

> **قاعدة Token Efficiency هذا الأسبوع:** وثّق كل compliance decision في `docs/COMPLIANCE_DECISIONS.md` — هذا السجل سيوفّر ساعات من الشرح للمدققين لاحقاً.

---

### اليوم 71 — ZATCA E-Invoicing

- [ ] راجع ZATCA Phase 2 requirements: `fetch_url("https://zatca.gov.sa/en/E-Invoicing")` وسجّل المتطلبات في `docs/ZATCA_REQUIREMENTS.md`
- [ ] أنشئ `services/zatca_invoice.py`: إنشاء XML invoice بـ UBL 2.1 format المطلوب من ZATCA
- [ ] أضف required fields: seller TRN، buyer TRN، invoice type code، line items، VAT 15%
- [ ] أضف digital signature على الـ invoice XML (استخدم ZATCA SDK أو implement manually)
- [ ] اكتب test: أنشئ invoice sample وتحقق أنه يتوافق مع ZATCA XML schema

---

### اليوم 72 — ZATCA API Integration

- [ ] أنشئ `services/zatca_client.py`: HTTP client للـ ZATCA Fatoora API
- [ ] Implement: `report_invoice(xml)` للـ B2B invoices (Phase 2 reporting)
- [ ] أضف error handling: ZATCA API قد يكون بطيئاً — timeout 30s، retry 3 مرات
- [ ] أضف logging لكل ZATCA submission مع الـ response UUID
- [ ] اكتب test مع ZATCA sandbox API (إذا متاح) أو mock الـ responses

---

### اليوم 73 — PDPL Compliance (Personal Data Protection Law)

- [ ] أنشئ `docs/PDPL_CHECKLIST.md`: قائمة متطلبات PDPL السعودي لـ SaaS
- [ ] أنشئ endpoint `GET /api/v1/privacy/data-export/{user_id}`: تصدير كل بيانات المستخدم (Data Subject Access Request)
- [ ] أنشئ endpoint `DELETE /api/v1/privacy/delete/{user_id}`: حذف كل البيانات (Right to Erasure)
- [ ] تأكد أن الحذف شامل: DB، Redis، audit logs (anonymize بدلاً من حذف لأغراض قانونية)
- [ ] أضف consent tracking: كل user يوافق على Privacy Policy عند التسجيل — سجّل: timestamp، IP، version

---

### اليوم 74 — سياسة الخصوصية والشروط والأحكام

- [ ] اكتب Privacy Policy بالعربي في `docs/legal/PRIVACY_POLICY_AR.md` — تغطي: ما نجمعه، كيف نستخدمه، حقوق المستخدم، PDPL compliance
- [ ] اكتب Terms of Service بالعربي في `docs/legal/TERMS_OF_SERVICE_AR.md` — تغطي: الاستخدام المقبول، المسؤولية، إلغاء الخدمة، الدفع
- [ ] اكتب DPA (Data Processing Agreement) template في `docs/legal/DPA_TEMPLATE_AR.md`
- [ ] أنشئ صفحات في Frontend: `/privacy` و`/terms` بـ نص قابل للقراءة وـ updated date
- [ ] أضف "آخر تحديث: [التاريخ]" في كل وثيقة قانونية

---

### اليوم 75 — NCA وSDIAIA Compliance

- [ ] راجع NCA Essential Cybersecurity Controls (ECC) للـ SaaS — سجّل المتطلبات ذات الصلة في `docs/NCA_COMPLIANCE.md`
- [ ] تحقق من المتطلبات التقنية: encryption at rest (PostgreSQL TDE أو disk encryption)، encryption in transit (TLS 1.2+)
- [ ] أضف TLS configuration في nginx/caddy config: فقط TLS 1.2 و 1.3، لا SSLv3 أو TLS 1.0/1.1
- [ ] وثّق data residency: أين تُخزَّن البيانات (يجب أن تكون في السعودية للامتثال) — استخدم AWS Riyadh region
- [ ] أنشئ `docs/SDAIA_AI_GOVERNANCE.md`: كيف يتوافق الـ AI مع توجيهات SDAIA للذكاء الاصطناعي

---

### اليوم 76 — Data Retention وDeletion Policies

- [ ] أنشئ `docs/DATA_RETENTION_POLICY.md`: كم نحتفظ بكل نوع بيانات
- [ ] Defaults: audit logs = 7 سنوات (متطلب قانوني)، personal data = 3 سنوات بعد انتهاء العقد، logs = 90 يوم
- [ ] أنشئ Celery task: `retention_cleanup_task` تعمل شهرياً وتحذف/تعمّي البيانات منتهية الصلاحية
- [ ] أضف soft delete بدلاً من hard delete لـ 30 يوم — لإمكانية الاسترجاع
- [ ] اكتب test: تأكد أن بيانات منتهية الصلاحية تُحذَف فعلاً بعد الـ retention period

---

### اليوم 77 (الجمعة) — مراجعة الأسبوع الحادي عشر + Truth Registry v10

- [ ] **مراجعة أسبوعية:** راجع كل `docs/legal/*.md` — هل تغطي كل المطالب؟ هل تحتاج مراجعة محامٍ؟
- [ ] **تحديث Truth Registry:** أضف: ZATCA ✅، PDPL ✅، Privacy Policy ✅، Terms of Service ✅، NCA ✅
- [ ] تأكد أن Privacy Policy وTerms of Service موجودة في الـ frontend قبل launch
- [ ] أنشئ `docs/WEEK11_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 11 Complete"
- [ ] **تذكير:** لا تدّعي أي compliance "معتمد رسمياً" بدون شهادة رسمية — وثّق "نسعى للامتثال مع [الجهة]" فقط

> **معلم الأسبوع 11:** ZATCA E-Invoicing ✅ | PDPL Data Rights ✅ | Legal Documents ✅ | NCA Controls ✅

---

## المرحلة 6: Go-to-Market Prep (أسبوع 12)

---

## الأسبوع 12 (أيام 78-84): التهيئة للإطلاق

> **قاعدة Token Efficiency هذا الأسبوع:** كل محتوى تسويقي يمر على Compliance Agent قبل النشر — تجنّب أي claims قد تكون مضللة.

---

### اليوم 78 — Landing Page

- [ ] أنشئ `app/(marketing)/page.tsx`: صفحة رئيسية بالعربي
- [ ] Sections: Hero (القيمة المقترحة)، Features (8 agents بشرح بسيط)، Pricing (1,499 ريال/شهر)، CTA
- [ ] Hero text: جملة واضحة تشرح ما يفعله Dealix في أقل من 15 كلمة بالعربي
- [ ] أضف "طلب تجربة مجانية" form يحفظ البيانات في DB ويرسل email تلقائي
- [ ] تأكد أن صفحة الـ landing تحمّل في < 3 ثواني (Next.js static generation)

---

### اليوم 79 — Pricing Page

- [ ] أنشئ `app/(marketing)/pricing/page.tsx`: صفحة تسعير شفافة
- [ ] خطة واحدة: 1,499 ريال/شهر — أذكر ما يشمل وما لا يشمل بوضوح
- [ ] أضف FAQ بالعربي: "ما هو حد الـ tokens؟"، "هل هناك عقد؟"، "كيف يعمل الإلغاء؟"
- [ ] أضف مقارنة "بدون Dealix / مع Dealix" في جدول واضح
- [ ] لا تكتب "وفّر [رقم]% من وقتك" بدون بيانات تدعمه — اكتب "يعتمد على حجم pipeline" بدلاً من ذلك

---

### اليوم 80 — Demo Video Script وRecording

- [ ] اكتب script الـ demo video بالعربي (3-5 دقائق): مشكلة → حل → كيف Dealix يحلها
- [ ] Flow الـ demo: إضافة prospect → Researcher يبحث → Qualifier يقيّم → Outreach يكتب رسالة → Closer يقترح خطوة
- [ ] سجّل الـ demo video بشاشة حقيقية (لا slides) — استخدم OBS أو Loom
- [ ] أضف subtitles بالعربي وـ thumbnail جذّاب
- [ ] ارفع الفيديو على YouTube أو Vimeo وأضفه في Landing Page

---

### اليوم 81 — Sales Collateral بالعربي

- [ ] أنشئ `docs/sales/ONE_PAGER_AR.md`: ورقة واحدة تشرح Dealix للـ decision makers
- [ ] أنشئ `docs/sales/PITCH_DECK_OUTLINE_AR.md`: هيكل عرض تقديمي 10 slides
- [ ] أنشئ `docs/sales/ROI_CALCULATOR.md`: كيف يحسب العميل الـ ROI من Dealix
- [ ] أنشئ email template بالعربي لأول تواصل مع pilot customers
- [ ] تأكد أن جميع المستندات خالية من claims لا يمكن إثباتها (لا "100%"، لا "الأفضل في السوق")

---

### اليوم 82 — Pilot Customer Outreach (3 عملاء)

- [ ] حدّد 3 شركات سعودية مناسبة كـ pilot customers: B2B، فريق sales موجود، تقدّر تتواصل معهم
- [ ] أنشئ profile لكل شركة في Dealix (لتجربة المنصة بيانات حقيقية)
- [ ] أرسل رسالة تواصل مخصصة لكل شركة عبر LinkedIn أو email المباشر
- [ ] الهدف من الـ pilot: feedback حقيقي + testimonials + case study
- [ ] وثّق حالة كل outreach في `docs/PILOT_CUSTOMERS.md`

---

### اليوم 83 — Production Environment Setup

- [ ] أنشئ production environment في AWS (Riyadh region) أو بديل سعودي
- [ ] Setup: RDS PostgreSQL 16، ElastiCache Redis 7، ECS أو EC2 للـ API، Vercel للـ frontend
- [ ] اضبط DNS وـ SSL certificate: `dealix.sa` أو domain المختار
- [ ] أضف CDN للـ static assets (CloudFront أو Cloudflare)
- [ ] شغّل `docker compose -f docker-compose.prod.yml up -d` على production server وتحقق من health checks

---

### اليوم 84 (الجمعة) — مراجعة الأسبوع الثاني عشر + Truth Registry v11

- [ ] **مراجعة أسبوعية:** راجع Landing Page، Pricing Page، Demo Video — هل هي جاهزة للعملاء؟
- [ ] **تحديث Truth Registry:** أضف: Landing Page ✅، Pricing Page ✅، Demo Video ✅، Sales Collateral ✅، Production Environment ✅
- [ ] تأكد أن production environment يعمل كامل بدون errors
- [ ] أنشئ `docs/WEEK12_RETROSPECTIVE.md` وأغلق GitHub Milestone "Week 12 Complete"
- [ ] أرسل reminder للـ pilot customers الـ 3 الذين تواصلت معهم

> **معلم الأسبوع 12:** Landing Page ✅ | Demo Video ✅ | Production Environment ✅ | 3 Pilot Outreach ✅

---

## المرحلة 7: التدشين (أسبوع 13)

---

## الأسبوع 13 (أيام 85-90): Soft Launch

> **قاعدة Token Efficiency هذا الأسبوع:** monitoring first — قبل الإعلان عن الإطلاق، تأكد أن كل المقاييس تُسجَّل. لا تدّع أي شيء "stable" قبل 30 يوم telemetry.

---

### اليوم 85 — Telemetry وMonitoring Setup

- [ ] أضف Sentry للـ error tracking: Backend (`sentry-sdk`) وFrontend (`@sentry/nextjs`)
- [ ] اضبط alerts: Sentry يرسل email/Slack عند كل unhandled exception
- [ ] أضف uptime monitoring (UptimeRobot أو Better Uptime): ping `/health` كل دقيقة
- [ ] أضف Prometheus + Grafana dashboard لـ production metrics: CPU، Memory، Request rate، Error rate
- [ ] تحقق أن جميع الـ metrics تُسجَّل: `curl http://production-url/metrics | head -50`

---

### اليوم 86 — Pre-launch Security Audit

- [ ] شغّل `bandit -r app/ -f html -o docs/final_security_audit.html` وأصلح كل High severity issues
- [ ] تحقق أن لا secrets مكشوفة: `git log --all --grep="password\|api_key\|secret" --oneline`
- [ ] اختبر OWASP Top 10 يدوياً: SQL injection، XSS، CSRF، broken auth، insecure direct object reference
- [ ] تحقق أن SSL certificate صحيح: `curl -v https://dealix.sa 2>&1 | grep -E "SSL|TLS|expire"`
- [ ] وثّق نتائج الـ security audit في `docs/SECURITY_AUDIT_FINAL.md`

---

### اليوم 87 — Soft Launch للـ Pilot Customers

- [ ] أرسل دعوة رسمية للـ pilot customers الـ 3 مع credentials مخصصة لكل منهم
- [ ] أنشئ Slack channel أو WhatsApp group للـ pilot feedback
- [ ] ابق متاحاً لمدة 8 ساعات للرد على أي مشاكل فورية
- [ ] وثّق كل feedback في `docs/PILOT_FEEDBACK.md` فور وصوله
- [ ] لا تعلن عن الـ launch علناً حتى الآن — هذا soft launch للـ pilot فقط

---

### اليوم 88 — Bug Fixes من الـ Pilot Feedback

- [ ] صنّف الـ bugs: Critical (block core flow)، Major (annoyance)، Minor (cosmetic)
- [ ] أصلح كل Critical bugs فوراً — deploy hotfix في نفس اليوم
- [ ] أضف كل الـ feedback كـ GitHub issues مع labels مناسبة
- [ ] تحقق من logs الـ production: `docker logs api --since 24h | grep ERROR | head -50`
- [ ] أرسل update للـ pilot customers: "اكتشفنا وأصلحنا [X] مشكلة شكراً لـ feedback كم"

---

### اليوم 89 — First Paying Customer

- [ ] راجع حالة الـ 3 pilot customers: أيهم أكثر engagement؟
- [ ] تحدّث مع الأكثر engagement واقترح تحويل الـ pilot لاشتراك مدفوع
- [ ] أعدّ ZATCA-compliant invoice بالـ 1,499 ريال + VAT 15% = 1,723.85 ريال
- [ ] أضف payment gateway (Moyassar أو HyperPay للسوق السعودي)
- [ ] وثّق "أول عميل مدفوع" في `docs/FIRST_CUSTOMER.md` — تاريخ، الشركة (مجهّلة)، التحديات، الدروس

---

### اليوم 90 (الجمعة) — مراجعة الـ 90 يوم + Post-mortem

- [ ] **مراجعة أسبوعية نهائية:** مقارنة الوضع في اليوم 1 vs اليوم 90 — كم LOC أضفت؟ كم test؟ كم endpoint؟
- [ ] **تحديث Truth Registry النهائي:** وثّق الحالة الكاملة للمشروع — ما يعمل ✅، ما يحتاج 30 يوم telemetry ⏳، ما لم يُنجَز ❌
- [ ] اكتب `docs/90DAY_POSTMORTEM.md`: ما نجح، ما فشل، ما ستفعله بشكل مختلف
- [ ] **تذكير الـ Truth Registry:** لا تدّعي أي feature "production-ready" إذا لم تمر عليه 30 يوم telemetry مستقرة — ضع tag ⏳
- [ ] أنشئ GitHub Release v1.0.0-beta مع changelog كامل

> **معلم اليوم 90:** Soft Launch ✅ | أول عميل مدفوع ✅ | Telemetry يعمل ✅ | Post-mortem مكتوب ✅

---

## ملاحظات هامة للمشروع بأكمله

### قواعد Token Efficiency (مرجع سريع)

| القاعدة | التطبيق |
|---------|---------|
| CLI > MCP | `grep -n` قبل قراءة الملف كاملاً |
| `grep` before `read` | حدد السطر أولاً، ثم افتح |
| `git log --oneline` | قبل فتح أي ملف من الـ history |
| `wc -l` قبل `cat` | اعرف حجم الملف قبل قراءته |
| `pytest -k "test_name"` | شغّل test محدد، لا كل الـ suite |
| `tsc --noEmit` | تحقق من TypeScript بدون build |
| `docker stats` | قبل `docker logs` للتشخيص الأولي |
| `git diff HEAD~1 --stat` | ملخص التغييرات قبل التفاصيل |
| max_tokens لكل agent | Qualifier=500، Outreach=300، Analytics=1000 |
| cache system prompts | TTL 24h، target hit rate > 40% |

### قواعد Truth Registry (لا تخالفها أبداً)

1. **لا تدّعي أي شيء "live in production"** بدون 30 يوم telemetry مستقرة
2. **لا تكتب "SOC 2" أو "ISO 27001"** بدون شهادة رسمية
3. **لا تكتب "100% accurate"** لأي AI agent — الـ AI يخطئ
4. **لا تكتب "bank-grade security"** أو **"military-grade encryption"** — هذه مصطلحات تسويقية بدون معنى تقني محدد
5. **لا تكتب "ZATCA certified"** حتى تحصل على اعتماد رسمي من ZATCA — اكتب "متوافق مع متطلبات ZATCA"
6. **UI بالعربي أولاً** — RTL layout هو الافتراضي، وليس LTR + mirror

### مراجعات الجمعة (ملخص)

| الأسبوع | المراجعة الأساسية |
|---------|------------------|
| 1 | CI أخضر؟ Docker يعمل؟ |
| 2 | Test coverage الحالي؟ |
| 3 | Security scan نظيف؟ |
| 4 | Audit chain سليمة؟ |
| 5 | Coverage ≥ 70%؟ |
| 6 | Token cost/prospect؟ |
| 7 | Pipeline latency < 30s؟ |
| 8 | Prompt optimization يوفّر tokens؟ |
| 9 | Lighthouse > 85؟ |
| 10 | `next build` بدون errors؟ |
| 11 | Legal documents كاملة؟ |
| 12 | Production environment سليم؟ |
| 13 | Post-mortem مكتوب؟ |

---

## موارد مفيدة

- **المستودع:** [https://github.com/VoXc2/dealix](https://github.com/VoXc2/dealix)
- **Vision:** [./DEALIX_VISION.md](./DEALIX_VISION.md)
- **Execution Blueprint:** [./DEALIX_EXECUTION_BLUEPRINT.md](./DEALIX_EXECUTION_BLUEPRINT.md)
- **Token Efficiency Rules:** [./docs/TOKEN_EFFICIENCY_RULES.md](./docs/TOKEN_EFFICIENCY_RULES.md)

---

*آخر تحديث: جدول التنفيذ — Dealix v1.0-beta | المطوّر: Sami Mohammed Assiri*
