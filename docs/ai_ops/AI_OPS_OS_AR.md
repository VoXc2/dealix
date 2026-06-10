# Agent 19 — AI Ops, Model Routing & Cost Governance (AR)

> **Tier:** A2 · Read + Local Write + Suggest
> **Input classes:** T1 (operator), T3 (model provider responses), T4 (eval results)
> **Output classes:** T1 (operator-facing)
> **Side effects:** writes to `./docs/ai_ops/`, `./data/ai_ops/`, `./reports/ai_ops/`
> **Owner:** Founder + Tech Lead

---

## Security Posture
- لا يُمرّر secrets للنماذج
- لا يُشغّل نماذج جديدة بدون تسجيل في registry
- لا يغيّر production model routing بدون founder approval
- كل model call = event في audit
- Eval results تُسجّل لكل change في routing

---

## الهدف

**AI Ops OS** = الطبقة التشغيلية التي تحكم:
- أي نموذج يُستخدم لأي مهمة
- كم يكلف
- هل النتيجة آمنة
- متى يفشل، ما الـ fallback
- كيف نقيس الجودة

**المشكلة التي يحلّها:**
- بدون routing: نماذج قوية لكل شيء = فاتورة ضخمة
- بدون governance: secrets تتسرب، prompt injection ينجح
- بدون eval: لا نعرف متى الجودة تنخفض

---

## الـ Deliverables المُنتجة

```
docs/ai_ops/
├── AI_OPS_OS_AR.md                         (هذا)
├── MODEL_REGISTRY_AR.md
├── TASK_TO_MODEL_ROUTING_AR.md
├── LLM_COST_GOVERNANCE_AR.md
├── LOCAL_VS_CLOUD_MODEL_POLICY_AR.md
├── PROMPT_SAFETY_POLICY_AR.md
├── PII_AND_SECRET_MODEL_POLICY_AR.md
├── MODEL_FALLBACK_POLICY_AR.md
├── OUTPUT_QUALITY_EVALS_AR.md
└── TOKEN_OPTIMIZATION_POLICY_AR.md

schemas/
├── model_registry.schema.json
├── ai_task.schema.json
├── model_usage_event.schema.json
└── ai_eval_result.schema.json

data/ai_ops/
├── model_registry.yaml
├── task_routing.yaml
├── model_usage_events.jsonl
└── eval_results.jsonl

reports/ai_ops/
├── AI_USAGE_REVIEW.md
├── MODEL_COST_REVIEW.md
├── MODEL_QUALITY_REVIEW.md
├── AI_RISK_REVIEW.md
└── AI_OPS_FINAL_REPORT.md
```

---

## Task Routing Tiers (R1–R3)

| Tier | الوصف | Examples | Model class |
|------|-------|----------|-------------|
| **R1 — Low risk** | ملخصات، تنسيق، ترجمة، قوائم | internal doc summary, report formatting | Haiku / local Ollama |
| **R2 — Medium risk** | استراتيجية، مسودات، تحليل | sector strategy, proposal drafts | Sonnet / DeepSeek |
| **R3 — High risk** | قانوني، تسعير، خصوصية، security | enterprise procurement answer, legal-sensitive copy | Sonnet + human review |

---

## Model Decision Matrix (R1 / R2 / R3 × Provider)

| Model | Provider | Cost class | R1 | R2 | R3 |
|-------|----------|-----------|----|----|-----|
| `claude-haiku-4-5` | MiniMax | Low | ✅ | ⛔ | ⛔ |
| `claude-sonnet-4-6` | MiniMax | Med | ✅ | ✅ | ✅ (with review) |
| `gpt-4o-mini` | OpenAI | Low | ✅ | ⛔ | ⛔ |
| `gpt-4o` | OpenAI | High | ⛔ | ✅ | ✅ (with review) |
| `deepseek-chat` | DeepSeek/OpenRouter | Low | ✅ | ✅ (non-sensitive) | ⛔ |
| `llama-3.1-8b-local` | Ollama | Free (compute) | ✅ | ⛔ | ⛔ |

**القاعدة:** أي model call = event يُسجّل + cost يُحسب.

---

## Cost Governance

### Budgets

- **Daily token budget:** 5M tokens (قابل للتعديل)
- **Monthly cost budget:** $X (يُحدد من المؤسس)
- **Alert threshold:** 80% من budget
- **Hard stop:** 100% (إلا بموافقة founder)

### Cost Optimization Tactics

1. **Routing:** R1 → cheap model، R2 → medium، R3 → premium
2. **Caching:** identical prompt within 1h → cached
3. **Truncation:** max context per task class
4. **Batch:** non-urgent = batch
5. **Local first:** internal/private → Ollama

---

## Output Quality Eval Suite

لكل model output، نقيّم:

| Dimension | Score 0–5 | Eval method |
|-----------|-----------|-------------|
| Factuality | ≥ 4 | Cross-check against source |
| Brand voice | ≥ 4 | Style guide match |
| Compliance | ≥ 5 (zero fail) | No forbidden claims |
| Personalization | ≥ 3 | Mentions client specifics |
| Arabic quality | ≥ 4 | Native speaker review sample |
| Commercial safety | ≥ 5 | No overclaim, no pricing leak |
| Schema validity | = 5 | Passes JSON schema |
| Actionability | ≥ 3 | Has next step |
| Evidence mapping | ≥ 4 | Claims linked to source |

**Pass threshold:** كل dimensions ≥ minimum + zero fail في compliance/commercial safety.

---

## Secret / PII Policy

- **Hard blocked patterns:** API key regex, JWT pattern, national ID regex, card number Luhn
- **Soft blocked patterns:** emails, phones (redact unless task requires)
- **Pre-prompt scan:** detect + abort if found
- **Post-prompt scan:** detect + log + alert

---

## Fallback Policy

```
[Primary model] → (fail or budget exceeded) → [Cheaper fallback] → (fail) → [Local model] → (fail) → [Operator alert + manual]
```

كل fallback = audit row + retry counter.

---

## Cross-references

- Security framework: `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`
- AI policy: `docs/governance/AI_USAGE_POLICY.md`
- Token optimizer: `token-optimizer/04-model-routing/`
- Pricing: `docs/30_pricing/`

---

> **Owner:** Founder + Tech Lead · **Review:** كل 30 يوم
