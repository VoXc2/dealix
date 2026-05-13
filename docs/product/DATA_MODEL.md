---
title: Data Model — Canonical Entities
doc_id: W6.T37.data-model
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T34, W4.T12]
kpi:
  metric: entities_with_schema_owner
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 0.5
  score: engineering-foundation
---

# Data Model — Canonical Entities

## 1. Context

Every system has a small set of nouns it returns to constantly. This list
is Dealix's canonical entities — the objects every other doc, every API,
every event refers to. New entities require CTO sign-off; renames require
a migration path.

## 2. Audience

CTO (owns the model), engineers (consume the entities), HoData (consumes
for event taxonomy and analytics), HoP (consumes for API design).

## 3. The Entities

| Entity | One-line description |
|--------|----------------------|
| **Client** | A paying organization Dealix serves; the legal counterpart on the SOW |
| **Workspace** | An isolated tenant boundary for a Client; one Client may have one or several Workspaces |
| **Project** | A scoped engagement (Sprint / Pilot / Retainer) running through the 8-stage Delivery Standard |
| **ServicePackage** | A catalog offering with scope, price, KPIs, supporting OS modules |
| **DataSource** | A registered source of records (CRM export, file drop, API connector, manual entry) |
| **Document** | A unit of unstructured content ingested into Knowledge OS (file, page, transcript) |
| **Account** | A target organization Dealix tracks (prospect or existing customer) within a Workspace |
| **ContactHint** | A non-PII signal about a person (role, seniority, sector) tied to an Account |
| **LeadBatch** | A delivered or in-progress batch of scored leads matched to ICP for a Workspace |
| **Opportunity** | A pursued deal tied to an Account, with stage, attribution, expected value |
| **Workflow** | A durable orchestration of steps with retries, approvals, handoffs |
| **Task** | An individual unit of work within a Workflow; assigned to an actor (human or agent) |
| **Approval** | A recorded decision per the approval matrix; pre-condition for the action it gates |
| **Draft** | Pre-send content (message, report, post); subject to forbidden-claims + PII scan |
| **Report** | A finalized customer-facing executive artifact, governed by the Quality Standard |
| **ProofEvent** | A datum in the Proof Ledger: outcome captured (records cleaned, hours saved, etc.) |
| **AuditLog** | An immutable record of a policy-relevant event (per the audit policy) |
| **RiskEvent** | A flagged risk signal (compliance, operational, brand) for Trust review |
| **InvoiceIntent** | A pre-billing commitment record before the invoice is generated |

## 4. Relationships at a Glance

- A `Client` has many `Workspaces`; each `Workspace` has many `Projects`.
- Each `Project` is a realization of one `ServicePackage`.
- A `Project` consumes one or more `DataSources`, ingests `Documents`,
  produces `Drafts`, `Reports`, and `ProofEvents`.
- A `Workflow` orchestrates `Tasks`; some `Tasks` require an `Approval`.
- Every action emits an `AuditLog` entry; risky signals emit a
  `RiskEvent`.
- Billing produces an `InvoiceIntent` that, on approval, becomes an
  invoice in the billing system.

## 5. Schema Ownership

Each entity has a named schema owner:

| Entity | Owner |
|--------|-------|
| Client, Workspace | CTO |
| Project, ServicePackage | HoP |
| DataSource, Document | HoData |
| Account, ContactHint, LeadBatch | HoP (Lead Engine) |
| Opportunity | CRO |
| Workflow, Task | CTO |
| Approval, AuditLog, RiskEvent | HoLegal |
| Draft, Report | HoCS |
| ProofEvent | HoCS |
| InvoiceIntent | CRO |

Schema changes require a PR review by the owner and a migration plan if
the change is backward-incompatible.

## 6. Cross-links

- API spec: [`API_SPEC.md`](API_SPEC.md)
- Module map: [`MODULE_MAP.md`](MODULE_MAP.md)
- Event taxonomy: [`../analytics/event_taxonomy.md`](../analytics/event_taxonomy.md)
- Data map: [`../DATA_MAP.md`](../DATA_MAP.md)
- ADRs: [`../adr/`](../adr/)

## 7. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly schema review with owners.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial canonical entity list with owners |
