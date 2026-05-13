# Model Portfolio

> Dealix routes work to the right model class — never names a vendor in
> contracts. The portfolio is task-driven: classification goes Haiku-class,
> balanced work goes Sonnet-class, high-stakes goes Opus-class, compliance
> uses a strong model behind a validator, and RAG splits retrieval from
> the grounded answer. Aligns with `docs/AI_MODEL_ROUTING_STRATEGY.md`.

## Routing table

| Task class | Default class | Why this class | Example agents | Eval thresholds |
|-----------|---------------|----------------|----------------|-----------------|
| Classification / triage | Haiku-class | Cheap, low-latency, deterministic enough for labels | DataQualityAgent (validation), SupportAgent (triage) | precision ≥ 0.9, p95 latency ≤ 800ms, cost ≤ SAR 0.005/run |
| Balanced drafting | Sonnet-class | Good Arabic quality, good reasoning, mid cost | OutreachAgent, ReportingAgent (Proof Pack) | Arabic-tone ≥ 4/5, claim violations = 0 |
| High-stakes reasoning | Opus-class | Best decision quality for executive outputs | ReportingAgent (Executive Report), StrategyAgent (Quick Win) | structural pass = 100%, exec rubric ≥ 4.5/5 |
| Compliance / guard | Strong model + validator | Defense-in-depth: model output is validated by `dealix/trust/forbidden_claims.py` + `pii_detector.py` | ComplianceGuardAgent | block recall ≥ 0.98, false-positive ≤ 5% |
| RAG (Company Brain) | Retrieval (BM25 + embeddings) + grounded answer (Sonnet-class) | Retrieval is deterministic & auditable; generation is small + cited | KnowledgeAgent | citation present = 100%, faithfulness ≥ 0.85 |

## Selection criteria (per task)

Every prompt in `PROMPT_REGISTRY.md` is scored against:

1. **Accuracy** — does it pass the agent's eval threshold?
2. **Arabic quality** — formal MSA, no machine-translated phrasing, sector tone — graded per `EVALUATION_REGISTRY.md`.
3. **Cost** — SAR per run; must fit margin per service (per `PRODUCT_TELEMETRY.md` economics).
4. **Latency** — p95 within the workflow SLA (`WORKFLOW_RUNTIME_DESIGN.md`).
5. **Context length** — large enough for the inputs without truncation (esp. RAG + Executive Report).
6. **Data sensitivity** — model provider's data handling must allow the data class; no customer data sent to a provider not on the approved list (`docs/governance/PDPL_DATA_RULES.md`).
7. **Reliability** — uptime & error rate; if a provider degrades, the router falls back to the next class.

## Routing principles

- **Abstract the vendor.** Contracts say "Sonnet-class balanced model"; the gateway picks the concrete provider.
- **Smallest model that passes.** Don't pay Opus prices for a triage task.
- **Validator on the output, not just the prompt.** Compliance and PII checks run on model output regardless of provider.
- **Fallback chains.** If primary provider fails or latency spikes, fall back to the secondary in the same class.
- **No customer data to providers that train on it.** Enforced at the gateway.

## Phase-1 vs Phase-2

- **Phase 1**: routing decisions are coded in `auto_client_acquisition/ai/model_router.py`. Single-provider per class; manual fallback.
- **Phase 2**: LiteLLM is the gateway; LiteLLM config holds the class → provider map; Langfuse records which provider answered each run. Costs surface in `AI_CONTROL_TOWER.md`.

## Cost guardrails (Phase 1 budget per run)

| Class | Soft budget | Hard cap |
|-------|------------:|---------:|
| Haiku | SAR 0.005 | SAR 0.02 |
| Sonnet | SAR 0.05 | SAR 0.20 |
| Opus | SAR 0.50 | SAR 2.00 |
| RAG generation | SAR 0.05 | SAR 0.20 |

Breach of hard cap halts the workflow and flags the run in `AI_RUN_LEDGER.md`.

## Forbidden combinations

- Customer PII to a model whose terms permit training on submitted data.
- Cross-border transfer of customer data without lawful basis per `docs/governance/PDPL_DATA_RULES.md`.
- Opus-class for bulk classification (cost violates margin per `PRODUCT_TELEMETRY.md`).
- Generation step that bypasses retrieval in the Company Brain workflow.

## Cross-links

- `/home/user/dealix/docs/AI_MODEL_ROUTING_STRATEGY.md`
- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/auto_client_acquisition/ai/model_router.py`
- `/home/user/dealix/auto_client_acquisition/llm_gateway_v10/`
