# Dealix Production Trust Hardening — 2026-09-06

North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

This branch is source-side hardening only. It grants no authority to merge,
deploy, change DNS/DB/secrets, enable live outbound/voice, publish, pay, or alter
`main` protection.

## Live problems this branch closes or makes explicit

1. **Git metadata permissions:** root-run Git operations created loose objects
   and refs unreadable to the canonical `dealix` account.
2. **Verifier harness drift:** self-improvement and Voice verifiers depended on
   caller CWD/PYTHONPATH and could fail before testing product behavior.
3. **Suppression durability:** controlled-live correctly stayed blocked because
   suppression was process-memory only despite an existing canonical
   PostgreSQL `data_suppression_list`.
4. **Secret triage quality:** the prior broad grep could report possible
   OpenAI-style keys without a non-disclosing filename/line proof path.
5. **Railway API trigger drift:** live API is now correctly Dockerfile +
   `railway.json` + governed preDeploy, but provider Watch Paths omitted
   canonical root runtime packages such as `api/**`, `app/**`, and `db/**`.
6. **Consent durability:** current consent evidence is process-memory. Saudi
   PDPL direct-marketing controls require consent/withdrawal evidence that can
   be verified later. Recipient flags remain useful for drafts but are not
   enough to unlock controlled-live.

## Implemented source controls

### CWD-independent verifiers

Both affected verifier entrypoints bootstrap the repository root before Dealix
imports. Their fail-closed assertions are unchanged.

### Bounded common-Git-directory guard

`scripts/ops/git_metadata_permission_guard.py` audits the **common** Git
metadata directory, including linked worktrees, and scopes itself to:

- `.git/objects`
- `.git/refs`
- `.git/logs`
- `.git/packed-refs`

Read-only is the default. `--repair` requires root and changes only group/mode
for root-owned metadata that the Dealix group cannot safely use. It never walks
or recursively chowns worktree files.

Git reference: https://git-scm.com/docs/git-init

### Non-disclosing literal-secret verifier

`scripts/ops/verify_secret_literals.py` scans Git-tracked text and emits only:

```text
path + line + detector
```

It never prints the candidate secret value. This complements existing Gitleaks,
detect-secrets, CodeQL and GitHub secret scanning rather than replacing them.

GitHub reference:
https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns

### Optional PostgreSQL suppression authority

`app/outbound/suppression.py` keeps `memory` as default. Postgres is explicit:

```text
DEALIX_SUPPRESSION_BACKEND=postgres
DATABASE_URL=<existing Dealix PostgreSQL URL>
```

Readiness requires the canonical table plus `SELECT` / `INSERT` / `DELETE`
privileges. Database/query uncertainty fails closed. Durable bulk-clear is
disabled, and durable unsuppression requires:

```text
DEALIX_SUPPRESSION_ALLOW_REMOVE=true
```

That flag does not enable sending; it only gates an authority-sensitive removal
operation.

### Durable consent is now an independent live gate

`app/outbound/consent.py` explicitly reports:

```text
consent_backend_kind=memory
persistent_consent_ready=false
```

The canonical policy gate and `/api/outbound/readiness/*` require **both**:

```text
persistent_suppression_ready() == true
AND
persistent_consent_ready() == true
```

Therefore Postgres suppression alone cannot produce a false-green live posture.
Issue #1533 owns the dedicated durable channel/purpose consent migration.

Engineering control map:
`docs/compliance/PDPL_DIRECT_MARKETING_CONTROL_MAP_2026-09-06.md`

Saudi PDPL portal:
https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL

### Railway API trigger authority

`railway.json` and `dealix/config/railway_services.json` now share one expected
Watch Path contract covering:

- all Python runtime files;
- Dockerfile;
- Railway config;
- dependency manifests;
- governed preDeploy;
- config/templates/prompts.

`scripts/ops/verify_railway_api_watch_contract.py` fails closed on drift.
Provider config and deployed SHA still require independent control-plane proof.

Railway references:
- https://docs.railway.com/deployments/monorepo#watch-paths
- https://docs.railway.com/builds/build-configuration#configure-watch-paths

## Railway IaC deadline

Railway currently marks legacy Config as Code (`railway.json` /
`railway.toml`) deprecated with a **2026-12-01 hard cutoff** for existing
services. Issue #1531 owns an isolated migration to `.railway/railway.ts` using:

```text
railway config init
railway config pull
railway config plan
railway config apply
```

Do not mix that migration into launch execution without exact-state plan,
non-production proof, rollback evidence, and action-bound Production approval.

Reference: https://docs.railway.com/config-as-code

## Public search-index residue

External search still surfaces stale historical URLs/snippets such as
`/pricing.html` and `/customer-portal.html` with legacy fixed-price/demo claims.
Current Next.js source already redirects legacy routes and current commercial
authority is quote-only. Treat this as **search-index residue**, not current
price authority.

First close the canonical front door. Then verify public permanent redirects and
request normal recrawl/removal of stale URLs. Never restore obsolete fixed
pricing merely to match cached search results.

## Hosted CI interpretation

Current GitHub-hosted jobs for this branch again fail before repository steps:
`steps=[]`, `runner_id=0`. That is not source-test evidence. Exact-head VPS
acceptance remains the execution authority until the hosted runner plane
actually executes repository steps reliably.

## Acceptance

Prefer the repo-owned executor:

```bash
DEALIX_EXPECTED_SHA=<exact-pr-head> \
  bash scripts/ops/accept_production_trust_hardening_v1.sh
```

It runs the Git guard, secret scanner, Railway watch verifier, self-improvement
and Voice verifiers, quarantine, launch/enterprise checks, focused outbound/API
regressions, and verifies that default controlled-live remains fail-closed.

Expected source result:

```text
PRODUCTION_TRUST_HARDENING_SOURCE_ACCEPTANCE=PASS
CONTROLLED_LIVE=HOLD_DURABLE_CONSENT
```

The second line is intentional until #1533 is implemented and accepted.

## Separate material gates after source acceptance

1. Merge #1529 — explicit approval must account for possible Railway autodeploy
   because `railway.json` changes are in the PR.
2. Prove/apply Production suppression backend separately.
3. Implement and later migrate durable consent separately (#1533).
4. Prove Railway API exact-release and Approval Center/Postgres parity.
5. Fix the custom front door only from provider control-plane evidence.
6. Apply Stage-A `main` protection separately (#1371).
7. Migrate Railway Config as Code to IaC before 2026-12-01 (#1531).

## Future tenant isolation

PostgreSQL Row-Level Security remains a strong later hardening layer: with RLS
enabled, row access must be allowed by policy and absence of a policy defaults
to deny. Introduce it only with explicit role design, migration tests and
rollback evidence — not as incidental launch scope.

PostgreSQL reference:
https://www.postgresql.org/docs/current/ddl-rowsecurity.html
