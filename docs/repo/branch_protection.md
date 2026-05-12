# Branch protection — required settings

Apply these in GitHub → Settings → Branches for `main` and any release
branches.

## Required reviewers

- At least **1** approving review from CODEOWNERS.
- Stale review dismissal on push.
- Owner approval still required for `api/security/`, `cerbos/`,
  `infra/`, `docs/compliance/`, `docs/legal/` (CODEOWNERS handles this).

## Required status checks

These workflows must pass before merge:

- `ci.yml` — pytest + coverage gate.
- `security_lint.yml` — Semgrep + Bandit (when paths touched).
- `api_lint.yml` — Spectral (when api/* or openapi.json touched).
- `llm_evals.yml` — Promptfoo (when dealix/prompts/* touched).
- `actionlint.yml` — workflow YAML validation.
- `lighthouse_ci.yml` — accessibility / SEO budgets (landing/*).
- `docker-build.yml` — Trivy + SBOM hard-fail on CRITICAL.

## Pushes

- No force-push to `main`.
- No direct commits to `main`; all changes via PR.
- Allow squash merging only (linear history).

## Tags

- Tag `v*.*.*` triggers `sdk.yml` (Fern publish to PyPI + npm) and
  `release.yml` (GitHub Release).
- Only the founder (or release manager) creates tags on `main`.

## Environments

- `production` environment requires reviewer approval (see
  `.github/workflows/promote.yml`).
- Secrets per environment, never repo-wide for prod values.
