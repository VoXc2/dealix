# CLAUDE.md

Guidance for Claude Code and AI agents working in this repository.

## What this repo is

**Dealix** — a Saudi B2B Revenue Engine: an AI revenue, growth, and compliance
platform that is PDPL-native, ZATCA-compliant, and approval-first. Three layers:

1. **Lead Engine** — acquire, enrich, score, and dedupe Saudi B2B leads.
2. **Service Engine** — 7 productized AI services exposed under `/api/v1/...`.
3. **Trust Engine** — PDPL wiring, ZATCA Phase 2 e-invoicing, decision audit trail.

See `README.md` for the full product description.

## Tech stack

- **Backend**: Python 3.11+, FastAPI 0.115+, Pydantic 2, SQLAlchemy 2.0 (async)
- **Data**: PostgreSQL 16, Redis 7, Alembic migrations
- **Frontend**: Next.js (in `frontend/`)
- **Tests**: pytest (`asyncio_mode = auto`), Playwright, Locust
- **Quality**: ruff, black, mypy, bandit, gitleaks (via `.pre-commit-config.yaml`)

## Top-level layout

| Path | Purpose |
|------|---------|
| `api/` | FastAPI routers (customer, sales, agents, compliance, analytics, webhooks) |
| `core/` | Core domain logic and utilities |
| `dealix/` | Package entry points |
| `integrations/` | PDPL, ZATCA, WhatsApp, email, Saudi-market adapters |
| `auto_client_acquisition/`, `autonomous_growth/` | Lead/growth engines |
| `db/`, `alembic/` | Schema and migrations |
| `frontend/`, `landing/` | Next.js app and marketing site |
| `tests/` | Unit, integration, e2e, playwright, load suites |
| `docs/` | Architecture, OS-layer modules, compliance, runbooks |

## Common commands

All driven by the `Makefile`:

| Command | What it does |
|---------|--------------|
| `make setup` | One-time dev setup (installs `[dev]` extra + pre-commit) |
| `make lint` | `ruff check .` + `black --check .` |
| `make format` | Auto-fix with ruff + black |
| `make type-check` | mypy |
| `make security` | bandit + detect-secrets |
| `make test` / `make test-unit` / `make test-integration` | pytest suites |
| `make run` | Run the API locally |
| `make docker-up` / `make docker-down` | Local Postgres + Redis + app |

**Note on pytest**: use `python3 -m pytest ...` (not the bare `pytest` binary)
so it runs against the project's installed dependencies. Coverage is on by
default; add `--no-cov` for fast smoke runs.

## Sub-agents

Five specialized agents live in `.claude/agents/`. Invoke the one that matches
the task:

- **dealix-pm** — owns the 90-day commercial activation plan; coordinates the others.
- **dealix-engineer** — Python code, FastAPI routers, tests, migrations.
- **dealix-delivery** — runs the 7-day Revenue Intelligence Sprint per customer.
- **dealix-sales** — qualifies leads, renders proposals, drafts outreach (founder-approved).
- **dealix-content** — bilingual AR+EN docs, SOPs, case studies, templates.

## Doctrine and constraints

- Read `AGENTS.md`, `DEALIX_COMPANY_OPERATIONAL_STATE.md`, and `SECURITY.md`
  before making non-trivial changes — they carry the project's non-negotiables.
- **Never** commit real prospect or customer data. Runtime/customer paths are
  gitignored (`data/customers/**`, `docs/wave*/live/**`).
- **Alembic**: do not auto-generate migrations blindly — see the warning in
  `AGENTS.md`. The current head is tracked in `alembic/`.
- Respect pre-commit hooks; never bypass with `--no-verify`.
- Work on feature branches; do not commit directly to `main`.

## Claude Code session setup

- `.claude/settings.json` registers a **SessionStart hook**
  (`.claude/hooks/session-start.sh`) that installs the Python `[dev]` extra so
  linters and tests are runnable in Claude Code on the web.
- Copy `.claude/settings.local.json.example` to `.claude/settings.local.json`
  for personal overrides (model, extra permissions, env vars). The local file
  is gitignored.
