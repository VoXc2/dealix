# AI Run Ledger — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** QA Lead / Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_RUN_LEDGER_AR.md](./AI_RUN_LEDGER_AR.md)

## Context
The AI Run Ledger is the operational record of every AI execution that
touches a client deliverable. It exists so that any output Dealix
hands to a client can be traced back to the prompt, the model, the
redaction status, the QA pass, and the risk classification that
produced it. The ledger is the spine of
`docs/AI_OBSERVABILITY_AND_EVALS.md`, feeds the runbook in
`docs/EVALS_RUNBOOK.md`, and uses the observability environment defined
in `docs/OBSERVABILITY_ENV.md`.

## Ledger Schema
The canonical row shape is below. Every AI run produces exactly one
ledger row.

| ID | Project | Task | Model | Prompt Version | Inputs Redacted | Output Schema | Cost | QA | Risk |
|---|---|---|---|---|---|---|---:|---:|---|
| AI-001 | Lead Sprint A | score accounts | model-x | v1.2 | Yes | ScoreBreakdown | 0.40 | 91 | Low |

Field meanings:
- **ID** — globally unique run identifier (e.g. `AI-001`).
- **Project** — project name and ID; links to `projects` table.
- **Task** — short description of what the run produced.
- **Model** — model name + version actually called.
- **Prompt Version** — version pointer into the Prompt Registry.
- **Inputs Redacted** — Yes/No; whether PII was redacted before the
  call.
- **Output Schema** — structured output schema applied.
- **Cost** — SAR cost of the run (see `COST_GOVERNANCE.md`).
- **QA** — QA score from the most recent review.
- **Risk** — Low / Medium / High; matches Action Taxonomy class.

## Mandatory Fields per Client-Facing Output
Every client-facing AI output must record at least:

- Prompt version (immutable pointer).
- Output schema (validates structure).
- Redaction status (Yes/No + redaction policy version).
- QA score (≥ pass threshold for the relevant eval).
- Risk level (Low/Medium/High + Action Taxonomy level).

If any of these are missing, the output may not be delivered.

## Use Cases for the Ledger
- **Client trust** — when a client asks "how did you get this?", we can
  show prompt, model, sources, and approval.
- **Incident response** — any incident under `INCIDENT_RESPONSE.md`
  starts by pulling the ledger rows for affected runs.
- **Cost governance** — `COST_GOVERNANCE.md` aggregates ledger costs
  per service, project, client.
- **Evaluation** — `EVALUATION_REGISTRY.md` rolls up pass/fail rates
  by prompt and project.
- **Capability scoring** — L3/L4 evidence in
  `CAPABILITY_MATURITY_MODEL.md` references ledger rows.

## Retention
Ledger rows are retained per `docs/DATA_RETENTION_POLICY.md`. Personal
data inside the original inputs is redacted at write time; the ledger
itself stores hashes and redaction-policy versions, not raw PII.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Every AI run | A ledger row | LLM Gateway | Per run |
| Ledger rows | QA reports, cost reports, audit reports | QA Lead, Founder | Daily / Weekly |
| Incident query | Ledger extract for affected runs | Governance Lead | Per incident |

## Metrics
- **Ledger Coverage** — share of AI runs with a complete ledger row
  (target = 100%).
- **Missing-Field Rate** — share of rows missing any mandatory field
  (target = 0%).
- **Median QA Score** — across the last 30 days (target ≥ 90).
- **Cost-per-Run Drift** — variance of SAR cost vs. service budget
  (target ≤ 15%).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability surface using
  this ledger.
- `docs/EVALS_RUNBOOK.md` — runbook that operates on ledger rows.
- `docs/OBSERVABILITY_ENV.md` — environment definitions backing the
  ledger telemetry.
- `docs/product/ADVANCED_DATA_MODEL.md` — sibling data model where the
  `ai_runs` table lives.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
