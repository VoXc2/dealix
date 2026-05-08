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

### Known issues

- **auth.py 204 endpoints**: The `/logout` and `/logout/all` routes in `api/routers/auth.py` need `response_model=None` in the decorator to work with FastAPI 0.115.x. Without this, `is_body_allowed_for_status_code` assertion fails at import time, blocking the entire app and any test that imports `api.main`.
- **middleware.py `MutableHeaders.pop`**: Starlette's `MutableHeaders` doesn't have a `.pop()` method. The `SecurityHeadersMiddleware` in `api/middleware.py` uses `pop("server", None)` which fails at runtime. Use `del response.headers[key]` with an `if key in` guard instead.
- **Frontend missing module**: `frontend/src/lib/hooks/useAuth` is imported in the root layout but the file does not exist in the repo. The Next.js frontend dev server starts but cannot compile pages. The backend works independently.
- **Lint (ruff/black)**: The codebase has ~1100 pre-existing ruff warnings and ~800 black formatting mismatches. These are pre-existing and not blockers.

### Running tests

```bash
APP_ENV=test pytest -v
```

The full test suite has 500+ test files. Many tests are fast static/contract checks. Some tests that import `api.main` at module level will fail if the auth.py fix is not applied. A targeted subset for quick verification:

```bash
pytest tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/test_live_gates_default_false.py -v
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

### Hello world test

Submit a lead to the governed pipeline:

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","name":"Test","email":"test@example.sa","phone":"+966501234567","sector":"technology","region":"Saudi Arabia","budget":50000,"message":"Test message"}'
```

This exercises intake, ICP matching, pain extraction, BANT qualification, CRM sync (skipped without HubSpot), and booking.
