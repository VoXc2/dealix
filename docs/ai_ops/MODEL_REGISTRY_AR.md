# Model Registry — Dealix

> **Canonical source:** `data/ai_ops/model_registry.yaml`
> **Schema:** `schemas/model_registry.schema.json`
> **Rule:** registry evidence may be prepared before production routing changes; production routing changes require a stable provider ID + official rate card + Dealix evals.
> **Implementation boundary:** this change prepares registry truth, bounded in-process telemetry, HTTP 402 circuit behavior, and an opt-in loopback-only Ollama fallback. It does **not** mutate the configured production model name, provider key, billing, or production environment.

## Required model truth

Every registry entry separates:

- `logical_routes`: business/workload intent such as `daily`, `light`, `code`, `proof_summary`.
- `model_name`: model Dealix requests.
- runtime `effective_model`: model the provider reports actually serving the request.
- `lifecycle`: `stable | beta | expired`.
- `api_name_stability`: `stable | experimental | expiring`.
- `production_eligible`: explicit fail-closed production permission.
- `effective_at/effective_on` and `expires_at/expires_on`.
- cache-hit/cache-miss/output prices, peak windows, concurrency, pricing source, and evaluation gates.

If a provider silently aliases a requested model, Dealix must record both `requested_model` and `effective_model`; cost and quality analysis uses the effective model where it is known.

## DeepSeek decision — 11 September 2026

DeepSeek officially released **V4.1 Flash** on 10 September 2026. The supported API model name is `deepseek-flash`. The provider also states that the old names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are offline and temporarily compatibility-routed to V4.1 Flash. Dealix therefore marks those old registry entries expired/non-production rather than pretending their requested model is still the effective model.

DeepSeek also announced an orderly V4 Pro retirement: after 14 September 2026 12:00 Beijing (07:00 Riyadh), and until V4.1 Pro launches, requests to `deepseek-v4-pro` will be routed to V4.1 Flash and billed at V4.1 Flash pricing. Dealix therefore holds new V4 Pro production promotion until requested/effective-model evidence and official pricing are revalidated.

The temporary `deepseek-v4.1-flash-expires-on-0910` beta is expired and superseded by `deepseek-flash`. The stable provider ID is now known, but `deepseek-flash` remains `production_eligible=false` in Dealix until the promotion gates below pass.

The official release announces lower V4.1 Flash pricing and says the new prices became effective on 10 September 2026 12:00 Beijing, but the exact numeric table is published as an image and is not text-verified in the current evidence set. The previously reported numeric price cut therefore remains an **inactive candidate**. `estimate_budget_cost_usd()` returns `None` for `deepseek-flash` until an official numeric rate card is verified; it must never silently interpret missing rates as zero cost.

Current production model names remain unchanged by this PR.

## Promotion gate for a new DeepSeek production ID

All of the following are required:

1. official stable model ID;
2. official DeepSeek pricing/rate card;
3. lifecycle is not expiring;
4. Dealix daily/light eval passes;
5. Dealix code eval passes;
6. Dealix proof-summary eval passes;
7. requested/effective-model telemetry shows no unexplained alias drift;
8. production fallback/circuit-breaker behavior is verified.

## HTTP 402 policy

A DeepSeek HTTP 402 is a billing/availability condition, not a transient transport error. `core/llm/openai_compat.py` does not retry it. `ModelRouter` opens an in-process `billing_402` circuit immediately and skips further DeepSeek attempts until `reset_provider_circuit(Provider.DEEPSEEK)` is called explicitly. There is no hidden timed auto-reset.

An Ollama fallback may be prepared only when `deepseek_402_ollama_fallback_enabled=true`. It accepts exact loopback URLs only (`127.0.0.1`, `localhost`, or `::1` on port 11434), defaults to the canonical `qwen3:4b-instruct-2507-q4_K_M`, and never changes production configuration by itself. If disabled, 402 fails closed into the existing provider fallback chain. If the local fallback itself fails, the router records the failure once and does not loop.

No policy may print API keys, mutate billing, purchase credits, or weaken provider validation.

## Cost telemetry

Per accepted result, capture at minimum:

`logical_route, requested_model, effective_model, cache_status, input_tokens, output_tokens, retries, accepted, occurred_at, budget_cost_usd, cost_per_accepted_result_usd`.

`core/llm/model_economics.py` provides side-effect-free registry loading, production eligibility, conservative cost estimation, and usage-event construction. `ModelRouter` now keeps a bounded in-memory deque of the latest 500 events and records requested/effective model, cache state, retries, acceptance, and budget cost without writing a new runtime database or exposing credentials.

## Onboarding / offboarding

New model: business case → security/data-flow review → registry → ≥50 eval prompts → R1 pilot → approval → promote only after thresholds pass.

Offboarding: mark deprecated/expired → stop new routing → audit usage → route to approved fallback → remove only after evidence confirms no active dependency.

> **Owner:** `dealix-engineer` · **Review cadence:** provider release/pricing change or model promotion event.
