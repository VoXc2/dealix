# Incident Response Runbook (Dealix)

## Severity
- P0: data loss, security breach, core feature down
- P1: partial feature down
- P2: degraded performance
- P3: cosmetic

## Response time
- P0: 1 hour
- P1: 4 hours
- P2: 1 business day
- P3: 1 week

## Steps
1. Confirm the incident (logs, reproduction)
2. Assign severity
3. Stop the bleed (rollback, disable feature)
4. Communicate (status page, founder channel)
5. Fix root cause
6. Postmortem within 14 days
7. Update runbooks

## On-call
- Founder (V1)
- Rotating team (V2+)

## Communication
- Internal: founder channel
- External: status page (when hosted)
