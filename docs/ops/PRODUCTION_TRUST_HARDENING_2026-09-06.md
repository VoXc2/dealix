# Dealix Production Trust Hardening — 2026-09-06

North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

This note records source-side hardening only. It grants no authority to deploy,
change DNS/DB/secrets, enable live outbound, activate voice, or mutate `main`
protection.

## Why this patch exists

The latest VPS acceptance exposed three independent problems:

1. Git metadata written by root became unreadable to the canonical `dealix`
   account, breaking `git fsck`/fetch despite an otherwise valid repository.
2. Two verifier entrypoints depended on the caller's CWD/PYTHONPATH and failed
   before they could test product behavior.
3. Controlled-live outbound remained correctly blocked because suppression was
   process-memory only, even though Dealix already owns a canonical PostgreSQL
   `data_suppression_list` model.

A fourth symptom — a broad "possible OpenAI-style key" grep — did not provide a
safe filename-only triage path.

## Changes in this branch

### 1. CWD-independent verifiers

Both verifier scripts add the repository root to `sys.path` before importing
Dealix packages. This removes harness dependence without weakening their
fail-closed assertions.

### 2. Bounded Git metadata guard

`scripts/ops/git_metadata_permission_guard.py` audits only:

- `.git/objects`
- `.git/refs`
- `.git/logs`
- `.git/packed-refs`

It never traverses or mutates worktree files. Read-only mode is the default.
`--repair` requires root and changes only group/mode for root-owned metadata
that the `dealix` group cannot safely use; it does not recursively chown the
repository.

Git's official documentation states that `core.sharedRepository=group` makes
Git metadata group-writable and is the intended mode for repositories shared
between users. Reference:
https://git-scm.com/docs/git-init

### 3. Non-disclosing secret-literal triage

`scripts/ops/verify_secret_literals.py` scans Git-tracked text files for
credential-shaped literals and emits only file path, line number, and detector
name. Secret values are never printed. Detector source code itself is not a
credential-shaped literal.

GitHub secret scanning supports provider-specific and generic patterns and push
protection for many credential types. Reference:
https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns

This local verifier complements — not replaces — repository-side Gitleaks,
CodeQL, detect-secrets, and GitHub secret scanning.

### 4. Optional PostgreSQL suppression authority

`app/outbound/suppression.py` keeps `memory` as the default backend. A
controlled-live environment may explicitly set:

```text
DEALIX_SUPPRESSION_BACKEND=postgres
DATABASE_URL=<existing Dealix PostgreSQL URL>
```

The backend reuses the existing `data_suppression_list` table and existing
`psycopg` dependency. It is fail-closed: database uncertainty suppresses rather
than authorizes a recipient, readiness is false unless the table can be proven,
and the durable backend cannot be bulk-cleared by the test helper.

No environment variable in this branch enables outbound by itself. The
canonical policy gate still requires external-send authority, controlled-live
mode, channel flags, approval, relationship/consent, unsubscribe requirements,
rate limits, and durable suppression.

## Production follow-up — separate material actions

These remain separate action-bound gates:

1. Prove exact-current-main source acceptance on the VPS.
2. Set `DEALIX_SUPPRESSION_BACKEND=postgres` only after the production table is
   verified and a rollback packet exists.
3. Prove Railway API release parity and Approval Center/Postgres runtime truth.
4. Fix the custom front door only from provider control-plane evidence.
5. Apply a Stage-A GitHub ruleset/branch protection: PR required, block force
   pushes/deletions, audited bypass. Do not require flaky hosted checks until
   their execution plane is trustworthy.

GitHub rulesets can require pull requests and block force pushes while exposing
rules to auditors. Reference:
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets

## Future data isolation hardening

Dealix already models tenant ownership in several tables. PostgreSQL Row-Level
Security is a strong later hardening layer for tenant-owned records because,
once enabled, row access must be allowed by policy and the absence of a policy
becomes default-deny. It should be introduced only with explicit role design,
migration tests, and production rollback evidence — not as an ad-hoc launch
mutation.

Reference:
https://www.postgresql.org/docs/current/ddl-rowsecurity.html

## Acceptance target for this branch

```bash
python scripts/ops/verify_secret_literals.py
python scripts/ops/git_metadata_permission_guard.py --repo /opt/dealix/workspace/dealix
python scripts/ops/verify_self_improvement_truth_quarantine.py
python scripts/ops/verify_voice_front_desk_realtime_2_1.py
pytest -q \
  tests/test_ops_production_trust_hardening.py \
  tests/test_postgres_suppression_backend.py \
  tests/test_controlled_live_outbound_policy.py
```

On a production-like environment with the Postgres backend configured and the
existing table reachable, `verify_controlled_live_readiness.py` should advance
past the two suppression durability failures. This does **not** itself authorize
or perform any live customer send.
