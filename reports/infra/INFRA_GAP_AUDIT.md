# Infra Gap Audit — Findings (2026-06-03)

Stack: Hono/tRPC API, React/Vite frontend, Drizzle/MySQL, S3, Kimi OAuth + JWT.

| Area | State | Gap |
|------|-------|-----|
| Environments separation | 🟡 | staging/prod separation not codified |
| Secrets management | 🟡 | prod secret manager not set; `.env` only |
| Deployment approval | 🟡 | no CI deploy pipeline yet (good: nothing auto-deploys) |
| Health endpoint | 🔴 | no `/health` in `api/` |
| DB migrations | 🟡 | drizzle configured; migration review process TBD |
| Backups / recovery | 🔴 | not implemented (policy drafted) |
| SLO/SLA | 🟡 | targets TBD |
| Drift detection | 🟢 | CI checks for docs/schema/workflow/secret drift |
| **Approval endpoint auth** | 🔴 | `governance-router.ts` `approve` is `publicQuery` |

## Highest-priority infra fixes
1. Authenticate the approval/governance mutations.
2. Add `/health` + DB connectivity check.
3. Stand up prod secret manager; never put prod secrets in CI.
4. Implement backups + a restore drill.

**Note:** No production changes were made in this pass (out of scope / unsafe).
