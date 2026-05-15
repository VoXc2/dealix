# Governance Agent Evaluation Plan

## Evaluation Assets

- Primary dataset: `evals/hallucination/cases.jsonl`
- Secondary dataset: `evals/hallucination/cases.jsonl`

## Gate-Linked Evaluations

| Eval ID | Objective | Gate ID | Pass Rule |
|---|---|---|---|
| EV-AGT-GOV-001 | instruction compliance | G-AGT-GOV-050 | >= 0.95 |
| EV-AGT-GOV-002 | policy-safe behavior | G-AGT-GOV-051 | >= 0.98 |
| EV-AGT-GOV-003 | evidence quality | G-AGT-GOV-052 | >= 0.90 |

## Release Rule

Block promotion when any eval falls below pass rule.
