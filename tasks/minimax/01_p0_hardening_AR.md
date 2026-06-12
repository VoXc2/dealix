# MiniMax Sub-prompt 01 — P0 Production Hardening

> **Scope:** Fill the two remaining P0 doc gaps and bind the existing P0 toolchain.
> **Do not break:** `scripts/check_env_contract.py`, `scripts/export_openapi.py`, `scripts/check_openapi_contract.py`, `scripts/security_smoke.py`, `make prod-verify`.
> **Branch:** `feature/minimax-factory-p0-hardening`
> **Acceptance:** `make env-check && make security-smoke && make api-contract-check` all exit 0.

---

## 1. Objective

Two P0 doc files are missing from the repo. The implementation (scripts + Makefile targets) already exists. This sub-prompt produces the **narrative docs** that turn scripts into an operator-friendly P0 surface.

---

## 2. Files to Create

### 2.1 `docs/ops/ENV_CONTRACT.md`

Purpose: explain the environment contract, what is enforced, what the failure modes are, and how to fix them.

Required sections:
1. **What this contract is** — one paragraph: a single source of truth for env vars, validated by `scripts/check_env_contract.py`.
2. **What is enforced** — list the 4 rules the script checks (duplicate keys, malformed assignments, public-admin exposure, required backend + frontend keys).
3. **Required keys** — table mapping `ENVIRONMENT`, `LOG_LEVEL`, `APP_SECRET_KEY`, `DATABASE_URL`, `APP_URL`, `ADMIN_API_KEYS`, `CORS_ORIGINS`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` to their role.
4. **What counts as a public-admin key** — explain why `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` is flagged.
5. **How to run locally** — `make env-check`.
6. **How to fix common failures** — 3-5 short recipes (duplicate key, missing required, public admin in `.env`, malformed `KEY=VALUE`).
7. **CI behavior** — what happens on FAIL (PR blocks).
8. **Versioning** — when to update the contract, who owns it (founder office).

### 2.2 `docs/ops/PRODUCTION_VERIFICATION_GUIDE.md`

Purpose: explain `make prod-verify` end-to-end so a new operator can run it and recover on FAIL.

Required sections:
1. **What `make prod-verify` is** — composition of 6 sub-checks: `env-check`, `security-smoke`, `api-contract-check`, `dependency-inventory`, `release-manifest`, `v5-verify`.
2. **Order of execution and why** — env must be sane before contract before security before release manifest.
3. **Output format** — what a PASS looks like (one-line per check + bundle complete banner), what a FAIL looks like (check name + exit code + log hint).
4. **Common failure playbook** — at least these 5:
   - `env-check` FAIL: missing required key.
   - `security-smoke` FAIL: secret in code, public admin exposure, weak `APP_SECRET_KEY`.
   - `api-contract-check` FAIL: removed a path that clients depend on.
   - `dependency-inventory` FAIL: new dep not declared in `pyproject.toml`.
   - `release-manifest` FAIL: missing version metadata.
5. **How to run a single sub-check** — `make env-check`, `make security-smoke`, etc.
6. **CI gate** — this is the canonical pre-deploy gate on Railway.
7. **Last PASS timestamp** — link to `reports/prod/PROD_VERIFY_LATEST.md` (created by the bundle).
8. **When to extend** — adding a new check means: write script, add Makefile target, append to `prod-verify` line in Makefile, add entry to this doc.

### 2.3 `reports/prod/PROD_VERIFY_LATEST.md` (only if missing)

Purpose: machine-written snapshot. If the canonical writer is missing, stub it with: a header, a timestamp, and a table with check name + status + duration. Real writer comes from a follow-up PR.

---

## 3. Constraints

- No code changes to existing scripts. The two files are docs only.
- Use Arabic for section headers, English for command/code examples. Match the existing `docs/ops/*.md` style.
- Do not duplicate the full Makefile — link to it.
- Do not add emojis to docs.
- Keep each doc under 200 lines.

---

## 4. Acceptance

```bash
# 1. New docs render in repo
test -f docs/ops/ENV_CONTRACT.md
test -f docs/ops/PRODUCTION_VERIFICATION_GUIDE.md

# 2. All existing P0 checks still pass
make env-check
make security-smoke
make api-contract-check
```
