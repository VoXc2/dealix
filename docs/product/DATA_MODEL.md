# Data Model — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Backend Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DATA_MODEL_AR.md](./DATA_MODEL_AR.md)

## Context
This file describes the canonical Dealix application data model. It is
the entity-relationship view that the platform, the LLM Gateway, the
governance runtime, and the reporting layer share. It anchors to
`docs/BEAST_LEVEL_ARCHITECTURE.md` for the architectural picture, to
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` for the storage layer
hardening, and to `docs/product/ADVANCED_DATA_MODEL.md` (the L2
sibling) for the extended platform model. The schema-level field
definitions live in `docs/data/DATA_SCHEMA_LIBRARY.md`.

## Entity List
- **Client** — a contracted Saudi company that buys Dealix services.
- **Workspace** — isolated tenant boundary per Client.
- **Project** — a delivery engagement under a Workspace.
- **ServicePackage** — the productized offering chosen for a Project.
- **DataSource** — a registered source of data (CRM, file, API).
- **Dataset** — a versioned, schema-conformant slice of a DataSource.
- **Record** — a row inside a Dataset.
- **Account** — a business account record (AccountSchema).
- **ContactHint** — a non-PII signal about a contact role.
- **Opportunity** — a sales pipeline entry tied to an Account.
- **Draft** — an AI-produced artifact pending review/approval.
- **Workflow** — a defined sequence of AI and human steps.
- **Approval** — a recorded approval per the Approval Matrix.
- **AuditEvent** — an immutable governance/runtime event.
- **GovernanceEvent** — a runtime check result.
- **ProofEvent** — a measurable business outcome event.
- **Report** — a generated executive or operational report.
- **AIRun** — a single LLM call ledger record.
- **QAReview** — a recorded quality and safety review.
- **CapitalAsset** — a reusable artifact in the IP Registry.
- **FeatureCandidate** — repeated demand surfacing into a feature
  request.
- **PlaybookUpdate** — a versioned change to a runbook/playbook.
- **ClientHealthScore** — periodic health score per Client.
- **CapabilityScore** — per-capability maturity score per Client.

## Primary Relationships
- A `Client` has many `Workspaces`.
- A `Workspace` has many `Projects` and many `DataSources`.
- A `Project` references one `ServicePackage` and many `Workflows`.
- A `Workflow` produces many `AIRuns`; each `AIRun` may produce a
  `Draft`.
- A `Draft` requires `QAReview` and an `Approval` before becoming a
  delivered artifact.
- A `DataSource` produces many `Datasets`; each `Dataset` carries a
  Data Readiness Score.
- A `Dataset` contains many `Records`. Records may be `Accounts`,
  `ContactHints`, or schema-specific entities.
- An `Opportunity` references an `Account`, a `Project`, and an
  `Owner`.
- `GovernanceEvent`, `AuditEvent`, and `ProofEvent` are append-only
  and reference the originating `AIRun` or `Approval`.
- `CapitalAsset` links back to the `Project` and `Workflow` that
  produced it.
- `ClientHealthScore` aggregates `ProofEvents`, `QAReviews`, and
  `CapabilityScores`.

## Tenancy
- Every entity except `CapitalAsset` and `FeatureCandidate` is
  scoped to a single `Workspace`.
- Cross-tenant access requires an explicit `Approval` of class C.
- Audit, governance, and AI run ledgers are partitioned by Workspace
  and replicated to a Dealix-only governance store.

## Identifiers
- All entity IDs are prefixed strings (e.g. `CLT-`, `PRJ-`, `DS-`,
  `AIR-`, `AUD-`, `APV-`).
- IDs are stable, never reused, and minted by the platform.
- Subject identifiers in PDPL-relevant records are stored as hashes.

## Indexing Strategy
- Append-only ledgers (AuditEvent, GovernanceEvent, ProofEvent, AIRun)
  use time-bucketed partitions.
- Account, Opportunity, and Draft tables are indexed by Workspace
  plus a sort key on time.
- Full-text indexes are restricted to non-PII fields by default.

## Lifecycle
- `Drafts` move through states: `created` → `qa_review` →
  `approval_pending` → `approved` or `rejected` → `delivered`.
- `Datasets` move through: `ingested` → `scored` → `usable` →
  `archived`.
- `Projects` move through: `intake` → `discover` → `build` →
  `validate` → `delivered` → `proved` → `expanded` or `closed`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Schema PR | Migration plan | Backend lead | Per change |
| New entity proposal | ER diagram update | Backend lead | Per change |
| Tenancy decision | Access policy update | Governance lead | Per change |
| Index design | Query plan validation | Backend lead | Per change |

## Metrics
- **Schema drift count** — entities in production that diverge from
  this model. Target: 0.
- **Cross-tenant access incidents** — Target: 0.
- **Ledger append latency p95** — Target: ≤ 200 ms.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture canonical.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — backend hardening.
- `docs/product/ADVANCED_DATA_MODEL.md` — extended platform model
  (sibling L2).
- `docs/data/DATA_SCHEMA_LIBRARY.md` — schema library.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
