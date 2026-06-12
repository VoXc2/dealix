# Dealix Production Verification Guide

> **Status:** Active (P0)
> **Owner:** Founder Office
> **Entry point:** `make prod-verify`
> **Last PASS:** see `reports/prod/PROD_VERIFY_LATEST.md`

This guide explains what `make prod-verify` does, in what order, why, and what to do when a sub-check fails. It is the canonical reference for the operator running the bundle before a deploy, on a Monday morning, or after a long pause.

## 1. What `make prod-verify` is

`make prod-verify` is a **bundle** of six independent checks. Each sub-check is a Makefile target that can also be run on its own. The bundle is non-skipping: if any sub-check exits non-zero, the bundle exits non-zero.

```text
prod-verify =
    env-check              (scripts/check_env_contract.py)
  + security-smoke         (scripts/security_smoke.py)
  + api-contract-check     (scripts/check_openapi_contract.py)
  + dependency-inventory   (scripts/export_dependency_inventory.py)
  + release-manifest       (scripts/export_release_manifest.py)
  + v5-verify              (scripts/post_redeploy_verify.sh)
```

The order is intentional:

1. **env-check** — if env is broken, nothing else is meaningful.
2. **security-smoke** — secrets and admin exposure must be clean before we trust the contract.
3. **api-contract-check** — if the OpenAPI contract drifted, the dependency inventory will lie.
4. **dependency-inventory** — locks the supply chain view.
5. **release-manifest** — what version is going out the door.
6. **v5-verify** — the 22-point founder verifier that exercises the live API.

The chain is: sanity → safety → surface → supply → shipping → live.

## 2. Output format

On PASS, each sub-check prints one line starting with the target name, then the bundle prints `Dealix production verification bundle completed`. Total runtime: ~30s in CI, ~10s locally.

On FAIL, the failing check prints its name + a short reason + the exit code, and stops. The bundle does not continue after a FAIL — fixing the first failure often resolves the next ones.

## 3. Common failure playbook

### 3.1 `env-check` FAIL

**Signal:** `Missing required key: X` or `Duplicate key: X` or `Public admin key flagged: X`.

**Fix:** open `docs/ops/ENV_CONTRACT.md` → "How to fix common failures" → follow the matching recipe.

**Time to fix:** 1–5 minutes.

### 3.2 `security-smoke` FAIL

**Signal:** one of:
- `Weak APP_SECRET_KEY` — current value is too short or predictable.
- `Public admin key without comment` — `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` is set but not dev-only annotated.
- `Secret-looking value in non-.env file` — a real key leaked into source.

**Fix:**
- Rotate `APP_SECRET_KEY` (any 32+ char random).
- Add the `# dev-only: rotate before staging` comment to the frontend env template.
- If a real secret leaked, follow `docs/SECURITY_RUNBOOK.md` immediately. This is an incident, not a config tweak.

**Time to fix:** 1 minute for the first two. Hours for the third.

### 3.3 `api-contract-check` FAIL

**Signal:** `Path X was removed but client Y depends on it` or `Method Z on path X is no longer exported`.

**Fix:** this means the OpenAPI schema drifted from a previous baseline. Two paths:

- **Intentional change** — re-export the OpenAPI schema (`make openapi-export`), commit the new `docs/architecture/openapi.json`, update the baseline.
- **Unintentional change** — revert the offending route. The contract check is the gate that prevents silent breaking changes.

**Time to fix:** 5–30 minutes depending on whether the change is desired.

### 3.4 `dependency-inventory` FAIL

**Signal:** `New dep X not declared in pyproject.toml` or `Lockfile drift detected`.

**Fix:** add the dep to `pyproject.toml` and re-run `pip-compile`. If the dep is dev-only, put it under `[project.optional-dependencies] dev`.

**Time to fix:** 5 minutes.

### 3.5 `release-manifest` FAIL

**Signal:** `Missing version metadata` or `Manifest path does not exist`.

**Fix:** check that `VERSION` exists at the repo root and matches the git tag. If you are cutting a release, run the release flow described in `docs/ops/CHANGELOG_AND_RELEASE_PROCESS.md`.

**Time to fix:** 1 minute.

### 3.6 `v5-verify` FAIL

**Signal:** the 22-point verifier against a live URL fails. Could be a transient network blip or a real regression.

**Fix:** first, re-run with `BASE_URL=https://api.dealix.me make v5-verify`. If the failure persists, the verifier tells you which gate failed. Map it to the corresponding submodule doc under `docs/transformation/`.

**Time to fix:** 10–60 minutes.

## 4. How to run a single sub-check

```bash
make env-check
make security-smoke
make api-contract-check
make dependency-inventory
make release-manifest
make v5-verify           # requires BASE_URL=
```

Each one prints a single verdict and exits. They are safe to run any time — none of them send anything external and none of them mutate production.

## 5. CI gate

On Railway, `make prod-verify` is the **canonical pre-deploy gate**. If it fails, the deploy is held. The reason: the bundle is small (under a minute) and catching a regression here is 100x cheaper than catching it in front of a customer.

For local development, the recommended cadence is:

```bash
make doctor              # 5-second sanity (env + alembic + security)
make prod-verify         # full bundle, before pushing
```

## 6. Last PASS timestamp

`reports/prod/PROD_VERIFY_LATEST.md` is the canonical "last successful run" record. It is regenerated on every PASS. The Monday morning ritual is:

1. `make prod-verify`
2. If PASS, read `reports/prod/PROD_VERIFY_LATEST.md` to confirm when it last ran in CI.
3. If FAIL, follow §3.

## 7. When to extend

Adding a new sub-check is straightforward:

1. Write the script (dependency-free if possible).
2. Add a Makefile target, e.g. `my-check: $(PYTHON) scripts/my_check.py`.
3. Append `my-check` to the `prod-verify` line in the Makefile.
4. Add a section to this doc explaining the new check + the fix recipe.
5. Wire it into `make doctor` if it is part of the daily ritual.

Do not skip any existing sub-check in the bundle. The order matters.

## 8. Related

- `docs/ops/ENV_CONTRACT.md` — what `env-check` validates
- `docs/SECURITY_RUNBOOK.md` — what to do when secrets leak
- `docs/contributing/DEPLOYMENT.md` — production env minimums
- `docs/ops/CHANGELOG_AND_RELEASE_PROCESS.md` — release flow
