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

- **Alembic — two heads**: `alembic heads` reports `0001` and `003`. Until a merge revision exists, `alembic upgrade head` may not apply both branches; use explicit revision targets or rely on dev `init_db` (which imports `db.models_revenue_events` so `revenue_events` is included in `create_all`).
- **`PostgresEventStore` vs sync callers**: `PostgresEventStore` methods are **async**. `Orchestrator`, module `append_event()`, and `api/routers/revenue_os.py` still call **`store.append()` synchronously**. Default remains in-memory; `get_default_store(backend="postgres")` is unsafe until those paths are async-ready or a sync adapter exists.
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

---

## Conventions for AI / human contributors

Every commit in this repo is written by either a human or an AI agent
(Claude, Cursor, Codex, etc.). To keep the codebase predictable and the
review loop fast, apply these rules **always**:

### Code style

- **Python**: 3.11+. Use `core.logging.get_logger(__name__)`; never
  `print(`, `eval(`, or `requests` (use `httpx` + the SSRF guard).
  Catch specific exceptions; bare `except Exception` requires a
  `# noqa: BLE001` comment justifying the boundary handler.
- **TypeScript**: React 19 + Next.js 15. Use the typed `apiClient` in
  `frontend/src/lib/api.ts`; never call `fetch` directly from
  components except for one-shot pages.
- **YAML / JSON**: 2-space indent. JSON for machine-consumed config
  (Grafana dashboards), YAML for human-edited config (Semgrep,
  Promptfoo, Cerbos).

### Type safety

- The modules listed in `pyproject.toml [[tool.mypy.overrides]]` run
  under `mypy --strict`. **Do not regress** them. New security-critical
  code goes in this list before merge.
- Run `make mypy-strict` before opening a PR.

### Tests

- Every new endpoint needs at least one integration test in `tests/`.
- Every new prompt needs at least one Promptfoo eval case in
  `evals/promptfoo/<name>.yaml`.
- Every new policy needs a `tests/test_authz_*` case.
- Mutation testing runs quarterly via `make mutmut` — survivors that
  map to security-critical paths become P1 issues.

### Commits

- Conventional Commits: `feat(scope): summary`, `fix(scope): summary`,
  `chore(scope): summary`, `docs(scope): summary`.
- **One logical change per commit.** Don't pile reviews on yourself
  by squashing unrelated work.
- The commit body explains the WHY, not the WHAT — the diff is the
  WHAT. Reference the docs/runbook the change supports (e.g. "closes
  CC6.3 in docs/compliance/CONTROLS.md").
- AI agents writing commits: include a one-line preamble noting that
  the commit was AI-authored. Until reviewed, the PR stays in draft.

### Architectural changes need ADRs

- Any choice that affects how the system is operated, scaled, or
  charged for goes into `docs/adr/`.
- Use the template at `docs/adr/template.md`. One change per ADR.
- Mark **Accepted** only after a human reviewer approves the PR.

### Inert-by-default for new integrations

- New external SDKs ship behind an env-var feature flag. When the key
  is missing, the feature returns a documented 503 or no-ops.
- Document the env vars in `.env.example` *and* in the route's
  docstring.

### The bar

Read `docs/QA_REVIEW.md` §13 once. The bar is: an engineer joins the
team, clones the repo, runs `make hooks dev`, and ships a feature in
the same week. Anything that gets in the way of that is a regression.
