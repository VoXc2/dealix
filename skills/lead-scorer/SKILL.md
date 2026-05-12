# Lead Scorer

Per-tenant tunable lead scorer combining fit, urgency, intent, and
sector weights. Reads the tenant's `meta_json.scoring_weights` so each
customer can tune without code.

## Output

```yaml
fit_score: 0..1
urgency_score: 0..1
intent_score: 0..1
overall: 0..1
priority: P1 | P2 | P3
recommended_channel: email | whatsapp | phone | meeting
rationale: string
```
