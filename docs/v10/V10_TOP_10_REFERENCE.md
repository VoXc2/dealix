# Dealix v10 Reference Library — Top 10 P0 Picks (Quick Reference)

> The ten OSS patterns that give Dealix the most value with the
> least risk. Every entry is `native_pattern` — no real dependency
> until founder signs Decision Pack §S6.

**Date:** 2026-05-05

---

## The 10

| # | Tool | Layer | What we build | Status |
|---|---|---|---|---|
| 1 | Open Design | DesignOps | DESIGN.md + 15 SKILL.md + safety_gate + 6 generators + exporter | ✅ shipped (`bf9516e`) |
| 2 | LiteLLM | LLM Gateway | `llm_gateway_v10/` cost router with cheap/balanced/strong tiers, per-customer + per-agent budget, cache policy | 🟡 Phase B |
| 3 | Promptfoo | Safety / Evals | `safety_v10/` eval pack with Arabic + English red-team cases (cold WA, LinkedIn, scraping, fake proof, guaranteed claims, prompt injection, PII leakage, secret leakage, excessive agency, unsafe tool use) | 🟡 Phase B |
| 4 | Langfuse / OpenLIT | Observability | `observability_v10/` extends `observability_v6/` TraceRecord with `cost_estimate`, `risk_score`, `model_name`, `prompt_version` | 🟡 Phase B |
| 5 | LangGraph | Workflow OS | `workflow_os_v10/` state machine + retry policy + idempotency + checkpoint (extends `customer_loop/`) | 🟡 Phase B |
| 6 | Chatwoot | Customer Inbox | `customer_inbox_v10/` model: conversation, channel, consent_status, SLA, AI_suggested_reply (no live send) | 🟡 Phase B |
| 7 | Twenty CRM | CRM / RevOps | `crm_v10/` object model (Account, Contact, Lead, Deal, Opportunity, ServiceSession, ProofEvent, CustomerHealth, ApprovalRequest, etc.) | 🟡 Phase B |
| 8 | PostHog | Growth / Analytics | `growth_v10/event_taxonomy.py` (17 canonical events: lead_created, diagnostic_requested, draft_created, approval_requested, unsafe_action_blocked, payment_requested_manual, proof_event_created, etc.) | 🟡 Phase B |
| 9 | Qdrant / Haystack | Knowledge / RAG | `knowledge_v10/retrieval_contract.py` + `answer_contract.py` + `eval_contract.py` (interface only — no vector DB yet) | 🟡 Phase B |
| 10 | Temporal / DBOS | Workflow durability | retry_policy + idempotency_policy + checkpoint contract (composes with #5) | 🟡 Phase B |

---

## Why these 10 (not the other 60)

Each P0 pick:
- ✅ Maps to an existing v5/v6/v7 module that needs a documented contract
- ✅ Returns a `native_pattern` that's ≤ 800 LOC + ≥ 6 tests
- ✅ Carries zero new dependencies
- ✅ Unblocks a real founder workflow (cost control / safety / observability / inbox / CRM / analytics / knowledge / workflow / DesignOps)

The other 60 stay in `inspiration_only` tier until concrete demand
signals arrive (e.g. Phase E delivers proof events that justify a
real vector DB).

---

## What each P0 unlocks operationally

### #2 LiteLLM cost router
Founder runs `python scripts/dealix_status.py --cost` and sees daily
LLM spend per agent + per customer with budget caps. Stops cost
runaway BEFORE the bill arrives.

### #3 Promptfoo safety evals
Founder runs `python scripts/run_safety_v10.py` and gets a verdict on
whether the AI workforce can be tricked into cold WhatsApp / live
charge / fake proof. Runs in CI on every PR.

### #4 Langfuse trace schema
Every workforce run produces a structured trace with cost + risk +
approval + redacted_payload. Founder can answer "what did agent X do
yesterday for customer Y?" in 5 seconds.

### #5 LangGraph workflow state machine
The 7-day Pilot delivery survives a server crash mid-day-3 because
each step is a checkpointed state with retry policy.

### #6 Chatwoot inbox model
Customer messages from WhatsApp / email / website chat land in one
typed conversation with consent + SLA + AI-suggested reply (drafts
only — no auto-send).

### #7 Twenty CRM object model
Replaces ad-hoc Lead/Deal tracking with a typed model: Account →
Contact → Lead → Deal → Opportunity → ServiceSession → ProofEvent.
Customer health computable from the timeline.

### #8 PostHog event taxonomy
Founder knows exactly which 17 events to emit + how to read funnel
conversion (lead → diagnostic → pilot → paid → proof) with no
ambiguity.

### #9 Qdrant knowledge interface
Future-proofs the Company Brain so Phase D can swap to a real vector
DB without changing callers.

### #10 Temporal retry policy
Pilot delivery state survives crashes; idempotent step IDs prevent
double-charging customers if a webhook fires twice.

---

## What's NOT in P0 (and why)

| Category | Tool | Why deferred |
|---|---|---|
| Customer Inbox | Real Chatwoot install | Native pattern proves the model first; real Chatwoot is P2 (after 5 customers) |
| Workflow | Real Temporal install | Native state machine handles 7-day Pilots; Temporal is P3 (after Pilots fail in production) |
| CRM | Real Twenty CRM | Native object model + Postgres is enough for first 10 customers |
| Vector DB | Real Qdrant / Weaviate / Milvus | No customer documents to embed yet (Phase D-gated) |
| Auth | Keycloak / Zitadel / Authentik | Current FastAPI auth handles single-tenant founder usage |
| Object Storage | MinIO | Proof packs are markdown files; S3 is P2 |
| Marketing automation | Mautic | Manual outreach only until customer #10 |
| Browser automation | Browser-use | Hard rule: no live browser actions on customer's behalf |

---

## How this connects to v10 Phase B

Phase B (next session, after Phase A docs ship) builds these 9 native
patterns (Open Design already done = picks #2–#10):

1. `auto_client_acquisition/llm_gateway_v10/` (≤ 600 LOC, ≥ 8 tests)
2. `auto_client_acquisition/safety_v10/` (≤ 800 LOC, ≥ 15 tests)
3. `auto_client_acquisition/observability_v10/` (≤ 400 LOC, ≥ 8 tests)
4. `auto_client_acquisition/workflow_os_v10/` (≤ 700 LOC, ≥ 12 tests)
5. `auto_client_acquisition/customer_inbox_v10/` (≤ 500 LOC, ≥ 8 tests)
6. `auto_client_acquisition/crm_v10/` (≤ 800 LOC, ≥ 15 tests)
7. `auto_client_acquisition/growth_v10/event_taxonomy.py` (≤ 300 LOC, ≥ 6 tests)
8. `auto_client_acquisition/knowledge_v10/` (≤ 500 LOC, ≥ 10 tests)
9. `auto_client_acquisition/ai_workforce_v10/` (extends existing, ≤ 400 LOC, ≥ 10 tests)

Each ships with its own router under `/api/v1/<layer>-v10/*`.

Bundle target after Phase B: 1262 (current) + ~90 new tests = ~1350.

---

— v10 Top-10 Reference v1.0 · 2026-05-05 · Dealix
