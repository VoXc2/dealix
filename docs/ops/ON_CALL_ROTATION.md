# On-Call Rotation

## Why
Every minute Dealix is down costs trust + revenue. A clear on-call rotation means alerts have a named owner with a phone in their pocket, not a Slack channel that pings into the void.

## Roles

### Primary (P1)
- First to receive alerts (UptimeRobot, Sentry SEV-1, PagerDuty-equivalent).
- Expected to **acknowledge within 15 minutes** during business hours and **30 minutes** off-hours.
- Authorised to: deploy rollback, scale services, declare incident SEV.

### Secondary (P2)
- Backup if P1 doesn't acknowledge within SLA.
- Receives all SEV-1 alerts in parallel as FYI, no acknowledgement required.

### Incident Commander (IC)
- For any SEV-1 / SEV-2 lasting > 30 min, an IC is named.
- Not necessarily the primary — IC coordinates, primary fixes.
- IC is typically founder or CTO.

## Pre-GA (T-21 → GA + 30 days)

Until the team grows beyond a single full-time engineer, rotation is:

| Week | Primary | Secondary |
|------|---------|-----------|
| GA week | Founder | Advisor / contractor |
| W+1 | Founder | Advisor / contractor |
| W+2 | Founder | Advisor / contractor |
| W+3 | Founder | Advisor / contractor |
| W+4 | Founder | Advisor / contractor |

After T+30, a second engineer is hired and a real weekly rotation begins.

## Contact directory

| Role | Name | Phone | Email | WhatsApp | Time zone |
|------|------|-------|-------|----------|-----------|
| Primary (default) | Sami Assiri | _on file_ | sami.assiri11@gmail.com | same as phone | AST |
| Secondary | _to fill_ | — | — | — | — |
| Incident Commander | Sami Assiri | _on file_ | — | — | AST |
| DPO (for breach events) | _to fill_ | — | — | — | — |
| Legal | _to fill_ | — | — | — | — |

**Fill the blanks before GA — empty cells are a launch blocker for SEV-1 readiness.**

## Alert routing

| Alert type | Channel | Owner |
|------------|---------|-------|
| UptimeRobot down | Email + WhatsApp | Primary |
| Sentry SEV-1 (webhook 5xx) | Email + WhatsApp | Primary |
| Sentry SEV-2 (error spike) | Email | Primary |
| Sentry SEV-3 (perf regression) | Email digest | Primary (next business day) |
| Moyasar webhook signature mismatch | Email + WhatsApp | Primary + Founder |
| Backup job failure | Email | Primary (next business day) |
| DLQ depth > 10 | Email | Primary (next business day) |

## Handoff

When primary rotates:
1. **48h before**: announce in #ops channel
2. **At handoff**: outgoing primary walks incoming through any open incidents
3. **Update**: this file's "Primary (default)" row
4. **Update**: UptimeRobot alert contacts + Sentry user permissions

## Compensation
- Off-hours alert acknowledged < SLA: counts as normal duty
- SEV-1 work outside business hours: 1.5× hourly equivalent paid in next cycle (or comp time)
- SEV-1 work on a weekend that lasts > 4h: extra day off

## Drills
- Monthly: 1 simulated SEV-2 (alert sent → ack verified → drill closed)
- Quarterly: 1 simulated SEV-1 (full incident channel + rollback dry run)

Drill outcomes go in `docs/ops/observability_drills.md`.
