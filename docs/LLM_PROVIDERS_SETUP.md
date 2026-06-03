# LLM Providers Setup — Dealix

**Date:** 2026-05-07
**Status:** 6 providers integrated · 1 active in production (Groq) · 5 ready-to-activate via env vars
**Companion:** `core/llm/router.py` · `core/config/models.py` · `auto_client_acquisition/llm_gateway_v10/` · `auto_client_acquisition/agent_observability/` · `dealix/observability/cost_tracker.py` · Plan §24.6

> **Audit verdict (Wave 7.5):** Dealix's LLM gateway is **95% built**. 4-tier system + smart routing + cost tracking + fallback chain all live. Activation = setting env vars on Railway + 5 small enhancements (rate-limit detection · per-tier budget caps · trace ID linking · cost-aware fallback · per-task tier matrix).

---

## 1. The 6 providers + their default models

| Provider | Default model | Tier | Strength | Cost (per 1M) |
|---|---|---|---|---|
| **Anthropic** | `claude-sonnet-4-5-20250929` | strong_for_strategy | Reasoning · proposals · narrative | $3 in / $15 out |
| **Anthropic Opus** | `claude-opus-4-5-20251110` | strong_for_strategy (premium) | Highest quality reasoning | $15 in / $75 out |
| **Anthropic Haiku** | `claude-haiku-4-5-20250502` | balanced_for_drafts | Fast + good quality | $0.25 in / $1.25 out |
| **Groq** | `llama-3.3-70b-versatile` | cheap_for_classification | Fast classification (free tier) | $0 in / $0 out |
| **Google Gemini** | `gemini-2.5-pro` | strong_for_strategy | Research · multimodal | $1.25 in / $5 out |
| **DeepSeek** | `deepseek-chat` | balanced_for_drafts | Code · implementation | $0.14 in / $0.28 out |
| **Zhipu GLM** | `glm-4` | balanced_for_drafts | Arabic-heavy text · bulk | $0.14 in / $0.28 out |
| **OpenAI** | `gpt-4o-mini` | cheap_for_classification | Fallback general-purpose | $0.15 in / $0.60 out |

**Source:** `dealix/observability/cost_tracker.py:38-56` (cost matrix) · `core/config/settings.py:54-81` (defaults).

---

## 2. Per-task tier matrix (Wave 7.5 §24.6 E5)

Each AI agent has a default tier. Routing happens via `core/config/models.py::smart_route()` (lines 194-237).

| Agent | Default tier | Provider chain | Why |
|---|---|---|---|
| Sales Agent (qualification, BANT scoring) | `cheap_for_classification` | Groq → DeepSeek → OpenAI | Speed > quality; classification doesn't need reasoning |
| Growth Agent (warm-route drafts AR) | `balanced_for_drafts` | GLM → Anthropic Sonnet → Gemini Flash | Arabic text quality + cost-balance |
| Support Agent (ticket classify) | `cheap_for_classification` | Groq → OpenAI | Throughput priority |
| Ops Agent (delivery checklist) | `local_no_model` | (deterministic) → Groq fallback | Rules-based; LLM unnecessary |
| Executive Agent (weekly brief, narrative) | `strong_for_strategy` | Anthropic Opus → Anthropic Sonnet → Gemini Pro | Quality cannot be compromised |
| Diagnostic generator (Saudi-Arabic narrative) | `strong_for_strategy` | Anthropic Opus → GLM (AR) | Narrative quality + Saudi dialect |
| Proof pack narrative builder | `strong_for_strategy` | Anthropic Opus | Customer-facing quality |
| Market research (sector intel) | `strong_for_strategy` | Gemini Pro → Anthropic Sonnet | Multi-modal + research strength |

---

## 3. Activation steps (Railway dashboard)

### Founder action — set env vars

For each provider, set the env var on Railway:

```bash
# Required (already active in production)
GROQ_API_KEY=gsk_<...>

# Recommended (activate Wave 7.5 — main GTM impact)
ANTHROPIC_API_KEY=sk-ant-<...>      # premium tier — narrative quality
GEMINI_API_KEY=AIza<...>             # research + multimodal

# Optional (cost optimization — activate Wave 8 when scale demands)
DEEPSEEK_API_KEY=<...>               # cheap code-task tier
ZHIPU_API_KEY=<...>                  # Arabic-heavy bulk
OPENAI_API_KEY=sk-<...>              # generic fallback
```

### Pricing source URLs

- Anthropic: https://www.anthropic.com/pricing — Claude Opus / Sonnet / Haiku
- Google AI: https://ai.google.dev/pricing — Gemini 2.5 Pro / Flash
- Groq: https://console.groq.com/pricing — Llama 3.3 70B (free tier currently)
- DeepSeek: https://platform.deepseek.com/pricing
- Zhipu GLM: https://open.bigmodel.cn/pricing
- OpenAI: https://openai.com/api/pricing — GPT-4o-mini

### Verification after Railway redeploy

```bash
# /health endpoint surfaces active providers (dynamic from env)
curl -s https://api.dealix.me/health | jq '.providers'
# Expected: ["groq","anthropic","gemini",...]

# Per-trace observability
curl -s "https://api.dealix.me/api/v1/agent-observability/cost-summary?window=1h" \
  -H "Authorization: Bearer $FOUNDER_TOKEN" | jq
```

---

## 4. Fallback chain (per `core/llm/router.py`)

When a provider fails (rate-limit, API error, network), the gateway tries the next provider in the chain:

```
ANTHROPIC → [OPENAI, GLM]
GEMINI    → [GROQ, OPENAI]
GROQ      → [OPENAI, GEMINI]
DEEPSEEK  → [ANTHROPIC, OPENAI]
GLM       → [ANTHROPIC, GROQ]
OPENAI    → [GROQ, ANTHROPIC]
```

Source: `core/llm/router.py::FALLBACK_CHAIN`.

---

## 5. Cost-aware routing

The `smart_route()` heuristic in `core/config/models.py:194-237` picks tier based on:

1. Task type → tier mapping (e.g. classification → cheap, narrative → strong)
2. Arabic language ratio (>30% → GLM)
3. Token estimate (<2K → DeepSeek for short extraction)
4. Multi-modal need → Gemini (with vision support)

Cost guard (`auto_client_acquisition/tool_guardrail_gateway/cost_budget.py`):
- Default per-call cap: $1.00 USD
- Token cap: 50,000 per call
- Returns `{passed, reasons, budget_remaining}` — caller decides retry

---

## 6. Wave 7.5 enhancements deferred (acknowledged but not built)

The full plan §24.6 listed 5 enhancements. Wave 7.5 ships the **doc + per-task matrix doc**; code patches deferred to Wave 8 trigger:

| # | Enhancement | Status | Why deferred |
|---|---|---|---|
| E1 | Rate-limit (429) detection in `core/llm/router.py` | DEFERRED | Existing fallback handles all exceptions; specific 429 detection adds 30 LOC, not blocking customer #1 |
| E2 | Per-tier hourly budget caps in `cost_budget.py` | DEFERRED | Existing per-call cap covers Wave 7 scale; per-tier caps activate at customer #4 |
| E3 | Trace ID linking in `cost_tracker.py` | DEFERRED | Per-call logging suffices for Wave 7 customer count |
| E4 | Cost-aware tier downgrade on cost-exceed | DEFERRED | Manual fallback chain works; auto-downgrade needs A/B telemetry first |
| E5 | Per-task tier matrix doc | ✅ DONE (this doc §2) | This is the customer-visible artifact |

**Trigger for E1-E4 activation:** when LLM monthly cost exceeds 200 SAR OR rate-limit observed in production logs OR customer #4 onboards.

---

## 7. Hard rules

- ❌ No real API keys committed to repo (env vars only — verified by `tests/test_no_committed_secrets.py`)
- ❌ No customer PII sent to LLM without `pii_redactor.redact_dict()` first (per `auto_client_acquisition/tool_guardrail_gateway/output_guardrails.py`)
- ❌ No prompt-injection bypass: input guardrails check before tool calls (per `auto_client_acquisition/tool_guardrail_gateway/input_guardrails.py`)
- ✅ Every LLM call logs to `dealix/observability/cost_tracker.py` Postgres `llm_calls` table
- ✅ Every prompt has `correlation_id` for downstream audit
- ✅ Forbidden-token output scrub runs on every customer-facing narrative (`output_guardrails.py`)

---

## 8. Smoke test (current state)

```bash
# Test classification routing → Groq
python3 -c "
from core.config.models import smart_route
provider, model = smart_route(task_type='CLASSIFICATION', input_tokens=100)
assert provider in ('GROQ', 'OPENAI'), provider
print(f'CLASSIFICATION → {provider}: {model}')
"

# Test narrative routing → Anthropic / Gemini
python3 -c "
from core.config.models import smart_route
provider, model = smart_route(task_type='REASONING', input_tokens=2000)
assert provider in ('ANTHROPIC', 'GEMINI'), provider
print(f'REASONING → {provider}: {model}')
"
```

---

## 9. What's deferred to Wave 8

- Rate-limit (429) auto-detection + retry with exponential backoff
- Per-tier hourly/daily budget caps (current: per-call only)
- Trace ID end-to-end across multi-LLM call chains
- Cost-aware automatic tier downgrade
- A/B model evaluation framework
- Multi-region routing (KSA-residency for sensitive prompts)
