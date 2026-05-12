# Restore Drill Log

Quarterly restore drill of the production database. Source: `scripts/restore_test.sh`.

| Date (UTC) | Backup tested | Time-to-restore | Rows verified | Exit | Operator | Notes |
|------------|---------------|-----------------|---------------|------|----------|-------|
| _pending_ | _to fill on first drill_ | — | — | — | — | First drill scheduled within 7 days of GA |

**Drill schedule:** 1st of January, April, July, October.

**Pass criteria:**
- Exit code 0
- `accounts` row count ≥ `EXPECTED_MIN_LEADS` (current baseline: 158, drill floor: 100)
- Total time-to-restore ≤ 60 minutes

**Failure protocol:** SEV-2 incident, page on-call, root-cause in INCIDENT_RUNBOOK.md format within 48h.
