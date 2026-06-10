# Token Optimization Policy (AR)

---

## 1. لماذا Token Optimization؟

- كل token = تكلفة
- Prompts طويلة = وقت + تكلفة
- Tokens غير ضرورية = هدر
- **الهدف:** أقل tokens مع نفس الجودة

---

## 2. Tactics (priority order)

1. **Route cheap tasks to cheap models** (أكبر تأثير)
2. **Cache identical prompts** (20-40% saving)
3. **Compress prompts** (10-30% saving)
4. **Truncate context per task tier** (15-25% saving)
5. **Batch non-urgent tasks** (10-15% saving)
6. **Strip redundant whitespace** (5% saving)
7. **Use structured output** (reduces back-and-forth)

---

## 3. Prompt Compression Patterns

### Before
```
You are a helpful assistant. I would like you to please review the following
content very carefully. The content is as follows: [long content]. Please
provide a comprehensive analysis. Thank you.
```

### After
```
Analyze: [content]. Output: [schema].
```

**Rules:**
- No politeness padding
- No meta-instructions
- Direct task statement
- Structured output spec

---

## 4. Context Window Management

| Task tier | Max context | Truncation strategy |
|-----------|-------------|---------------------|
| R1 | 4K | tail (most recent) |
| R2 | 16K | head + tail |
| R3 | 32K+ | relevance-ranked |

---

## 5. Caching Strategy

- **Cache key:** hash(system + task + input)
- **TTL:** 1 hour for R1, 30 min for R2, no cache for R3
- **Storage:** Redis
- **Invalidation:** on prompt template change

---

## 6. Batch Processing

- **Eligible:** R1, non-urgent
- **Window:** 5 min
- **Max batch:** 20 prompts
- **Trade-off:** latency vs cost

---

## 7. Streaming vs Non-Streaming

- **Stream:** long outputs (R3 with detailed responses)
- **Non-stream:** short outputs (R1)
- **Cost:** similar
- **UX:** stream = better perceived latency

---

## 8. Token Counting

- Use provider's tokenizer (not characters)
- Track in `model_usage_events.jsonl`
- Alert if single call > 100K tokens

---

## 9. Output Token Limits

| Task | Max output tokens |
|------|-------------------|
| Summary | 500 |
| Classification | 50 |
| Draft | 2000 |
| Analysis | 4000 |
| Long report | 8000 |

`max_tokens` parameter enforced.

---

## 10. What We Don't Do

- ❌ Sacrifice quality for tokens
- ❌ Strip context that affects accuracy
- ❌ Cache sensitive content (D4+)
- ❌ Skip eval to "save tokens"

---

> **Owner:** Tech Lead · **Review:** monthly
> **Cross-ref:** `token-optimizer/`
