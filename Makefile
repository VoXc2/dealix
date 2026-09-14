# ═══════════════════════════════════════════════════════════════
# Dealix — Makefile
# الأوامر الشائعة
# ═══════════════════════════════════════════════════════════════

.PHONY: help install install-dev install-observability install-security install-evals install-docs \
        setup first-setup test test-unit test-integration full-repo-test railway-env-check \
        lint format type-check security security-smoke security-smoke-ci clean run demo cockpit doctor \
        docker-build docker-up docker-down docker-logs \
        pre-commit-install pre-commit-run db-init alembic-heads requirements \
        env-check openapi-export api-contract-check dependency-inventory release-manifest production-smoke prod-verify \
        design-os-list design-os-generate design-os-all design-os-daily design-os-validate design-os-index design-os-html test-design-os \
        v5-status v5-smoke v5-snapshot v5-diagnostic v5-verify v5-digest \
        v5-proof-pack v10-verify v10-reference \
        ai-provider-radar ai-provider-radar-json ai-provider-coding ai-provider-arabic ai-provider-batch daily-value-loop \
        launch-validate launch-vertical-score launch-icp-score launch-trust-preflight \
        launch-outreach-drafts launch-proposal launch-founder-command launch-weekly-review \
        launch-content launch-pipeline launch-all-dry-runs test-launch \
        score-prospect score-batch analyze-pipeline intelligence-test brand-growth-verify brand-growth-run

# Python binary (override with PYTHON=python3.12 make ...)
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
OPENAPI_OUTPUT ?= docs/architecture/openapi.json
PRODUCTION_BASE_URL ?= https://api.dealix.me
TYPE ?= revenue-command-room
CONTEXT ?= Dealix operating system launch and commercial command room.

help: ## Show this help
	@echo "🏢 Dealix — Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ── Environment setup ──────────────────────────────────────────
install: ## Install production dependencies
	$(PIP) install -e .

install-dev: ## Install dev dependencies (tests, lint, etc.)
	$(PIP) install -e ".[dev]"

install-observability: ## Install optional observability stack
	$(PIP) install -e ".[observability]"

install-security: ## Install optional security and supply-chain tooling
	$(PIP) install -e ".[security]"

install-evals: ## Install optional evaluation and analysis tooling
	$(PIP) install -e ".[evals]"

install-docs: ## Install optional documentation site tooling
	$(PIP) install -e ".[docs]"

setup: install-dev pre-commit-install ## One-time dev setup
	@test -f .env || (cp .env.example .env && echo "✅ Created .env from template — edit it now")

first-setup: ## Interactive onboarding — generates .env, installs hooks, smoke-tests api.main
	bash scripts/first_setup.sh

requirements: ## Export requirements.txt from pyproject
	$(PIP) install pip-tools
	$(PIP) compile pyproject.toml -o requirements.txt
	$(PIP) compile --extra dev pyproject.toml -o requirements-dev.txt

# ── Quality ────────────────────────────────────────────────────
lint: ## Run ruff + black checks
	ruff check .
	black --check .

format: ## Auto-format with ruff + black
	ruff check --fix .
	black .

type-check: ## Run mypy
	mypy core auto_client_acquisition autonomous_growth integrations api

security: security-smoke ## Run security scans
	bandit -c pyproject.toml -r core auto_client_acquisition autonomous_growth integrations api
	detect-secrets scan --baseline .secrets.baseline || true

security-smoke: ## Run dependency-free repository security smoke checks
	$(PYTHON) scripts/security_smoke.py

security-smoke-ci: ## Run CI-safe security smoke checks for docs/tests synthetic fixtures
	$(PYTHON) scripts/ops/security_smoke_ci.py

tenant-scope-check: ## Fail on tenant-owned records queried by id without a tenant filter
	$(PYTHON) scripts/ops/check_tenant_scoped_queries.py

env-check: ## Validate .env.example contract and duplicate keys
	$(PYTHON) scripts/check_env_contract.py

railway-env-check: ## Validate Railway production env names without printing secret values
	$(PYTHON) scripts/ops/check_railway_production_env.py

openapi-export: ## Export FastAPI OpenAPI schema (OPENAPI_OUTPUT=...)
	$(PYTHON) scripts/export_openapi.py --output $(OPENAPI_OUTPUT)

api-contract-check: ## Check OpenAPI contract for removed paths/methods
	$(PYTHON) scripts/check_openapi_contract.py

dependency-inventory: ## Export lightweight dependency inventory
	$(PYTHON) scripts/export_dependency_inventory.py

release-manifest: ## Export production release manifest
	$(PYTHON) scripts/export_release_manifest.py

production-smoke: ## Run production API smoke test (PRODUCTION_BASE_URL=...)
	$(PYTHON) scripts/dealix_smoke_test.py --base-url $(PRODUCTION_BASE_URL)

prod-verify: env-check security-smoke api-contract-check dependency-inventory release-manifest v5-verify ## Canonical production-readiness verification bundle
	@echo "✅ Dealix production verification bundle completed"

full-repo-test: ## Run the full repo test matrix with TestSprite when TESTSPRITE_API_KEY is set
	bash scripts/ops/run_full_repo_test_matrix.sh

launch-engine: ## Run the full local launch machine + readiness audit (writes data/daily_ops/<date>/)
	$(PYTHON) scripts/dealix_launch_engine.py

# ── Free LLM Provider Radar ────────────────────────────────────
# Read-only/draft-only operating layer for choosing low-cost AI providers.
# It never sends customer messages and never commits secrets.

ai-provider-radar: ## Show daily provider choices for coding, Arabic, batch, and sensitive work
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task coding --limit 3
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task arabic --limit 3
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task batch --limit 3
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task sensitive --limit 3

ai-provider-radar-json: ## Print machine-readable provider radar for coding
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task coding --json

ai-provider-registry-check: ## Guard: fail if the free-LLM provider registry is stale (improve executor safety)
	$(PYTHON) scripts/ops/check_provider_registry_freshness.py

ai-provider-coding: ## Provider radar optimized for repo/code work
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task coding --limit 5

ai-provider-arabic: ## Provider radar optimized for Arabic/Saudi draft work
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task arabic --limit 5

ai-provider-batch: ## Provider radar optimized for daily batch drafting
	$(PYTHON) scripts/ops/free_llm_provider_radar.py --task batch --limit 5

daily-value-loop: ai-provider-radar distribution-day ## Run provider radar then founder distribution day
	@echo "✅ Daily value loop ready — review docs/ops/FREE_LLM_DAILY_VALUE_LOOP.md before external action"

# ── Design Command Room OS ─────────────────────────────────────
# Draft-only artifact generation. No external sends, no production mutations,
# no runtime dependency changes. Outputs go to reports/design/.

design-os-list: ## Design OS: list available artifact templates
	$(PYTHON) scripts/design_command_room.py --list

design-os-generate: ## Design OS: generate one draft artifact (TYPE=... CONTEXT=...)
	$(PYTHON) scripts/design_command_room.py --type $(TYPE) --context "$(CONTEXT)"

design-os-all: ## Design OS: generate all core draft artifacts
	$(PYTHON) scripts/design_command_room.py --type all --context "$(CONTEXT)"

design-os-daily: ## Design OS: generate daily pack + index + validation + HTML preview
	$(PYTHON) scripts/design_os_suite.py daily-pack --context "$(CONTEXT)"

design-os-validate: ## Design OS: validate generated draft artifacts
	$(PYTHON) scripts/design_os_suite.py validate

design-os-index: ## Design OS: build artifact index
	$(PYTHON) scripts/design_os_suite.py index

design-os-html: ## Design OS: render reports/design/latest.md to HTML preview
	$(PYTHON) scripts/design_os_suite.py html

test-design-os: ## Design OS: run focused generator and automation tests
	$(PYTHON) -m pytest -q tests/test_design_command_room.py tests/test_design_os_suite.py

# ── Tests ──────────────────────────────────────────────────────
test: ## Run full test suite with coverage
	pytest -v

test-unit: ## Unit tests only
	pytest -v -m "not integration" tests/unit

test-integration: ## Integration tests only
	pytest -v tests/integration

# ── Pre-commit ─────────────────────────────────────────────────
pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

# ── Run locally ────────────────────────────────────────────────
run: ## Run API server (dev mode, reload on changes)
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

demo: ## Run interactive CLI demo
	$(PYTHON) cli.py

cockpit: ## Founder Daily Brief — single-screen status (composes Bottleneck Radar + Hard Gates + Service Catalog)
	$(PYTHON) scripts/dealix_founder_daily_brief.py

doctor: env-check alembic-heads security-smoke ## Health check — env contract + single alembic head + security smoke
	@echo "✅ Repo doctor passed — see docs/playbooks/FOUNDER_NEXT_STEPS.md for what to do today"

alembic-heads: ## Fail if alembic reports >1 migration head
	$(PYTHON) scripts/check_alembic_single_head.py

agents-audit: ## Audit agent-team governance (strict — same gate as CI agent-team-audit)
	$(PYTHON) scripts/audit_agent_team.py --strict

pr-triage: ## Triage open PRs into buckets (report-only — never merges or comments)
	$(PYTHON) scripts/triage_open_prs.py

# ── Database ───────────────────────────────────────────────────
db-init: ## Initialize database tables (dev only)
	$(PYTHON) -c "import asyncio; from db.session import init_db; asyncio.run(init_db())"

# ── Docker ─────────────────────────────────────────────────────
docker-build: ## Build Docker image
	docker build -t dealix:latest .

docker-up: ## Start full stack (app + postgres + redis + mongo)
	docker compose up -d --build

docker-down: ## Stop and remove containers
	docker compose down

docker-logs: ## Tail application logs
	docker compose logs -f app

# ── Cleanup ────────────────────────────────────────────────────
clean: ## Remove build artifacts, caches
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# ── Distribution / Revenue Execution OS ────────────────────────
# Approval-first revenue execution. All read-only or draft-only — none of
# these send anything externally or charge a customer.

distribution-day: ## Founder morning command report (pending drafts, due follow-ups, queues)
	$(PYTHON) scripts/distribution_day.py

draft-quality: ## Draft Quality Gate — fail on guaranteed-outcome / forbidden-channel drafts
	$(PYTHON) scripts/check_draft_quality.py

distribution-metrics: ## Write the daily + weekly distribution KPI snapshot
	$(PYTHON) scripts/distribution_metrics.py

# ── v5 founder CLIs ────────────────────────────────────────────
# These wrap the read-only Dealix v5 founder tooling. Each is safe
# to run any time — none of them write to production or send anything.

v5-status: ## v5: bilingual local snapshot (services + reliability + live gates)
	$(PYTHON) scripts/dealix_status.py

v5-smoke: ## v5: cross-platform smoke test against a deploy (BASE_URL=...)
	$(PYTHON) scripts/dealix_smoke_test.py $(if $(BASE_URL),--base-url $(BASE_URL))

v5-snapshot: ## v5: write JSON audit snapshot to docs/snapshots/<today>.json
	$(PYTHON) scripts/dealix_snapshot.py

v5-diagnostic: ## v5: list available bundles for the Diagnostic generator
	$(PYTHON) scripts/dealix_diagnostic.py --list-bundles

v5-verify: ## v5: 22-point production verifier (set BASE_URL=...)
	bash scripts/post_redeploy_verify.sh

v5-digest: ## v5: print the daily founder digest markdown (no email)
	$(PYTHON) scripts/dealix_morning_digest.py --print

v5-proof-pack: ## v5: assemble bilingual Proof Pack from JSONL events (HANDLE=...)
	$(PYTHON) scripts/dealix_proof_pack.py --customer-handle $(HANDLE)

# ── v10 founder + reference library ────────────────────────────
# v10 = AI Business Operating System reference architecture.
# Each target is read-only diagnostics — never live actions.

v10-verify: ## v10: full master verification (reference + modules + safety + tests)
	bash scripts/v10_master_verify.sh

v10-reference: ## v10: show 70-tool reference library summary
	$(PYTHON) scripts/verify_reference_library_70.py

# ── Launch OS (GTM Revenue Intelligence) ───────────────────────
# All targets are read-only dry-runs — no external sends, no production mutations.

launch-validate: ## Launch OS: validate schemas + file inventory
	$(PYTHON) scripts/launch/launch_bundle_validate.py

launch-vertical-score: ## Launch OS: print ranked Saudi verticals + top wedge
	$(PYTHON) scripts/launch/vertical_score_dry_run.py

launch-icp-score: ## Launch OS: score sample accounts, print tier table
	$(PYTHON) scripts/launch/icp_score_dry_run.py

launch-trust-preflight: ## Launch OS: run trust preflight on sample drafts
	$(PYTHON) scripts/launch/trust_preflight_dry_run.py

launch-outreach-drafts: ## Launch OS: generate sample outreach drafts (email/linkedin/phone)
	$(PYTHON) scripts/launch/outreach_draft_factory_dry_run.py

launch-proposal: ## Launch OS: render sample proposal pack to markdown
	$(PYTHON) scripts/launch/proposal_pack_dry_run.py

launch-founder-command: ## Launch OS: generate today's founder daily brief
	$(PYTHON) scripts/launch/founder_daily_command_dry_run.py

launch-weekly-review: ## Launch OS: print weekly GTM review from sample pipeline
	$(PYTHON) scripts/launch/weekly_gtm_review_dry_run.py

launch-content: ## Launch OS: generate sample content assets (LinkedIn / video / email)
	$(PYTHON) scripts/launch/content_factory_dry_run.py

launch-pipeline: ## Launch OS: print pipeline summary from sample data
	$(PYTHON) -c "from dealix.launch_os.pipeline_tracker import PipelineTracker; t = PipelineTracker(); t.seed_sample(); print(t.pipeline_summary())"

launch-all-dry-runs: launch-validate launch-vertical-score launch-icp-score launch-trust-preflight launch-outreach-drafts launch-proposal launch-founder-command launch-weekly-review launch-content ## Launch OS: run all dry-run scripts in sequence
	@echo "✅ All Launch OS dry-runs completed"

# ── Commercial Intelligence CLI ─────────────────────────────────

score-prospect: ## CI: score one Saudi prospect
	$(PYTHON) -m cli.sales_strategist --company "$(COMPANY)" --sector "$(SECTOR)" --city "$(CITY)" --employees $(EMPLOYEES) --website "$(WEBSITE)"

score-batch: ## CI: score a batch of prospects from JSON
	$(PYTHON) -m cli.sales_strategist --batch $(BATCH_FILE)

analyze-pipeline: ## CI: analyze a pipeline CSV and print recommendations
	$(PYTHON) scripts/analyze_pipeline.py --input $(PIPELINE_CSV)

intelligence-test: ## CI: run the new intelligence layer tests
	$(PYTHON) -m pytest tests/test_intelligence_layer.py tests/test_sales_strategist_agent.py -q


# ── Brand & Growth Portfolio V2 ─────────────────────────────────

brand-growth-verify: ## Verify the multi-arm portfolio contract and runtime gates
	$(PYTHON) scripts/verify_brand_growth_portfolio_v2.py
	$(PYTHON) scripts/verify_brand_growth_portfolio_runtime_v1.py

brand-growth-run: ## Compile an explicit Market Radar snapshot (RADAR_SNAPSHOT=...)
	@test -n "$(RADAR_SNAPSHOT)" || (echo "RADAR_SNAPSHOT is required; no synthetic input is allowed" >&2; exit 2)
	$(PYTHON) scripts/commercial/run_brand_growth_portfolio_v2.py \
		--input "$(RADAR_SNAPSHOT)" \
		--out "data/founder_briefs/brand_growth_portfolio_$(date -u +%F).json"

# ── Sovereign Verify ─────────────────────────────────────────────
dealix-verify: ## Run canonical verification (MODE=trust|pr|full|production|security|runtime|commercial|changed) — use MODE=...
	@bin/dealix verify $(MODE)

verify-trust: ## Alias for bin/dealix verify trust
	bin/dealix verify trust

verify-pr: ## Full PR gate via isolated worktree
	bin/dealix verify pr --worktree

verify-full: ## Full verification (trust+security+runtime+commercial)
	bin/dealix verify full

verify-production: ## External production probes only
	bin/dealix verify production
