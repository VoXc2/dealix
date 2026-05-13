# Model Portfolio — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [MODEL_PORTFOLIO_AR.md](./MODEL_PORTFOLIO_AR.md)

## Context
Dealix runs many tasks across many tenants; using one model for everything
is wasteful and risky. The Model Portfolio defines the canonical task set,
selection criteria, and routing rules. It complements
`docs/AI_MODEL_ROUTING_STRATEGY.md`, `docs/LLM_PROVIDERS_SETUP.md`, and
`docs/AI_STACK_DECISIONS.md`.

## Canonical task set

- Classification.
- Extraction.
- Summarization.
- Scoring.
- Arabic executive writing.
- RAG answering.
- Compliance checking.
- Report generation.

## Selection criteria

- Accuracy on task-specific eval suite.
- Arabic quality where applicable.
- Cost per 1k tokens / per call.
- Latency.
- Context length needed.
- Data sensitivity and provider posture.
- Reliability (uptime, rate limits).

## Routing

| Task | Tier | Validation |
|---|---|---|
| simple classification | low-cost | schema check |
| outreach draft | mid | claims check |
| executive report | high | QA review |
| RAG answer | high + retrieval | citation check |
| compliance | high + rules | hard fail rules |

## Portfolio discipline

- Every task has a primary and a fallback model.
- Every model pinned by version.
- Cost and latency tracked per model per task in the Control Tower.
- Quarterly portfolio review: prune, promote, replace.

## Anti-patterns

- One mega-model for everything regardless of task.
- Changing models silently without an eval pass.
- Routing high-sensitivity tasks to unvetted providers.
- Ignoring Arabic quality in favor of English benchmarks.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Task taxonomy | Routing rules | Head of AI | Quarterly |
| Eval results | Promote / prune decision | Head of AI | Per change |
| Provider catalog | Approved provider list | Head of AI | Quarterly |
| Control Tower | Model performance telemetry | Head of AI | Continuous |

## Metrics
- Cost per Task — average cost by canonical task.
- Latency P50 / P95 — by task and model.
- Arabic Quality Score — for Arabic-applicable tasks.
- Fallback Rate — % of calls served by fallback model.

## Related
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing strategy
- `docs/LLM_PROVIDERS_SETUP.md` — provider setup
- `docs/AI_STACK_DECISIONS.md` — stack-level decisions
- `docs/COST_OPTIMIZATION.md` — cost discipline
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
