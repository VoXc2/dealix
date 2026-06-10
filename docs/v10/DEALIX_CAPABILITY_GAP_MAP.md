# Dealix Capability Gap Map / خريطة الفجوات

> Per-layer answer to: **what does Dealix have today, what's the
> target state, and what concrete pattern do we ship to close the
> gap?**

**Date:** 2026-05-05
**Companion docs:** `docs/V10_MASTER_PLAN.md`, `docs/v10/REFERENCE_LIBRARY_70.yaml`, `docs/v10/V10_TOP_10_REFERENCE.md`
**Hard rule:** every "Recommended P0 implementation" is a `native_pattern` (zero new dependency).

---

## 1. AI Workforce / فريق الذكاء الصناعيّ

### Current state
`auto_client_acquisition/ai_workforce/` (commit `bf9516e`):
- 12 specialized agents with hard autonomy + ComplianceGuard veto
- 4 endpoints (`/status`, `/agents`, `/agents/{id}`, `POST /run`)
- 30 tests (registry + policy + orchestrator)

### Target state
Add reviewer + planner roles per AutoGen pattern; memory pattern from LangGraph; explicit handoff per CrewAI.

### Gap
- No reviewer agent (each agent's output goes straight to ComplianceGuard)
- No planner agent (Orchestrator hardcodes `route_for_goal`)
- No memory across runs (each `WorkforceRun` is independent)

### Recommended P0 implementation
- New module: `auto_client_acquisition/ai_workforce_v10/` (extends existing)
- ReviewerAgent + PlannerAgent specs added to AGENT_REGISTRY
- ≤ 400 LOC, ≥ 10 tests
- Endpoint: `POST /api/v1/ai-workforce-v10/plan`

### Tools that inform this layer
- LangGraph (P0) — state + memory pattern
- AutoGen (P0) — reviewer pattern
- CrewAI (P1) — handoff
- OpenAI Swarm (P2) — minimal orchestrator
- Semantic Kernel (P3) — skill plugin reference
- Pydantic AI / Instructor (P1) — typed output schema

### Tests required
`tests/test_ai_workforce_v10.py` covering reviewer-runs-after, planner-decomposes-goal, memory-stays-within-customer.

### Evidence gates
- ReviewerAgent fires AFTER each main agent and BEFORE ComplianceGuard
- No agent escapes ComplianceGuard veto
- Memory state never crosses customer boundaries (PDPL)

### Founder decision required
§S6 — first 3 `optional_adapter` integrations (LiteLLM + Langfuse + Qdrant)

---

## 2. Workflow OS / Durable Execution

### Current state
`auto_client_acquisition/customer_loop/` (12-state journey machine + `ALLOWED_TRANSITIONS`).
`auto_client_acquisition/diagnostic_workflow/` (orchestrates the Pilot pipeline).

### Target state
Retry policy + idempotency + checkpoint contract so the 7-day Pilot survives a server crash mid-day.

### Gap
- No retry policy on individual steps
- No idempotency tokens
- No durable checkpoints (each advance is in-memory only)

### Recommended P0 implementation
- New module: `auto_client_acquisition/workflow_os_v10/`
- `state_machine.py` + `retry_policy.py` + `idempotency.py` + `checkpoint.py`
- ≤ 700 LOC, ≥ 12 tests
- Endpoints: `POST /api/v1/workflow-os-v10/start`, `GET /{id}`, `POST /{id}/advance`

### Tools that inform this layer
- Temporal (P0) — durable workflow + retry semantics
- LangGraph (P0) — checkpoint pattern
- DBOS (P1) — Postgres-backed durability
- Trigger.dev (P2) — retry decorator
- Prefect / Dagster (P3) — defer

### Tests required
`tests/test_workflow_os_v10.py` covering retry-up-to-N, idempotent-replay-no-double-charge, checkpoint-resume-after-crash.

### Evidence gates
- A Pilot workflow survives a process restart
- Same idempotency_key replayed N times → 1 effect
- Retry exhaustion produces a `blocked` outcome with reason

### Founder decision required
None for Phase B (native pattern). §S7 for real Temporal in Phase E.

---

## 3. CRM / RevOps

### Current state
Ad-hoc Lead/Deal tracking inside `auto_client_acquisition/intake/` and `customer_loop/`. No formal Account/Contact/Deal/Opportunity hierarchy.
`auto_client_acquisition/finance_os/` has InvoiceDraft + manual payment guard.

### Target state
Typed object model: Account → Contact → Lead → Deal → Opportunity → ServiceSession → ProofEvent → CustomerHealth, with stage machine + lead/deal scoring + customer health score.

### Gap
- No Account/Contact/Opportunity types
- No lead scoring
- No customer health score
- No customer timeline view

### Recommended P0 implementation
- New module: `auto_client_acquisition/crm_v10/` (object_model + stage_machine + lead_scoring + deal_scoring + account_timeline + customer_health)
- ≤ 800 LOC, ≥ 15 tests
- Endpoints: `GET /api/v1/crm-v10/schema`, `POST /score-lead`, `POST /score-deal`

### Tools that inform this layer
- Twenty CRM (P0) — custom-objects model
- Linear pattern (P1) — state-machine UX
- Monica CRM (P2) — timeline pattern
- SuiteCRM / ERPNext / Odoo / EspoCRM (P3) — reference only

### Tests required
`tests/test_crm_v10.py` covering schema integrity, stage machine transitions, score deterministic.

### Evidence gates
- All 14 object types defined with Pydantic v2
- No PII exposed without consent
- Customer health score reproducible from same inputs

### Founder decision required
§S7 for real Twenty install (Phase E).

---

## 4. Customer Inbox / Support

### Current state
`auto_client_acquisition/customer_data_plane/` handles consent + redaction. No conversation/message inbox.

### Target state
Typed conversation model with channel + consent_status + SLA + AI suggested reply (drafts only).

### Gap
- No conversation/message types
- No SLA tracker per channel
- No AI suggested reply (founder writes manually)

### Recommended P0 implementation
- New module: `auto_client_acquisition/customer_inbox_v10/`
- conversation_model + consent_status + sla_policy + routing_policy + reply_suggestion + escalation
- ≤ 500 LOC, ≥ 8 tests
- Endpoint: `POST /api/v1/customer-inbox-v10/suggest-reply`

### Tools that inform this layer
- Chatwoot (P0) — omnichannel inbox model
- Zammad (P1) — SLA tracker
- FreeScout (P2) — shared mailbox UX
- Cal.com (P1) — booking integration

### Tests required
`tests/test_customer_inbox_v10.py` covering: outbound WhatsApp blocked unless opt-in, AI suggestion ALWAYS draft_only, SLA timer triggers escalation.

### Evidence gates
- Cold WhatsApp send blocked at routing
- Opt-out updates consent registry immediately
- SLA breach raises an approval-required alert

### Founder decision required
§S6 for real Chatwoot adapter (Phase D).

---

## 5. Growth / Marketing / Analytics

### Current state
`auto_client_acquisition/gtm_os/` (content_calendar + experiment) + `self_growth_os/` modules. No unified event taxonomy.

### Target state
PostHog-style event taxonomy + funnel model + attribution model + content calendar with consent-aware lifecycle.

### Gap
- No canonical event names
- No funnel definition
- No attribution model

### Recommended P0 implementation
- New module: `auto_client_acquisition/growth_v10/`
- event_taxonomy.py + funnel_model + campaign_lifecycle + experiment_model + attribution_model + feedback_model + content_calendar
- ≤ 300 LOC for event_taxonomy alone, ≥ 6 tests
- Endpoint: `GET /api/v1/growth-v10/event-taxonomy`

### Tools that inform this layer
- PostHog (P0) — event taxonomy + funnel
- GrowthBook (P1) — feature flags + experiments
- Mautic (P1) — campaign lifecycle (gated on consent)
- Umami / Plausible (P1) — site analytics adapter
- Postiz / Listmonk / Keila (P2/P3) — content + email (gated on consent)

### Tests required
`tests/test_growth_v10.py` — 17 canonical events present, funnel converts in correct order, no PII in event payloads.

### Evidence gates
- Lead → Diagnostic → Pilot → Paid → Proof funnel computable from events
- Every event payload runs through redactor
- Marketing automation defaults to draft-only

### Founder decision required
§S6 for real PostHog adapter (Phase D).

---

## 6. Knowledge / RAG / Search

### Current state
No formal Company Brain knowledge backend. `auto_client_acquisition/self_growth_os/search_radar.py` is curated-only.

### Target state
Retrieval contract + answer contract + RAG eval contract + source policy (no scraping by default).

### Gap
- No retrieval interface
- No RAG eval (faithfulness / context recall)
- No document manifest (PDF/DOC ingestion)

### Recommended P0 implementation
- New module: `auto_client_acquisition/knowledge_v10/`
- source_policy + document_manifest + retrieval_contract + answer_contract + citation_policy + rag_eval_contract + search_router
- ≤ 500 LOC, ≥ 10 tests
- Endpoints: `POST /api/v1/knowledge-v10/search`, `POST /answer`, `POST /evaluate`

### Tools that inform this layer
- Qdrant (P0) — production vector DB schema
- Haystack (P0) — pipeline DAG pattern
- LlamaIndex (P1) — document manifest
- Open RAG Eval / Ragas (P1) — eval metrics
- Unstructured / Docling (P1) — document parsing
- Crawl4AI / Firecrawl (P3, default-blocked) — web extraction
- LanceDB / Chroma / Weaviate / Milvus (P2/P3) — alternatives

### Tests required
`tests/test_knowledge_v10.py` — every answer has source confidence, "insufficient_evidence" returned when no source, scraping blocked at policy level.

### Evidence gates
- No hallucinated facts (every answer references a source_id)
- No PII ingested without explicit customer permission
- Allowed-source policy enforced at ingestion

### Founder decision required
§S6 for Qdrant adapter (Phase D).

---

## 7. LLM Gateway / Cost Control

### Current state
`auto_client_acquisition/ai_workforce/cost_guard.py` (CostBudget + CostEstimate + ModelTier + estimate_for_task + enforce_run_budget + simple estimate_cost / enforce_budget). No model routing, no cache, no fallback chain.

### Target state
LiteLLM-style gateway with model routing per task purpose, per-customer budget, fallback chain, cache policy.

### Gap
- No actual model routing (cost_guard is a budget calculator)
- No fallback chain
- No cache policy

### Recommended P0 implementation
- New module: `auto_client_acquisition/llm_gateway_v10/`
- model_catalog + routing_policy + budget_policy + token_estimator + cache_policy + fallback_policy + run_summary
- ≤ 600 LOC, ≥ 8 tests
- Endpoints: `POST /api/v1/llm-gateway-v10/route`, `POST /estimate-cost`

### Tools that inform this layer
- LiteLLM (P0) — gateway pattern
- Helicone (P2) — request log schema
- Langfuse (P0) — cost attribution

### Tests required
`tests/test_llm_gateway_v10.py` — cheap_model for classification, strong_model for strategy, budget hard-stop returns deterministic decision.

### Evidence gates
- No live API call from this module (router only)
- Per-customer budget never silently exceeded
- Cache hit rate measurable

### Founder decision required
§S6 for real LiteLLM install (Phase D).

---

## 8. Safety / Evals / Policy

### Current state
`tests/test_v7_*.py` has 8 safety perimeter test files. `auto_client_acquisition/security_privacy/` has secret_scan + log_redaction + minimization. No unified eval pack.

### Target state
Promptfoo-style eval pack with red-team cases (Arabic + English) + policy engine + output validator + report.

### Gap
- No unified safety eval runner (tests are scattered)
- No policy engine that takes structured input + returns block/allow
- No output validator (Pydantic catches schema, not content policy)

### Recommended P0 implementation
- New module: `auto_client_acquisition/safety_v10/`
- eval_cases + redteam_cases + policy_engine + output_validator + report
- ≤ 800 LOC, ≥ 15 tests
- Script: `scripts/run_safety_v10.py`
- Endpoint: `POST /api/v1/safety-v10/run`

### Tools that inform this layer
- Promptfoo (P0) — test-case-as-yaml + CI integration
- Guardrails AI (P1) — output validator pattern
- DeepEval / Ragas / TruLens (P1/P2) — eval metric library
- Open Policy Agent (P2) — policy engine inspiration

### Tests required
`tests/test_safety_v10.py` — every red-team case returns blocked, prompt injection cannot override policy, output validator catches forbidden tokens.

### Evidence gates
- Every red-team category covered (cold WA, LinkedIn, scraping, fake proof, guaranteed claims, prompt injection, PII leakage, secret leakage, excessive agency, unsafe tool use)
- CI gates on safety_v10 result
- No safety case can be "approved" by an agent

### Founder decision required
None for Phase B (native pattern).

---

## 9. Observability / Tracing / Errors

### Current state
`auto_client_acquisition/observability_v6/` (TraceRecord + AuditEvent + Incident schemas + thread-safe in-memory buffers + PII redaction on insert + 3 endpoints).

### Target state
Extends v6 TraceRecord with `cost_estimate`, `risk_score`, `model_name`, `prompt_version`. OpenTelemetry-aligned field names.

### Gap
- TraceRecord lacks cost + risk + model fields
- No Sentry adapter (errors live in logs only)

### Recommended P0 implementation
- New module: `auto_client_acquisition/observability_v10/`
- trace_schema (extends v6) + span_schema + metric_schema + error_schema + redaction (re-uses pii_redactor) + report
- ≤ 400 LOC, ≥ 8 tests
- Endpoints: `POST /api/v1/observability-v10/trace/validate`, `GET /schema`

### Tools that inform this layer
- OpenTelemetry (P0) — vendor-neutral trace standard
- Langfuse (P0) — LLM-specific extension
- OpenLIT (P1) — OTel-LLM convergence
- Helicone (P2) — request log schema
- Sentry (P1) — error capture + PII scrubbing
- AgentOps (P2) — agent run trace tree
- Grafana / Prometheus / Loki / Tempo / Jaeger (P3) — defer until production needs

### Tests required
`tests/test_observability_v10.py` — every trace has redacted_payload, cost field is optional but typed, no PII survives roundtrip.

### Evidence gates
- Trace schema validates against OTel naming
- PII redaction on every insert
- Buffer is thread-safe (parallel writes)

### Founder decision required
§S6 for Sentry adapter; §S7 for real Langfuse (Phase D/E).

---

## 10. DesignOps / Artifacts

### Current state
**SHIPPED at `bf9516e`.** `auto_client_acquisition/designops/` has schemas + skill_registry + design_system_loader + safety_gate + brief_builder + visual_directions + 6 generators + exporter + 11 endpoints. 15 SKILL.md files. 78 tests passing.

### Target state
Add real PDF/PPTX export via Marp adapter (founder-gated).

### Gap
- PDF/PPTX export is stub (markdown + html only)

### Recommended P0 implementation
**No P0 work — already shipped.** P2 adds Marp adapter when first paying customer requests PDF/PPTX.

### Tools that inform this layer
- Open Design (P0) — already shipped
- Marp (P2) — PDF/PPTX export adapter
- Slidev (P2) — alternative deck generator
- Storybook / Docusaurus / Mermaid (P1/P3) — defer/native

### Tests required
Already shipped: `tests/test_designops_*.py` (78 tests).

### Evidence gates
- safe_to_send=False default
- Approval banner on every artifact
- No forbidden-token leak at any rendered surface

### Founder decision required
§S7 for Marp adapter (Phase E, optional).

---

## 11. Platform / Auth / Storage

### Current state
FastAPI + Postgres + Redis (existing). Single-tenant.

### Target state
**Reference only.** Current stack stays primary. Future multi-tenant + RLS + object storage gated on customer #10+.

### Gap
- No row-level security (single-tenant today)
- No external object storage (proof packs are local files)

### Recommended P0 implementation
- New module: `auto_client_acquisition/platform_v10/`
- storage_contract + auth_contract + tenant_contract + rls_contract (interface contracts only — current stack stays primary)
- ≤ 300 LOC, ≥ 4 tests
- No new endpoints

### Tools that inform this layer
- Supabase (P2) — RLS pattern + auth
- Appwrite / Keycloak / Zitadel (P3) — defer
- MinIO (P2) — object storage adapter

### Tests required
`tests/test_platform_v10.py` — contract types validate, no replacement of FastAPI/Postgres assumed.

### Evidence gates
- Current FastAPI/Postgres stays primary
- No new dep added in Phase B
- Contracts ready for adapter when needed

### Founder decision required
§S7 for any real platform install (Phase E).

---

## 12. Founder Command Center

### Current state
`api/routers/founder.py` — extended dashboard with v6 sections (first_3_customers, pending_approvals, unsafe_blocks, next_founder_action). `landing/founder-dashboard.html` is bookmarkable.

### Target state
Compose v10 layers (cost_summary + risk_register + evidence_summary) into one daily brief.

### Gap
- No daily LLM-cost summary surfaced to founder
- No risk register (incidents live in observability_v6)
- No structured evidence summary (proof packs grouped by month)

### Recommended P0 implementation
- New module: `auto_client_acquisition/founder_v10/`
- daily_brief + blockers + next_actions + evidence_summary + cost_summary
- ≤ 300 LOC, ≥ 6 tests
- Endpoints: `GET /api/v1/founder-v10/today`, `GET /blockers`, `GET /evidence`

### Tools that inform this layer
- Composes everything above (no new tools).

### Tests required
`tests/test_founder_v10.py` — daily brief composes from existing layers, cost summary integrates with llm_gateway_v10.

### Evidence gates
- Daily brief never references unsourced metrics
- Cost summary matches sum of llm_gateway_v10 runs
- No PII in daily brief

### Founder decision required
None for Phase B (composes existing modules).

---

## Summary table

| # | Layer | Current | Target | Gap | P0 module | Tools |
|---|---|---|---|---|---|---|
| 1 | AI Workforce | 12 agents + Orchestrator | + Reviewer + Planner + Memory | 3 missing roles + memory | `ai_workforce_v10/` | LangGraph, AutoGen, CrewAI |
| 2 | Workflow OS | 12-state machine | + retry + idempotency + checkpoint | no durability | `workflow_os_v10/` | Temporal, DBOS |
| 3 | CRM | Ad-hoc tracking | 14-object typed model + scoring | no formal types | `crm_v10/` | Twenty, Linear pattern |
| 4 | Inbox | Consent + redaction | conversation model + SLA + suggested reply | no inbox | `customer_inbox_v10/` | Chatwoot, Zammad |
| 5 | Growth | content calendar + experiments | event taxonomy + funnel + attribution | no canonical events | `growth_v10/` | PostHog, GrowthBook |
| 6 | Knowledge | curated search radar | retrieval + answer + eval contract | no RAG | `knowledge_v10/` | Qdrant, Haystack |
| 7 | LLM Gateway | cost_guard (budget calc) | model routing + fallback + cache | no router | `llm_gateway_v10/` | LiteLLM |
| 8 | Safety | 8 perimeter test files | unified eval pack + policy engine | scattered | `safety_v10/` | Promptfoo, Guardrails |
| 9 | Observability | observability_v6 (Trace + Audit + Incident) | + cost + risk_score + model_name | partial | `observability_v10/` | OpenTelemetry, Langfuse |
| 10 | DesignOps | ✅ shipped (`bf9516e`) | optional Marp adapter | none for P0 | (already shipped) | Open Design, Marp |
| 11 | Platform | FastAPI + Postgres | reference contracts only | no replacement needed | `platform_v10/` | Supabase, MinIO (defer) |
| 12 | Founder | Dashboard + 4 v6 sections | + cost + risk + evidence summary | partial | `founder_v10/` | composes 1-11 |

---

— Capability Gap Map v1.0 · 2026-05-05 · Dealix
