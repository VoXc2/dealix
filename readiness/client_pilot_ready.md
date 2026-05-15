# Client Pilot Ready

Dealix is **Client Pilot Ready** for the Enterprise Control Plane.

## What this means

A single customer can run the governed Revenue-OS flow end to end:
inbound lead → tenant resolved → agent governed → high-risk action
escalated → human approval → value recorded with a source → full run
trace → rollback only with approval.

## Proof

```
bash scripts/verify_enterprise_control_plane.sh
# → ENTERPRISE CONTROL PLANE: PASS
```

10 proof test files, 47 assertions, plus API import + compile + ruff.

## Not yet (tracked in the scorecard)

- Persistence is in-memory/tenant-keyed — Postgres migration is the
  next step before multi-customer production.
- Frontend control surfaces beyond `/agents` and `/approvals`.

To move from Pilot Ready → Enterprise Ready, hold this gate green for
3 live customers with Postgres-backed ledgers and CI enforcement.
