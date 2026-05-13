# Model Router Strategy

Inside `llm_gateway/` there are **no direct calls**. Every AI request passes through a router that converts context into a decision.

## 1. Routing inputs

- Task type
- Risk level
- Data sensitivity
- Cost budget
- Quality requirement
- Language requirement
- Latency requirement

## 2. Routing decisions

- Cheap model
- Balanced model
- Premium model
- Local / private model (when available)
- No-model / rule-based path

## 3. Example record

```json
{
  "task": "draft_outreach",
  "risk_level": "medium",
  "contains_pii": true,
  "language": "ar",
  "required_quality": "high",
  "decision": "premium_model_with_redaction_and_human_review"
}
```

## 4. Why a router, not a direct call

- It removes provider lock-in.
- It makes cost a controllable variable, not a surprise.
- It applies governance posture *before* the model is invoked.
- It is the single chokepoint where evaluations, redactions, and audit are wired in.

## 5. Operating discipline

- A new model is registered with a card describing strengths, limits, cost, residency, and approved use cases.
- Cost guards are enforced — the router does not silently exceed budget.
- Quality regressions are detected via eval hook and surface as decisions, not as ignored errors.
- The router emits an entry in the AI Run Ledger for every call.

## 6. Failure modes

- Code paths that bypass `llm_gateway`.
- Default fallback to a single provider when others are unavailable.
- Quality regressions caught only by users, not by evals.
- Cost budgets that exist as docs, not as enforced limits.

## 7. The principle

> Dealix does not sell model output. Dealix sells *governed outcomes*. The router is what makes that possible.
