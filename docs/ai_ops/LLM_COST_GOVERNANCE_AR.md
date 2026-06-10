# LLM Cost Governance — Dealix (AR)

---

## 1. لماذا Cost Governance؟

بدون governance:
- فاتورة LLM تنفجر بدون warning
- نماذج قوية لمهام بسيطة = هدر
- لا visibility على ROI لكل agent
- لا ability لإيقاف عند حد معين

---

## 2. Budget Layers

| Layer | Cadence | Default | Override |
|-------|---------|---------|----------|
| **Per task** | per call | 50K tokens | founder override |
| **Per agent** | per hour | 200K tokens | tier-based |
| **Per day** | rolling 24h | 5M tokens | configurable |
| **Per month** | calendar | $X (TBD) | council approval |
| **Per model** | per day | varies | per registry |

---

## 3. Cost Calculation

```python
cost = (input_tokens × input_rate) + (output_tokens × output_rate)
```

Rates from `MODEL_REGISTRY_AR.md` §"Cost Snapshot".

---

## 4. Alert & Stop Thresholds

| Threshold | Action |
|-----------|--------|
| 50% of budget | Info log |
| 80% of budget | Email alert to founder |
| 95% of budget | Pause non-essential R1 tasks |
| 100% of budget | Hard stop, require founder override |
| 110% of budget | All non-R3 paused, council review |

---

## 5. Optimization Tactics

1. **Routing:** R1 → cheap, R3 → premium (no waste)
2. **Caching:** hash(prompt) → cache for 1h
3. **Truncation:** max context per tier
4. **Batching:** non-urgent batched
5. **Local-first:** internal tasks → Ollama
6. **Streaming:** for long outputs (better UX, similar cost)
7. **Compression:** strip redundant whitespace in prompts

---

## 6. Cost Attribution

لكل cost event:
- agent_id
- task_id
- model_id
- input_tokens
- output_tokens
- cost_usd
- client_id (if billable)
- project_id (if internal)

→ `data/ai_ops/model_usage_events.jsonl`

---

## 7. Reporting

- **Daily:** cost summary to founder dashboard
- **Weekly:** cost by agent + by model
- **Monthly:** cost vs budget + ROI
- **Quarterly:** model performance review (cost + quality)

---

## 8. Optimization Levers (priority order)

1. **Move R1 to local/cheap** — biggest savings
2. **Cache repeated prompts** — 20-40% savings typical
3. **Reduce prompt size** — 10-30% savings
4. **Batch R1** — 15% savings
5. **Negotiate volume** — for sustained high usage

---

## 9. What We Don't Do

- ❌ Auto-upgrade to premium without logging
- ❌ Skip eval suite to "save time"
- ❌ Disable budget alerts to "ship faster"
- ❌ Use client data for training to "save cost"

---

## 10. Cost Anomaly Detection

- Alert if model cost > 2x weekly average
- Alert if agent cost > 2x weekly average
- Alert if new model added without registry update
- Alert if same prompt called > 100x in 1h (potential loop)

---

> **Owner:** Tech Lead + Founder · **Review:** كل أسبوع
