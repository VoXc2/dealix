## [3.0.0] — 2026-04-23

### 🚀 Production-ready with cost optimization

This is the production-grade release of Dealix, renamed from ai-company-saudi.

### ✨ Added (in this release cycle, more incoming)
- Renamed project: ai-company-saudi → dealix
- Prepared infrastructure for cost optimization layer
- Clean history reset for consistent CI/CD

### 🔄 Changed
- Project name in pyproject.toml
- App name in settings
- Version bumped to 3.0.0

### 🗑️ Removed
- Orphan Dependabot branches (pointing to non-existent frontend/backend)


# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] — 2026-04-21

### 🏛️ Dealix Tier-1 governance layer

This release adds the full Dealix sovereign governance layer on top of the v2.0.0 platform. The underlying Phase 8 and Phase 9 agents are unchanged; they are now composed under a non-bypassable Trust Plane.

### ✨ Added

**Master Blueprint & governance documents** (`docs/blueprint/` + `dealix/masters/`)
- `docs/blueprint/master-architecture.md` — 18-section canonical source of truth
- `dealix/masters/constitution.md` — binding AI Operating Constitution (13 articles)
- `dealix/masters/trust_fabric_spec.md` — Trust Plane components + interface contracts
- `dealix/masters/execution_fabric_spec.md` — Execution Plane rules and phased plan
- `dealix/masters/repo_operating_pack.md` — branch model, CI gates, release process
- `dealix/masters/evidence_pack_spec.md` — full Evidence Pack specification
- `dealix/masters/incident_rollback_runbook.md` — P0/P1 playbooks + rollback procedures
- `dealix/masters/release_readiness_checklist.md` — pre-release gate

**Governance registers** (`dealix/registers/`)
- `no_overclaim.yaml` — 25+ public claims tracked with status (Production/Partial/Pilot/Planned) and evidence paths
- `compliance_saudi.yaml` — PDPL + NCA ECC 2-2024 + DCC-1:2022 + CCC 2:2024 + NIST AI RMF + OWASP LLM Top 10 mapped
- `technology_radar.yaml` — ADOPT/TRIAL/ASSESS/HOLD status for every dependency
- `90_day_execution.yaml` — three-phase plan with weekly tasks

**Contracts as working Pydantic models with generated JSON Schemas** (`dealix/contracts/`)
- `DecisionOutput` — the canonical output of any critical agent decision, with `model_validator` enforcing that A2+/R3 decisions carry at least one `Evidence` item
- `Evidence`, `NextAction`, `PolicyRequirement`
- `EventEnvelope` — CloudEvents 1.0 + Dealix extensions (classifications, trace/correlation IDs)
- `EvidencePack` + `BilingualMemo` + `ToolCallRecord` (with intended-vs-actual fields)
- `AuditEntry` + `AuditAction` enum
- `dump_schemas.py` — emits all four JSON Schemas to `dealix/contracts/schemas/`
- `builders.py` — adapters that lift existing Phase 8/9 agent outputs into `DecisionOutput` contracts without rewriting the agents

**Mandatory classifications** (`dealix/classifications/`)
- `ApprovalClass` (A0–A3) with `requires_approval` / `minimum_approvers` properties
- `ReversibilityClass` (R0–R3) with `blocks_auto_execution` property
- `SensitivityClass` (S0–S3) with `is_pdpl_scope` property
- `ACTION_CLASSIFICATIONS` — canonical table mapping every Phase 8/9 action to its (A, R, S) tuple
- `NEVER_AUTO_EXECUTE` — frozenset of actions that always require human approval (pricing commits, contract changes, NDAs, payment terms changes, regulator comms, sensitive data exports)

**Trust Plane** (`dealix/trust/`)
- `PolicyEvaluator` with 6 built-in rules: `never_auto_execute`, `r3_blocks_auto`, `a2_plus_requires_evidence`, `s3_requires_pdpl_check`, `low_confidence_high_stakes`, `approval_class_routing`
- `ApprovalCenter` with TTL, multi-approver support, pluggable notifier hook
- `AuditSink` abstract + `InMemoryAuditSink` concrete implementation
- `ToolVerificationLedger` — records every tool call with `intended_action` vs `actual_action`, flags contradictions

**Governed pipeline** (`dealix/execution/__init__.py`)
- `GovernedPipeline` — wraps `AcquisitionPipeline` and overlays governance without modifying existing code
- Produces `DecisionOutput`s from agent results
- Runs every `NextAction` through the `PolicyEvaluator`
- Creates `ApprovalRequest`s for escalated actions
- Appends `AuditEntry` for every step

**Tests — 38 new tests, all passing**
- `tests/unit/test_dealix_contracts.py` — 16 tests covering classifications, validators, CloudEvents envelope, audit entries
- `tests/unit/test_dealix_trust.py` — 18 tests covering PolicyEvaluator (all 6 rules), ApprovalCenter lifecycle, AuditSink, ToolVerificationLedger
- `tests/integration/test_governed_pipeline.py` — 4 end-to-end tests

**Updated documentation**
- `README.md` — rewritten with Dealix positioning, the Prime Operating Rule, six OS tracks, five planes
- `README.ar.md` — Arabic mirror aligned with new positioning

### 🔒 Security

- Contracts enforce that high-stakes decisions carry evidence at the type level — cannot be bypassed
- `NEVER_AUTO_EXECUTE` list is enforced at the policy layer before execution
- PDPL lawful-basis requirement enforced for S3 actions
- Audit log is append-only by design (no mutation API exposed)

### 📊 Test summary

**63 tests passing** (29 existing + 34 new Dealix tests).

### 📝 Migration notes

- **Fully backward-compatible.** Existing callers of `AcquisitionPipeline` continue to work unchanged.
- **Opt-in governance.** Callers wanting the Trust Plane use `GovernedPipeline` from `dealix.execution` instead.
- **Register update required.** Any new public claim MUST be added to `dealix/registers/no_overclaim.yaml` in the same PR.

---

## [2.0.0] — 2026-04-21

### 🎉 Major release — production-ready multi-agent platform

This release marks the complete ship of the AI Company Saudi platform:
Phase 8 (Auto Client Acquisition) and Phase 9 (Autonomous Growth) are
both feature-complete, tested, documented, and containerized.

### ✨ Added

**Foundation**
- `pydantic-settings`-based configuration loading from `.env` only
- `SecretStr` wrapping for all API keys and credentials
- Comprehensive `.gitignore` preventing secret leaks
- Pre-commit hooks: `gitleaks`, `detect-secrets`, `bandit`, `ruff`, `black`, `mypy`, `hadolint`
- Custom `.gitleaks.toml` with provider-specific secret patterns
- Structlog-based structured logging (JSON in prod, colored in dev)
- Custom exception hierarchy with typed errors

**LLM Routing**
- Task-to-provider routing table with automatic fallback chains
- Unified `LLMClient` interface with 5 concrete implementations:
  - `AnthropicClient` (Claude — reasoning, proposals, writing)
  - `GeminiClient` (research, multimodal)
  - `GroqClient` (Llama 3.3 70B — fast classification)
  - `DeepSeekClient` (code)
  - `GLMClient` (Arabic, Chinese, bulk)
  - `OpenAIClient` (fallback)
- Per-provider usage tracking (calls, tokens, errors, fallbacks)
- Tenacity-powered retry with exponential backoff

**Phase 8 — Auto Client Acquisition**
- `IntakeAgent`: multi-source lead capture with phone/email normalization, dedup hashing, Arabic/English locale detection
- `ICPMatcherAgent`: 5-dimension weighted Fit scoring with tier labels (A/B/C/D)
- `PainExtractorAgent`: hybrid keyword + LLM extraction routed to GLM for Arabic
- `QualificationAgent`: BANT questions (Budget/Authority/Need/Timeline)
- `BookingAgent`: Calendly → Google Calendar → manual fallback, Saudi weekend-aware
- `CRMAgent`: HubSpot contact upsert + deal creation + association with retry
- `ProposalAgent`: Claude-authored proposals with region-aware SAR/USD pricing
- `OutreachAgent`: bilingual cold opener generation per channel
- `FollowUpAgent`: cadence-based messages (canned + LLM)
- `AcquisitionPipeline`: end-to-end orchestration with per-step error isolation

**Phase 9 — Autonomous Growth**
- `SectorIntelAgent`: 12 Saudi sectors with curated market size, growth, pain points, opportunities, AI readiness, regulators, Vision 2030 alignment
- `ContentCreatorAgent`: bilingual articles, LinkedIn posts, case studies, newsletters
- `DistributionAgent`: multi-channel scheduling with Riyadh-timezone optimal posting times
- `EnrichmentAgent`: domain hints + LLM inference for sector/size/region
- `CompetitorMonitorAgent`: positioning, pricing hints, counter-moves
- `MarketResearchAgent`: Gemini-powered research with bullet-pointed findings
- `GrowthOrchestrator`: full sector-campaign workflow

**Integrations**
- WhatsApp Business Cloud API (Meta) with webhook signature verification
- Email: Resend / SendGrid / SMTP with automatic provider selection
- Google Calendar (service account) + Calendly (scheduling links + webhooks)
- HubSpot CRM (thin wrapper over CRMAgent)
- LinkedIn (safe-by-default — ToS compliant)
- n8n webhook client for automation orchestration
- Saudi market constants (GCC countries, Vision 2030 programs, regulators, holidays)

**API**
- FastAPI app with lifespan management
- CORS middleware + structured-logging request-ID middleware
- 6 routers: health, leads, sales, sectors, agents, webhooks
- Full OpenAPI/Swagger at `/docs`, ReDoc at `/redoc`
- Custom exception handlers for `AICompanyError` subclasses

**Database**
- SQLAlchemy 2.0 async models: `LeadRecord`, `DealRecord`, `AgentRunRecord`
- Async session factory with dependency injection
- Alembic migrations stub ready for init

**Dashboard / Analytics**
- KPI aggregation: leads by status/source/sector, deal count, pipeline SAR, agent run stats

**DevOps**
- Multi-stage Dockerfile (Python 3.12-slim, non-root user, tini, healthcheck)
- docker-compose stack: app + PostgreSQL 16 + Redis 7 + MongoDB 7 with healthchecks
- Makefile with 20+ commands for common dev/ops tasks
- GitHub Actions CI: gitleaks + detect-secrets + trufflehog + ruff + black + mypy + bandit + pytest + hadolint + Docker build
- GitHub Actions Release: auto-create GitHub release + build/push Docker image to GHCR
- Dependabot weekly updates for Python, GitHub Actions, Docker
- Issue templates (bug, feature), PR template, CODEOWNERS

**Testing**
- pytest + pytest-asyncio + pytest-cov setup
- Shared fixtures: LLM mock router, async HTTPX client, sample AR/EN lead payloads
- Unit tests: intake, ICP matcher, pain extractor, model router
- Integration tests: API endpoints, full Phase 8 pipeline

**Documentation**
- Bilingual `README.md` + `README.ar.md` with mermaid architecture diagram
- Full CHANGELOG (this file)
- CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- Documentation tree: architecture, agents, api, deployment, pricing, runbook

### 🔒 Security

- All secrets loaded from `.env` only (no hardcoded keys anywhere in the codebase)
- `SecretStr` wraps every sensitive value to prevent accidental logging/repr leaks
- Pre-commit secret scanning prevents committing API keys
- GitHub Actions CI enforces secret scans on every push and PR
- Webhook signature verification for WhatsApp (HMAC-SHA256)
- Non-root Docker container
- LinkedIn integration disabled by default (ToS compliance)

### 📝 Notes

- Minimum Python version: 3.11
- All LLM providers are optional; the router gracefully degrades if keys are missing
- Phase 8 pipeline has per-step error isolation — one failing step does not abort the pipeline

---

## [1.0.0] — Initial baseline

Initial project structure with partial Phase 8 (intake, icp_matcher, pain_extractor) and partial Phase 9 (sector_intel) agents. Superseded by 2.0.0.
