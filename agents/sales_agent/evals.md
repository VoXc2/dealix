# Sales Agent Evaluation Plan

## Evaluation Assets

- Primary dataset: `evals/business_impact/revenue_workflow_impact_cases.jsonl`
- Secondary dataset: `evals/hallucination/cases.jsonl`

## Gate-Linked Evaluations

| Eval ID | Objective | Gate ID | Pass Rule |
|---|---|---|---|
| EV-AGT-SLS-001 | instruction compliance | G-AGT-SLS-050 | >= 0.95 |
| EV-AGT-SLS-002 | policy-safe behavior | G-AGT-SLS-051 | >= 0.98 |
| EV-AGT-SLS-003 | evidence quality | G-AGT-SLS-052 | >= 0.90 |

## Release Rule

Block promotion when any eval falls below pass rule.
