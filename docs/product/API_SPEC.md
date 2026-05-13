---
title: API Spec — Canonical Endpoints
doc_id: W6.T37.api-spec
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W6.T34, W4.T21]
kpi:
  metric: endpoints_with_versioning_and_audit
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 0.5
  score: engineering-foundation
---

# API Spec — Canonical Endpoints

## 1. Context

Dealix's public + internal API surface lives under `/api/v1/`. This file is
the index of canonical endpoints. Versioning rules are in
[`../adr/0005-api-versioning.md`](../adr/0005-api-versioning.md). Each
endpoint must pass Trust gating + emit audit events per
[`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md).

## 2. Audience

Engineers (own + extend the surface), HoP (designs new endpoints),
partners and integrators (consume).

## 3. Endpoint Index

### 3.1 Delivery Surface — `/api/v1/delivery/`

Per the canonical Delivery OS plan; sourced from
`auto_client_acquisition/delivery_factory/`:

- `POST /delivery/projects` — create project from intake
- `GET  /delivery/projects/{id}` — project state + current stage
- `POST /delivery/projects/{id}/transition` — advance Stage Machine
- `POST /delivery/projects/{id}/qa` — submit QA gates + score
- `GET  /delivery/projects/{id}/qa` — read latest QA report
- `POST /delivery/projects/{id}/handoff` — build handoff packet
- `POST /delivery/projects/{id}/handoff/sign` — record customer signoff
- `POST /delivery/projects/{id}/renewal` — generate renewal recommendation

### 3.2 Revenue OS Surface — `/api/v1/revenue-os/`

Implemented in `api/routers/revenue_os.py`:

- **Memory**: `GET /events/types`, `POST /events`, `GET /timeline/{account_id}`, `GET /replay/{customer_id}`, `GET /retention-summary`
- **Agents / Workflows**: `POST /workflows/run`, `GET /tasks`, `POST /tasks/{id}/approve`, `POST /tasks/{id}/reject`
- **Market Radar**: `GET /market-radar/signal-types`, `POST /market-radar/detect/hiring`, `POST /market-radar/sectors/{sector}/pulse`, `POST /market-radar/opportunities`
- **Copilot**: `POST /copilot/ask`, `GET /copilot/intents`, `GET /copilot/actions`, `GET /copilot/actions/{id}`
- **Forecast / Science**: `POST /forecast`, `POST /attribution`, `POST /impact`, `POST /churn`, `POST /expansion`
- **Compliance**: `POST /compliance/contactability`, `POST /compliance/campaign-risk`, `GET /compliance/ropa`, `POST /compliance/dsr`, `GET /compliance/vendors`
- **Verticals**: `GET /verticals`, `GET /verticals/{id}`, `GET /verticals/{id}/templates`
- **Seeds & Leads**: `POST /seed`, `GET /leads`, `POST /leads/rank`

### 3.3 Reports Surface — `/api/v1/reports/`

Implemented in `api/routers/reports.py`:

- `POST /reports/executive` — generate an executive report from a project
- `POST /reports/proof-pack` — assemble a proof pack from ProofEvents
- `POST /reports/weekly` — weekly customer status
- `GET  /reports/health` — surface health

### 3.4 Trust / Policy Surface — `/api/v1/policy/`, `/api/v1/audit/`

Implemented under Trust OS:

- `POST /policy/check` — pre-action policy decision (returns allow / deny / require-approval)
- `GET  /audit/events` — query audit events (role-gated)
- `POST /audit/export` — export tenant audit slice (HoLegal-gated)

### 3.5 Intake / Onboarding Surface — `/api/v1/onboarding/`

- `POST /onboarding/intake` — submit intake form, create project shell
- `GET  /onboarding/intake/{id}` — read intake state

### 3.6 Data Quality Surface — `/api/v1/data-quality/`

- `POST /data-quality/check` — synchronous quality scan
- `POST /data-quality/batches` — async batch job

### 3.7 Scoring Surface — `/api/v1/scoring/`

- `POST /scoring/score` — score entities (leads / tickets / risks)
- `GET  /scoring/models` — list registered model versions

### 3.8 Knowledge Surface — `/api/v1/knowledge/`

- `POST /knowledge/query` — cited answer over indexed Documents
- `POST /knowledge/documents` — ingest a Document
- `GET  /knowledge/documents/{id}` — fetch metadata + freshness

### 3.9 Outreach Surface — `/api/v1/outreach/`

- `POST /outreach/draft` — generate a draft (AR / EN), forbidden-claims scan
- `POST /outreach/send` — send with approval gate per [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)

## 4. Versioning Rules

Per [`../adr/0005-api-versioning.md`](../adr/0005-api-versioning.md):
endpoints expose versioned paths (`/api/v1/...`); breaking changes carry a
12-month deprecation window. Versions ship side-by-side until sunset.

## 5. Cross-Cutting Requirements

- **Authentication** — every endpoint requires a tenant-scoped token.
- **Authorization** — RBAC per role; HoLegal-only endpoints are tagged.
- **Audit** — every state-mutating endpoint emits an audit event.
- **Rate limits** — per-tenant; cost guards on LLM-backed endpoints.
- **Errors** — structured error responses with stable error codes.

## 6. Cross-links

- ADRs: [`../adr/`](../adr/) — especially 0005 versioning
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Module map: [`MODULE_MAP.md`](MODULE_MAP.md)
- Data model: [`DATA_MODEL.md`](DATA_MODEL.md)
- Code: `api/routers/revenue_os.py`, `api/routers/reports.py`, `auto_client_acquisition/delivery_factory/`

## 7. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly endpoint review; immediate on a new module or
  breaking change.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial endpoint index across delivery / revenue / trust / data / knowledge / outreach |
