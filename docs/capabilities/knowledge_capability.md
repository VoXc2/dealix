# Knowledge Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Head of Knowledge / Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [knowledge_capability_AR.md](./knowledge_capability_AR.md)

## Context

The Knowledge capability turns a company's scattered documents into
source-backed, governed answers. It is the operational form of the
"Company Brain" offer and depends on the stack choices in
`docs/AI_STACK_DECISIONS.md`, the routing strategy in
`docs/AI_MODEL_ROUTING_STRATEGY.md`, and the evaluation discipline in
`docs/AI_OBSERVABILITY_AND_EVALS.md`. Maturity is scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Turn scattered knowledge into source-backed answers that employees and
customers can trust.

## Typical Problems

- Documents are undiscoverable across drives and chats.
- Contradictory information across versions.
- Answers without a source.

## Required Inputs

- Approved documents with owners.
- Sensitivity tags per document.
- Access rules (who sees what).

## AI Functions

- Ingest documents and metadata.
- Index for retrieval.
- Retrieve top-k passages per query.
- Answer with explicit citation to the source passage.

## Governance Controls

- Source required for every answer; no source = no answer.
- Access mirrored — AI never returns content the user could not read.
- Freshness tracked — stale documents flagged.
- Audit log of every retrieval and answer.

## KPIs

- Indexed docs — count and % of approved set.
- Citation rate — % of answers with valid citation.
- Search time reduction — minutes saved per query vs baseline.

## Services

- Company Brain Sprint — first capability build.
- Brain Management Retainer — recurring operating retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Approved docs | Indexed corpus | Delivery | Per sprint |
| User query | Cited answer | Runtime | Real-time |
| Stale doc flag | Refresh task | Client owner | Weekly |
| Eval results | Answer-quality report | Delivery | Weekly |

## Metrics

- Indexed docs and citation rate (see KPIs).
- Answer accuracy from evals — % passing.
- Freshness — median age of cited documents.

## Related

- `docs/AI_STACK_DECISIONS.md` — stack choices for the brain.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing for retrieval and answer.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval discipline.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
