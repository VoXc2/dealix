# Approval Center Postgres Cutover — Governed Runbook

## Objective

Replace the process-scoped Approval Center singleton with the canonical Postgres
snapshot store without losing pending decisions, creating a second source of
truth, printing credentials, or enabling any external action.

This runbook prepares a material production change. Applying the migration,
changing Railway variables, or restarting production requires its own bounded
authority and exact-head evidence.

## Canonical contract

- Backend selector: `DEALIX_APPROVAL_STORE_BACKEND`.
- Production value after acceptance: `postgres`.
- DSN source: `DEALIX_APPROVAL_DATABASE_URL`, falling back only to the explicit
  `DATABASE_URL` environment variable.
- Table: `approval_center_snapshots`.
- Migration: `20260905_022_approval_center_snapshots`.
- Read-only verifier: `python scripts/verify_approval_center_backend.py --json`.
- Explicit Postgres configuration is fail-closed. It never falls back to memory.

## Pre-cutover gates

1. Exact source SHA accepted on VPS; abort if the branch head moves.
2. Full Approval Center contract tests PASS for memory and Postgres.
3. Alembic reports the single current head
   `20260823_021_collaboration_events` before this migration and the single new
   head `20260905_022_approval_center_snapshots` after migration.
4. A database backup/restore reference exists and is recorded without secrets.
5. External sends, payment execution, public publish, and paid spend remain off.
6. Approval intake is briefly frozen so no process-memory approval can be created
   between snapshot capture and backend activation.

## Read-only preflight

```bash
set -Eeuo pipefail
python -m pytest -q tests/test_approval_center_postgres_cutover.py
alembic heads
alembic current
DEALIX_APPROVAL_STORE_BACKEND=postgres \
  python scripts/verify_approval_center_backend.py --json || true
```

Before migration the verifier must return `HOLD` with
`approval_center_schema_not_migrated`; it must not create the table.

## Governed cutover sequence

1. Freeze creation/decision of approvals; keep all external action gates closed.
2. Capture the exact pre-cutover approval count and IDs from the active process.
3. Export the in-memory approval snapshot to an encrypted, access-controlled
   evidence location when any live records exist. Do not place customer data in
   GitHub comments or CI logs.
4. Apply `alembic upgrade 20260905_022_approval_center_snapshots` under the
   separately authorized database-change window.
5. Confirm `alembic heads` reports exactly
   `20260905_022_approval_center_snapshots` and the table exists.
6. Import the captured snapshot exactly once when it is non-empty; verify record
   count, IDs, statuses, timestamps, and audit history.
7. Set `DEALIX_APPROVAL_STORE_BACKEND=postgres`. Use
   `DEALIX_APPROVAL_DATABASE_URL` only when Approval Center needs an explicit DSN
   override; never paste the value into logs.
8. Restart the canonical API/worker deployment on the accepted SHA.
9. Run the read-only verifier and require `PASS`, `backend=postgres`,
   `schema_ready=true`, `read_only=true`, and `contains_secret=false`.
10. Verify one synthetic internal approval lifecycle in a non-customer namespace:
    create -> read after process restart -> edit -> approve -> audit history.
11. Unfreeze approval intake only after the same record is visible to every API
    and worker instance.

## Rollback law

- Before the first Postgres write, variables and deployment may be returned to
  the pre-cutover state under the same bounded change window.
- After the first Postgres write, **do not switch back to process memory**. That
  would create two approval authorities and can lose pending decisions.
- A post-write rollback must keep Postgres as the source of truth, preserve the
  table, and use a code revision compatible with the Postgres backend. If that is
  impossible, freeze approvals and restore from the captured database backup;
  do not silently resume with an empty in-memory store.

## Evidence receipt

Record only non-secret evidence:

```json
{
  "schema": "dealix.approval-center-cutover-receipt.v1",
  "git_sha": "<accepted-40-char-sha>",
  "migration": "20260905_022_approval_center_snapshots",
  "backend": "postgres",
  "schema_ready": true,
  "restart_persistence": true,
  "multi_instance_visibility": true,
  "pre_count": 0,
  "post_count": 0,
  "external_effects": 0,
  "contains_secret": false,
  "rollback_reference": "<sealed-reference>"
}
```

A quote, invoice, or approval record is not payment evidence. This cutover does
not authorize customer communication, invoice sending, charging, refunds,
contracts, DNS changes, public publishing, or production deployment outside the
bounded cutover action.
