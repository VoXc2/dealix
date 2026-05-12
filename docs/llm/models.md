# LLM model registry

The single source of truth for which model powers which workflow, the
fallback chain, and the last time we verified that combination behaves
well on our golden set.

| Workflow | Primary | Fallback chain | Last verified | Cost ceiling |
| --- | --- | --- | --- | --- |
| Proposal drafting | `claude-3-5-sonnet-latest` | `claude-3-5-haiku-latest` → `gpt-4o-mini` | 2026-05-12 | $0.30 / proposal |
| ICP matching | `claude-3-5-sonnet-latest` | `claude-3-5-haiku-latest` | 2026-05-12 | $0.05 / lead |
| Lead qualification | `claude-3-5-haiku-latest` | `gpt-4o-mini` | 2026-05-12 | $0.02 / lead |
| Reply classifier | `claude-3-5-haiku-latest` | `gpt-4o-mini` | 2026-05-12 | $0.01 / reply |
| WhatsApp draft | `claude-3-5-haiku-latest` | none | 2026-05-12 | $0.02 / message |
| Daily targeting personalization | `claude-3-5-haiku-latest` | `groq:llama-3.1-8b-instant` | 2026-05-12 | $0.03 / row |
| Weekly digest | `claude-3-5-sonnet-latest` | `gpt-4o-mini` | 2026-05-12 | $0.20 / digest |

## How "last verified" is computed

`promptfoo eval -c evals/promptfoo/<workflow>.yaml` runs every Tuesday
03:00 Riyadh on the golden set. A green run updates this row's date.
A red run blocks the corresponding PR and pings the founder via Knock.

## Choosing the primary

- Default to Claude Sonnet for any task that emits Arabic text to a
  customer — Sonnet's Arabic + brand-tone alignment is currently better.
- Default to Claude Haiku for classification / scoring tasks where cost
  per call matters.
- OpenAI / Gemini / Groq are fallbacks; switch on consistent provider
  errors > 3 in the last 5 minutes (Portkey policy).

## Cost guardrails (see `core/llm/cost_guard.py`)

- `LLM_MAX_USD_PER_REQUEST` = $0.50 (hard cap; throws `CostCapExceeded`).
- `LLM_MAX_USD_PER_TENANT_DAY` = $25.00 (tracked in Redis with a
  per-process fallback).
- `LLM_DEGRADE_MODEL` = `claude-3-5-haiku-latest` — when set, capped
  calls swap to this model instead of 5xx-ing.

## Provider env keys

| Provider | Env var | Required for |
| --- | --- | --- |
| Anthropic | `ANTHROPIC_API_KEY` | Primary path; at least one of Anthropic / OpenAI is mandatory in production. |
| OpenAI | `OPENAI_API_KEY` | Fallback / TS workflows. |
| Google | `GOOGLE_GENERATIVE_AI_API_KEY` | Optional. |
| Groq | `GROQ_API_KEY` | Cheap fallback for personalization. |
| Portkey gateway | `PORTKEY_API_KEY` | Optional; when set, all the above route through Portkey for cost attribution. |
| Langfuse | `LANGFUSE_*` | Trace inspection. |
