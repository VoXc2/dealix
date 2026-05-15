# Dealix AI OS — Gap Analysis & Phased Roadmap

> **Status**: Working analysis · Companion to [`docs/blueprint/master-architecture.md`](../blueprint/master-architecture.md)
> **Last updated**: 2026-05-15
> **Scope**: Internal / technical

---

## 1. Purpose & scope

This document measures the Dealix codebase against an 8-layer **AI Operating
System** reference model and lays out a roadmap to close the gaps.

The 8 layers:

1. **Identity** — human and agent identity, RBAC, agent registry
2. **Policy Engine** — declarative rules, evaluation, ALLOW / ESCALATE / DENY
3. **Workflow Runtime** — deterministic, replayable, resumable state machines
4. **Tool Execution** — tools as governed capabilities (schema, risk, audit)
5. **Memory** — scoped, attributed, permission-aware, expirable
6. **Observability** — traces, token usage, tool calls, policy violations
7. **Evaluation** — continuous, business-outcome-oriented
8. **Human Oversight** — Human-in-the-Loop approval with full context

### The phasing rule

Dealix operates a **revenue-first doctrine** (the 11 non-negotiables; "don't
build ahead of paid customers"). This roadmap honors it: **the AI OS is the
target state, but each layer is pulled forward only when a paid offer needs
it.** Pure-platform work with no offer behind it is explicitly deferred
(Section 6). The phasing maps each layer to a rung of the productized offer
ladder (see [`DEALIX_REVENUE_PLAYBOOK_FINAL.md`](../DEALIX_REVENUE_PLAYBOOK_FINAL.md)).

---

## 2. Scorecard

Dealix is well past a blank slate — most layers exist in some form. The gap is
less about missing subsystems and more about (a) some layers not being
first-class named subsystems and (b) the layers not being **wired together**
(see Section 4).

| Layer | Maturity | Strong today | Primary gap |
|---|---|---|---|
| 1. Identity | ~50% | Human RBAC complete | No agent registry / declarative specs |
| 2. Policy Engine | ~60% | YAML registry + evaluator | Rules hard-coded; no DSL |
| 3. Workflow Runtime | ~40% | Deterministic state machine | In-memory only; not wired to live pipelines |
| 4. Tool Execution | ~30% | Tool dataclass + permission matrix | No risk / timeout / audit on tools |
| 5. Memory | ~70% | Event store + semantic search + retention | Not permission-aware; no per-entry expiry |
| 6. Observability | ~50% | OTel + structlog + Sentry configured | Span helpers not auto-called in execution |
| 7. Evaluation | ~20% | YAML eval packs + offline runner | Offline-only; not business-outcome metrics |
| 8. Human Oversight | ~75% | Approval store + audit + founder rules | No UI; approval payload lacks context |

---

## 3. Per-layer detail

### Layer 1 — Identity (~50%)

**Exists.** Human identity and RBAC are fully implemented: `db/models.py`
defines `TenantRecord` (multi-tenant isolation), `RoleRecord` (permissions JSON,
immutable system roles) and `UserRecord` (auth, MFA/TOTP, role assignment).
Agents carry a runtime `agent_id` (`core/agents/base.py`). A bare agent-identity
dataclass exists at
`auto_client_acquisition/agent_identity_access_os/agent_identity.py`
(`agent_id`, `tenant_id`, `owner_principal`).

**Gap.** No **agent registry** — no machine-readable specs defining each agent's
id, owner, scope, permitted tools, resource budget, or `risk_level`. Agents are
defined in Python only. Agent identity is not enforced at the tool boundary
(any agent can call any tool).

### Layer 2 — Policy Engine (~60%)

**Exists.** A versioned declarative registry at
`auto_client_acquisition/governance_os/policies/default_registry.yaml`
(forbidden actions, risk categories). The evaluator
`governance_os/policy_check.py` returns a structured `PolicyCheckResult` with an
ALLOW / ALLOW_WITH_REVIEW / BLOCK verdict. `governance_os/draft_gate.py` audits
draft text; `governance_os/approval_matrix.py` routes actions to a risk tier.

**Gap.** Rules beyond simple enum/string lists are hard-coded as Python
`if/elif` chains (`approval_matrix.py`, `policy_check.py`). There is no rule
**DSL** — adding a non-trivial policy requires a code deploy. No policy change
audit trail, no context-aware policies (customer maturity, tenant plan).

### Layer 3 — Workflow Runtime (~40%)

**Exists.** A real deterministic state machine at
`auto_client_acquisition/workflow_os_v10/state_machine.py`: typed
`WorkflowRun` / `WorkflowStep`, strict `ALLOWED_TRANSITIONS`, per-step
`idempotency_key` (replay is a no-op), configurable retry with exponential
backoff, a `paused_for_approval` state. `workflow_os/approval_flow.py` links
pauses to approval requests.

**Gap.** Workflow runs live in an in-memory `_RUN_BUFFER` — **no Postgres
persistence**, so runs do not survive a restart and cannot be resumed across
processes. No live API pipeline routes requests through the workflow engine
(it is exercised by tests only). No distributed/queued execution.

### Layer 4 — Tool Execution (~30%)

**Exists.** A `Tool` dataclass (`core/agents/tools.py`) with a JSON-Schema
parameter spec and Anthropic/OpenAI formatters. A permission matrix at
`auto_client_acquisition/tool_guardrail_gateway/tool_guardrails.py`
(`_TOOL_REGISTRY` with `permitted` / `requires_approval` / `always_blocked`
flags; e.g. `whatsapp_send_live` and `scrape_external` are always blocked).

**Gap.** Tools are not governed capabilities: no `risk_level`, no `timeout`, no
per-tool retry, no `audit_mode`, no version on the `Tool` dataclass. The
`action_mode` from `check_tool_permission()` is not wired into the Approval
Center. Tool invocations are not instrumented (no span, no token, no audit
entry).

### Layer 5 — Memory (~70%)

**Exists.** The most mature non-oversight layer. An append-only event store
(`auto_client_acquisition/revenue_memory/event_store.py`, with in-memory and
SQLAlchemy backends) plus projections — this is **operational + episodic**
memory. Semantic memory via `core/memory/revenue_memory.py` over pgvector
embeddings (`ContactEmbeddingRecord`), tenant-scoped. A retention policy
(`revenue_memory/retention.py`) enforces PDPL expiry.

**Gap.** Memory search is **not permission-aware** — `tenant_id` is the only
isolation. Retention is bulk, not per-entry TTL. No `created_by` attribution and
no audit trail of who read which memory.

### Layer 6 — Observability (~50%)

**Exists.** OpenTelemetry configured in `dealix/observability/otel.py` (OTLP
exporter, FastAPI/SQLAlchemy/HTTPX instrumentation, `llm_span` / `agent_span` /
`tool_span` context managers). structlog JSON logging (`core/logging.py`).
Sentry with PII scrubbing (`dealix/observability/sentry.py`). Cost tracking
(`dealix/observability/cost_tracker.py`).

**Gap.** The span helpers exist but are **not automatically invoked** inside
`BaseAgent.run()` or tool execution — instrumentation is opt-in and largely
unused on live paths. No cost alerting when budget is exceeded. Policy
violations and approval decisions are not recorded as spans.

### Layer 7 — Evaluation (~20%)

**Exists.** Five YAML eval packs in `evals/` and an offline runner
`scripts/run_evals.py` that loads JSONL cases, calls in-process FastAPI routes,
and checks JSON shape (`expect_keys`, `forbid_substrings`, score bounds).

**Gap.** Evaluation is **offline and test-only**. It validates JSON shape, not
**business outcomes** (conversion rate, MTTR, SLA compliance, time-to-proof).
No live hooks from lead/deal/approval handlers, no regression/drift detection,
no A/B comparison of workflow variants.

### Layer 8 — Human Oversight (~75%)

**Exists.** The most mature layer. `auto_client_acquisition/approval_center/`
provides a Pydantic `ApprovalRequest` (bilingual summaries, `risk_level`,
`action_mode`, append-only `edit_history`), a thread-safe `ApprovalStore` with
enforced state transitions, founder pre-approval rules
(`founder_rules.py`, HMAC-signed, expiring, with immutable channels), a policy
layer (`approval_policy.py`) and an HTTP API (`api/routers/approval_center.py`,
audit-logged, `extra='forbid'`).

**Gap.** No web UI. The approval payload carries a human summary but **not** the
full decision context — retrieved evidence, the precise intended action,
expected outcome, or the policy result that triggered it. No escalation routing
by role, no SLA alerting on `due_date`, no approval metrics endpoint.

---

## 4. Critical integration gaps

The layers exist but do not yet form a single loop. These cross-layer gaps
matter more than any single layer's maturity:

1. **Workflow ↔ Approval not closed.** A workflow can enter
   `paused_for_approval`, but that does not create an Approval Center request,
   and approving a request does not resume the workflow.
2. **Policy ↔ Approval not connected.** Policy results don't set the approval
   `risk_level` — risk is computed independently in two places.
3. **Tools not instrumented.** Tool calls produce no span, no token record, no
   audit entry.
4. **Agent identity not enforced at the tool boundary.** No scope/permission
   check when an agent invokes a tool.
5. **Evaluation not live.** Eval packs exist but no handler runs them on real
   leads/deals/approvals.

---

## 5. Phased roadmap

Each phase is pulled by a specific paid offer. No phase builds ahead of the
offer that justifies it.

### Phase A — pulled by the 7-Day Revenue Intelligence Sprint (499 SAR) · days 0–30

The Sprint *is* a workflow with a governance gate and founder approval, so it
needs the workflow → policy → approval loop to actually close.

- Persist `WorkflowRun` / `WorkflowStep` to Postgres (replace `_RUN_BUFFER`).
- Wire `paused_for_approval` to create an Approval Center request; resume the
  workflow when the request is approved (gaps 1).
- Derive approval `risk_level` from the `PolicyCheckResult` (gap 2).
- Route the 7-day sprint through the workflow engine end to end.

Layers touched: **3, 8, 2** — no new subsystems, just the integration loop.

### Phase B — pulled by Managed Revenue Ops retainer (2,999–4,999 SAR/mo) · days 30–60

The retainer's value proposition is executive observability and *proving
ongoing value* — both require live instrumentation and outcome measurement.

- Auto-invoke `agent_span` / `tool_span` inside `BaseAgent.run()` and tool
  execution; record token usage and policy violations as spans (gaps 3).
- Add cost alerting on budget breach.
- Build the Evaluation Engine: business-outcome metrics (conversion, SLA,
  time-to-proof) wired into live lead/deal/approval handlers (gap 5).

Layers touched: **6, 7**.

### Phase C — pulled by Custom AI Setup (5–25K SAR) and Governance Review (25–50K SAR) · days 60–90+

Per-customer agents and a sellable governance audit require real agent identity
and governable tools.

- Agent Registry: declarative agent specs (id, owner, scope, permitted tools,
  `risk_level`); enforce agent scope at the tool boundary (gap 4).
- Tool Execution hardening: `risk_level`, `timeout`, retry, `audit_mode` on the
  `Tool` dataclass; wire `action_mode` to the Approval Center.
- Policy DSL: move hard-coded rules into a declarative rule language so a
  governance engagement can demonstrate policy-as-data.

Layers touched: **1, 4, 2**.

---

## 6. Explicitly deferred

The following are part of the long-term AI OS vision but have **no paid offer
behind them yet**. They are deliberately *not* scheduled, to stay honest to the
revenue-first doctrine:

- Distributed / queued workflow execution (Temporal-style orchestration).
- Full multi-tenant platformization, public SDK, API gateway.
- Policy A/B testing and policy-change versioning.
- Memory versioning / rollback of semantic embeddings.
- Multi-agent autonomous orchestration (kept to orchestrated agents only).

These move onto the roadmap the moment an offer requires them.
