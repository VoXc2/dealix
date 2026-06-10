# Task-to-Model Routing — Dealix (AR)

> يُكمل `MODEL_REGISTRY_AR.md` بمنطق الاختيار الديناميكي.

---

## Routing Logic

```python
def select_model(task: AITask) -> ModelDecision:
    # 1. Classify task
    tier = classify_tier(task)  # R1, R2, R3
    
    # 2. Check task flags
    if task.contains_secrets_d5 or task.requires_pii_d4:
        return local_or_redact_path(task)
    
    # 3. Filter by tier
    candidates = registry.filter(allowed_tasks=tier)
    
    # 4. Filter by PII policy
    candidates = [m for m in candidates if m.pii_policy matches task.pii_class]
    
    # 5. Apply cost preference
    if task.cost_sensitive:
        candidates.sort(by=cost_class)
    
    # 6. Pick primary
    primary = candidates[0]
    
    # 7. Set fallback
    fallback = primary.fallback_model_id
    
    return ModelDecision(primary=primary, fallback=fallback, reason="...")
```

---

## Task Classification Rules

| Task type | Tier | Default model |
|-----------|------|---------------|
| Internal doc summary | R1 | haiku / local |
| Report formatting | R1 | haiku |
| Translation (approved copy) | R1 | haiku / deepseek |
| Checklist generation | R1 | haiku / local |
| Sector strategy | R2 | sonnet / gpt-4o |
| Proposal draft | R2 | sonnet |
| Objection handling | R2 | sonnet |
| Commercial reasoning | R2 | sonnet / gpt-4o |
| Legal-sensitive copy | R3 | sonnet + human review |
| Pricing-sensitive proposal | R3 | sonnet + human review |
| Enterprise procurement answer | R3 | sonnet + human review |
| Privacy-sensitive decision | R3 | sonnet + human review |
| Security review | R3 | sonnet + human review |
| Client-facing commitment | R3 | sonnet + human review |

---

## Cost-Sensitive vs Quality-Sensitive

- **Cost-sensitive:** R1, internal use, exploration → prefer haiku/local
- **Quality-sensitive:** R2, R3, client-facing → prefer sonnet/gpt-4o

**Override:** founder can force `quality_bias=true` for any task.

---

## Local vs Cloud Decision

| Condition | Decision |
|-----------|----------|
| Task = internal brainstorming | Local |
| Task = PII-heavy (D4) | Local (redacted) |
| Task = public content | Cloud (cheap) |
| Task = reasoning-heavy | Cloud (sonnet) |
| Cloud unavailable | Local fallback |
| Budget exceeded | Local only + alert |

---

## Fallback Chain (default)

```
sonnet → haiku → deepseek → ollama-local
gpt-4o → gpt-4o-mini → ollama-local
```

كل fallback = audit row.

---

## Eval Integration

- أي model جديد يجب أن يجتاز eval suite (≥ 0.7) قبل R2
- ≥ 0.8 قبل R3
- Continuous monitoring: نموذج يتدنى score → demoted

---

## Cross-ref

- `data/ai_ops/task_routing.yaml` — concrete routing config
- `docs/ai_ops/MODEL_REGISTRY_AR.md`
- `docs/ai_ops/MODEL_FALLBACK_POLICY_AR.md`

---

> **Owner:** Tech Lead
