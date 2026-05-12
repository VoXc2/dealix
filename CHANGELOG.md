# Changelog

## [3.3.0] — 2026-05-22

T5 — AI excellence + Saudi sovereignty deep + platform power. 8 more
commits beyond v3.2.0 turn Dealix into the AI-native operating system
the founder pitched: agent framework, RAG knowledge layer, Arabic
voice channel, Saudi national integrations, deeper observability,
search + time-series + graph, polish + safety + mobile skeleton.

### T5a — AI agent framework
LangChain + LangGraph + DSPy + LiteLLM + Instructor/Outlines + MCP
server exposing Dealix as a Claude Desktop tool + AgentOps/Phoenix
+ DeepEval. Reference graph: dealix-proposal-draft as a 5-node
StateGraph with checkpointed state.

### T5b — RAG knowledge layer
pgvector + migration 006 + KnowledgeDocument/Chunk models. Voyage v3
→ Cohere multilingual v3 → OpenAI 3-small embed chain. Cohere Rerank
top-N. LlamaIndex sentence splitter when installed; naive fallback.
`/api/v1/knowledge/{ingest,search,list,delete}` with PDPL DSR cascade.

### T5c — Voice channel
Deepgram → Whisper → AssemblyAI STT chain. ElevenLabs → Cartesia TTS.
Vapi voice agent + Unifonic Saudi SIP/SMS upstream.
`/api/v1/voice/{inbound,outbound,transcripts}`.

### T5d — Saudi sovereignty deep
Nafath + Yakeen identity clients. Tap + Tabby + Tamara payment
clients. Salla + Zid e-commerce connectors. SAMA Open Banking AIS
stub. `docs/strategic/VISION_2030_ALIGNMENT.md` traceability matrix.

### T5e — Observability deep
HyperDX OTLP exporter, Logfire structured logs, Highlight consent
gate, Prometheus `/metrics` via prometheus-fastapi-instrumentator.

### T5f — Search + data
Meilisearch per-tenant indexes with Postgres ILIKE fallback.
TimescaleDB hypertable migration 007 + ActivityEventRecord. Memgraph
knowledge-graph stub. DuckDB read-only admin warehouse query.

### T5g — Platform polish
Renovate weekly PRs. Snyk daily scans (Python + Node + Docker).
axe-core a11y workflow. Strawberry GraphQL opt-in gateway. In-app
HelpCenter drawer. WorkspaceSwitcher for agency partners. Expo
mobile skeleton. Postman collection builder.

### Closing
requirements.txt + .env.example + 22 sub-processors + QA_REVIEW T5
addendum + CHANGELOG.

### T5 — still founder-owned
Regulator-issued credentials (Nafath / Yakeen / SAMA OB). Vendor
sign-ups (Voyage / Cohere / Deepgram / ElevenLabs / Vapi / Tap /
Tabby / Tamara / HyperDX / Highlight / Logfire / Snyk / Cloudflare
Turnstile / Salla / Zid / Meilisearch / Memgraph). Expo EAS account.
Mintlify hosting + Fern publish tokens.

## [3.2.0] — 2026-05-12

T4 — end-to-end closure. 8 commits making everything cohere: tests,
frontend completeness, audit + authz integration, docs per resource,
integration polish, reliability, compliance.

### T4a — Tests
Integration coverage on every T0-T3 router. Unit coverage for
cost_guard / guardrails / prompt registry / authz / business-hours /
feature flags. Vitest spec for Hijri helpers.

### T4b — Frontend
New pages: support, trial, settings/team, settings/api-keys,
settings/profile, admin/llm, admin/whatsapp/templates, status.
Enterprise SSO button on login. TanStack Query Providers wired.
PDPL cookie banner on landing.

### T4c — Audit + authz
`api/security/audit_writer.audit()` adopted by invite/revoke/
onboarding-finalize/stripe-webhook/support. Billing health honors
PostHog feature flags.

### T4d — Docs
11 Mintlify per-resource pages, DOCS_INDEX, issue + PR templates,
branch-protection guide, README badge refresh.

### T4e — Integration polish
InvoiceRecord + migration 005, Stripe webhook fan-out (Lago + Loops
+ Knock + audit), Wathq verification at onboarding, Jinja renderer
with Hijri + Gregorian, WhatsApp intent helper.

### T4f — Reliability
actionlint CI, monthly DR drill cron, Semgrep in pre-commit, S3
backup verifier, PgBouncer tuning doc, vendor status in deep-health.

### T4g — Compliance
DPA template, GDPR↔PDPL article map, canonical sub-processor list
(29 rows), RFC 9116 security.txt, public legal pages
(privacy/terms/cookies/dpa), live sub-processors page.

### Closing
CI coverage gate raised 70 → 75%. QA_REVIEW T4 addendum.

### Still founder-owned
Legal review of DPA; GitHub branch-protection rules; S3 bucket + IAM;
PagerDuty integration key; Cerbos PDP prod deploy; Inngest Cloud prod
deploy; ISO 27001 audit; Mintlify hosting + Fern publish tokens.

## [3.1.0] — 2026-05-12

T0 + T1 + T2 + T3 — full commercial-readiness + best-tech-company stack
delivered on `claude/comprehensive-qa-review-ZLsYG` across 21 commits.

### T0 — Sellable in two weeks

- Customer portal real DB queries (`/api/v1/customers/{id}/summary|subscription|invoices|team`).
- Self-serve onboarding API + Next.js wizard with DPA capture.
- Stripe scaffold for international checkout; Moyasar remains SAR primary.
- Customer-facing audit log + CSV streaming export.
- Plain support ticketing with Resend email fallback.

### T1 — Enterprise-procurable

- WorkOS Enterprise SSO + Cerbos policy bundle + static-RBAC fallback.
- Portkey LLM gateway with per-tenant cost metadata.
- Knock multi-channel notifications + Infisical secrets vault.
- Mintlify docs portal + Fern SDK codegen + Spectral OpenAPI lint +
  TanStack Query in frontend.

### T2 — Scales to 50 customers

- Inngest durable workflow runtime with reference functions.
- Apollo + Clearbit + Wathq enrichment chain (Saudi-first).
- WhatsApp template admin; Lago usage metering; Loops marketing
  automation; BetterStack heartbeat.

### T3 — Best tech company

#### Engineering rigor (T3a)
- mypy strict-on-subset for security-critical + commercial modules.
- Custom Semgrep ruleset banning print/eval/os.system, raw requests,
  bare except, SQL text injection, hardcoded secrets.
- k6 performance budgets in CI; mutation-testing quarterly drill.
- VS Code + Codespaces devcontainer with Postgres/Redis/Cerbos.
- ADR system seeded with two decisions.
- Mermaid architecture diagrams for every major flow.

#### AI/ML rigor (T3b)
- Per-tenant LLM cost guardrails ($0.50/request, $25/tenant/day) with
  degrade-model fallback.
- Versioned prompt registry + Promptfoo evals in CI.
- Guardrails-AI-style PII + shape validators for proposal outputs.
- Per-tenant LLM usage endpoint + model registry doc.

#### Real-time + analytics (T3c)
- SSE stream for live dashboards (Redis pubsub fan-in).
- Tinybird embedded customer-facing benchmarks.
- dbt project (DuckDB-local + BigQuery-prod profiles).
- Metabase compose for internal BI.
- driver.js first-login product tour.
- PostHog Surveys server-side helper for Day-14 NPS.

#### Operational maturity (T3d)
- Terraform IaC modules for Railway / Postgres / Redis / Cerbos.
- Multi-environment promote workflow with manual approval gate.
- Incident-response runbook + blameless postmortem template + log dir.
- Grafana dashboards-as-code + multi-burn-rate SLO alerts.
- CODEOWNERS + on-call rotation + PagerDuty stub.

#### Saudi sovereignty (T3e)
- ZATCA CSR rotation script.
- PDPL Data-Subject-Rights API (access / delete / portability).
- Arabic-first RTL transactional email templates with dual-calendar.
- Hijri JS helpers.
- Saudi region migration runbook.
- Opt-in business-hours middleware (Sun-Thu 09-18 Riyadh).

#### Customer experience (T3f)
- Customer-health auto-alert Inngest function.
- In-app changelog popover.
- Public roadmap with JSON-driven landing page.
- Founder-only NPS dashboard.
- 11 documented Loops trigger events.

#### Open-source motion (T3g)
- `dealix` CLI (typer) wrapping leads / webhooks / onboarding /
  support / audit.
- Six SDK examples (Python + TypeScript).
- AGENTS.md extended with conventions for AI + human contributors.
- GitHub Discussions template for partner Q&A.

### Out-of-scope (founder-owned)

External account signups (WorkOS, Stripe, Plain, Knock, BetterStack,
Portkey, Lago, Loops, Apollo, Clearbit, Wathq, Infisical, Tinybird,
Grafana, PagerDuty, dbt Cloud); SOC 2 Type I auditor; Saudi-region
cloud contract; PyPI/npm publishing tokens; Cerbos production deploy;
Inngest Cloud production deploy; pen-test vendor.

## [3.0.0] — 2026-04-23

### ✨ Features — Dealix v3.0.0 الإطلاق الكامل

#### Phase 2 — Cost Optimization
- **Prompt caching** (Anthropic): `cache_control: ephemeral` على system prompts ≥ 1024 توكن (توفير 90%)
- **Semantic cache**: Redis-backed + multilingual MiniLM embeddings (threshold 0.95, TTL 24h)
- **Cost tracker**: Postgres `llm_calls` table + ring buffer + MODEL_PRICES
- **Smart routing** (`core/config/models.smart_route`): Groq للتصنيف، DeepSeek للكود، GLM للعربية، Gemini Flash للبحث، Anthropic للحرج
- **Batch mode** (`AcquisitionPipeline.run_batch`): asyncio.Semaphore=8 للـ≥5 عملاء

#### Phase 3 — Security
- **Rate limiting** (slowapi): leads 10/min, sales 30/min, WA 100/min, generic 60/min, global 1000/min
- **API key middleware** مع `hmac.compare_digest`
- **Webhook signatures**: HubSpot v3 + Calendly + n8n HMAC verification
- **scripts/rotate_secrets.sh**: تدوير API_KEYS / HUBSPOT_APP_SECRET / CALENDLY_WEBHOOK_SECRET / N8N_WEBHOOK_SECRET / JWT_SECRET / DEALIX_INTERNAL_TOKEN

#### Phase 4 — Observability
- **OpenTelemetry**: FastAPI + HTTPX + SQLAlchemy instrumentation + custom LLM/agent/tool spans → Langfuse
- **Sentry** مع FastApiIntegration + SqlalchemyIntegration
- `/health/deep` يفحص Postgres + Redis + LLM providers
- `/api/v1/admin/costs` يجمع الإنفاق حسب model/provider/task
- `/api/v1/admin/cache/stats`

#### Phase 5 — Integrations
- **ConnectorFacade** موحّد: timeout/retry/idempotency/policy/audit
- **EnrichSoClient** lead enrichment عبر إيميل
- **HubSpotTwoWay**: upsert_contact + handle_inbound_webhook
- **CalendlyDynamic**: create_single_use_link

#### Phase 6 — Intelligence
- **Arabic NLP**: normalize (hamza/taa/tashkeel/tatweel) + segment + is_arabic
- **Arabic sentiment** (lexicon خليجي + negator detection)
- **Intent classifier** (quote/demo/support/partnership/greeting/compliment/complaint)
- **Lead scorer** heuristic + ML-ready sklearn interface

#### Phase 7 — Dashboard
- Streamlit RTL لوحة: Overview / Leads / Approvals / Evidence / Costs / Audit
- Port 8501، يقرأ من API

#### Phase 8 — CI/CD
- **CodeQL** Python (security-and-quality queries)
- **Docker build** مع Trivy CRITICAL/HIGH + SBOM (SPDX-JSON) + GHCR
- **Release Please** لتوليد إصدارات وchangelog تلقائياً
- **Dependabot** أسبوعي (pip + github-actions + docker)
- **pre-commit**: ruff + mypy + bandit + gitleaks

#### Phase 9 — Infrastructure
- `scripts/infra/ssh_harden.sh`: port 2222 + fail2ban + UFW
- `scripts/infra/ssl_certbot.sh`: Let's Encrypt auto-renew
- `scripts/infra/backup_pg.sh`: pg_dump يومي + استبقاء 14 يوم
- `scripts/infra/uptimerobot_setup.md`
- `scripts/infra/logrotate.conf`

#### Phase 10 — Tests + Docs
- Unit tests: smart_routing، arabic_nlp، lead_scorer، sentiment، webhook_signatures (72 اختبار نجحت)
- Integration tests: connector_facade retry + policy
- docs/COST_OPTIMIZATION.md + SECURITY_GUIDE.md + DASHBOARD.md + API_REFERENCE.md + postman_collection.json

#### Phase 11 — Release
- tests/e2e/test_e2e.py (smoke ضد instance مشغّل)
- tests/load/k6_smoke.js (100 VU لـ2.5 دقيقة)
- tag v3.0.0

### Phase 1 — GitHub Cleanup (sesión سابقة)
- حذف 10 branches dependabot قديمة
- main protected (linear history, no force push, PR review, conversation resolution)
- Dependabot alerts + secret scanning + push protection مفعّلة
- tag v3.0.0 تم تعيينه

---

**Breaking changes:** لا يوجد (هذا أول إصدار رسمي public).
