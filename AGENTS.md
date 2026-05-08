# AGENTS.md

## Cursor Cloud specific instructions

### Services Overview

| Service | Port | Purpose |
|---------|------|---------|
| **FastAPI Backend** | 8000 | Main API (`uvicorn api.main:app --reload`) |
| **PostgreSQL 16** | 5432 | Primary DB (via `docker compose up -d postgres`) |
| **Redis 7** | 6379 | Cache/queue (via `docker compose up -d redis`) |
| **Next.js Frontend** | 3000 | Dashboard UI (`npm run dev` in `frontend/`) |

### Starting infrastructure

```bash
docker compose up -d postgres redis
```

Then start the backend:

```bash
APP_ENV=development uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Resolved in repo (do not re-diagnose as bugs)

- **auth.py 204 + logout**: `/logout` and `/logout/all` use `response_model=None` for FastAPI 0.115.x.
- **middleware.py**: Server fingerprint removal uses `del response.headers[key]` (no `.pop()` on `MutableHeaders`).
- **Frontend `frontend/src/lib/`**: `utils.ts`, `hooks/useAuth.tsx`, and `api.ts` exist; use `git add -f` if `.gitignore` blocks `lib/` (Python artifact pattern).

### Operational caveats (still important)

- **Alembic**: merge revision `004_merge_heads` joins `0001` + `003`; head continues as `005_revenue_events_tenant` (`tenant_id` on `revenue_events`). Run `alembic upgrade head` after pull.
- **`PostgresEventStore` vs sync callers**: methods are **async** and rows now carry optional **`tenant_id`** (filter via `read_for_customer(..., tenant_id=...)`). Sync callers (`Orchestrator`, `append_event()`, `api/routers/revenue_os.py`) still need an async bridge before `get_default_store(backend="postgres")` is safe in those paths.
- **Lint (ruff/black)**: Large pre-existing drift; not API correctness gates.

### Environment — frontend API URL

- Set `NEXT_PUBLIC_API_URL` when the backend is not on `http://localhost:8000` (`frontend/src/lib/api.ts`).

### Running tests

```bash
APP_ENV=test pytest -v
```

The full test suite has 500+ test files; full runs take ~15–20 minutes. Quick regression bundle:

```bash
pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py -q --no-cov
```

### Running lint

```bash
ruff check .
black --check .
```

### Environment variables

Copy `.env.example` to `.env`. Key settings for local dev:
- `ENVIRONMENT=development` (not `production`)
- `DATABASE_URL=postgresql+asyncpg://ai_user:ai_password@localhost:5432/ai_company`
- All LLM keys and external service keys are optional; the app degrades gracefully.

### Decision Passport (Revenue OS)

- `GET /api/v1/decision-passport/golden-chain` — السلسلة الذهبية (مرجع منتج)
- `GET /api/v1/decision-passport/evidence-levels` — مستويات أدلة L0–L5
- `POST /api/v1/leads` — يعيد `decision_passport` + `customer_readiness` مع كل تشغيل للـ pipeline
- `GET /api/v1/revenue-os/catalog` — Source Registry + enrichment waterfall order + action catalog (Trust Plane defaults)
- `POST /api/v1/revenue-os/signals/normalize` — يحوّل `MarketSignal` (مدخلات من المؤسس، بدون scraping) إلى Why Now / Offer / Proof target
- `POST /api/v1/revenue-os/anti-waste/check` — قواعد: لا إجراء خارجي بدون جواز قرار، لا upsell بدون proof، لا تسويق عام تحت L4
- `GET /api/v1/revenue-os/learning/weekly-template` — هيكل تقرير التعلّم الأسبوعي (فارغ حتى ربط التحليلات)
- `GET /api/v1/revenue-os/tenant-context/ping` — يتطلب JWT؛ للـ `super_admin` يجب تمرير `X-Tenant-ID`

Webhook leads (`/api/v1/leads/import/google-ads` و Meta): عيّن `DEFAULT_INGESTION_TENANT_ID` في البيئة إلى `TenantRecord.id` حقيقي إن أردت ربط الليدز بمستأجر.

تحقق سريع للوكلاء: `bash scripts/revenue_os_master_verify.sh` (يطبع `DEALIX_REVENUE_OS_VERDICT`).

استراتيجية التشغيل الكاملة: `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`

### Hello world test

Submit a lead to the governed pipeline:

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","name":"Test","email":"test@example.sa","phone":"+966501234567","sector":"technology","region":"Saudi Arabia","budget":50000,"message":"Test message"}'
```

This exercises intake, ICP matching, pain extraction, BANT qualification, CRM sync (skipped without HubSpot), and booking.
