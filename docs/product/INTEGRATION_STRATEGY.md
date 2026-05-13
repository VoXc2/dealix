---
title: Integration Strategy — Phase 4 Integration OS Plan
doc_id: W6.T37.integration-strategy
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T34, W6.T37]
kpi:
  metric: enterprise_deals_unlocked_by_integrations
  target: 5
  window: 12m
rice:
  reach: 0
  impact: 3
  confidence: 0.8
  effort: 2
  score: engineering-roadmap
---

# Integration Strategy — Phase 4

## 1. Context

Through Phase 1–3, Dealix delivers value within its own customer
workspace. Phase 4 (Integrate) opens the boundary: CRM, inbox, and billing
adapters connect Dealix into the customer's existing operational stack.
This is what makes Dealix sellable to enterprise IT — and what unlocks the
retainer machine at scale.

Integrations are **enterprise-only**: SME and mid-market plans do not
include adapters by default. Adapters carry recurring engineering cost
and an SLA — pricing reflects that.

## 2. Audience

CTO (architecture + ADRs), HoP (productization), CRO (commercial gating),
enterprise architects on the customer side (consume).

## 3. Adapter Families

### 3.1 CRM Adapters

| Target | Phase | Read | Write |
|--------|------|------|-------|
| HubSpot | Phase 4a | Contacts, Accounts, Deals, Pipelines | Bulk update (CRM_BULK_UPDATE) with approval matrix |
| Salesforce | Phase 4a | Accounts, Opportunities, Activities | Same — with sandbox-first contract |
| Zoho (later) | Phase 4b | Same as above | Same |

Patterns:
- **Direction**: read-mostly. Writes are bulk with approval gating.
- **Auth**: OAuth 2.0 with refresh tokens; per-tenant credential vault.
- **Schema mapping**: declarative YAML per tenant; reviewed by HoP.
- **Sync mode**: incremental cursor-based; full-resync run on demand.

### 3.2 Inbox / Workspace Adapters

| Target | Phase | Read | Write |
|--------|------|------|-------|
| Google Workspace | Phase 4a | Threads, contacts (with consent) | Send drafts via approval matrix |
| Microsoft 365 | Phase 4b | Same | Same |

Patterns:
- **Scope minimization**: request the narrowest possible OAuth scopes.
- **PII**: all inbound content scanned by `pii_detector` before storage.
- **Send gating**: outbound mail routes through `OUTBOUND_EMAIL` action
  with CSM approval at L2+ ([`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)).

### 3.3 Billing Adapters

| Target | Phase | Direction | Notes |
|--------|------|-----------|-------|
| Moyasar (KSA) | Phase 4a | Bi-directional | ZATCA-aligned; invoice + payment events |
| Stripe (GCC partner geographies) | Phase 4b | Bi-directional | Partner-fronted contracts only |

Patterns:
- `INVOICE_GENERATION` requires Head of CS approval at L3+.
- Webhook reconciliation with retries; DLQ per
  [`../governance/DATA_RETENTION.md`](../governance/DATA_RETENTION.md).
- Tokenised payment data only; no PAN handling.

### 3.4 Sectoral / Compliance Adapters (Later Phases)

Reserved for enterprise BFSI / public-sector deployments:
- SAMA / NDMO reporting feeds.
- ZATCA e-invoicing surfaces (live, monitored).
- Sector-specific identity providers (SSO via OIDC).

## 4. Architectural Rules

- **No direct mutation from customer to Dealix DB** — all writes pass
  through the API surface and Trust gating.
- **Per-tenant credentials** — encrypted at rest; BYOK on Enterprise.
- **Idempotency** — every adapter operation carries an idempotency key.
- **Audit** — every adapter call emits an audit event with the external
  request ID.
- **Schema migrations** — adapter schemas are versioned; breaking changes
  follow the same 12-month deprecation window as the public API
  ([`../adr/0005-api-versioning.md`](../adr/0005-api-versioning.md)).

## 5. Phase 4 Sequencing

- **Phase 4a** (first 6 months of Phase 4): HubSpot read, Google Workspace
  read + draft, Moyasar invoice send.
- **Phase 4b** (next 6 months): Salesforce, Microsoft 365, Stripe, write
  capabilities for HubSpot.
- **Phase 4c** (next): sectoral adapters by deal demand.

Each adapter ships under a feature flag, with a paid pilot customer named
before promotion to general availability.

## 6. Commercial Gates

- Adapters are enterprise-only (named CSM, multi-year preferred).
- Each enabled adapter carries a recurring fee element per the pricing
  schedule.
- Adapter-level SLAs are contractual: error rate, latency, support
  response times.

## 7. Anti-Patterns

- **Free integrations**: enterprise expectations require enterprise
  pricing.
- **Custom-per-customer adapters**: adapters are productized; tenant
  configuration via YAML, not bespoke code (see
  [`internal_os_modules.md`](internal_os_modules.md) §6).
- **Unaudited bulk writes**: every bulk write requires explicit approval
  per the matrix.

## 8. Cross-links

- Roadmap: [`PRODUCT_ROADMAP.md`](PRODUCT_ROADMAP.md)
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- API spec: [`API_SPEC.md`](API_SPEC.md)
- Module map: [`MODULE_MAP.md`](MODULE_MAP.md)
- Approval matrix: [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)
- Data retention: [`../governance/DATA_RETENTION.md`](../governance/DATA_RETENTION.md)
- ADRs: [`../adr/`](../adr/)

## 9. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly with HoP + CRO; per-adapter health check monthly.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial Phase-4 plan: CRM / inbox / billing / sectoral adapters |
