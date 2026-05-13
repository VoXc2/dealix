# LLM Gateway — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** AI Platform Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [LLM_GATEWAY_AR.md](./LLM_GATEWAY_AR.md)

## Context
Every model call inside Dealix must pass through a single Gateway.
The Gateway is the choke point that lets Dealix enforce governance,
route to the right model tier, cap cost, redact PII, log runs, and
plug evaluations. It is referenced by
`docs/AI_MODEL_ROUTING_STRATEGY.md` for routing logic,
`docs/LLM_PROVIDERS_SETUP.md` for provider wiring, and
`docs/AI_STACK_DECISIONS.md` for the stack-level decisions. Direct
provider calls outside the Gateway are forbidden (FA-14).

## Responsibilities
The Gateway has ten responsibilities. Each maps to a check or service
inside the runtime.

1. **Model routing** — route the request to the right model tier
   (`fast` / `balanced` / `deep`) based on task and policy.
2. **Cost guard** — enforce per-tenant and per-task budget caps;
   refuse when a cap is exceeded.
3. **Prompt registry** — load prompts from a versioned registry;
   reject unregistered prompts.
4. **Redaction** — strip PII from inputs unless an explicit lawful
   basis allows it.
5. **Schema validation** — validate outputs against the declared
   output schema; reject malformed outputs.
6. **Fallback** — when a provider fails, fall back to the configured
   alternative.
7. **Cache** — cache deterministic outputs to cut cost.
8. **AI run log** — write a record per call to the AI Run Ledger.
9. **Eval hook** — emit a sample for evaluations per
   `docs/EVALS_RUNBOOK.md`.
10. **Risk score** — attach a risk score to every output based on
    content, channel, and action class.

## Routing Tiers
| Tier | Use cases | Cost class |
|---|---|---|
| `fast` | Classification, extraction, light edits | Low |
| `balanced` | Drafts, summaries, Q&A | Medium |
| `deep` | Long-context reasoning, complex briefs | High |

Routing rules are declared in code and audited per change. Manual
overrides require a logged Approval.

## Sample AI Run Record
Every Gateway call produces a record like the following. The record
is the unit of observability and audit.

```json
{
  "ai_run_id": "AIR-001",
  "agent": "RevenueAgent",
  "task": "score_accounts",
  "model_tier": "balanced",
  "prompt_version": "lead_scoring_v1",
  "inputs_redacted": true,
  "output_schema": "AccountScore",
  "qa_score": 91,
  "risk_level": "medium",
  "cost": 0.42
}
```

The record is appended to the AI Run Ledger and linked to the
`AuditEvent` written by `governance/check`.

## Failure Modes
- Provider timeout → fallback to alternate provider, attach
  `fallback_used: true`.
- Schema validation failure → return error with retryable code; do
  not surface raw model output.
- Cost cap exceeded → block with `cost_cap_exceeded`; alert the
  owner.
- Forbidden content match → block with `forbidden_action` and the
  rule ID from `docs/governance/FORBIDDEN_ACTIONS.md`.

## Observability
- p50 / p95 / p99 latency per tier and per task.
- Cache hit rate.
- Schema rejection rate.
- Cost per task and per Workspace.
- Eval sample rate.

These metrics flow into `docs/AI_OBSERVABILITY_AND_EVALS.md` and the
founder command center.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Prompt registry PR | New prompt version | AI platform lead | Per change |
| Routing policy change | Deployed routing config | AI platform lead | Per change |
| Cost budget update | Updated cost guard | Finance + AI platform lead | Per change |
| Provider change | Failover plan | AI platform lead | Per change |

## Metrics
- **Gateway compliance** — share of model calls routed via the
  Gateway. Target: 100%.
- **Cache hit rate** — Target: ≥ 30%.
- **Cost-cap breach count** — Target: 0.
- **Eval sample coverage** — Target: ≥ 5% per task.

## Related
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing strategy.
- `docs/LLM_PROVIDERS_SETUP.md` — provider setup.
- `docs/AI_STACK_DECISIONS.md` — stack decisions.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability and evals.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
