# AGENTS.md

## AI Coding Agent Guidance

This file is the primary repo-specific guide for AI coding agents working in `dealix`.
- Use this file first for local dev commands, repo conventions, and where to find detailed docs.
- Do not duplicate long docs from `README.md` or `docs/`; link to them instead.
- Preserve existing operational knowledge and avoid treating resolved issues as new bugs.

### Token Optimization
See `token-optimizer/` for 12 guides covering: `.claudeignore` (40-90% savings), CLAUDE.md hygiene, session management, model routing (Haiku/Sonnet/Opus), MCP discipline, subagents, hooks, prompt templates, file handling, monitoring, git hygiene, and env config. Run `bash token-optimizer/12-environment-config/apply-all.sh` to apply all settings.

### Repo anatomy
- `api/` — FastAPI app entry, dependencies, middleware, 120+ routers, and schema definitions.
- `api/routers/commercial.py` — 13 commercial chain endpoints (diagnostic→pilot→proof→payment→upsell). Skill: `@token-optimizer/02-claude-md/skills/commercial.md`
- `dealix/commercial/` — commercial business logic (diagnostic_engine, warm_intro_generator, pilot_delivery, proof_builder, upsell_engine, case_study_generator, zatca_invoice).
- `dealix/payments/` — Moyasar payment links. Sandbox by default; `MOYASAR_LIVE_MODE=1` for live.
- `data/templates/` — AR/EN content templates (warm intros, proposals, proof packs, daily checklist).
- `auto_client_acquisition/`, `autonomous_growth/`, `dealix/`, `core/`, `integrations/` — business logic, AI agents, policy, and execution workflows.
- `frontend/` — Next.js dashboard and public landing experience. Skill: `@token-optimizer/02-claude-md/skills/frontend.md`
- `tests/` — pytest-based test suites, including integration and regression bundles.
- `scripts/` — operational and verification helpers used by CI and launch workflows.
- `docs/` — architecture, launch runbooks, compliance, and product docs.

### Primary goals for agents
- Make small, safe changes only when asked.
- Prefer fixing or clarifying existing code over adding new features.
- Run/tests commands only when explicitly requested by the user.
- Avoid changing deployment, secret, or production config unless the user explicitly asks.

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

- **Alembic**: migration graph includes merge revision `006` (joins `005` + `0001`) and later enterprise revisions. **CI enforces a single Alembic head** via `python scripts/check_alembic_single_head.py` (from repo root). Run `alembic heads` before production `upgrade head`; if multiple heads appear, add a merge revision (see [docs/ops/ALEMBIC_MIGRATION_POLICY.md](docs/ops/ALEMBIC_MIGRATION_POLICY.md)).
- **`get_default_store(backend="postgres")`**: uses [`auto_client_acquisition/revenue_memory/isolated_pg_event_store.py`](auto_client_acquisition/revenue_memory/isolated_pg_event_store.py) — a **dedicated worker thread + separate async engine** (same `DATABASE_URL`) so `Orchestrator`, `append_event()`, and sync `store.append()` callers stay safe. The main app’s `db.session` pool remains separate (**two async pools** to the same DB when the worker is active — budget connections; see module docstring).
- **Lint (ruff/black)**: Large pre-existing drift; not API correctness gates.

### Enterprise readiness (links)

- [docs/SECURITY_RUNBOOK.md](docs/SECURITY_RUNBOOK.md) — استجابة الحوادث والأسرار
- [docs/SLO.md](docs/SLO.md) — أهداف التوفر والزمن
- [docs/ON_CALL.md](docs/ON_CALL.md) — تغطية الطوارئ

### Business NOW (all pillars — today)

- **Doc:** [docs/business/DEALIX_BUSINESS_NOW_AR.md](docs/business/DEALIX_BUSINESS_NOW_AR.md)
- **One command:** `bash scripts/run_business_now.sh` (Windows: `powershell -File scripts/run_business_now.ps1`)
- **Verdict cache:** [dealix/transformation/business_now_cache.yaml](dealix/transformation/business_now_cache.yaml) (updated by generator; API reads cache when not running live verify)
- **API:** `GET /api/v1/business-now/snapshot` · `GET /api/v1/business-now/commercial-strategy` · `POST /api/v1/business-now/commercial-strategy/simulate` · `GET /api/v1/business-now/operator-signals` (admin `X-Admin-API-Key`)
- **Focus override (optional):** [dealix/transformation/commercial_focus_override.yaml](dealix/transformation/commercial_focus_override.yaml)
- **Commercial strategy doc:** [docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md](docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md) — `python3 scripts/generate_commercial_strategy_doc.py`
- **Ops client pack (AR):** [docs/commercial/ops_client_pack/](docs/commercial/ops_client_pack/) — runbook + executive deck pptx
- **Founder go-live (sell + verify + agents):** `bash scripts/founder_go_live_verify.sh` (Windows: `scripts/founder_go_live_verify.ps1`) — [FOUNDER_GO_LIVE_DAY0_AR.md](docs/ops/FOUNDER_GO_LIVE_DAY0_AR.md) · [FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md](docs/ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md) · [FOUNDER_AGENT_PLAYBOOK_AR.md](docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md)
- **Founder Operating System:** [FOUNDER_OPERATING_SYSTEM_AR.md](docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md) · **Comprehensive plan execution:** [FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md](docs/ops/FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md) · daily anchor [FOUNDER_DAILY_ANCHOR_AR.md](docs/ops/FOUNDER_DAILY_ANCHOR_AR.md) · **`python scripts/founder_comprehensive_plan_status.py`** · **CEO Master Plan:** [CEO_90_DAY_OKR_AR.md](docs/commercial/operations/CEO_90_DAY_OKR_AR.md) · **`python scripts/run_ceo_master_plan_status.py`** · **`python scripts/founder_daily_five_metrics.py`** · **`GET /api/v1/ops-autopilot/founder/ceo-master-plan`** · close tools: `phase_0_1_close_helper.py` · `gtm_conversation_log.py` · `render_diagnostic_proposal.py` · weekly retro: `founder_weekly_ceo_retro.py` · **أقوى خطة (138 مهمة):** · **`bash scripts/founder_one_command.sh`** (أمر واحد — أقصى أتمتة) · **`python scripts/verify_full_autonomous_ops_stack.py`** · **`python scripts/run_dealix_complete_autonomous_day.py`** · **`POST /api/v1/ops-autopilot/founder/complete-autonomous-day/run`** [FOUNDER_STRONGEST_PLAN_AR.md](docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md) · **`python scripts/founder_strongest_plan_status.py`** · **`bash scripts/founder_weekly_loop.sh`** (Sunday gates; Windows: `.ps1`) · **`bash scripts/founder_cadence.sh`** (morning/evening/weekly) · **`bash scripts/run_founder_commercial_day.sh`** (canonical morning; Windows: `.ps1`; `--full` syncs evidence both ways) · **`bash scripts/verify_founder_ops_launch.sh`** (launch gate) · **`bash scripts/run_founder_revenue_day.sh`** (wrapper: commercial + `--with-business-now`)
- **Founder ops UI:** `/[locale]/ops/founder` (90-min cockpit) · war-room · marketing (today + factory) · sales · partners · evidence · support — prod: `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1` + server `DEALIX_ADMIN_API_KEY` (see `frontend/src/app/api/dealix-proxy/`)
- **Integrations:** HubSpot sync on lead capture/war-room patch (`HUBSPOT_ACCESS_TOKEN`) · Calendly webhooks → `POST /api/v1/webhooks/calendly` · `CALENDLY_URL` in booking + outreach
- **Company ready (founder — start here):** [DEALIX_COMPANY_READY_MASTER_AR.md](docs/company/DEALIX_COMPANY_READY_MASTER_AR.md) · `bash scripts/company_ready_verify.sh`
- **Official Railway launch:** `bash scripts/railway_prod_bootstrap.sh` (Alembic + War Room seed once) · `bash scripts/official_launch_verify.sh` → `OFFICIAL_LAUNCH_VERDICT=PASS` · env matrix: `python3 scripts/railway_launch_env_check.py` · full A–D: `bash scripts/launch_execution_railway.sh`
- **Unified revenue (founder commercial):** [COMMERCIAL_VALUE_MAP_AR.md](docs/commercial/COMMERCIAL_VALUE_MAP_AR.md) (material value map — all angles) · `python scripts/commercial_value_map_status.py` · [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) (thesis) · [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) (GTM depth) · [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) (5 min daily) · [FOUNDER_REVENUE_DAY_ONE_AR.md](docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md) (day playbook) · **`python scripts/run_dealix_daily_ops.py`** (`--api-only` with `DEALIX_API_BASE` + `DEALIX_ADMIN_API_KEY`; full loop offline with `--skip-api`) — Postgres→Autopilot replay, Full Ops Health JSON, Monday weekly marketing pack — brief in `data/founder_briefs/` · UI: `/[locale]/ops/founder` (command center), `/ops/marketing` · targeting seed: `docs/commercial/operations/targeting/agency_accounts_seed.csv` · War Room [DEALIX_REVENUE_WAR_ROOM_AR.md](docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md)
- **Official commercial launch gate:** **`bash scripts/verify_dealix_commercial_go_live.sh`** (Windows: `powershell -File scripts/verify_dealix_commercial_go_live.ps1`) — prints `DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS|FAIL`; optional `DEALIX_VERIFY_WITH_API=1` / `DEALIX_VERIFY_WITH_FRONTEND_BUILD=1` for live API + `npm run build`
- **Commercial soft launch:** [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md) · `python3 scripts/verify_commercial_launch_ready.py` (`--with-api`, `--with-frontend-build`) · public home **`/[locale]`** (CommercialLaunchHome)
- **GTM public funnel:** `/[locale]` (launch home) · `/dealix-diagnostic` · `/risk-score` · `/proof-pack` · `/learn/[slug]` · `/partners`
- **GTM ops (admin key):** `/[locale]/ops` (hub) · `/ops/founder` · `/ops/war-room` · `/ops/marketing` · `/ops/sales` · `/ops/partners` · `/ops/evidence` · `/ops/approvals` — APIs: `GET /api/v1/ops-autopilot/war-room/today-pack` · `POST .../marketing/queue-approval` · `GET .../marketing/social-today` (no live LinkedIn/WhatsApp send)
- **UI:** `/[locale]/business-now` (8 pillars + commercial strategy — complements `/cloud` for founder decisions)
- **Optional UI env:** `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` for operator-signals block locally

### Global AI transformation (CEO / operating spine)

- Weekly executive checklist: `bash scripts/run_executive_weekly_checklist.sh` (proof pack + `verify_global_ai_transformation.py` + audit log; syncs `weekly_ops.last_checklist_run_iso` when PASS).
- **CTO weekly anchor:** `bash scripts/run_cto_weekly_anchor.sh` — checklist + platform KPIs + commercial registry status (see [CTO_EXECUTIVE_CADENCE_AR.md](docs/transformation/CTO_EXECUTIVE_CADENCE_AR.md)).
- **One-session full readiness:** `bash scripts/run_ceo_one_session_readiness.sh` — checklist + platform KPI signals + pre-scale gates + full verify + session report (see [CEO_ONE_SESSION_MASTER_PLAN_AR.md](docs/transformation/CEO_ONE_SESSION_MASTER_PLAN_AR.md)).
- **12-pillar verify:** `bash scripts/run_cto_pillar_verify_bundle.sh` — transformation + control plane + gap spot checks.
- **Compliance/GTM gates:** `bash scripts/run_compliance_gtm_gate_bundle.sh` — PDPL artifact + pre-scale + revenue_os + Moyasar/DPA docs.
- Commercial KPIs: copy `kpi_founder_commercial_import.example.yaml` → `kpi_founder_commercial_import.yaml` (gitignored), fill from CRM, then `python3 scripts/apply_kpi_founder_commercial.py` (never invent CRM numbers in automation).
- CTO master index: [docs/transformation/CTO_MASTER_OPERATING_INDEX_AR.md](docs/transformation/CTO_MASTER_OPERATING_INDEX_AR.md)
- KPI snapshot API: `GET /api/v1/transformation/kpi-snapshot`
- Embeddings readiness: `python3 scripts/check_embeddings_readiness.py`
- Readiness helper (defaults to **transformation** when run with no args): `bash scripts/verify_ceo_signal_readiness.sh`
- Doc map: [docs/transformation/README.md](docs/transformation/README.md) — Arabic operating SOP: [docs/transformation/EXECUTIVE_OPERATING_CHECKLIST_AR.md](docs/transformation/EXECUTIVE_OPERATING_CHECKLIST_AR.md)

### Cloud deployment (align with Cursor Cloud dev)

| Concern | Doc / command |
| --- | --- |
| Universal deploy | [docs/contributing/DEPLOYMENT.md](docs/contributing/DEPLOYMENT.md) |
| API-keys-only quick path | [docs/QUICK_DEPLOY_API_KEYS_ONLY.md](docs/QUICK_DEPLOY_API_KEYS_ONLY.md) |
| Railway (AR) | [docs/RAILWAY_DEPLOY_GUIDE_AR.md](docs/RAILWAY_DEPLOY_GUIDE_AR.md) |
| Railway production policy | [docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md](docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md) · [RAILWAY_PRODUCTION_SETTINGS_AR.md](docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md) · `python scripts/verify_railway_production_config.py` · **`bash scripts/founder_production_smoke.sh`** (Windows: `.ps1`) · `python scripts/run_founder_production_gates.py` |
| GTM public surfaces | [docs/ops/GTM_PUBLIC_SURFACES_AR.md](docs/ops/GTM_PUBLIC_SURFACES_AR.md) · `python scripts/verify_gtm_public_surfaces.py` · agent packets: `python scripts/print_agent_work_packets.py` |
| Founder weekly metrics | [docs/ops/FOUNDER_WEEKLY_METRICS_AR.md](docs/ops/FOUNDER_WEEKLY_METRICS_AR.md) · `python scripts/founder_weekly_metrics_bundle.py --write` |
| Dealix Cloud UI map | [docs/product/DEALIX_CLOUD_UI_MAP.md](docs/product/DEALIX_CLOUD_UI_MAP.md) — frontend hub at `/[locale]/cloud` |
| Frontend API base | `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`) |

Production env minimums match `docs/contributing/DEPLOYMENT.md` (`APP_SECRET_KEY`, `DATABASE_URL`, Moyasar when billing). Keep `ENVIRONMENT=development` locally; never enable auto external sends in any environment.

### Environment — frontend API URL

- Set `NEXT_PUBLIC_API_URL` when the backend is not on `http://localhost:8000` (`frontend/src/lib/api.ts`).

### Running tests

```bash
APP_ENV=test pytest -v
```

The full test suite has 500+ test files; full runs take ~15–20 minutes. Quick regression bundle:

```bash
pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py tests/test_isolated_pg_event_store.py tests/test_saudi_targeting_profile.py tests/test_leads_batch_router.py tests/test_strategy_os_scoring.py tests/test_strategy_os_ai_readiness.py tests/test_data_os_quality.py tests/test_governance_os_draft_gate.py tests/test_delivery_os_framework.py tests/test_commercial_engagements_lead_intelligence.py tests/test_commercial_engagements_support_desk.py tests/test_commercial_engagements_quick_win_ops.py tests/test_commercial_roadmap_mvp.py tests/test_service_readiness_score.py tests/test_readiness_gates.py tests/test_db_sync_url.py tests/test_sync_weekly_ops_from_checklist_log.py tests/test_workflow_control_registry.py tests/test_populate_kpi_baselines_platform_signals.py tests/test_ceo_master_plan_status.py tests/test_founder_comprehensive_plan.py -q --no-cov
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
تحقق Company OS (وثائق + سكربتات): `py -3 scripts/verify_full_mvp_ready.py --skip-tests` أو بدون `--skip-tests` لتشغيل pytest المرتبط.

تحقق الحزمة الكاملة محليًا (Docker data plane + بوابات Python + smoke + Next.js + Playwright Tier-1):

```bash
bash scripts/dealix_local_stack_verify.sh                       # تشغيل كامل
bash scripts/dealix_local_stack_verify.sh --skip-docker --skip-frontend   # البوابات + pytest فقط
```

نفس السطح متاح على GitHub عبر **Actions → Local stack verify → Run workflow** (`.github/workflows/local_stack_verify.yml`).

**اصطلاح Python:** خطوات السكربتات في GitHub Actions تستخدم `python3` (تكافؤ مع صور Linux الأدنى).

- مكينة ليدز سعودية: `docs/ops/SAUDI_LEAD_MACHINE_AR.md`؛ بذرة YAML + `python3 scripts/import_seed_leads.py --dry-run`؛ دفعة API: `POST /api/v1/leads/batch`.

استراتيجية التشغيل الكاملة: `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`

### Hello world test

Submit a lead to the governed pipeline:

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","name":"Test","email":"test@example.sa","phone":"+966501234567","sector":"technology","region":"Saudi Arabia","budget":50000,"message":"Test message"}'
```

This exercises intake, ICP matching, pain extraction, BANT qualification, CRM sync (skipped without HubSpot), and booking.
