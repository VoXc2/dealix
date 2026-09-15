---
name: dealix-release-engineer
description: Stabilize Dealix branches, PRs, CI, build, Railway, frontend/backend surfaces, safe defaults, and release reports without direct pushes to main.
---

# Dealix Release Engineer OS

## When to use

Use this skill when the user asks to:

- fix a broken Dealix branch or PR
- stabilize CI, build, typecheck, tests, Docker, Railway, or deployment surfaces
- prepare the repo for merge or commercial launch
- rescue work from a closed or stale PR
- create a clean branch and PR
- stop agents from doing uncontrolled `do everything` changes

## Release doctrine

Dealix should be built with release discipline:

```text
Plan -> small branch -> focused fix -> local validation -> PR -> checks -> merge -> next phase
```

Do not push directly to `main`.
Do not use admin merge.
Do not hide failures.
Do not expand scope while fixing release blockers.
Do not revive `docker-compose.prod.yml`; it is retired non-authoritative history. `deploy/selfhost/compose.yml` is the single self-host deployment authority.

A required acceptance command is fail-closed. Never convert a non-zero test,
typecheck, build, security, truth, or verifier exit code into PASS with `|| true`,
a later unconditional PASS label, or pipeline masking.

## Files to inspect first

```text
package.json
pnpm-lock.yaml
package-lock.json
Makefile
.env.example
.env.production.example
.github/workflows/
Dockerfile
Dockerfile.worker
deploy/selfhost/compose.yml
scripts/ops/verify_selfhosted_production_plane.py
docs/ops/SELFHOSTED_PRODUCTION_PLANE.md
railway.toml
railway.web.toml
railway.company-brain.toml
apps/web/package.json
apps/web/package-lock.json
apps/web/app/
apps/web/lib/
api/
app/
core/
db/
scripts/ops/fail_closed_gate.sh
scripts/verify_railway_surfaces.py
scripts/verify_no_auto_external_send.py
scripts/verify_company_launch_ready.py
reports/go_live/
tests/
```

## Branch rules

1. Check current branch and status first.
2. If user work is dirty, save it before changing anything.
3. Create one focused branch.
4. Keep generated files out of commits unless intentionally part of release evidence.
5. Commit with a clear message.
6. Open a PR with commands run and remaining blockers.

## Required safe environment

```bash
export APP_ENV=test
export ENVIRONMENT=test
export PYTHONIOENCODING=utf-8
export EXTERNAL_SEND_ENABLED=false
export EMAIL_SEND_ENABLED=false
export WHATSAPP_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export SMS_SEND_ENABLED=false
export OUTBOUND_MODE=draft_only
```

## Stabilization checklist

Discovery commands may be non-blocking, but required validation must propagate
its real exit status.

```bash
git status --short
git branch --show-current
git log --oneline -5
gh pr list --limit 20

python -m compileall -q api app core db dealix scripts
scripts/ops/fail_closed_gate.sh PYTHON_TESTS python -m pytest -q
scripts/ops/fail_closed_gate.sh NO_AUTO_EXTERNAL_SEND python scripts/verify_no_auto_external_send.py
scripts/ops/fail_closed_gate.sh COMPANY_LAUNCH_TRUTH python scripts/verify_company_launch_ready.py
scripts/ops/fail_closed_gate.sh RAILWAY_SURFACE_TRUTH python scripts/verify_railway_surfaces.py

npm --prefix apps/web ci
scripts/ops/fail_closed_gate.sh WEB_ACCEPTANCE npm --prefix apps/web run verify

python scripts/ops/verify_selfhosted_production_plane.py
```

If a tool is unavailable, report `SKIPPED_ENVIRONMENT` or `BLOCKED_ENVIRONMENT`
explicitly. Do not report PASS for a command that did not run.

## CI triage policy

Fix in this order:

1. syntax/runtime errors
2. missing dependencies or lock mismatch
3. environment contract errors
4. frontend build/type errors
5. Railway/Docker surface mismatch
6. safety gates
7. tests
8. formatting/lint debt

Do not ignore undefined names, syntax errors, runtime boot failures, or a non-zero
required gate.

## False-green prevention

For shell orchestration, either call `scripts/ops/fail_closed_gate.sh` or capture
and check the real status directly:

```bash
set +e
required_command
rc=$?
set -e
if (( rc != 0 )); then
  echo "REQUIRED_GATE=FAIL rc=$rc" >&2
  exit "$rc"
fi
echo "REQUIRED_GATE=PASS"
```

When a command is piped through `tee`, preserve the producer status with
`PIPESTATUS[0]`. A successful `tee` must never hide a failed producer.

## Required release report

Create or update:

```text
reports/go_live/RELEASE_STABILIZATION_REPORT.md
```

Include branch, scope, changed files, commands run, exact exit codes, checks
passed/failed/skipped, safety status, deploy status, remaining blockers, and
merge recommendation.

## Definition of done

A release PR is ready when:

- scope is small and reviewable
- build/test status is clear and fail-closed
- safe outbound defaults remain intact
- no secrets are committed
- PR body documents commands run and exact outcomes
- remaining blockers are explicit

## Final response format

```text
Dealix Release Status:
- branch:
- PR:
- changed files:
- checks:
- safety defaults:
- blockers:
- merge recommendation:
```
