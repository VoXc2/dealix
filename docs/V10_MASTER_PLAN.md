# Dealix v10 — Master Plan (Reference Architecture + Capability Expansion)

> **Status:** Planning document. **Not yet executed.**
> The two long prompts that arrived (the "35-tool reference library"
> and the "70-tool v10 expansion") are merged here into one focused,
> phased execution roadmap.
>
> **Rule:** Dealix studies 70 OSS projects. Dealix does NOT install 70
> dependencies. Each tool produces (a) a documented pattern, (b) an
> optional native lightweight module, (c) maybe-later real adapter.
> Founder approves each step.

**Date drafted:** 2026-05-05
**Prerequisite commit:** `bf9516e` (v7 ai_workforce + DesignOps OS shipped)
**Bundle baseline:** 1262 passed, 8 skipped, 4 xfailed

---

## 0. Strategic synthesis

### What the two prompts asked for (combined)

Both prompts converge on the same insight: **stop adding random
features; turn Dealix into an "AI Business Operating Company"** by
borrowing proven patterns from ~70 OSS projects, but staying native +
lightweight + safe.

The deliverable is **NOT** "install 70 dependencies." The deliverable
is:

1. **Reference Library** — 70 OSS projects studied, each mapped to a
   Dealix capability with risk + priority.
2. **12 Capability Layers** — every layer has a native Pydantic+FastAPI
   implementation, NOT a vendor SDK.
3. **4-Tier Integration Strategy** — every tool is classified as:
   - `inspiration_only` — read the README, copy patterns, never install
   - `native_pattern` — build a small in-repo module mirroring the pattern
   - `optional_adapter` — add a thin adapter the founder can wire in later
   - `real_dependency` — only after founder signs Decision Pack §S6+
4. **Phased Roadmap** — P0/P1/P2/P3 with concrete gating criteria
5. **Hard Rules Unchanged** — no live charge, no live WhatsApp, no
   cold WhatsApp, no LinkedIn automation, no scraping, no fake proof,
   no guaranteed claims, no PII in logs, no secret in repo.

### Why this approach

- **OSS dependency bloat is a known anti-pattern** — every dependency
  is supply-chain risk + license risk + version-skew risk. We avoid
  it by default.
- **Native lightweight modules** — easier to test, easier to audit,
  easier to swap when a real dependency lands.
- **Patterns > products** — Twenty's "custom-objects" data model is
  a pattern; we don't need Twenty itself.
- **Founder-pace shipping** — the founder doesn't need 70 modules; he
  needs the next 3 paying customers. Each layer maps to that loop.

---

## 1. The 12 capability layers

| # | Layer | Dealix module path | Inspired by |
|---|---|---|---|
| 1 | AI Workforce | `auto_client_acquisition/ai_workforce_v10/` (extends existing `ai_workforce/`) | LangGraph, CrewAI, AutoGen, OpenAI Swarm patterns, Semantic Kernel |
| 2 | Workflow OS / Durable Execution | `auto_client_acquisition/workflow_os_v10/` | Temporal, DBOS, Prefect, Dagster, Windmill, Trigger.dev |
| 3 | CRM / RevOps | `auto_client_acquisition/crm_v10/` | Twenty CRM, SuiteCRM, ERPNext, Odoo, EspoCRM, Plane |
| 4 | Customer Inbox / Support | `auto_client_acquisition/customer_inbox_v10/` | Chatwoot, Zammad, FreeScout, Papercups |
| 5 | Growth / Marketing / Analytics | `auto_client_acquisition/growth_v10/` | Mautic, PostHog, GrowthBook, Umami, Matomo, Formbricks, Cal.com |
| 6 | Research / RAG / Knowledge / Search | `auto_client_acquisition/knowledge_v10/` | Haystack, LlamaIndex, Qdrant, Weaviate, Typesense, Meilisearch, Crawl4AI, Firecrawl, OpenRAG, Open RAG Eval, Unstructured, Docling |
| 7 | LLM Gateway / Cost Control | `auto_client_acquisition/llm_gateway_v10/` | LiteLLM, Helicone, Langfuse, OpenLIT, AgentOps |
| 8 | Safety / Evals / Policy | `auto_client_acquisition/safety_v10/` | Promptfoo, Guardrails AI, DeepEval, Ragas, TruLens, Open Policy Agent |
| 9 | Observability / Tracing / Errors | `auto_client_acquisition/observability_v10/` (extends existing `observability_v6/`) | OpenTelemetry, Langfuse, OpenLIT, Sentry, Grafana, Prometheus, Loki, Tempo/Jaeger |
| 10 | DesignOps / Artifact Factory | `auto_client_acquisition/designops_v10/` (extends existing `designops/`) | Open Design, Storybook, Docusaurus, Slidev, Marp, Mermaid |
| 11 | Platform / Auth / Storage | `auto_client_acquisition/platform_v10/` | Supabase, Appwrite, Keycloak, Zitadel, MinIO (reference only — current FastAPI/Postgres stays primary) |
| 12 | Founder Command Center | `auto_client_acquisition/founder_v10/` (extends existing founder dashboard) | composes everything above |

---

## 2. The 4-tier integration strategy

Every tool from the 70-list gets classified into one of these tiers in
the Reference Library Matrix. Defaults are conservative.

| Tier | What it means | Cost | Risk |
|---|---|---|---|
| `inspiration_only` | Read the README. Borrow the pattern. Don't install. | 0 | none |
| `native_pattern` | Build an in-repo module mirroring the pattern in ≤500 lines | small dev time | small (we own the code) |
| `optional_adapter` | Thin adapter file that imports the package only IF installed; raises a friendly error if missing | small | small (founder opts in) |
| `real_dependency` | Listed in `requirements.txt`; CI installs it; production uses it | medium | medium-high (supply chain) |

**Hard rule:** No tool moves to `real_dependency` without:
1. A specific Decision Pack item (§S6+) signed by founder
2. A documented use-case that the native pattern can't cover
3. Security/license review documented in `docs/v10/DEPENDENCY_DECISION_RECORD.md`

---

## 3. Reference Library — 70 tools, 12 categories

The full matrix lives at `docs/v10/REFERENCE_LIBRARY_70.yaml`
(machine-readable) + `docs/v10/REFERENCE_LIBRARY_70.md` (human-readable
narrative per tool). Both are produced in Phase 1 below.

**Top-10 P0 picks** (most impact for least risk):

| # | Tool | Tier | What we build | Why now |
|---|---|---|---|---|
| 1 | Open Design | `native_pattern` | DesignOps OS (already shipped at `bf9516e`) | Done ✅ |
| 2 | LiteLLM | `native_pattern` | `llm_gateway_v10/` cost router (cheap/balanced/strong tiers; budget caps; no actual LiteLLM dep) | Cost control before LLM bills explode |
| 3 | Promptfoo | `native_pattern` | `safety_v10/` eval pack (Arabic + English red-team cases; CI integration) | Catches prompt-injection regressions |
| 4 | Langfuse / OpenLIT | `native_pattern` | `observability_v10/` trace schema (already partially shipped as `observability_v6/`; v10 extends with cost + risk_score) | Founder visibility into what agents do |
| 5 | LangGraph | `native_pattern` | `workflow_os_v10/` state machine (already partially in `customer_loop/`; v10 extends with retry + idempotency) | Reliable 7-day pilot delivery |
| 6 | Chatwoot | `native_pattern` | `customer_inbox_v10/` model (conversation, channel, consent_status, SLA) | Customer conversations become trackable |
| 7 | Twenty CRM | `native_pattern` | `crm_v10/` object model (Account, Contact, Lead, Deal, Opportunity, ServiceSession, ProofEvent, etc.) | Replaces ad-hoc lead tracking |
| 8 | PostHog | `native_pattern` | `growth_v10/event_taxonomy.py` (17 canonical events) | Funnel + attribution measurement |
| 9 | Qdrant / Haystack | `native_pattern` | `knowledge_v10/` retrieval contract (no actual vector DB yet — schema only) | Future-proof Company Brain interface |
| 10 | Temporal / DBOS | `native_pattern` | `workflow_os_v10/` retry + idempotency policies | Pilot delivery survives crashes |

**11–30 P1 picks** ship after first 3 paying pilots produce real data.

**31–70 P2/P3 picks** ship after first 5–10 customers + signed Decision Pack §S6.

---

## 4. Phased execution roadmap

### Phase A — Reference Library + Capability Map (this is the next session)

Goal: produce the research artifacts so the founder knows exactly what
each of the 70 tools is for, what it costs, and what risk it carries.
**No code changes** in this phase beyond the docs.

**Deliverables:**
- `docs/v10/REFERENCE_LIBRARY_70.md` — narrative per tool
- `docs/v10/REFERENCE_LIBRARY_70.yaml` — machine-readable matrix
- `docs/v10/DEALIX_CAPABILITY_GAP_MAP.md` — 12 layers × current/target/gap
- `docs/v10/DEPENDENCY_DECISION_RECORD.md` — empty template; populated as decisions are signed
- `scripts/verify_reference_library_70.py` — checks 70 entries, no dups, every tool has tier+risk+priority
- `tests/test_reference_library_70.py` — pytest verifier

**Acceptance gates:**
- 70 unique tools, each mapped to a layer + tier + risk + priority
- No tool defaults to `real_dependency`
- Every tool with `cold_whatsapp` / `linkedin_automation` / `scraping` capability marked `risk_blocked` and tier `inspiration_only_with_policy_warning`
- Founder reads the 12-layer capability map and can decide P0 picks per layer

**Time estimate:** 2–3 hours of agent + main-thread work.

---

### Phase B — P0 Native Patterns (10 modules)

Goal: build the 10 P0 native patterns from the table above, each as a
small Python module with tests. **No new dependencies** in
`requirements.txt`.

**Modules to build (mostly extend existing v6/v7 modules):**

| # | New module | Approx LOC | Tests | Endpoint |
|---|---|---|---|---|
| 1 | `llm_gateway_v10/` | ≤ 600 | 8+ | POST /api/v1/llm-gateway-v10/route + estimate-cost |
| 2 | `safety_v10/` | ≤ 800 | 15+ | POST /api/v1/safety-v10/run |
| 3 | `observability_v10/` (extends v6) | ≤ 400 | 8+ | GET /api/v1/observability-v10/schema |
| 4 | `workflow_os_v10/` | ≤ 700 | 12+ | POST /api/v1/workflow-os-v10/start + advance |
| 5 | `customer_inbox_v10/` | ≤ 500 | 8+ | POST /api/v1/customer-inbox-v10/suggest-reply |
| 6 | `crm_v10/` | ≤ 800 | 15+ | GET /api/v1/crm-v10/schema; POST /score-lead |
| 7 | `growth_v10/event_taxonomy.py` | ≤ 300 | 6+ | GET /api/v1/growth-v10/event-taxonomy |
| 8 | `knowledge_v10/` | ≤ 500 | 10+ | POST /api/v1/knowledge-v10/search + answer |
| 9 | `ai_workforce_v10/` (extends existing) | ≤ 400 | 10+ | POST /api/v1/ai-workforce-v10/plan |
| 10 | `founder_v10/` (extends founder dashboard) | ≤ 300 | 6+ | GET /api/v1/founder-v10/today |

**Acceptance gates:**
- Each module is ≤ 800 LOC, all-Python, no new dep
- Each module has Pydantic v2 schemas with `extra="forbid"`
- Each module has ≥ 6 tests
- Bundle stays at ≥ 1350 passing (current 1262 + ~90 new = 1352)
- Each endpoint advertises canonical guardrails block
- ComplianceGuardAgent veto applies to every workforce action
- No live action gets enabled

**Time estimate:** 8–12 hours of parallel-agent + main-thread work.

---

### Phase C — Verifier + Master Evidence

Goal: lock the v10 perimeter so future drift is caught.

**Deliverables:**
- `scripts/v10_master_verify.sh` — runs every layer's check + secret scan + safety eval
- `docs/v10/V10_MASTER_EVIDENCE_TABLE.md` — row-by-row evidence + verdict block
- Update `docs/QUICK_DEPLOY_API_KEYS_ONLY.md` with the ~12 new endpoint paths
- Update `Makefile` with `make v10-verify`

**Time estimate:** 1–2 hours main-thread.

---

### Phase D — P1 Adapters (post-first-3-customers)

Gated on:
- 3 paying Pilots delivered
- 3 signed Proof Packs
- Founder signs Decision Pack §S6 ("authorize first real dependencies")

Then add:
- LiteLLM as `optional_adapter` (real LLM gateway, behind env flag)
- Langfuse as `optional_adapter` (real trace export)
- Qdrant as `optional_adapter` (real vector DB)

Each adapter is a thin file that imports the package and falls back to
the native pattern if not installed.

---

### Phase E — P2/P3 Real Dependencies (post-5-customers)

Gated on:
- 5+ customers
- Decision Pack §S7 signed
- Security review of each dependency in `DEPENDENCY_DECISION_RECORD.md`

Then optionally:
- Add Chatwoot as a real inbox (replaces our model with actual conversations)
- Add Temporal as the real workflow runtime
- Add Twenty CRM as the real CRM (replaces our object model)

This is months out — by then real customer data will tell us which
dependencies are actually needed.

---

## 5. Hard rules — unchanged across all phases

| ❌ Forbidden | Where enforced |
|---|---|
| Live charge under any env combination | `tests/test_finance_os_no_live_charge_invariant.py` (5 tests) |
| Live WhatsApp send | `whatsapp_allow_live_send=False` default + `tests/test_live_gates_default_false.py` |
| Cold WhatsApp | `compliance_os.assess_contactability` blocks default |
| LinkedIn automation | `agent_governance.FORBIDDEN_TOOLS` |
| Web scraping | `agent_governance.FORBIDDEN_TOOLS` |
| Marketing claims (`نضمن`, `guaranteed`, `blast`, `scrape`) | `tests/test_landing_forbidden_claims.py` regex perimeter |
| Fake customer / fake proof | DesignOps `safety_gate.check_artifact` |
| PII in logs | `redact_log_entry` + `tests/test_pii_redaction_perimeter.py` |
| Secret in repo | gitleaks pre-commit + `tests/test_v7_secret_leakage_guard.py` |
| Test weakening | every PR diff reviewed against existing assertions |
| Real dependency without Decision Pack | `scripts/verify_reference_library_70.py` |

---

## 6. Verification gates per phase

| Phase | Pre-condition | Post-condition |
|---|---|---|
| A | bundle ≥ 1262 passing | 70-tool YAML loads + 12 layers documented + verifier exits 0 |
| B | Phase A complete | bundle ≥ 1350 passing + every v10 endpoint reachable in-process |
| C | Phase B complete | `bash scripts/v10_master_verify.sh` exits 0 |
| D | 3 paid Pilots + Decision §S6 | adapters land behind env flag; existing native patterns still default |
| E | 5+ customers + Decision §S7 | real deps in `requirements.txt`; security review documented |

---

## 7. Critical files this plan would touch

### Phase A (docs only)

| New | Modified |
|---|---|
| `docs/v10/REFERENCE_LIBRARY_70.md` | — |
| `docs/v10/REFERENCE_LIBRARY_70.yaml` | — |
| `docs/v10/DEALIX_CAPABILITY_GAP_MAP.md` | — |
| `docs/v10/DEPENDENCY_DECISION_RECORD.md` | — |
| `docs/v10/V10_MASTER_PLAN.md` | (this file) |
| `scripts/verify_reference_library_70.py` | — |
| `tests/test_reference_library_70.py` | — |

### Phase B (10 modules, 10 routers, 10 test files)

Routers added to `api/main.py`:
```
ai_workforce_v10, workflow_os_v10, crm_v10, customer_inbox_v10,
growth_v10, knowledge_v10, llm_gateway_v10, safety_v10,
observability_v10, founder_v10
```

### Phase C (verifier + evidence)

| New | Modified |
|---|---|
| `scripts/v10_master_verify.sh` | — |
| `docs/v10/V10_MASTER_EVIDENCE_TABLE.md` | — |
| — | `docs/QUICK_DEPLOY_API_KEYS_ONLY.md` |
| — | `Makefile` |

---

## 8. Reusable infra (DO NOT rebuild — extend)

| Existing module | Becomes part of |
|---|---|
| `auto_client_acquisition/ai_workforce/` (12 agents + Orchestrator) | `ai_workforce_v10/` extends with reviewer + planner patterns from AutoGen |
| `auto_client_acquisition/customer_loop/` (12-state journey) | `workflow_os_v10/` extends with retry + idempotency from Temporal pattern |
| `auto_client_acquisition/customer_data_plane/` (consent + redaction) | stays as-is; `customer_inbox_v10/` references it for `consent_status` |
| `auto_client_acquisition/proof_ledger/` (file + Postgres backend + HMAC) | stays as-is; `observability_v10/` writes spans here for cost+latency |
| `auto_client_acquisition/finance_os/` (pricing + invoice + live-charge guard) | stays as-is; `crm_v10` adds InvoiceIntent + ManualPaymentRecord |
| `auto_client_acquisition/executive_reporting/` (weekly bilingual report) | `founder_v10/` composes this + cost summary + blockers |
| `auto_client_acquisition/designops/` (skills + safety_gate + 6 generators) | `designops_v10/` only adds 4 new skills (proposal, customer-room, exec-report, mini-diagnostic) — already shipped |
| `auto_client_acquisition/observability_v6/` (TraceRecord + AuditEvent + Incident) | `observability_v10/` extends TraceRecord with `cost_estimate`, `risk_score`, `model_name` |
| `auto_client_acquisition/security_privacy/` (secret_scan + log_redaction + minimization) | stays as-is; `safety_v10/` calls into it |
| `auto_client_acquisition/agent_governance/` (FORBIDDEN_TOOLS + autonomy levels) | `safety_v10/policy_engine.py` reads from this; never mutates |

**Net new code in v10:** maybe 4,000 LOC across 10 modules. Net new
dependencies: zero (until Phase D).

---

## 9. Founder decisions still NOT touched

The 10 in `docs/EXECUTIVE_DECISION_PACK.md` (B1-B5 + S1-S5) stay open.
v10 adds 2 new optional founder decisions only:

- **§S6** — Authorize first 3 `optional_adapter` integrations (gated on Phase D)
- **§S7** — Authorize first 1–2 `real_dependency` installations (gated on Phase E)

Neither blocks Phase A/B/C.

---

## 10. What "تدشين كامل" means after Phase C

After Phase C ships:

1. ✅ 70 OSS tools researched + documented + matrix verified
2. ✅ 12 capability layers each have a native v10 module
3. ✅ ~12 new `/api/v1/*-v10/*` endpoints reachable in-process
4. ✅ Bundle ≥ 1350 passing
5. ✅ `bash scripts/v10_master_verify.sh` exits 0
6. ✅ Production redeploy required (founder action)
7. ✅ Phase E (first warm intro) unblocked per `docs/V5_PHASE_E_DAY_BY_DAY.md`

The v10 architecture **does not block** Phase E. The founder can begin
warm intros immediately on the existing v5/v6/v7 stack while v10
research/docs/native modules ship in parallel.

---

## 11. Open questions (founder decides before/during execution)

1. Should we ship Phase A (docs + matrix) in this session, then defer
   Phase B to a fresh session?
   - **Recommendation:** yes. Phase A is research; Phase B is the
     biggest code drop yet (~4,000 LOC across 10 modules). Two
     sessions keeps each focused.
2. Should we ship native patterns for ALL 10 P0 picks at once, or
   ship 3 at a time?
   - **Recommendation:** 3 at a time. Order: cost+safety+observability
     first (Phase B-1), then workflow+CRM+inbox (Phase B-2), then
     growth+knowledge+ai_workforce_v10+founder_v10 (Phase B-3).
3. Should we wire any v10 endpoint into the founder dashboard now or
   wait?
   - **Recommendation:** wait. Founder dashboard already aggregates
     v6+v7; v10 adds detailed views, but the summary already covers
     the founder's morning routine.
4. Should we update Issue #138 with the v10 plan?
   - **Recommendation:** yes — one comment with this doc's link.
5. Should we add a `dealix-v10-research` branch separate from
   `claude/service-activation-console-IA2JK`?
   - **Recommendation:** no. v10 is additive; same branch keeps the
     evidence table coherent.

---

## 12. Final shape after Phase C ships

```
Dealix v10 — Final Shape
========================

Dealix Core (already shipped)
├─ v5 Customer Loop / Role Command / Service Quality / Agent Governance
├─ v5 Reliability / Vertical Playbooks / Customer Data Plane
├─ v5 Finance OS / Delivery Factory / Proof Ledger / GTM OS / Security
├─ v6 Diagnostic Engine / Company Brain v6 / Approval Center
├─ v6 Executive Reporting / Diagnostic Workflow / Observability v6
├─ v7 AI Workforce (12 agents + Orchestrator + ComplianceGuard)
├─ v7 Service Mapping v7 / Cost Guard
└─ DesignOps OS (15 skills + safety_gate + 6 generators + exporter)

Dealix v10 (this plan)
├─ AI Workforce v10 (extends with reviewer + planner)
├─ Workflow OS v10 (state machine + retry + idempotency)
├─ CRM v10 (object model + lead/deal scoring + customer health)
├─ Customer Inbox v10 (consent + SLA + reply suggestion)
├─ Growth v10 (event taxonomy + funnel + attribution)
├─ Knowledge v10 (retrieval contract + answer contract + RAG eval)
├─ LLM Gateway v10 (cost router + budget policy + cache policy)
├─ Safety v10 (Promptfoo-style eval cases + policy engine)
├─ Observability v10 (extends v6 TraceRecord with cost + risk_score)
├─ Platform v10 (storage + auth + tenant contracts — reference only)
├─ DesignOps v10 (artifact generators — already shipped)
└─ Founder v10 (composes everything for daily brief)

Reference Library
├─ docs/v10/REFERENCE_LIBRARY_70.md
├─ docs/v10/REFERENCE_LIBRARY_70.yaml
├─ docs/v10/DEALIX_CAPABILITY_GAP_MAP.md
├─ docs/v10/V10_MASTER_PLAN.md (this file)
├─ docs/v10/V10_MASTER_EVIDENCE_TABLE.md
└─ docs/v10/DEPENDENCY_DECISION_RECORD.md
```

---

## 13. Verdict block (after Phase A+B+C)

```
DEALIX_V10_VERDICT=PASS
LOCAL_HEAD=<final tip on claude/service-activation-console-IA2JK>
PROD_GIT_SHA=<unknown until Railway redeploy>
REFERENCE_LIBRARY_70=pass (70 tools, 12 layers, no dups)
P0_NATIVE_PATTERNS=10/10 shipped
LLM_GATEWAY_V10=pass
SAFETY_V10=pass
WORKFLOW_OS_V10=pass
CRM_V10=pass
CUSTOMER_INBOX_V10=pass
GROWTH_V10=pass
KNOWLEDGE_V10=pass
OBSERVABILITY_V10=pass
AI_WORKFORCE_V10=pass
FOUNDER_V10=pass
DESIGNOPS_V10=pass (already shipped at bf9516e)
DEPENDENCIES_ADDED=0 (P0 is native-only)
FULL_PYTEST=≥1350 passing
NO_LIVE_*=blocked across the board
NO_FAKE_PROOF=pass
NO_GUARANTEED_CLAIMS=pass
SECRET_SCAN=clean
OUTREACH_GO=diagnostic_only (until Railway redeploy)
NEXT_FOUNDER_ACTION=Trigger Railway redeploy → bash scripts/v10_master_verify.sh → begin Phase E first warm intro per docs/V5_PHASE_E_DAY_BY_DAY.md
```

---

## 14. What I'm NOT doing in this plan

To be explicit:

- ❌ I'm NOT adding 70 dependencies to `requirements.txt`
- ❌ I'm NOT replacing FastAPI/Postgres with Supabase/Appwrite
- ❌ I'm NOT installing Temporal as a runtime now
- ❌ I'm NOT installing Chatwoot as a real inbox
- ❌ I'm NOT building real LLM Gateway with vendor SDK calls
- ❌ I'm NOT changing pricing
- ❌ I'm NOT enabling any live action
- ❌ I'm NOT auto-resolving any of the 10 founder Decision Pack items
- ❌ I'm NOT building 70 modules — only the 10 P0 picks in Phase B

---

## 15. Approval needed

To execute this plan, the founder approves:

1. **Phase A** — research + matrix + capability map (this session if he says go)
2. **Phase B** — 10 native modules in 3 batches (next session, if Phase A clean)
3. **Phase C** — verifier + master evidence (same session as Phase B end)
4. **Defer Phases D + E** — gated on real customer data

If approved, I dispatch ~4 parallel agents for Phase A (Reference
Library docs + matrix + 12-layer capability map + tests + verifier)
and ship the docs in one omnibus commit.

— V10 Master Plan v1.0 · 2026-05-05 · Dealix
