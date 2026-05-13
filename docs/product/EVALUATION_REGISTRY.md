# Evaluation Registry — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** QA Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [EVALUATION_REGISTRY_AR.md](./EVALUATION_REGISTRY_AR.md)

## Context
Evaluations are how Dealix proves that an AI output is good enough to
ship. They turn quality from an opinion into a measured pass/fail
gate. The Evaluation Registry is the catalogue of named evals, the
checks they perform, and the thresholds that gate release. It pairs
with the Prompt Registry in `PROMPT_REGISTRY.md`, is operationalised
through `docs/EVALS_RUNBOOK.md` and `docs/AI_OBSERVABILITY_AND_EVALS.md`,
and informs the stack decisions in `docs/AI_STACK_DECISIONS.md`.

## Registry Table
The canonical registry shape:

| Eval | Service | Checks | Pass Threshold |
|---|---|---|---:|
| lead_scoring_eval | Lead Intelligence | relevance, explainability, consistency | 85 |
| claims_safety_eval | Outreach | no guarantees, no fake proof | 100 |
| rag_grounding_eval | Company Brain | citation, no-source-no-answer | 95 |
| arabic_quality_eval | All | clarity, tone, Saudi business fit | 85 |
| governance_eval | All | PII, source, approval | 100 |

## Hard Thresholds
- **Governance eval = 100.** Any failure blocks release.
- **Claims safety eval = 100.** Forbidden behaviour failures block.
- **RAG grounding eval ≥ 95.** Lower means hallucinated citations are
  possible.
- **Arabic quality eval ≥ 85.** Lower means tone or clarity loss is
  likely for Saudi business audiences.
- Other service-specific evals declare their own thresholds.

## Eval Composition
Each eval is composed of:

- **Dataset** — a versioned set of cases (positive, negative, edge).
- **Checks** — atomic verifications (e.g. "output cites at least one
  source from the allowed set").
- **Scorers** — code or LLM-judge scorers, with calibration notes.
- **Thresholds** — minimum acceptable score for release.
- **Owner** — named human responsible for accuracy and drift.

## Lifecycle
1. **Define** — eval added when a new service or prompt enters
   production.
2. **Run** — eval is run on every prompt version change and on a daily
   schedule for production.
3. **Drift** — eval datasets are reviewed monthly for drift; failing
   cases captured from incidents are added.
4. **Retire** — when a service is sunset, its eval is archived but
   remains queryable for audit.

## Use in Gates
- **Prompt promotion** to a major version requires passing all evals
  in the prompt's gating list (see `PROMPT_REGISTRY.md`).
- **Action Taxonomy Level ≥ 4** runs require claims safety and
  governance evals at 100.
- **Capability level transitions** to L4 require service-specific
  evals at threshold for the trailing 14 days.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI runs, prompt versions, eval datasets | Pass/fail decisions, drift reports | QA Lead | Daily + per release |
| Incident cases | New eval cases | QA Lead, Governance Lead | Per incident |
| Eval outcomes | Capability evidence, release decisions | Delivery Lead, Founder | Per release |

## Metrics
- **Eval Coverage** — share of registered prompts with at least one
  gating eval (target = 100%).
- **Daily Pass Rate** — share of production runs passing all
  applicable evals (target ≥ 98%).
- **Drift Detection Lead Time** — median days between drift onset and
  detection (target ≤ 14 days).
- **Eval-Caught Incident Share** — share of incidents caught by evals
  before client impact (target ≥ 80%).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability surfacing eval
  results.
- `docs/EVALS_RUNBOOK.md` — runbook for running and triaging evals.
- `docs/AI_STACK_DECISIONS.md` — stack decisions referencing eval
  thresholds.
- `docs/product/PROMPT_REGISTRY.md` — sibling prompt registry.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
