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
- **api/middleware/http_stack.py**: Server fingerprint removal uses `del response.headers[key]` (no `.pop()` on `MutableHeaders`).
- **Frontend `frontend/src/lib/`**: `utils.ts`, `hooks/useAuth.tsx`, and `api.ts` exist; use `git add -f` if `.gitignore` blocks `lib/` (Python artifact pattern).

### Operational caveats (still important)

- **Alembic**: migration graph includes merge revision `006` (joins `005` + `0001`) and continues to **`009` as the expected single head**. CI runs `python scripts/check_alembic_single_head.py`. Run `alembic heads` before production `upgrade head`; if a future PR introduces multiple heads, add another merge revision (see [docs/ops/ALEMBIC_MIGRATION_POLICY.md](docs/ops/ALEMBIC_MIGRATION_POLICY.md)).
- **`get_default_store(backend="postgres")`**: uses [`auto_client_acquisition/revenue_memory/isolated_pg_event_store.py`](auto_client_acquisition/revenue_memory/isolated_pg_event_store.py) — a **dedicated worker thread + separate async engine** (same `DATABASE_URL`) so `Orchestrator`, `append_event()`, and sync `store.append()` callers stay safe. The main app’s `db.session` pool remains separate (**two async pools** to the same DB when the worker is active — budget connections; see module docstring).
- **Lint (ruff/black)**: Large pre-existing drift; not API correctness gates.

### Enterprise readiness (links)

- [docs/SECURITY_RUNBOOK.md](docs/SECURITY_RUNBOOK.md) — استجابة الحوادث والأسرار
- [docs/SLO.md](docs/SLO.md) — أهداف التوفر والزمن
- [docs/ON_CALL.md](docs/ON_CALL.md) — تغطية الطوارئ

### Environment — frontend API URL

- Set `NEXT_PUBLIC_API_URL` when the backend is not on `http://localhost:8000` (`frontend/src/lib/api.ts`).

### Running tests

```bash
APP_ENV=test pytest -v
```

The full test suite has 500+ test files; full runs take ~15–20 minutes. Quick regression bundle:

```bash
pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py tests/test_isolated_pg_event_store.py tests/test_saudi_targeting_profile.py tests/test_leads_batch_router.py tests/test_strategy_os_scoring.py tests/test_strategy_os_ai_readiness.py tests/test_data_os_quality.py tests/test_governance_os_draft_gate.py tests/test_delivery_os_framework.py tests/test_commercial_engagements_lead_intelligence.py tests/test_commercial_engagements_support_desk.py tests/test_commercial_engagements_quick_win_ops.py tests/test_commercial_roadmap_mvp.py tests/test_service_readiness_score.py tests/test_readiness_gates.py -q --no-cov
```

`tests/test_revenue_os_catalog.py` (included in `scripts/revenue_os_master_verify.sh`) imports the FastAPI app stack and **requires optional deps from `requirements.txt`** (notably **`pyotp`**). Run `pip install -r requirements.txt` before that script or the catalog test locally.

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

Optional — isolated Postgres revenue memory integration test ([`tests/test_isolated_pg_event_store.py`](tests/test_isolated_pg_event_store.py)): set `RUN_REVENUE_PG_ISOLATION_TEST=1` with a reachable `DATABASE_URL` and Alembic-applied `revenue_events` table; default CI/local runs skip this test.

### Decision Passport (Revenue OS)

- `GET /api/v1/decision-passport/golden-chain` — السلسلة الذهبية (مرجع منتج)
- `GET /api/v1/decision-passport/evidence-levels` — مستويات أدلة L0–L5
- `POST /api/v1/leads` — يعيد `decision_passport` + `customer_readiness` مع كل تشغيل للـ pipeline
- `GET /api/v1/revenue-os/catalog` — Source Registry + enrichment waterfall order + action catalog (Trust Plane defaults)
- `POST /api/v1/revenue-os/signals/normalize` — يحوّل `MarketSignal` (مدخلات من المؤسس، بدون scraping) إلى Why Now / Offer / Proof target
- `POST /api/v1/revenue-os/anti-waste/check` — قواعد: لا إجراء خارجي بدون جواز قرار، لا upsell بدون proof، لا تسويق عام تحت L4
- `GET /api/v1/revenue-os/learning/weekly-template` — هيكل تقرير التعلّم الأسبوعي (فارغ حتى ربط التحليلات)

تحقق سريع للوكلاء: `bash scripts/revenue_os_master_verify.sh` (يطبع `DEALIX_REVENUE_OS_VERDICT`).  
تحقق جاهزية الخدمات والبوابات: `bash scripts/dealix_capability_verify.sh`.  
تحقق جاهزية التوسّع (10 أنظمة + اختبار نهائي): `bash scripts/dealix_scale_verify.sh` — انظر [docs/scale/SCALE_READINESS.md](docs/scale/SCALE_READINESS.md).  
تحقق Company OS (وثائق + سكربتات): `py -3 scripts/verify_full_mvp_ready.py --skip-tests` أو بدون `--skip-tests` لتشغيل pytest المرتبط.

- مكينة ليدز سعودية: `docs/ops/SAUDI_LEAD_MACHINE_AR.md`؛ بذرة YAML + `python scripts/import_seed_leads.py --dry-run`؛ دفعة API: `POST /api/v1/leads/batch`.

استراتيجية التشغيل الكاملة: `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`

### Hello world test

Submit a lead to the governed pipeline:

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","name":"Test","email":"test@example.sa","phone":"+966501234567","sector":"technology","region":"Saudi Arabia","budget":50000,"message":"Test message"}'
```

This exercises intake, ICP matching, pain extraction, BANT qualification, CRM sync (skipped without HubSpot), and booking.
