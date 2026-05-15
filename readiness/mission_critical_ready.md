# Mission Critical Ready

**Status: NOT YET REACHED.** This file states the exit criteria.

Mission Critical Ready is the highest tier — the control plane can
carry workloads where a failure has material business consequence.

It requires **Enterprise Ready** (`readiness/enterprise_ready.md`) plus:

| Criterion | Required |
|---|---|
| Full observability: trace + metrics + logs per run/action/tool | yes |
| Incident-response runbook exercised in a live drill | yes |
| Frontend control surfaces (run trace, kill switch, approvals, ROI) | yes |
| Kill-switch + circuit-breaker drill passes under load | yes |
| RTO/RPO targets defined and met for the control ledgers | yes |
| Disaster-recovery restore tested from Postgres backup | yes |

## Principle

At this tier, "the AI works" is necessary but not sufficient. The
system must be observable, recoverable, and humanly controllable under
stress. Reaching this tier is a deliberate, separately-scoped program —
not a side effect of the current hardening branch.
