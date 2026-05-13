# Advanced Data Model — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Platform Lead / Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ADVANCED_DATA_MODEL_AR.md](./ADVANCED_DATA_MODEL_AR.md)

## Context
The Advanced Data Model is the canonical shape of the data that runs
Dealix as a business and as a platform. Without a single data model,
the governance, observability, proof, and reporting stories all drift.
This file lists the core tables and their relationships so that
`docs/BEAST_LEVEL_ARCHITECTURE.md`, `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`,
and the autonomous revenue OS in
`docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` share one vocabulary. It also
encodes the capability and governance concepts from the Layer-2 model.

## Core Tables
The system has the following core tables. Names are stable contracts.

- **clients** — legal entities buying from Dealix.
- **workspaces** — isolated tenant context per client (or department).
- **projects** — engagements (Sprint, Pilot, Retainer) within a
  workspace.
- **service_packages** — definitions from the service ladder.
- **requests** — inbound requests entering the Decision Layer.
- **decisions** — qualification, scope, governance, build, pricing,
  retainer decisions.
- **data_sources** — registered sources (CRM exports, files, APIs).
- **datasets** — derived working datasets, with lineage.
- **documents** — ingested documents for the Knowledge Capability.
- **accounts** — target accounts in the Revenue Capability.
- **opportunities** — pipeline items linked to accounts.
- **workflows** — orchestrated automations.
- **approvals** — approval requests and resolutions.
- **ai_runs** — every AI execution (links to `AI_RUN_LEDGER.md`).
- **qa_reviews** — quality reviews on AI outputs.
- **governance_events** — runtime governance check results.
- **proof_events** — client-visible proof of delivery.
- **reports** — generated management reports.
- **feature_candidates** — learning-layer feature ideas.
- **playbook_updates** — versioned playbook changes.
- **client_health_scores** — periodic client health snapshots.
- **capability_scores** — per-capability level scores per client.

## Key Relationships
- **Client** has many **Workspaces**.
- **Workspace** has many **Projects**.
- **Project** uses one **ServicePackage**.
- **Project** has many **DataSources**, **GovernanceEvents**,
  **QAReviews**, and **ProofEvents**.
- **Project** updates **Playbooks** via **playbook_updates**.
- **Project** creates **FeatureCandidates**.
- **Client** has many **CapabilityScores** (one per capability per
  snapshot).
- **AIRun** belongs to a **Project**, references a **prompt_version**,
  links to one **QAReview** and zero-or-more **GovernanceEvents**.
- **Approval** is keyed to a **Workflow** step and a named user.

## Lineage and Identity
- Every dataset records its source `data_source_id` and the operations
  applied (PII redaction, deduping, enrichment).
- Every AI run records `model`, `prompt_version`, `inputs_redacted`,
  and `output_schema`.
- Every governance and proof event is keyed to `project_id` and
  `run_id` for end-to-end traceability.

## Retention and Sensitivity
- Sensitivity classification is required on `datasets`, `documents`,
  and `accounts`.
- Retention follows `docs/DATA_RETENTION_POLICY.md` and the PDPL
  schedule in `docs/ops/PDPL_RETENTION_POLICY.md`.
- Cross-border records are tagged with jurisdiction per
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Inbound data, requests, AI outputs | Structured rows in the tables above | Data Lead | Continuous |
| Schema changes | Versioned migrations | Platform Lead | Per release |
| Audit/governance queries | Compliance reports | Governance Lead | Monthly |

## Metrics
- **Schema Conformance** — share of writes matching the published
  schema (target = 100%).
- **Lineage Completeness** — share of datasets with complete source
  lineage (target ≥ 95%).
- **PII Tagging Coverage** — share of personal-data fields with
  classification tags (target = 100%).
- **Capability Score Freshness** — share of active clients with a
  capability score in the last 90 days (target ≥ 90%).

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture document the model
  is part of.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability plan
  governing migrations and integrity.
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — autonomous revenue OS
  consuming this model.
- `docs/product/OPERATING_SYSTEM_MAP.md` — sibling map naming the
  layers each table serves.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
