# Quality as Code — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [QUALITY_AS_CODE_AR.md](./QUALITY_AS_CODE_AR.md)

## Context
Dealix promises a Standard. A standard cannot exist if quality is judged
by feel. This file defines the testable quality rules Dealix runs on every
relevant artifact, and the planned folder structure for evaluators and
rubrics. It links the eval discipline in `docs/EVALS_RUNBOOK.md` and
`docs/AI_OBSERVABILITY_AND_EVALS.md` with the KPI surfaces in
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`.

## Principle

> Every quality claim must be a **rule**, **evaluator**, or **rubric** —
> reproducible and visible in CI.

## Core quality rules (testable)

- Every report has an executive summary **and** a next action.
- Every proof pack has inputs **and** outputs.
- Every Company Brain answer has a citation or "insufficient evidence."
- Every outreach draft avoids guaranteed claims.
- Every Arabic output passes tone review.

These rules apply to AI outputs and to human deliverables alike.

## Future structure

```
quality_os/
  rules/        # boolean assertions (e.g., has_exec_summary)
  evaluators/   # scoring functions (e.g., tone_score)
  rubrics/      # human-graded rubrics for offline runs
  fixtures/
```

- `rules/` — fast assertions; failing one blocks delivery.
- `evaluators/` — graded scores feeding QA dashboards.
- `rubrics/` — for nuanced cases reviewed by humans.
- `fixtures/` — pinned examples used in CI.

## Operational flow

```
artifact → rules pass? → evaluators score → rubric (if needed) → owner sign
```

- A rule failure stops delivery.
- An evaluator below threshold raises a Control Tower alert.
- A rubric review is the last gate for client-facing artifacts.

## Anti-patterns

- "Looks good" without a passing rule.
- Numbers cited without a versioned dataset.
- Arabic text translated by template rather than written natively.
- Reports without "next action."

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Artifact | Rule pass/fail | Quality OS | Per artifact |
| Artifact | Evaluator score | Quality OS | Per artifact |
| Sample artifact | Rubric score | Reviewer | Sampling |
| QA telemetry | Control Tower QA tile | Head of Delivery | Continuous |

## Metrics
- Rule Pass Rate — % of artifacts passing all rules first time.
- Median Evaluator Score — by evaluator across last 30 days.
- Rubric Sampling Coverage — % of client-facing artifacts sampled.
- Defect Escape — defects found after delivery per 100 artifacts.

## Related
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval coverage
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI surfaces
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — quality posture
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
