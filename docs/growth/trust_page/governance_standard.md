# Governance Standard — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [governance_standard_AR.md](./governance_standard_AR.md)

## Context
This page is the public summary of the Dealix Governance Standard. It is
the customer-readable companion to
`docs/product/GOVERNANCE_AS_CODE.md`,
`docs/DEALIX_OPERATING_CONSTITUTION.md`, and the trust pack
`docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`.

## What the Dealix Standard is

A small, executable set of guarantees that Dealix runs in production:

- **Runtime checks.** Every AI output is evaluated by the Compliance
  Guard Agent before it can leave the workflow.
- **Action taxonomy.** Every AI action is classified by risk class and
  approval requirement (see HITL matrix).
- **Approvals.** Actions above Medium risk require explicit human
  approval, logged and time-bound.
- **Audit logs.** Every run records prompts (versioned), inputs (with
  provenance), outputs, governance verdicts, and reviewer identity.
- **Eval thresholds.** Each agent has a published eval suite; performance
  below threshold blocks delivery.

## What clients receive

- A summary of the Standard at engagement start.
- Access to the AI Control Tower view for their workspace.
- Proof packs that reference verdicts, prompt versions, and eval scores.
- A point of contact for governance questions.

## Versioning

The Standard is versioned. The current version and changelog appear at
the top of `docs/product/GOVERNANCE_AS_CODE.md` and on this page when
material changes are made.

## Anti-patterns we publicly refuse

- Standards that exist only as policy text.
- Hidden, agent-side rule changes without versioning.
- Approval flows without time bounds.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Constitution + rules | Standard summary | Compliance | Per change |
| Runtime telemetry | Public evidence | Compliance | On request |
| Client questions | Governance Q&A | Compliance | Per request |

## Metrics
- Standard Adherence — % of runs honoring the Standard.
- Evidence Fulfillment — % of client evidence requests answered.
- Version Currency — % of agents pinned to current Standard version.
- Public Drift — public commitments vs operational reality (target = 0).

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — business trust pack
- `docs/DPA_DEALIX_FULL.md` — data processing agreement
- `docs/DATA_RETENTION_POLICY.md` — retention rules
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic trust pack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
