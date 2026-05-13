# AI Control Tower — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_CONTROL_TOWER_AR.md](./AI_CONTROL_TOWER_AR.md)

## Context
The AI Control Tower is the operational dashboard that lets Dealix run an
AI workforce safely. It surfaces every run, cost, eval, prompt version,
governance flag, approval status, error, and client-facing output across
the agent fleet. It connects to the telemetry described in
`docs/AI_OBSERVABILITY_AND_EVALS.md` and the environments in
`docs/OBSERVABILITY_ENV.md`, and projects business KPIs from
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`.

## What is monitored

- AI runs — count, success/failure, latency.
- Cost — by agent, model, engagement, tier.
- Prompt versions — current pinned versions and recent diffs.
- Eval scores — by suite, with thresholds and trends.
- Governance flags — blocks, redactions, escalations.
- Approval status — pending, approved, expired.
- Error rates — by agent and root cause class.
- Client-facing outputs — proof of delivery, with provenance.

## Alerts

- Cost over budget per engagement / per model / per day.
- QA below threshold on any agent.
- Governance block spikes on a single rule family.
- PII detected in an unexpected destination.
- Source missing on a Knowledge Agent answer slated for external use.
- Hallucination risk score above threshold.
- Approval overdue beyond SLA.

## UI layout

```
Runs   |  Costs   |  Evals    |  Prompts
Risks  |  Approvals  |  Incidents
```

Each tile shows current value, 7-day sparkline, threshold, owner.

## Operating cadence

- Hourly: alert sweep.
- Daily: cost vs budget and QA trend review.
- Weekly: prompt and eval changes review.
- Monthly: governance and approval audit.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent telemetry | Live dashboard | Head of AI | Continuous |
| Eval suite results | Eval tile + alerts | Head of AI | Continuous |
| Governance verdicts | Risk tile | Head of Compliance | Continuous |
| Approval queue | Approvals tile | Owners | Continuous |

## Metrics
- Time-to-Detect — minutes from anomaly start to first alert.
- Cost Adherence — % of engagements within budget.
- QA Recovery Time — hours to return failing suite to threshold.
- Approval SLA — % of approvals within target.

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability foundation
- `docs/OBSERVABILITY_ENV.md` — environment posture
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — business KPIs surfaced
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating posture
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
