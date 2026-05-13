# Management API Spec — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Platform Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [MANAGEMENT_API_SPEC_AR.md](./MANAGEMENT_API_SPEC_AR.md)

## Context
Dealix runs its own business as software. Decisions about which client
to take, what to deliver, what to govern, and what to charge are not
left to spreadsheets — they are surfaced through a Management API.
This spec is the contract behind the operating-system map in
`OPERATING_SYSTEM_MAP.md`, complements
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, extends the foundation in
`docs/API_REFERENCE.md`, and makes management itself software, in line
with `docs/BEAST_LEVEL_ARCHITECTURE.md`.

## Design Principles
- **One purpose per endpoint.** Each endpoint owns one decision or one
  read.
- **Idempotent writes.** Every POST accepts an `Idempotency-Key`
  header.
- **Auditable by default.** Every write emits a governance event and a
  proof event when relevant.
- **ACL on every call.** Permission Mirroring (see
  `governance/PERMISSION_MIRRORING.md`) is enforced by the gateway, not
  by the endpoint.
- **Versioned contracts.** Path-prefixed `/v1/...` with deprecation
  windows ≥ 90 days.

## Endpoints (Future)
Endpoints are grouped by the Operating System Map layer they serve.

### Readiness
- `GET /readiness/company` — overall readiness scorecard for a client.
- `GET /readiness/services` — readiness per service the client can
  consume.
- `POST /readiness/service-score` — submit/refresh a readiness score
  from a diagnostic run.

### Requests
- `POST /requests` — create a new inbound request.
- `GET /requests` — list and filter requests.
- `POST /requests/{id}/decision` — record a sellability/scope decision.

### Clients
- `POST /clients` — create a client + workspace.
- `GET /clients/{id}/health` — client health score and trend.
- `GET /clients/{id}/capability-roadmap` — current and target capability
  levels with planned sprints.

### Governance
- `POST /governance/check` — run runtime checks for an AI action.
- `POST /governance/approval` — submit or resolve an approval request.
- `GET /governance/events` — query governance events for audit.

### Quality
- `POST /quality/score` — submit a QA review score.
- `GET /quality/reviews` — list QA reviews for a project.

### Proof
- `POST /proof-pack/generate` — generate a delivery proof pack.
- `GET /proof-ledger` — read the proof ledger entries.

### Learning
- `POST /post-project-review` — record a post-project review.
- `GET /feature-candidates` — list candidate features from learning.

## Cross-cutting Headers
- `Authorization` — bearer token from SSO.
- `X-Workspace-Id` — workspace context.
- `Idempotency-Key` — required on all POSTs.
- `X-Correlation-Id` — propagated to logs and observability.

## Error Model
- `400` — invalid input, with `code`, `field`, `message`.
- `401` / `403` — authentication / authorisation failures.
- `409` — idempotency conflict.
- `422` — business-rule violation, with `rule_id`.
- `5xx` — internal; surfaced to observability.

## Versioning and Deprecation
- Breaking changes ship behind a new path version.
- Deprecation notices include sunset date and migration link.
- Each release notes which Operating System Map layer is affected.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| API calls from internal cockpit, partners, automations | Decisions, events, scores, packs | Platform Lead | Continuous |
| Audit/governance events | Compliance feeds | Governance Lead | Continuous |
| Release notes | API change log | Platform Lead | Per release |

## Metrics
- **API Availability** — share of successful API requests per month
  (target ≥ 99.5%).
- **P95 Latency** — 95th-percentile response time per endpoint group
  (target ≤ 500 ms for GETs, ≤ 1.5 s for governance POSTs).
- **Idempotency Conflict Rate** — share of POSTs returning 409 (target
  ≤ 1%).
- **Audit Completeness** — share of write calls with a matching
  governance event (target = 100%).

## Related
- `docs/API_REFERENCE.md` — foundational API reference this spec
  extends.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability plan that
  constrains availability and latency targets.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture from which these
  endpoints derive.
- `docs/product/OPERATING_SYSTEM_MAP.md` — sibling map naming the
  layers these endpoints serve.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
