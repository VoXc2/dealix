# التحكم في تكلفة API — Dealix API Cost Control

> **كل API call عالي التكلفة يحتاج budget cap و alert.** هذا الـ doc
> يحدد القواعد والحدود.

**الحالة:** مسودة — Phase 2 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. APIs عالية التكلفة (High-Cost APIs)

| API | التكلفة | ميزانية يومية | ميزانية شهرية |
| --- | --- | --- | --- |
| Anthropic (Claude Opus) | $15/1M output tokens | $5 | $150 |
| Anthropic (Claude Haiku) | $1.25/1M output | $1 | $30 |
| MiniMax (M2) | varies | $2 | $60 |
| OpenAI (GPT-4) | $30/1M output | $3 | $90 |
| Groq | $0.27/1M output | $1 | $30 |
| Firecrawl | $0.50/1000 pages | $1 | $30 |
| Tavily | $0.10/call | $0.50 | $15 |
| Hunter.io | $0.20/lookup | $0.50 | $15 |

## 2. القواعد

1. **Daily cap صارم:** لو LLM spend > $10/day ⇒ alert.
2. **Per-agent cap:** كل agent له HERMES_COST_BUDGET_USD=$5 (default).
3. **Token cap:** أي LLM call > 10K tokens output ⇒ split or summarize.
4. **Cache:** نتائج LLM المتكررة ⇒ cache TTL 1h.
5. **Rate limit:** API calls per minute per service (table below).

| API | Calls/min limit |
| --- | --- |
| Anthropic | 60 |
| MiniMax | 60 |
| OpenAI | 60 |
| Groq | 30 |
| WhatsApp (any provider) | 30 (per channel policy) |
| Moyasar | 100 (webhook read) |

## 3. التخزين (Storage)

`data/procurement/api_costs.jsonl`:

```json
{
  "cost_id": "cost_2026_06_03_001",
  "date": "2026-06-03",
  "vendor_id": "v_anthropic",
  "agent_id": "agent_15",
  "model": "claude-opus-4-8",
  "tokens_in": 1500,
  "tokens_out": 800,
  "cost_usd": 0.014,
  "task_ref": "task_abc",
  "cached": false,
  "timestamp": "2026-06-03T10:00:00+03:00"
}
```

## 4. المراقبة (Monitoring)

- **يومي:** aggregated cost per vendor في `reports/procurement/api_costs_daily.md`.
- **أسبوعي:** cost vs budget variance.
- **شهري:** review + optimization proposals.

## 5. تحسين التكلفة (Optimization)

1. **Caching:** TTL 1h default.
2. **Batching:** group small LLM calls.
3. **Model selection:** Haiku للحاجة البسيطة، Opus للمعقد.
4. **Prompt optimization:** متوسط tokens.
5. **Token limits:** max_tokens=1000 default.
6. **Lazy eval:** لا evaluation إلا عند الحاجة.

## 6. التنبيهات (Alerts)

- Daily LLM spend > $10 ⇒ Slack.
- Per-agent spend > budget ⇒ kill switch + alert.
- API error rate > 5% over 10min ⇒ alert.

## 7. المراجع

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/SLO.md` (Tier 3 cost)
- `docs/V7_COST_CONTROL_POLICY.md`
- `data/procurement/vendors.jsonl`
- `data/procurement/api_costs.jsonl`
- `schemas/api_cost.schema.json` (TBD)
