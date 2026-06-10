# Model Fallback Policy (AR)

---

## 1. لماذا Fallback؟

- Model outage
- Budget exceeded
- Eval score drop
- Provider incident
- Region unavailability

---

## 2. Fallback Chains (per Primary)

| Primary | Tier | Fallback 1 | Fallback 2 | Final |
|---------|------|------------|------------|-------|
| sonnet | R2/R3 | haiku | deepseek | ollama-local |
| gpt-4o | R2/R3 | gpt-4o-mini | deepseek | ollama-local |
| haiku | R1 | deepseek | ollama-local | operator |
| deepseek | R1/R2 | haiku | ollama-local | operator |
| ollama-local | R1 | (none — already local) | operator | operator |

---

## 3. Trigger Conditions

| Trigger | Action |
|---------|--------|
| Primary returns error (3 retries) | Switch to Fallback 1 |
| Fallback 1 returns error (3 retries) | Switch to Fallback 2 |
| All fallbacks fail | Operator alert + queue task |
| Budget exceeded | Skip Fallback 1+2 (premium), go to local/operator |
| Provider incident detected | Force-switch to alternate provider |
| Eval score drop > 0.2 | Demote to lower tier, alert |

---

## 4. Retry Policy

- Max 3 retries per model
- Exponential backoff (1s, 2s, 4s)
- Audit row per retry

---

## 5. Circuit Breaker

If a model fails > 10 times in 5 min:
- Open circuit (skip model)
- Auto-close after 10 min
- Alert founder

---

## 6. Operator Alert

When all fallbacks fail:
- Page founder (WhatsApp, email)
- Log full failure context (no secrets)
- Provide "manual override" option
- Post-mortem within 24h

---

## 7. Quality Degradation Handling

If fallback model gives lower quality:
- Mark output as `quality=degraded` in audit
- If R3 task, force human review
- If R1/R2, allow with monitoring

---

## 8. Cost During Fallback

Fallback may be **more expensive** (Sonnet → GPT-4o) or **cheaper** (Sonnet → Haiku).
- Set cost ceiling per task to prevent runaway
- Alert if fallback cost > 2x primary expected

---

## 9. Testing

- Quarterly chaos drill: simulate model outage
- Verify fallback works end-to-end
- Update chains based on learnings

---

## 10. Provider Diversity

Don't put all fallbacks in same provider:
- MiniMax primary → OpenAI/DeepSeek fallback (different providers)
- OpenAI primary → MiniMax/DeepSeek fallback

---

> **Owner:** Tech Lead · **Review:** كل 90 يوم
