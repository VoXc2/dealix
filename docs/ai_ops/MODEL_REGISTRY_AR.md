# Model Registry — Dealix (AR)

> **Source of truth:** `data/ai_ops/model_registry.yaml`
> **Schema:** `schemas/model_registry.schema.json`
> **Update rule:** أي model جديد يُضاف هنا **قبل** استخدامه في production.

---

## Registry Format

```yaml
- model_id: <unique>
  provider: <MiniMax|OpenAI|DeepSeek|Ollama|...>
  model_name: <e.g., claude-sonnet-4-6>
  cost_class: low|medium|high
  allowed_tasks: [R1, R2, R3]   # see AI_OPS_OS_AR.md
  forbidden_tasks: []
  pii_policy: forbid|redact|allow
  max_context_tokens: <int>
  fallback_model_id: <id>
  eval_score_threshold: 0.7
  owner: <name>
  added_at: <date>
  status: active|deprecated|testing
  notes: ""
```

---

## Initial Models (مُقترح)

| model_id | provider | model_name | cost | tasks | PII |
|----------|----------|------------|------|-------|-----|
| `minimax-haiku-45` | MiniMax | claude-haiku-4-5 | low | R1 | forbid |
| `minimax-sonnet-46` | MiniMax | claude-sonnet-4-6 | med | R1, R2, R3 | redact |
| `openai-gpt4o-mini` | OpenAI | gpt-4o-mini | low | R1 | forbid |
| `openai-gpt4o` | OpenAI | gpt-4o | high | R2, R3 | redact |
| `deepseek-chat` | DeepSeek | deepseek-chat | low | R1, R2 (non-sensitive) | forbid |
| `ollama-llama31-8b` | Ollama | llama-3.1-8b | free | R1 (internal) | allow |

> **ملاحظة:** قائمة النماذج ديناميكية. تُحدّث عند إضافة/إزالة نموذج.

---

## Onboarding a New Model

1. Business case
2. Security review (DPA, data flow, PII handling)
3. Add to `data/ai_ops/model_registry.yaml`
4. Eval suite (≥ 50 test prompts)
5. Pilot in low-risk task (R1)
6. Council approval
7. Promote to R2/R3 if eval ≥ 0.8
8. Update this doc

---

## Offboarding a Model

1. Mark `status: deprecated`
2. Route remaining traffic to fallback
3. Audit usage
4. Remove from routing after 30 days
5. Update registry

---

## Cost Snapshot (per 1M tokens, approximate)

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Haiku 4.5 | $1 | $5 | fast, cheap |
| Sonnet 4.6 | $3 | $15 | balanced |
| GPT-4o-mini | $0.15 | $0.60 | cheapest API |
| GPT-4o | $5 | $15 | premium |
| DeepSeek | $0.27 | $1.10 | very cheap, review needed for sensitive |
| Ollama local | $0 | $0 | compute cost only |

**تحذير:** الأسعار تتغير. راجع صفحة كل provider.

---

> **Owner:** Tech Lead · **Cadence:** يُحدّث عند كل إضافة/إزالة
