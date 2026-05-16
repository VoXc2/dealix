# Risk Engine Specification

## Objective

Score proposed actions and enforce governance routing based on risk tier.

## Risk Inputs

- action type
- data sensitivity
- external side effects
- customer impact potential
- compliance impact
- historical failure pattern

## Risk Levels

| Level | Range | Default Handling |
|---|---:|---|
| low | 0.00–0.39 | auto-execute with audit |
| medium | 0.40–0.69 | execute with enhanced logging |
| high | 0.70–0.89 | human approval required |
| critical | 0.90–1.00 | block or dual-approval policy |

## Mandatory Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-RSK-001 | every governed action gets risk score | T-RSK-001 |
| G-RSK-002 | risk score is deterministic for same input | T-RSK-002 |
| G-RSK-003 | high/critical risk routes to approval/block | T-RSK-003 |
| G-RSK-004 | risk decision is auditable with factors | T-RSK-004 |

## Output Contract

```json
{
  "risk_score": 0.82,
  "risk_level": "high",
  "factors": ["external_side_effect", "sensitive_data"],
  "required_action": "human_approval"
}
```

## Governance Integration

Risk output feeds:
1. policy engine,
2. approval engine,
3. eval report for governance quality metrics.
