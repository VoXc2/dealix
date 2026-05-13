# Human-in-the-Loop Matrix — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [HUMAN_IN_THE_LOOP_MATRIX_AR.md](./HUMAN_IN_THE_LOOP_MATRIX_AR.md)

## Context
The Human-in-the-Loop (HITL) matrix is the single source of truth for what
AI may do, where a human must approve, and what is forbidden outright. It
collapses dozens of ad-hoc rules into a readable matrix and is referenced
by every agent card. It implements the autonomy posture declared in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and the incident discipline in
`docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.

## Matrix

| AI Action | Risk | Human Role | Approval Required |
|---|---|---|---|
| classify data | Low | reviewer spot-checks | No |
| score leads | Medium | delivery owner reviews top accounts | Yes before delivery |
| draft email | Medium | human approves before use | Yes |
| answer from KB | Medium | source check required | For external use |
| update CRM stage | Medium | owner approval | Yes |
| send message | High | explicit approval + consent | Yes |
| publish claim | High | claim QA | Yes |
| autonomous external action | Critical | not allowed | Blocked |

## MVP posture

- Read / classify / draft / recommend — broadly allowed with QA.
- Execute external — blocked or approval-only.
- Autonomous external — not allowed.

## Decision flow

```
candidate action
   │
   ▼
classify by AI Action
   │
   ▼
look up row in matrix
   │
   ├── Low → run + log
   ├── Medium → run + reviewer
   ├── High → require explicit approval
   └── Critical → block
```

## Edge cases

- **Composite actions** — broken down to leaves before evaluating; the
  highest risk wins.
- **Time-bound approvals** — approvals expire after the engagement window.
- **Emergency override** — only the operating owner can override and the
  override is itself logged and reviewed.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Action class | Allow / Approve / Block | Compliance Guard Agent | Per action |
| Reviewer feedback | Matrix tuning | Head of Compliance | Quarterly |
| Incident learnings | Matrix update | Head of Compliance | After each incident |

## Metrics
- Matrix Coverage — % of actions classifiable by the matrix without override.
- Approval Throughput — median time-to-approval for High actions.
- Override Count — overrides per quarter (target near zero).
- Block Repetition — repeat blocks for the same root cause.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — autonomy posture
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — incident protocol
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic frame
- `docs/product/GOVERNANCE_AS_CODE.md` — executable rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
