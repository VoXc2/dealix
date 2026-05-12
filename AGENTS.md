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

---

## T6 / T7 / T8 capability map (for AI contributors)

If you're an AI contributor writing code in this repo, here is the
T6–T8 surface you must respect. Don't re-invent these — extend them.

### Skills (T6a + T8a)

- **Catalogue:** `skills/MANIFEST.yaml` (one row per skill).
- **Per-skill folder:** `skills/<slug>/SKILL.md` (Anthropic format) +
  `skills/<slug>/prompt.yaml` (+ optional `eval.yaml` for Promptfoo).
- **Loader:** `dealix/agents/skills/__init__.py` (`load()`, `by_id()`,
  `reload()`).
- **Runtime registry:** `dealix/agents/skills/handlers.py` —
  `@register("skill_id")` decorator. Handlers are
  `async def(inputs: dict) -> dict`. Side-effect-light by default;
  external calls gated on env keys.
- **HTTP surface:** `api/routers/skills.py` (`GET /api/v1/skills`,
  `GET /api/v1/skills/handlers`, `GET /api/v1/skills/{id}`,
  `POST /api/v1/skills/{id}/run`).
- **MCP exposure:** `dealix/mcp/server.py` auto-registers every
  skill as an MCP tool.
- **Adding a skill:** SKILL.md + prompt.yaml + manifest row + (optional)
  `@register(...)` handler. Restart picks it up; tests in
  `tests/unit/test_skills_loader.py` enforce the manifest contract.

### Industry verticals (T6c)

- **Per-vertical folder:** `dealix/verticals/<slug>/config.yaml` +
  `landing/index.html` (snippet).
- **Loader:** `dealix/verticals/__init__.py` (`Vertical` dataclass,
  `list_all()`, `by_id()`).
- **HTTP surface:** `api/routers/verticals.py` (`GET /api/v1/verticals`,
  `GET /api/v1/verticals/{id}`, `POST /api/v1/verticals/apply`).
- **Adding a vertical:** new folder under `dealix/verticals/` with
  `config.yaml` (label_ar/en, description_ar/en, agents, workflows,
  pricing_default_plan, lead_form_fields). Tests in
  `tests/unit/test_verticals_loader.py` enforce the contract.

### BYOA agent builder (T6d)

- **Manifest:** `agent.yaml` — id (lowercase, 3–64 chars,
  `[a-z0-9_-]`), name, model, tools (every tool must exist in the
  Skills catalogue), prompt_override, max_usd_per_request (in (0,10]),
  locale.
- **Validator:** `dealix/agents/builder/validate()` raises
  `AgentValidationError` on every bad field.
- **HTTP surface:** `api/routers/agents_builder.py` (`/api/v1/agents`
  CRUD + `/api/v1/workflows/marketplace` + `/api/v1/workflows/install`).

### Enterprise admin (T6e)

- **IP allowlist middleware:** `api/middleware/ip_allowlist.py`
  reads `TenantRecord.meta_json.ip_allowlist`. `/api/v1/public/*` and
  `/healthz` always bypass.
- **Audit forwarding:** `dealix/audit/forward.py` — best-effort
  Datadog / Splunk HEC / S3 sinks. Failures log + return False.
- **BYOK:** `dealix/audit/byok.py` — `BYOKProvider.from_env()` dispatches
  on `KMS_PROVIDER` (aws|gcp|azure).
- **HTTP surface:** `api/routers/admin_enterprise.py` — sandbox spin-up,
  IP allowlist set/clear, webhook rotation, byok/audit-forward status.
  Admin-gated via `ADMIN_API_KEYS` env or `super_admin` JWT claim.

### Saudi-government APIs (T6f)

- **Clients:** `dealix/integrations/{etimad,maroof,najiz,najm,tadawul,misa}_client.py`
  — each exposes `is_configured()` + dataclass result types. 503
  `<service>_not_configured` when env unset.
- **HTTP surface:** `api/routers/saudi_gov.py` — six endpoints under
  `/api/v1/saudi-gov/*`.

### GCC payments (T8b)

- **Clients:** `dealix/payments/{knet,benefit,magnati}_client.py`
  mirror the Moyasar/Stripe contract: `create_checkout_session()` +
  `verify_webhook()` + module-level `get_*_client()` singleton.
- **HTTP surface:** `api/routers/billing_gcc.py` — health, checkout/{gw},
  webhooks/{gw}.
- **Currency helper:** `dealix/gcc/currency.py` — single source of truth
  for SAR/AED/QAR/KWD/BHD/OMR minor units + formatting + weekend rules.

### Newsletter (T6g)

- `api/routers/newsletter.py` — PDPL consent gate; Loops when
  configured; degraded path otherwise.

### Production patterns to reuse

- **Inert-by-default:** Every new vendor integration ships behind an
  env-var feature flag. 503 + descriptive `<service>_not_configured`
  rather than silent stubs.
- **Bilingual UI:** `t(ar, en)` helper in frontend pages; the existing
  `[locale]/admin/{skills,verticals,agents,enterprise}/page.tsx`
  routes show the pattern.
- **CLI parity:** every router gets a `cli/dealix_cli.py` group. The
  CLI uses `_request()` which honours `DEALIX_API_BASE`,
  `DEALIX_API_KEY`, `DEALIX_BEARER_TOKEN`.
- **SDK example:** new endpoints get a `docs/api/examples/python/<name>.py`
  + `typescript/<name>.ts` pair.
- **Deep health:** `api/routers/health.py` `/health/deep` reports
  `configured/unconfigured` for every new T6+ dependency.
- **Test discipline:** every new router → an integration test;
  every new pure function → a unit test. Pattern in
  `tests/{integration,unit}/test_*_router.py`.
- **Mintlify doc:** every new router gets a `docs/api/<name>.mdx`
  page and a row in `mint.json` navigation.
