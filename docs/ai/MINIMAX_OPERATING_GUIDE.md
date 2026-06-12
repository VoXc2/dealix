# Dealix MiniMax Operating Guide

> **Status:** Active (P1)
> **Audience:** engineers, founder, AI agents (MiniMax itself)
> **Provider class:** `dealix.hermes.providers.minimax_provider.MiniMaxProvider`
> **Last updated:** 2026-06-12

This guide is the operating manual for the MiniMax LLM provider as wired into the Dealix hermes router. It explains what MiniMax is allowed to do, what it is not, how the cost guard works, and how to extend it.

## 1. What MiniMax is, in Dealix

MiniMax is **one** provider in the hermes router. It is the **high-volume daily generation** provider — drafts, translations, AR/EN outreach, proposal sections, proof-pack summaries, founder report bodies. It is **not** the deep-analysis provider and **not** the governance-review provider. Those go to a heavier model (e.g. Anthropic Claude) with a higher `evidence_level` and a tighter approval gate.

The split is deliberate: high-volume cheap generation must be cheap and fast; deep reasoning must be expensive and slow. Mixing them in one provider is how you burn budget without raising quality.

## 2. Where it lives

| File | Role |
| --- | --- |
| `dealix/hermes/providers/minimax_provider.py` | OpenAI-compatible async client |
| `data/ai_ops/model_registry.yaml` | Single source of truth: provider, model, cost, tasks, evidence level |
| `schemas/model_registry.schema.json` | JSON Schema that validates the registry |
| `scripts/minimax_status.py` | One-shot health snapshot — `make minimax-status` |
| `scripts/minimax_evals.py` | Eval harness (mock by default, real with key) — `make minimax-evals` |
| `tests/test_minimax_provider.py` | Mock-mode coverage |
| `tests/test_model_registry.py` | Schema + import coverage |
| `tasks/minimax/MASTER_MINIMAX_EXECUTION_PROMPT_AR.md` | The canonical read-only prompt that drives the factory |
| `tasks/minimax/0[1-6]_*_AR.md` | Per-PR sub-prompts (P0, Revenue Factory, Control Room, WhatsApp, Payment, Media) |
| `docs/ai/MODEL_PROVIDER_MATRIX.md` | Existing provider matrix — read for the historical OpenAI/Anthropic/Kimi/DeepSeek/OpenRouter/deterministic view |
| `docs/ai/AI_MODEL_ROUTER_PLAN.md` | The router architecture this guide is a binding for |

## 3. The hard rules

These are not guidelines. They are enforced by tests, by the governance OS, and by the approval queue.

1. **No cold WhatsApp.** Never, regardless of evidence level.
2. **No LinkedIn automation.** Drafts only; the approval queue gates send.
3. **No scraping without consent.** Whitelist in `consent_records` is required.
4. **No fake proof.** Every claim needs `evidence_level` (L0–L5) and a `proof_id` reference.
5. **No guaranteed ROI.** Reject or rephrase.
6. **No PII in logs.** Redaction layer is mandatory on every output.
7. **No secrets in prompts or reports.** Reference env names, never values.
8. **No external sends without approval.** Every draft carries `approval_required=true` + `risk_level`.

The governance OS (`auto_client_acquisition/governance_os/`) is the source of truth for these rules. The MiniMax provider itself is dumb — it does not enforce them. Enforcement happens at the router, the approval queue, and the safety tests.

## 4. The model registry

`data/ai_ops/model_registry.yaml` is the single source of truth. Every provider in `dealix/hermes/providers/` must be registered. Every registered provider has:

- `id` — stable identifier
- `provider_class` — fully-qualified import path
- `tasks` — list of task names this provider is allowed to handle
- `cost` — input and output USD per 1k tokens
- `latency_p95_ms` — for routing decisions
- `evidence_level_default` — L0 (no evidence) to L5 (external audited)
- `approval_required` — boolean
- `daily_cap` — optional requests + tokens guard

If you add a new provider:

1. Implement it in `dealix/hermes/providers/`.
2. Add an entry to `model_registry.yaml`.
3. Run `make minimax-status` — must pass.
4. Run `make minimax-evals` — must pass.
5. Add a test in `tests/test_model_registry.py` if the entry has unusual shape.

If you change a cost, latency, or evidence level, the same steps apply. The registry is part of the contract.

## 5. The cost guard

`data/ai_ops/model_registry.yaml` declares a `daily_cap.requests` and `daily_cap.tokens` per provider. The router (in `dealix/hermes/router.py`) reads these and rejects requests that would exceed the cap. The cap is reset on the local timezone midnight.

In v0 the guard logs the rejection and falls back to a stub. It does **not** page anyone. The founder sees the rejection in `make minimax-status`. A future sub-prompt will wire alerting.

## 6. The eval harness

`make minimax-evals` runs:

- `tests/test_model_registry.py` — schema + import coverage
- `tests/test_minimax_provider.py` — mock-mode coverage
- Every case in `data/evals/{security_prompt_injection,outbound_safety,whatsapp_safety,agent_permission,commercial_claim}_cases.jsonl` that is marked as applying to MiniMax

Eval runs in **mock mode** unless `MINIMAX_API_KEY` is set in the environment. Mock mode uses deterministic stubs and runs offline. This is by design: CI must not depend on external network or paid API quotas.

When you add a new task to the registry, add at least 3 eval cases to the matching JSONL file. The cases should cover: happy path, edge case, forbidden case (one that the safety rule must reject).

## 7. How the founder uses it

The founder does not call the MiniMax provider directly. The founder runs:

```bash
make minimax-status        # today's factory health
make minimax-evals         # eval deltas
make cockpit               # founder daily brief (consumes drafts)
```

Or in the UI: `/[locale]/ops/founder` → 90-min cockpit. The cockpit is read-only — it shows drafts in the approval queue, never sends.

## 8. Stop conditions

Stop and ask the founder if:

- A test in `tests/test_*safety*` starts failing after a registry change.
- You need to edit `auto_client_acquisition/governance_os/` (the trust core).
- A client's PII appears in any file you are about to write.
- You want to raise `daily_cap.requests` or `daily_cap.tokens` by more than 20%.

## 9. Related

- `tasks/minimax/MASTER_MINIMAX_EXECUTION_PROMPT_AR.md` — canonical prompt
- `data/ai_ops/model_registry.yaml` — registry
- `scripts/minimax_status.py` — status command
- `docs/governance/COMPLIANCE_PERIMETER.md` — what is forbidden
- `docs/ops/PRODUCTION_VERIFICATION_GUIDE.md` — what `make prod-verify` does
