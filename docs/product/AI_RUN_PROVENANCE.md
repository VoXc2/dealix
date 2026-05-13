# AI Run Provenance — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Technical Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_RUN_PROVENANCE_AR.md](./AI_RUN_PROVENANCE_AR.md)

## Context
An AI output without provenance is hearsay. For enterprise buyers, only provenanced outputs can survive risk review, audit, and post-decision questioning. This file defines the minimum provenance record every client-facing AI output must carry. It plugs into the observability framework at `docs/AI_OBSERVABILITY_AND_EVALS.md`, the environment configuration in `docs/OBSERVABILITY_ENV.md`, and the eval discipline in `docs/EVALS_RUNBOOK.md`. It enforces the Dealix promise that no client-facing output ships without a recorded source story.

## Required provenance record
Every client-facing AI output must include:

- `ai_run_id` — unique identifier for the run that produced the output.
- `agent_id` — the agent that generated the output.
- `model` — the model identifier (provider, name, version).
- `prompt_version` — the version of the prompt used.
- `input_sources` — explicit list of dataset, document, or record IDs the agent read.
- `redaction_status` — confirmation that PII redaction was applied where required, with the redaction policy ID.
- `governance_status` — `approved` / `qa_passed` / `awaiting_approval` / `blocked` at the moment of delivery.
- `qa_score` — the quality score assigned by QA review (where applicable).
- `human_reviewer` — the named human who reviewed and approved the output (where applicable).
- `output_version` — the version of the output; corrections increment this.
- `delivered_at` — UTC timestamp of the delivery moment.

## Hard rule
**No provenance = no delivery.** A client-facing output without a complete provenance record is not delivered. Delivery without provenance is a governance incident.

## Display
- Provenance is attached as a structured footer (or metadata block) to every report, deck, or message-class output.
- For UI surfaces inside Dealix Cloud, provenance is one click away from any rendered output.
- For email deliveries, provenance is included as a link to a versioned provenance page within the client workspace.

## Retention
Provenance records are retained for the longer of: the client contract retention requirement, the Dealix internal retention floor, and any regulatory retention rule that applies (PDPL, sector-specific). See `docs/DATA_RETENTION_POLICY.md` for the floor.

## Tampering
Provenance records are append-only. Corrections do not overwrite prior records — they produce a new `output_version` with a back-reference. Any attempt to modify a delivered provenance record is a governance incident.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI run telemetry, QA result, approval record | Complete provenance record | Technical Owner + QA | Per output |
| Client retention requirement | Provenance retention configuration | Governance + Delivery | Per engagement |
| Correction or re-issue request | New `output_version` + back-reference | Delivery Owner | As needed |

## Metrics
- Provenance Completeness — % of client-facing outputs with all required fields present (target: 100%).
- Provenance-Linked Approvals — % of `governance_status = approved` outputs with a named human reviewer.
- Average QA Score — mean `qa_score` across delivered outputs by service.
- Correction Re-delivery Rate — % of outputs that produced a `v2` within 30 days of delivery.

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability framework powering provenance
- `docs/OBSERVABILITY_ENV.md` — environment for telemetry capture
- `docs/EVALS_RUNBOOK.md` — eval runbook feeding `qa_score`
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
