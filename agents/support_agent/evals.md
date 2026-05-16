# Support Agent Evaluation Plan

## Evaluation Assets

- Primary dataset: `evals/agent_behavior/agent_behavior_cases.jsonl`
- Secondary dataset: `evals/hallucination/cases.jsonl`

## Gate-Linked Evaluations

| Eval ID | Objective | Gate ID | Pass Rule |
|---|---|---|---|
| EV-AGT-SUP-001 | instruction compliance | G-AGT-SUP-050 | >= 0.95 |
| EV-AGT-SUP-002 | policy-safe behavior | G-AGT-SUP-051 | >= 0.98 |
| EV-AGT-SUP-003 | evidence quality | G-AGT-SUP-052 | >= 0.90 |

## Release Rule

Block promotion when any eval falls below pass rule.
