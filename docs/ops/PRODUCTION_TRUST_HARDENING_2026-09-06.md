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

Live Railway reconciliation exposed a fifth issue: the canonical API service is
now correctly configured as Dockerfile + `railway.json` + governed pre-deploy,
but provider watch paths were too narrow to cover canonical root packages such
as `api/**`, `app/**`, and `db/**`. Railway documents that when watch paths are
configured, a commit that does not match them is skipped. The source contract in
this branch therefore watches Python runtime changes globally plus the build,
dependency, migration-predeploy, config, template, and prompt authorities.

References:
- https://docs.railway.com/builds/build-configuration
- https://docs.railway.com/config-as-code/reference

## Changes in this branch

### 1. CWD-independent verifiers

Both verifier scripts add the repository root to `sys.path` before importing
Dealix packages. This removes harness dependence without weakening their
fail-closed assertions.

### 2. Bounded Git metadata guard

`scripts/ops/git_metadata_permission_guard.py` audits only the **common** Git
metadata directory, including when invoked from a linked worktree:

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
than authorizes a recipient. Readiness is false unless the canonical table and
`SELECT` / `INSERT` / `DELETE` privileges are proven. Durable suppression cannot
be bulk-cleared by the test helper, and durable removal is blocked unless the
process is explicitly started with `DEALIX_SUPPRESSION_ALLOW_REMOVE=true`.

No environment variable in this branch enables outbound by itself. The
canonical policy gate still requires external-send authority, controlled-live
mode, channel flags, approval, relationship/consent, unsubscribe requirements,
rate limits, and durable suppression.

### 5. Railway API trigger authority

`railway.json` now carries canonical API watch patterns and
`dealix/config/railway_services.json` records the same expected contract. The
patterns include all Python runtime files plus the Dockerfile, Railway config,
dependency manifests, governed pre-deploy script, configs, templates, and
prompts. `scripts/ops/verify_railway_api_watch_contract.py` fails closed on
source drift.

This is source authority only. Provider configuration and actual deployment SHA
must still be verified independently.

## Railway infrastructure-as-code migration deadline

Railway's current documentation marks legacy Config as Code (`railway.json` /
`railway.toml`) as deprecated for existing services with a **hard cutoff on
2026-12-01**. Railway recommends Infrastructure as Code with
`.railway/railway.ts` and exposes:

```text
railway config init
railway config pull
railway config plan
railway config apply
```

Reference:
https://docs.railway.com/config-as-code

Do not perform this migration as an incidental launch change. Before the cutoff,
create a separate exact-state migration packet: pull current provider state,
compare it to Dealix source authority, plan with zero unintended domain/DB/secret
changes, test in a non-production environment, then apply to Production only with
rollback evidence and action-bound approval.

## Public search/index residue

A fresh external search still surfaced historical cached pages such as
`/pricing.html`, `/customer-portal.html`, and other legacy snippets with fixed
prices/demo claims, while the current public authority is quote-only and the
current Next.js source redirects those legacy routes. This is **search-index
residue, not current price authority**.

The live front door must be fixed first. After canonical custom-domain routing
is proven, verify the permanent redirects from the public origin and then use
normal search-engine recrawl/removal workflows for stale URLs. Do not re-add
legacy pages or fixed pricing merely to match cached search snippets.

## Production follow-up — separate material actions

These remain separate action-bound gates:

1. Prove exact-current-main source acceptance on the VPS.
2. Set `DEALIX_SUPPRESSION_BACKEND=postgres` only after the production table and
   privileges are verified and a rollback packet exists.
3. Prove Railway API release parity and Approval Center/Postgres runtime truth.
4. Fix the custom front door only from provider control-plane evidence.
5. Apply a Stage-A GitHub ruleset/branch protection: PR required, block force
   pushes/deletions, audited bypass. Do not require flaky hosted checks until
   their execution plane is trustworthy.
6. Migrate Railway Config as Code to Railway IaC before 2026-12-01 as an isolated
   production-change program, not as hidden launch scope.

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
python scripts/ops/verify_railway_api_watch_contract.py
python scripts/ops/verify_self_improvement_truth_quarantine.py
python scripts/ops/verify_voice_front_desk_realtime_2_1.py
pytest -q \
  tests/test_ops_production_trust_hardening.py \
  tests/test_postgres_suppression_backend.py \
  tests/test_controlled_live_outbound_policy.py
```

On a production-like environment with the Postgres backend configured and the
existing table + privileges reachable, `verify_controlled_live_readiness.py`
should advance past the two suppression durability failures. This does **not**
itself authorize or perform any live customer send.
