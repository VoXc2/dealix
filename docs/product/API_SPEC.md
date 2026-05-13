# API Specification — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Backend Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [API_SPEC_AR.md](./API_SPEC_AR.md)

## Context
This file is the MVP endpoint contract for Dealix's platform API.
Every endpoint is governed by the LLM Gateway, the Approval Matrix,
and the governance runtime. The spec pairs with the API reference at
`docs/API_REFERENCE.md`, the backend hardening plan in
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, and the management-API
sibling `docs/product/MANAGEMENT_API_SPEC.md` (L2). External clients
are expected to consume v1 only; v0 is internal.

## Conventions
- Base path: `/api/v1`.
- Auth: bearer token tied to a Workspace.
- Idempotency: every mutating endpoint accepts an `Idempotency-Key`
  header.
- Errors: JSON with `error_code`, `message`, and `correlation_id`.
- Time: ISO 8601 UTC.

## Endpoints
- `POST /api/v1/data/import-preview` — preview an inbound dataset
  before commit, returning the schema match and a draft DRS.
- `POST /api/v1/data/quality-score` — compute the Data Readiness
  Score for a registered dataset.
- `POST /api/v1/governance/check` — run the governance runtime
  against a candidate action.
- `POST /api/v1/revenue/score-accounts` — score accounts for the
  Revenue capability.
- `POST /api/v1/revenue/draft-pack` — produce a revenue draft pack
  (subject to QA and approval).
- `POST /api/v1/reporting/proof-pack` — generate a proof pack from
  audit, AI run, and QA events.
- `POST /api/v1/delivery/qa-score` — record a QA score for a Draft.
- `POST /api/v1/capital/assets` — register or list capital assets.
- `GET  /api/v1/founder/command-center` — founder-only command-center
  rollup view.

## Universal Response Shape
Every endpoint returns the following envelope. Result-specific fields
live under `result`. The remaining keys carry governance metadata that
every consumer must respect.

```json
{
  "result": {},
  "risk_status": "medium",
  "governance_status": "approved_with_review",
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

`risk_status` values: `low | medium | high | critical`.
`governance_status` values: `approved | approved_with_review |
draft_only | requires_approval | redacted | blocked | escalated`.
`next_action` values: `none | human_review | request_approval |
remediate | block_and_alert`.

## Rate Limits
- 60 requests per minute per Workspace for read endpoints.
- 20 requests per minute per Workspace for write endpoints.
- LLM-Gateway-backed endpoints (revenue, reporting) also enforce the
  Gateway's cost guard.

## Versioning
- Breaking changes require a new path version (e.g. `/api/v2`).
- Additive changes are made within v1 with a `min_capability` flag
  in the request.

## Audit and Idempotency
- Every request writes an `AuditEvent`. The response always returns
  `audit_event_id`.
- Replays with the same `Idempotency-Key` return the prior response
  for 24 hours.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| OpenAPI PR | Versioned spec release | Backend lead | Per change |
| Endpoint draft | Governance review record | Governance lead | Per endpoint |
| Cost guard policy | Gateway enforcement | AI platform lead | Per change |
| Client integration | Consumer migration note | Backend lead | Per change |

## Metrics
- **Endpoint availability p99** — Target: ≥ 99.5%.
- **Median response time** — Target: ≤ 800 ms for non-LLM endpoints.
- **Governance-block rate** — Share of requests blocked by runtime
  governance. Reported weekly.
- **Idempotency replay correctness** — Target: 100%.

## Related
- `docs/API_REFERENCE.md` — public API reference.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — backend hardening.
- `docs/product/MANAGEMENT_API_SPEC.md` — management API sibling
  (L2).
- `docs/product/LLM_GATEWAY.md` — LLM Gateway companion spec.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
