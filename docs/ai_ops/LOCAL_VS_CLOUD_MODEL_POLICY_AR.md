# Local vs Cloud Model Policy (AR)

---

## 1. Decision Matrix

| Use case | Recommended | Reason |
|----------|-------------|--------|
| Internal brainstorming | **Local** | لا يحتاج cloud quality |
| Draft preprocessing | **Local** | cost optimization |
| PII-heavy draft | **Local** (redacted) | data minimization |
| Non-sensitive reasoning | **Cloud cheap** | speed + cost balance |
| Approved generated text | **Cloud cheap** | quality sufficient |
| Strategic synthesis (no secrets) | **Cloud premium** | quality matters |
| Secrets / API keys | **Forbidden** | even local model gets nothing |
| Legal docs with sensitive info | **Forbidden / redacted** | policy gate |
| PII-heavy files | **Redacted first** | then cloud if needed |

---

## 2. Local Setup

- **Ollama** on local hardware
- Models: `llama-3.1-8b` (start), add more as needed
- Use cases: R1, internal, classification, summarization
- **No internet required** → strongest isolation

---

## 3. Cloud Setup

- MiniMax, OpenAI, DeepSeek, OpenRouter
- All require API keys (env vars, never in code)
- Each call = audit row

---

## 4. Hybrid (default in Wave 3)

```
[Input] → [PII/Secret Check] → [Local preferred if available] → [Cloud cheap for quality] → [Cloud premium for R3] → [Output Filter] → [Audit]
```

---

## 5. When to Force Local

- Budget exceeded (cloud paused)
- Cloud outage
- Compliance requirement (data residency)
- Sensitive data with no redaction safe path

---

## 6. When to Force Cloud

- Local model quality insufficient
- Reasoning-heavy R2/R3
- Speed critical
- Eval demands it

---

## 7. Risks

| Risk | Mitigation |
|------|------------|
| Local model leak via output | output filter (forbidden content patterns) |
| Cloud model stores data | provider DPA review + redaction |
| Local model hallucination | eval suite, R1 only |
| Cloud model prompt injection | untrusted data isolation |

---

## 8. Cost Comparison

| Option | Cost/run (typical) | Latency | Privacy |
|--------|--------------------|---------|---------|
| Local (Ollama 8B) | $0 (compute) | < 1s | Highest |
| Cloud cheap (Haiku) | $0.001 | 1–3s | Medium |
| Cloud premium (Sonnet) | $0.01 | 2–5s | Medium |
| Cloud GPT-4o | $0.015 | 2–5s | Medium |

---

## 9. Honesty

- **Local** doesn't mean free — compute, electricity, maintenance
- **Cloud** doesn't mean unsafe — with proper controls
- The choice is **per use case**, not "always local" or "always cloud"

---

> **Owner:** Tech Lead · **Review:** كل 90 يوم
