---
title: Model Cost Governance — per-workflow caps, Haiku/Sonnet/Opus routing, caching, fallback chain, unit economics
doc_id: W4.T24.model-cost-governance
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T23.slo-framework, W4.T26.ab-framework, W4.T13.executive-kpi-spec]
kpi: { metric: llm_cost_per_paid_workflow_sar, target: 1.20, window: monthly }
rice: { reach: 0, impact: 3, confidence: 0.8, effort: 4pw, score: engineering }
---

# Model Cost Governance

## 1. Purpose

Bound LLM spend per customer workflow, prevent runaway costs, and make the cost of every Revenue OS decision attributable, predictable, and reportable.

Why this matters: a single un-bounded enrichment storm in March 2026 cost 1,420 USD in three hours. The same workflow today, with caps and routing, would have cost 38 USD. This document encodes the rules that produce that outcome by default.

## 2. Scope

In scope: every LLM call made by Dealix services — Revenue OS workflows, decision passport enrichment, signal normalization, customer-facing chat surfaces, internal evaluations.

Out of scope: third-party SaaS that bills separately (Apollo, ZATCA data) — covered by source registry budgets.

## 3. Cost Caps

### 3.1 Per-workflow caps (hard ceilings, enforced in code)

| Workflow | Median target | p95 cap | Absolute hard cap | Action on breach |
|---|---|---|---|---|
| Lead enrichment (single lead) | 0.40 SAR | 1.00 SAR | 2.50 SAR | abort, log P3 |
| Lead qualification | 0.20 SAR | 0.60 SAR | 1.50 SAR | abort |
| Signal normalization (single signal) | 0.05 SAR | 0.15 SAR | 0.40 SAR | abort silently, retry with cheaper model |
| Decision passport assembly | 0.30 SAR | 0.80 SAR | 2.00 SAR | abort, log P2 |
| Outbound message draft | 0.60 SAR | 1.50 SAR | 4.00 SAR | abort, fall back to template |
| Customer-facing chat turn | 0.15 SAR | 0.40 SAR | 1.00 SAR | abort, return canned "I'm thinking" + queue |

Enforced in `dealix/trust/policy.py` via a `CostBudget` check on every LLM call. Exceeding the absolute cap raises `BudgetExceededError`, which is caught and converts the call into a policy-blocked outcome (passport carries `policy_block: cost_cap_exceeded`).

### 3.2 Per-tenant monthly cap

| Tier | Soft cap (notify) | Hard cap |
|---|---|---|
| Starter | 600 SAR | 900 SAR |
| Growth | 2,400 SAR | 3,500 SAR |
| Sovereign | 9,000 SAR | 14,000 SAR (configurable) |

Soft cap → tenant admin notified. Hard cap → workflows return `429 quota_exceeded` until next billing cycle or upgrade.

## 4. Model Routing Strategy

Three tiers by task complexity. Names are vendor-neutral within the doc; concrete vendor models below.

| Tier | Use cases | Default vendor models | Rationale |
|---|---|---|---|
| **Cheap-fast** | Signal normalization; field extraction; classification; intent detection; ETL transforms. | Claude Haiku 4.5; GPT-4.1-mini; Gemini Flash. | 90% of calls. Cost ~0.05 SAR per call. |
| **Balanced** | Enrichment composition; lead qualification reasoning; passport assembly. | Claude Sonnet 4.7; GPT-4o; Gemini Pro. | Workhorse. 85% of remaining 10% of calls. |
| **Heavy** | Complex multi-document reasoning; high-stakes decisions (escalations, regulatory ambiguity). | Claude Opus 4.7; GPT-5; Gemini Ultra. | < 2% of calls. Cost guarded by absolute cap + manual approval for tasks > 4.00 SAR. |

Routing logic lives in `auto_client_acquisition/revenue_os/enrichment_waterfall.py` and is informed by:

- `task_type` (enum).
- `evidence_level_required` (low / medium / high — from policy).
- Tenant tier.
- Cost-so-far in the current workflow (don't escalate past cap).

Routing is **policy-driven, not engineer-driven**. Adding a new workflow requires registering a route in `model_routing_rules.yaml` reviewed by Head of Data + CTO.

## 5. Caching Policy

Three caches in order:

1. **Prompt prefix cache (provider-side)** — Anthropic prompt caching with 5-minute TTL. Used for any prompt whose stable prefix exceeds 1,024 tokens. Estimated saving: 35–50% on input tokens for hot prefixes.
2. **Response cache (Redis)** — keyed on `sha256(model + prompt_text + tools + temperature)`. TTL 24 h for deterministic prompts (temperature ≤ 0.1). Bypass on temperature > 0.1. Estimated hit rate: 18% on signal normalization, 8% on enrichment.
3. **Embedding cache (Postgres)** — keyed on `sha256(model + text)`. TTL infinite. Embeddings reused across workflows.

Cache backends never store PII in cleartext keys: keys are hashes, values are encrypted at rest (KMS).

Cache invalidation:

- Manual: admin endpoint `POST /api/v1/admin/cache/invalidate` (audit-logged).
- Automatic: 24 h TTL; model version change invalidates entire response cache.

## 6. Fallback Chain

Every LLM call uses a chain `[primary, secondary, tertiary]` with monotonically increasing cost OR monotonically decreasing capability:

```
Tier "Cheap-fast":
  primary   = Anthropic Haiku 4.5
  secondary = OpenAI GPT-4.1-mini
  tertiary  = rule-based stub (if applicable) OR fail with degraded result

Tier "Balanced":
  primary   = Anthropic Sonnet 4.7
  secondary = OpenAI GPT-4o
  tertiary  = Anthropic Haiku 4.5 (cheaper but still functional)

Tier "Heavy":
  primary   = Anthropic Opus 4.7
  secondary = OpenAI GPT-5
  tertiary  = Anthropic Sonnet 4.7 (downgrade explicitly logged in passport)
```

Trigger for failover: provider returns 5xx, 429, or exceeds 8 s timeout. Failover is automatic and logged.

If primary AND secondary fail, the workflow consults policy: actions requiring `evidence_level=high` must abort and emit a passport with `blocked: provider_outage`. Lower-stakes actions degrade to tertiary.

## 7. Monthly Unit-Economics Report

Auto-generated on the 1st of each month, delivered to CEO and Head of Data.

Contents:

- LLM spend by workflow (table).
- LLM spend by tenant (top 20).
- LLM spend by provider (Anthropic / OpenAI / Google).
- Cost per paid workflow (target: ≤ 1.20 SAR median).
- Cost per Sovereign tenant (informational; for renewal pricing).
- Cache hit rates by cache layer.
- Top 10 most expensive single workflow executions (anomaly hunting).
- YoY trend; budget vs. actual.

Source: domain metric `llm_cost_sar_total{tenant_id, workflow, model, cache_hit}`.

## 8. Budget Alerts

Alert routes:

- **Tenant 80% of monthly soft cap**: Slack + email to tenant admin; internal #finops Slack.
- **Tenant 100% of monthly soft cap**: tenant admin email; CSM ticket.
- **Tenant 90% of monthly hard cap**: CTO Slack DM; CEO email.
- **Tenant 100% of monthly hard cap**: workflows return `429`; CEO + CTO paged for Sovereign.
- **Global daily spend > 150% of 7-day moving average**: CTO + Head of Data Slack DM (anomaly likely).
- **Per-workflow p95 cost > 1.5× weekly average for 2 hours**: ticket to on-call.

## 9. Governance

- Model-routing rules (`model_routing_rules.yaml`) require dual sign-off (Head of Data + CTO) on change.
- Adding a new model to the allow-list requires:
  - Eval pass on `docs/EVALS_RUNBOOK.md` suite (≥ 95% pass on critical eval set).
  - Cost projection vs. existing model on 1,000-call replay.
  - DPA review for data-residency implications.
  - Rollout under preview-header gating (ADR-0005) for 14 days before GA.
- Quarterly cost retrospective: review top 10 workflows by spend; route changes proposed.

## 10. Observability Wiring

Per ADR-0004:

- Trace attribute `llm.cost_sar` on every span that involves a model call.
- Prometheus `llm_call_total{model, result, cache_hit}` and `llm_cost_sar_total`.
- Sentry breadcrumb on every LLM call with model + token counts (no prompt content).
- Decision passport carries `cost_attribution[{model, tokens_in, tokens_out, cost_sar}]`.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Provider price increase | dual-provider routing; renegotiation triggered if cost per workflow > 1.50 SAR for 2 consecutive weeks. |
| Cache poisoning | hashed keys with model version; cache entries signed with HMAC. |
| Tenant gaming caps via many small workflows | rate limit per tenant on workflow start (handled in `dealix/trust/policy.py`). |
| Engineer adds new uncapped workflow | CI lint requires every workflow to register a budget entry; fails build otherwise. |

## 12. References

- ADRs: ADR-0001 (event store), ADR-0004 (observability), ADR-0005 (API versioning).
- Code: `dealix/trust/policy.py`, `auto_client_acquisition/revenue_os/enrichment_waterfall.py`, `auto_client_acquisition/revenue_os/signal_normalizer.py`.
- Existing: `docs/AI_MODEL_ROUTING_STRATEGY.md`, `docs/COST_OPTIMIZATION.md`, `docs/V7_COST_CONTROL_POLICY.md`.
- SLO framework: `docs/sre/slo_framework.md`.
- Unit economics: `docs/UNIT_ECONOMICS_AND_MARGIN.md`.
