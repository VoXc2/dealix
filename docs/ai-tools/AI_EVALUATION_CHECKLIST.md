# AI Evaluation Checklist

## Purpose
Make AI outputs measurable, reviewable, and safe before they affect customers or business decisions.

## Evaluation dimensions

| Dimension | Question | Pass criteria |
|---|---|---|
| Accuracy | Is the output factually correct? | No unsupported critical claims |
| Grounding | Is the output based on supplied or cited data? | Evidence is traceable |
| Usefulness | Does it help the user complete the job? | User can take action faster |
| Safety | Does it avoid sensitive exposure or unsafe action? | No policy or data violation |
| Consistency | Does similar input produce stable quality? | Regression cases pass |
| Explainability | Can the user understand why? | Reason is visible |
| Human review | Is ownership clear? | Reviewer is assigned |

## Test set template

| Test ID | Workflow | Input class | Expected behavior | Risk | Result | Notes |
|---|---|---|---|---|---|---|
| AI-001 | TBD | Normal | TBD | Low | Pass/Fail | TBD |
| AI-002 | TBD | Edge case | TBD | Medium | Pass/Fail | TBD |
| AI-003 | TBD | Sensitive | TBD | High | Pass/Fail | TBD |
| AI-004 | TBD | Adversarial | TBD | High | Pass/Fail | TBD |

## Release gate

An AI workflow can ship only when:

- Use case is registered.
- Owner is assigned.
- Data used is documented.
- Human review path is defined.
- Evaluation results are recorded.
- Fallback path exists.
- Incident handling is known.
- Customer-facing claims are backed by evidence.

## Review cadence

- High-risk workflows: before each release.
- Medium-risk workflows: monthly.
- Low-risk workflows: quarterly.

## Incident trigger examples

- Wrong claim used externally.
- Sensitive data appears in output.
- Output creates legal, security, or trust concern.
- Customer challenges explanation.
- Automation runs without approval.
