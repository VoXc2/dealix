# Core OS Architecture — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** Head of Dealix Core (CTO)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CORE_OS_ARCHITECTURE_AR.md](./CORE_OS_ARCHITECTURE_AR.md)

## Context
The Dealix Core OS is the **single, shared platform** that every Business Unit consumes. It is the structural enforcement of the holding rule: no BU builds parallel infrastructure. The architecture here is the high-level layered view that aligns with `docs/BEAST_LEVEL_ARCHITECTURE.md` and the reliability posture in `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`. AI-stack decisions are in `docs/AI_STACK_DECISIONS.md`.

## Seven layers

```
┌────────────────────────────────────────────────────┐
│ 7. Learning Layer                                  │
│    Evals, prompt tuning, model selection, feedback │
├────────────────────────────────────────────────────┤
│ 6. Integration Layer                               │
│    Connectors, webhooks, event bus, ETL            │
├────────────────────────────────────────────────────┤
│ 5. Data Layer                                      │
│    Source registry, data quality, lineage, PII     │
├────────────────────────────────────────────────────┤
│ 4. Governance Layer                                │
│    Policies, approvals, audit log, PDPL guardrails │
├────────────────────────────────────────────────────┤
│ 3. AI Control Layer                                │
│    LLM Gateway, model routing, cost, telemetry     │
├────────────────────────────────────────────────────┤
│ 2. Application Layer                               │
│    BU modules: Revenue, Operations, Brain, etc.    │
├────────────────────────────────────────────────────┤
│ 1. Presentation Layer                              │
│    Client Workspace, Admin Console, Reports        │
└────────────────────────────────────────────────────┘
```

### Layer 1 — Presentation
- Client Workspace (multi-tenant UI).
- Admin Console (group + BU operators).
- Reports & Dashboards (BU + Board).
- Authentication, RBAC, tenant boundaries.

### Layer 2 — Application
- One application module per BU (Revenue, Operations, Brain, Support, Governance, Data).
- Each module exposes the BU's services via the same OS contracts (auth, governance, data, telemetry).

### Layer 3 — AI Control
- LLM Gateway with model routing (`docs/AI_MODEL_ROUTING_STRATEGY.md`).
- Prompt Registry, Evaluation Registry.
- Cost ledger; per-tenant budgets.
- AI Control Tower telemetry (`docs/product/AI_CONTROL_TOWER.md`).

### Layer 4 — Governance
- Policy Registry (`docs/product/GOVERNANCE_AS_CODE.md`).
- Approval workflow engine.
- Audit log (immutable, append-only).
- PDPL guardrails: residency, retention, DSR, breach (`docs/ops/PDPL_BREACH_RUNBOOK.md`, `docs/ops/PDPL_RETENTION_POLICY.md`).

### Layer 5 — Data
- Source Registry (datasets, owners, freshness).
- Data Quality Score per source.
- Lineage graph.
- PII detection and tagging.

### Layer 6 — Integration
- Connectors (CRM, email, Slack, WhatsApp, billing).
- Outbound webhooks.
- Domain Event Bus (see [`EVENT_DRIVEN_OPERATING_MODEL.md`](../product/EVENT_DRIVEN_OPERATING_MODEL.md)).
- ETL / reverse-ETL into client systems.

### Layer 7 — Learning
- Eval harness (`docs/EVALS_RUNBOOK.md`).
- Feedback loop: outcomes feed eval datasets.
- Prompt + model tuning.
- Model selection rules (`docs/AI_STACK_DECISIONS.md`).

## Architectural rules

1. **Modular monolith first.** Microservices only when justified by independent scaling, team boundaries, or compliance isolation.
2. **One auth, one tenancy, one audit log.** No per-BU duplication.
3. **Events are first-class.** Every meaningful state change emits a domain event.
4. **PDPL by default.** Data residency and retention defaults are PDPL-aligned; deviations require GC approval.
5. **Public contract per layer.** No BU reaches across layers to a private implementation detail.
6. **Cost and quality observable per call.** LLM Gateway records cost and eval score on every prompt.
7. **Capital Ledger writable from every layer.** Reusable artifacts must be registerable from anywhere in the stack.

## Inter-layer contracts

| From | To | Contract |
|---|---|---|
| Presentation | Application | Authenticated session + tenant context |
| Application | AI Control | `model_call` with policy id + prompt id |
| AI Control | Governance | Policy check, audit log entry |
| Application | Data | Query via Source Registry; PII tags respected |
| Any layer | Integration | Publish event to bus |
| Any layer | Learning | Submit eval record |

## Anti-patterns
- **BU bypasses Governance Layer** for "speed" → automatic deploy block.
- **Direct LLM provider calls** from Application Layer → routed through LLM Gateway only.
- **Per-BU dashboards** that don't read from the Core OS metrics store → rejected at code review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| BU feature candidates | Core OS roadmap commits | Head of Core | Bi-weekly |
| Incidents | Reliability remediation | SRE | Per incident |
| Eval failures | Prompt/model changes | AI lead | Daily |
| Governance audit findings | Policy / runtime updates | DPO | Monthly |

## Metrics
- **Core OS uptime** — % availability per layer.
- **Latency p95** — Gateway-side latency.
- **Gateway cost / call** — LLM token cost per inference.
- **Audit log completeness** — % of model calls captured in audit log.
- **Eval pass rate** — % of prompts in registry passing thresholds.
- **PII tagging coverage** — % of fields in Source Registry with PII status.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural foundation.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability posture.
- `docs/AI_STACK_DECISIONS.md` — AI stack decisions.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing rules.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability posture.
- `docs/product/AI_CONTROL_TOWER.md` — control tower module.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
