# V10 Observability Plan (Dealix)

## Goals
- See at a glance: is the system healthy?
- Find issues before the client does
- Recover from incidents within RTO

## Health snapshot (5 min)
- Build: `python3 scripts/generate_health_snapshot.py`
- Output: `reports/health/health-snapshot-YYYY-MM-DD.md`

## Metrics
- accounts in CRM
- drafts pending review
- proof items logged
- last backup time
- audit log size
- daily operator last run

## Alerts
- V1: email to founder
- V2: Slack webhook
- V3: PagerDuty (out of V10 scope)

## Logs
- `reports/audit/audit-YYYY-MM.jsonl` (mutations)
- `reports/sources/source-audit-YYYY-MM-DD.md` (connector runs)
- `reports/ai/evals-YYYY-MM-DD.md` (AI evals)

## Incident levels
- P0: data loss, security breach
- P1: core feature down
- P2: degraded performance
- P3: cosmetic
