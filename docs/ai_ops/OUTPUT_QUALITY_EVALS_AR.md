# Output Quality Evaluations (AR)

---

## 1. لماذا Eval؟

- نماذج تتغير (provider updates)
- Tasks تتطور
- بدون eval = انحراف تدريجي بدون detection
- eval suite = safety net

---

## 2. Eval Dimensions (9)

لكل output، نقيّم:

| Dimension | 0–5 | Pass threshold | Method |
|-----------|-----|----------------|--------|
| **Factuality** | 0–5 | ≥ 4 | cross-check against source |
| **Brand voice** | 0–5 | ≥ 4 | style guide match |
| **Compliance** | 0–5 | = 5 (zero fail) | forbidden claims scan |
| **Personalization** | 0–5 | ≥ 3 | mentions client specifics |
| **Arabic quality** | 0–5 | ≥ 4 | native speaker review sample |
| **Commercial safety** | 0–5 | = 5 | no overclaim, no pricing leak |
| **Schema validity** | 0–5 | = 5 | passes JSON schema |
| **Actionability** | 0–5 | ≥ 3 | has next step |
| **Evidence mapping** | 0–5 | ≥ 4 | claims linked to source |

**Overall pass:** كل dimensions ≥ minimum + **zero fail** in compliance + commercial safety.

---

## 3. Eval Methods

| Method | Description | Use |
|--------|-------------|-----|
| **Auto (rule)** | regex, schema, keyword | compliance, schema, commercial |
| **Auto (LLM-as-judge)** | second model rates output | factuality, brand voice |
| **Human spot-check** | sample review | Arabic quality, all dims |
| **User feedback** | thumbs up/down | ongoing learning |
| **Red team** | adversarial prompts | safety |

---

## 4. Eval Cadence

| Eval type | Cadence | Sample size |
|-----------|---------|-------------|
| Per-call compliance scan | 100% | كل output |
| Per-call schema | 100% | كل output |
| Per-call commercial | 100% | كل output |
| Daily LLM-as-judge | 5% sample | random |
| Weekly human spot-check | 10 outputs | per agent |
| Monthly deep review | 50 outputs | per agent |
| Quarterly red team | full suite | every agent |

---

## 5. Eval Suite (stored)

- `data/ai_ops/eval_results.jsonl` — per-output results
- Test prompts in `data/ai_ops/eval_prompts/`
- Red team payloads: separate folder, restricted access

---

## 6. Score Aggregation

Per agent per week:
- Average score per dimension
- Trend (improving/declining)
- Top failure modes
- Action items

→ `reports/ai_ops/MODEL_QUALITY_REVIEW.md` (weekly)

---

## 7. Regression Detection

- Compare this week vs last week
- If any dimension drops > 0.5: alert
- If overall pass rate drops > 10%: pause + review

---

## 8. Model Demotion / Promotion

| Condition | Action |
|-----------|--------|
| New model eval ≥ 0.8 | eligible for R2/R3 |
| Existing model drops < 0.6 overall | demote to lower tier |
| Eval < 0.4 | pause + council review |

---

## 9. Continuous Improvement

- New failure modes → new test prompts
- Updated brand voice → eval criteria update
- New compliance rules → eval integration

---

## 10. Eval Output Schema

راجع `schemas/ai_eval_result.schema.json`.

```json
{
  "eval_id": "...",
  "ts": "...",
  "agent_id": 19,
  "task_id": "...",
  "model_id": "...",
  "output_text_hash": "...",
  "scores": {
    "factuality": 4,
    "brand_voice": 5,
    "compliance": 5,
    "personalization": 4,
    "arabic_quality": 4,
    "commercial_safety": 5,
    "schema_validity": 5,
    "actionability": 4,
    "evidence_mapping": 4
  },
  "overall_pass": true,
  "failure_modes": [],
  "reviewer": "auto|human"
}
```

---

> **Owner:** Tech Lead · **Review:** weekly
