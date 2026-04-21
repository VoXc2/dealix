# Local AI (On-Prem LLM) — Dealix

> **الهدف**: تشغيل Dealix باستخدام نماذج لغوية مفتوحة على نفس الخادم بدون مفاتيح سحابية،
> بحيث يستطيع الخادم «التفكير» وتنفيذ المهام محلياً.

---

## 1. What was integrated / ماذا تمت إضافته

| Module | Path | Purpose |
| --- | --- | --- |
| Catalog | `backend/app/services/local_ai/catalog.py` | Tier-aware open-weight model registry + host capacity detection. |
| Ollama client | `backend/app/services/local_ai/client.py` | Async chat / streaming / pull, retries, timeouts. |
| Local router | `backend/app/services/local_ai/router.py` | Maps Dealix task keys → best local model; optional 2-way "race". |
| LLM integration | `backend/app/services/llm/provider.py` | New `LocalAIProvider` in the main `LLMRouter` (tries local before cloud). |
| API | `backend/app/api/v1/local_ai.py` | `/api/v1/local-ai/{status,catalog,chat,health-check,tasks}` |
| Install script | `scripts/local-ai/install_local_ai.sh` | Installs Ollama, pulls tier-matched models, prints `.env` hints. |
| Health check | `scripts/local-ai/health_check.py` | Stand-alone AR/EN diagnostic script. |
| Tests | `backend/tests/local_ai/` | Unit tests for catalog / client / router. |

**Everything is opt-in.** Local mode stays off until you set `LOCAL_LLM_ENABLED=1`.
If Ollama is down or no model is pulled, the stack transparently falls back to
Groq / OpenAI — nothing breaks.

---

## 2. Why not Claude / GPT-4 / Gemini / Grok locally?

The screenshots referenced models like **Claude 3.5 Sonnet, GPT-4 Classic,
Gemini 2.5 Flash, Grok 3**. These are **API-hosted** by their vendors and
**cannot be downloaded or run locally** — they have no published weights.

Likewise, **NousResearch/Hermes 4 405B** is a real open-weight model but
needs ≈ 200 GB of VRAM; it is not realistic on a modest Ubuntu server.

Instead, Dealix ships a curated catalog of **genuinely runnable** open
models whose weights Ollama can download:

| Family | Best for | Smallest tag | Largest tag |
| --- | --- | --- | --- |
| Qwen 2.5 (Alibaba) | Arabic business reasoning | `qwen2.5:0.5b` | `qwen2.5:14b-instruct` |
| Llama 3.x (Meta) | English general-purpose | `llama3.2:1b` | `llama3.1:8b` |
| Gemma 2 (Google) | Lightweight general | `gemma2:2b` | — |
| Phi-3 (Microsoft) | Small reasoner | `phi3:mini` | — |
| Qwen2.5-Coder / DeepSeek-Coder-V2 | Coding | `qwen2.5-coder:7b` | `deepseek-coder-v2:lite` |

Cloud models (Claude, GPT-4, Gemini, Grok, GLM-5) remain available through
the existing `backend/app/services/model_router.py` — nothing there changed.

---

## 3. Server tiers / فئات الخادم

`catalog.detect_server_tier()` inspects `/proc/meminfo`, free disk, and GPU
presence and picks one of four conservative tiers:

| Tier | RAM | Default models | Notes |
| --- | --- | --- | --- |
| `nano` | < 4 GB or < 6 GB disk | `qwen2.5:0.5b` | Router / classification only. |
| `small` | 4 – 8 GB | `qwen2.5:3b-instruct`, `qwen2.5:0.5b` | CPU-friendly Arabic chat. |
| `balanced` | 8 – 16 GB | `qwen2.5:7b-instruct`, `qwen2.5-coder:7b`, `qwen2.5:0.5b` | Recommended default for the Saudi-SMB server. |
| `performance` | 16 GB+ or GPU | adds `qwen2.5:14b-instruct` | Full reasoning stack. |

You can override detection with `LOCAL_LLM_FORCE_TIER=small|balanced|…`.

---

## 4. Installation / التثبيت

### Ubuntu server

```bash
# From repo root
sudo bash scripts/local-ai/install_local_ai.sh
```

The script will:

1. Install Ollama via the official installer (skips if present).
2. Start the `ollama` daemon (systemd if available, `nohup` otherwise).
3. Detect RAM / disk / GPU and pick the tier.
4. Pull the tier-matched models (idempotent — safe to re-run).
5. Print the `.env` lines to paste into `backend/.env`.

Environment overrides before running:

```bash
FORCE_TIER=balanced bash scripts/local-ai/install_local_ai.sh   # force a tier
SKIP_PULL=1         bash scripts/local-ai/install_local_ai.sh   # daemon only
MIN_DISK_GB=10      bash scripts/local-ai/install_local_ai.sh   # stricter guard
```

### Enable in Dealix

Add to `backend/.env`:

```env
LOCAL_LLM_ENABLED=1
LOCAL_LLM_BASE_URL=http://localhost:11434
LOCAL_LLM_DEFAULT_MODEL=qwen2.5:7b-instruct
LOCAL_LLM_ROUTER_MODEL=qwen2.5:0.5b
LOCAL_LLM_CODER_MODEL=qwen2.5-coder:7b
# Optional — prefer local over cloud:
# LLM_PRIMARY_PROVIDER=local
```

Restart the backend. Verify:

```bash
python scripts/local-ai/health_check.py
curl http://localhost:8000/api/v1/local-ai/status | jq
```

---

## 5. How the router decides

For each agent call, `LLMRouter.complete()` now tries providers in order:

1. **Local** (`LocalAIProvider`) — only if enabled **and** daemon reachable **and** at least one model pulled.
2. **Groq** — fast cloud inference.
3. **OpenAI** — reliable fallback.

Inside the local provider, `LocalModelRouter.resolve_task()` maps the Dealix
task-key (e.g. `arabic_summarization`, `fast_classify`, `coding`,
`complex_reasoning`) to a `TaskKind`, then `pick_model_for_task()` picks the
best-scoring catalogued model that the tier can host.

### Optional "race" mode

Inspired by the model-racing pattern seen in multi-model demos, `/local-ai/chat`
accepts `race=true`. When enabled **and** two catalogued models match the task,
the router runs both in parallel and keeps whichever response scores higher on
a cheap length/structure heuristic.

> **Safety note.** Dealix does **not** adopt the "liberated" / jailbreak prompts
> from projects like `elder-plinius/G0DM0D3`. All system prompts remain
> business-grade (sales assistant, QA reviewer, compliance). Only the *routing
> and racing* mechanics were borrowed.

---

## 6. API surfaces

| Method | Path | What it returns |
| --- | --- | --- |
| GET  | `/api/v1/local-ai/status` | Daemon health, tier, pulled tags, overrides. |
| GET  | `/api/v1/local-ai/catalog` | Full catalog + eligible + recommended-install list. |
| GET  | `/api/v1/local-ai/tasks`  | Known task keys. |
| POST | `/api/v1/local-ai/health-check` | Force-refresh daemon ping. |
| POST | `/api/v1/local-ai/chat` | Run a single prompt on the best local model (body: `task`, `prompt`, `system?`, `temperature?`, `max_tokens?`, `json_mode?`, `race?`). |

Example:

```bash
curl -X POST http://localhost:8000/api/v1/local-ai/chat \
  -H "Content-Type: application/json" \
  -d '{"task":"arabic_summarization","prompt":"لخّص الفقرة التالية بثلاث نقاط: ...","race":false}'
```

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `/local-ai/status` → `daemon_healthy: false` | Ollama not running | `systemctl status ollama` or re-run `install_local_ai.sh`. |
| `/chat` → 503 "no models pulled" | Tag not installed | `ollama pull qwen2.5:3b-instruct`. |
| OOM during chat | Model too large for RAM | Set `LOCAL_LLM_DEFAULT_MODEL` to a smaller tag or `LOCAL_LLM_FORCE_TIER=small`. |
| Arabic output quality weak | Using a Llama/Phi model | Switch default to a Qwen 2.5 tag (stronger Arabic). |
| Port clash | Another service on 11434 | Change `OLLAMA_HOST` + `LOCAL_LLM_BASE_URL`. |

---

## 8. Cost & PDPL considerations

* Local inference = zero per-token spend; only hardware + electricity.
* Data **never leaves the server**, which simplifies PDPL compliance for
  sensitive Saudi customer data (see `docs/saudi-compliance-matrix.md`).
* We still log token counts / latency in the existing `ai_conversations`
  table via `AgentExecutor._log_conversation`, so observability parity is
  preserved.
