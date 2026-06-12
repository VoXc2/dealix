# MiniMax Sub-prompt 02 — Revenue Factory Binding

> **Scope:** Wire MiniMax as the daily draft engine into the existing Outreach / Approval / Compliance stack.
> **Do not break:** `dealix/hermes/providers/minimax_provider.py`, the governance OS, the outbound safety tests.
> **Branch:** `feature/minimax-factory-p0-hardening`
> **Acceptance:** `make minimax-status` exits 0 and prints provider health + today's queue depth.

---

## 1. Objective

MiniMax is already integrated as an OpenAI-compatible provider. The gap is **operational**: there is no single source of truth for which provider handles which task, what the cost guard is, and what the eval harness expects. This sub-prompt produces that source of truth plus one status command.

---

## 2. Files to Create

### 2.1 `data/ai_ops/model_registry.yaml`

A single registry listing every model provider Dealix routes to, with cost + latency + evidence level. YAML format. Schema-validated.

```yaml
version: 1
updated: 2026-06-12
providers:
  - id: minimax-text
    provider_class: dealix.hermes.providers.minimax_provider.MiniMaxProvider
    base_url_env: MINIMAX_BASE_URL
    api_key_env: MINIMAX_API_KEY
    model_env: MINIMAX_MODEL
    default_model: MiniMax-Text-01
    tasks: [outreach_draft_ar, outreach_draft_en, translation_ar_en, proposal_section, proof_pack_summary, founder_daily_brief]
    cost:
      input_per_1k_usd: 0.001
      output_per_1k_usd: 0.002
    latency_p95_ms: 1800
    evidence_level_default: L2
    approval_required: true
    daily_cap:
      requests: 5000
      tokens: 4_000_000
  - id: anthropic-claude
    provider_class: dealix.hermes.providers.anthropic_provider.AnthropicProvider
    api_key_env: ANTHROPIC_API_KEY
    default_model: claude-sonnet-4-5
    tasks: [deep_analysis, governance_review, red_team_simulation]
    cost:
      input_per_1k_usd: 0.003
      output_per_1k_usd: 0.015
    latency_p95_ms: 2500
    evidence_level_default: L4
    approval_required: true
```

(Keep the file under 120 lines. Include only providers that actually exist in `dealix/hermes/providers/`.)

### 2.2 `schemas/model_registry.schema.json`

JSON Schema (Draft 2020-12) for the YAML above. Required fields per provider: `id`, `provider_class`, `tasks[]`, `cost.{input_per_1k_usd, output_per_1k_usd}`, `latency_p95_ms`, `evidence_level_default`, `approval_required`. Optional: `base_url_env`, `api_key_env`, `model_env`, `default_model`, `daily_cap.{requests, tokens}`.

### 2.3 `tests/test_model_registry.py`

Pytest that:
- Loads `data/ai_ops/model_registry.yaml`.
- Validates it against `schemas/model_registry.schema.json`.
- Asserts every `provider_class` is importable (skip with `pytest.importorskip` if optional dep missing).
- Asserts every task in `tasks[]` is listed in `prompts/registry.py` (or skip if registry absent — print a warning).

### 2.4 `tests/test_minimax_provider.py`

Pytest that:
- Initializes `MiniMaxProvider` with **no key** and asserts `_mock_response` path is taken.
- Initializes with a **fake key** (using `monkeypatch.setenv("MINIMAX_API_KEY", "test")`) and asserts the client is constructed (or `ImportError` is caught — depends on `openai` being optional).
- Verifies `chat()` returns `{text, tool_calls, usage}` shape even in mock mode.

### 2.5 `reports/minimax/MINIMAX_IMPLEMENTATION_REPORT.md`

Status snapshot. Header + 4 tables:
1. **Provider health** — one row per provider in registry: `provider_id`, `api_key_set` (yes/no, never value), `default_model`, `evidence_level`, `approval_required`.
2. **Today's queue** — counts from `reports/outreach/DRAFT_PRODUCTION_DAILY.md` if it exists, else "no queue yet".
3. **Last 7-day eval delta** — placeholder table; populated when the eval harness is wired in the next sub-prompt.
4. **Open items** — bullet list of gaps still pending.

### 2.6 Makefile additions (additive only)

```makefile
minimax-status: ## Print MiniMax provider health + today's draft queue
	$(PYTHON) scripts/minimax_status.py

minimax-evals: ## Run MiniMax eval suite (mock by default; real with MINIMAX_API_KEY)
	$(PYTHON) scripts/minimax_evals.py
```

### 2.7 `scripts/minimax_status.py`

One-shot script: loads registry, prints provider health table to stdout, prints exit 0. No external calls. No network. No PII. Uses only stdlib + the registry loader from `dealix/hermes/` if available; else inline.

### 2.8 `scripts/minimax_evals.py`

Wrapper around the eval datasets in `data/evals/`. Runs `pytest tests/test_model_registry.py` plus any new eval cases. With `MINIMAX_API_KEY` unset, runs in **mock mode** (deterministic stub responses). With it set, runs a real smoke test (capped at 5 calls).

---

## 3. Constraints

- No provider must be enabled by default. `MINIMAX_API_KEY` unset → mock mode → no network.
- No real outbound send from these scripts. Read-only diagnostics.
- Schema must be valid against `https://json-schema.org/draft/2020-12/schema` (assert in test).
- Registry must not contain any real API keys. Only env var *names*.
- Do not edit `dealix/hermes/providers/minimax_provider.py` — it works as-is.

---

## 4. Acceptance

```bash
# Schema validates
python -c "import json, yaml; js=json.load(open('schemas/model_registry.schema.json')); yaml.safe_load(open('data/ai_ops/model_registry.yaml'))"

# New tests pass
pytest tests/test_model_registry.py tests/test_minimax_provider.py -v

# Status command works
make minimax-status
```

Output of `make minimax-status` must include, at minimum:

```
DEALIX_MINIMAX_STATUS
provider            api_key_set  model              evidence  approval_required
minimax-text        no           MiniMax-Text-01    L2        yes
...
DEALIX_MINIMAX_STATUS=OK
```
