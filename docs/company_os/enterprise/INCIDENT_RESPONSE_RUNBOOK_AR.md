# Incident Response Runbook

## Severity

### SEV1

Production API or Web is down.

Action:
1. Check /healthz and /ar/demo.
2. Check Railway deployment logs.
3. Rollback latest deploy if needed.
4. Record incident.
5. Notify affected clients if client-facing.

### SEV2

Feature broken but core pages work.

Action:
1. Capture route.
2. Open issue.
3. Patch.
4. Run build and smoke tests.

### SEV3

Docs/content/offer issue.

Action:
1. Patch docs.
2. Commit.
3. No production emergency.

## Incident Record

Every incident needs:
- time
- impact
- root cause
- fix
- prevention
