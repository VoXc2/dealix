# Deploy Runbook — Railway Production (Step-by-Step)

> **Audience:** founder + on-call contractor.
> **Frequency:** every deploy (not just GA). Print this. Tape it next to your monitor.
> **Time budget:** 15 min happy path. 45 min if rollback is needed.
> **Cross-refs:** `docs/ops/PRODUCTION_ENV_TEMPLATE.md`, `docs/ops/ROLLBACK_RUNBOOK.md`, `docs/ops/INCIDENT_RUNBOOK.md`, `scripts/preflight_check.py`, `scripts/daily_sanity.sh`.

---

## Phase 0 — Pre-Flight (locally, before pushing anything)

Do all of this on your laptop in the branch you intend to deploy:

```bash
git fetch origin main
git rebase origin/main          # absorb anything new
./scripts/daily_sanity.sh       # green required
python scripts/preflight_check.py --dev --json | jq .exit_code  # 0 required
```

Stop if any of the above fails. Do NOT push a failing branch and hope CI catches it — CI is for catching what locals miss, not the other way around.

## Phase 1 — Open PR + CI

```bash
git push origin HEAD:claude/<your-branch>
gh pr create --base main --head claude/<your-branch> --title "..." --body-file PR_BODY.md
```

Then watch CI in the GitHub UI:
- `build` ✓
- `test` ✓
- `Analyze Python` (CodeQL) ✓ — wait the full 2 min

If CodeQL flags anything new, do not merge — fix in a follow-up commit on the same branch.

## Phase 2 — Merge to main

Once all checks green and at least one human reviewer approves (founder is sufficient if solo):

```bash
gh pr merge --squash --delete-branch <PR_NUMBER>
```

Squash merge keeps `main` history clean. Branch auto-deleted.

## Phase 3 — Railway Auto-Deploy Watch

Railway auto-deploys `main` to production. Watch the deploy log in Railway UI:

1. **Build step:** Python install, asset compilation. Usually 90–180s.
2. **Migrate step:** `alembic upgrade head` runs in pre-deploy hook.
   - If this fails, Railway aborts the deploy. Production stays on previous version. Safe.
3. **Health-check step:** Railway hits `/healthz`. If 500 within 5 attempts, deploy rolls back.

**Watch for:**
- Build duration > 5 min → cancel + investigate (dep tree issue?)
- Migration error → check `db/migrations/versions/` chain locally with `alembic heads`
- Health check fail → Railway will auto-rollback; do NOT fight it

## Phase 4 — Post-Deploy Smoke (manual, 3 min)

Run these in order. STOP at first failure and trigger rollback (Phase 6):

```bash
# Set BASE_URL to your production URL
export BASE_URL=https://api.dealix.me

# 1. Liveness
curl -fsS $BASE_URL/healthz | jq .
# Expect: 200 OK with all dependencies green

# 2. Pricing endpoint (public)
curl -fsS $BASE_URL/api/v1/pricing/plans | jq '.plans | length'
# Expect: ≥ 3 plans listed (starter, growth, scale)

# 3. Moyasar webhook signature rejects garbage
curl -sS -X POST $BASE_URL/api/v1/webhooks/moyasar \
  -H 'Content-Type: application/json' \
  -d '{"id":"deploy_smoke","secret_token":"WRONG"}' -o /dev/null -w "%{http_code}\n"
# Expect: 401 or 403

# 4. CORS rejects unlisted origin
curl -sS -X OPTIONS $BASE_URL/api/v1/pricing/plans \
  -H "Origin: https://evil.example.com" \
  -H "Access-Control-Request-Method: GET" \
  -o /dev/null -w "%{http_code}\n"
# Expect: not 200 with ACAO=evil.example.com — i.e., browser would block

# 5. PDPL middleware audit logging (manually check Sentry for 'pdpl_access' events)
curl -fsS $BASE_URL/api/v1/leads/_diag > /dev/null
# Then in Sentry: filter event_type=pdpl_access in last 5 min
```

If all 5 pass: deploy is verified. Update `docs/ops/active_pilots.md` with deploy timestamp.

## Phase 5 — Notification (when deploy is healthy)

Post in `#dealix-launch` Slack (or whatever's your team channel):

```
🚀 Deployed {short_sha} to production
- PR: #{NUMBER}
- Migrations applied: {alembic_head}
- Smoke: ✓ all 5 checks
- Active pilots affected: {N customers, list handles}
```

If any active pilot customer is in onboarding Day 1-3, also send them a WhatsApp:
"Quick heads up — we just pushed an update. If you notice anything weird in the next 10 minutes, ping me."

## Phase 6 — Rollback (when smoke fails)

DO NOT debug in production. Roll back first, debug after.

### Option A: Railway UI (preferred — 30s)

1. Open Railway → Deployments → pick the last green deployment → "Redeploy"
2. Wait for health check green
3. Verify with Phase 4 smoke again

### Option B: Revert commit (if Option A unavailable — 5 min)

```bash
git checkout main
git revert <BAD_COMMIT_SHA>
git push origin main
```

Railway auto-deploys the revert. Watch Phase 3 and Phase 4 again.

### Option C: Database migration rollback (RARE — only if migration corrupted data)

```bash
# CAREFUL: this is destructive if you have writes since the bad migration
alembic downgrade -1
```

**Never do Option C without:**
1. A current backup verified working (see `docs/ops/BACKUP_RESTORE.md`)
2. Notifying every active pilot customer (data may be temporarily inconsistent)
3. CTO + DPO sign-off

## Phase 7 — Post-Rollback Investigation

Within 24 hours of any rollback:

1. Open incident in `docs/ops/incidents/{YYYY-MM-DD}-{slug}.md`
2. Identify root cause (5 whys, not symptoms)
3. Add a test that catches the regression
4. Add a preflight check item if applicable
5. Schedule postmortem call (15 min, no blame)

---

## Deploy Frequency Guidance

| Phase of company | Deploy cadence | Reasoning |
|------------------|----------------|-----------|
| **Pre-customer #1** | Weekly batch | High latency tolerable, low pressure |
| **Customer 1–10** | 2× per week | Customer feedback loop matters |
| **Customer 10+** | Daily | But never Friday after 15:00 |
| **Customer 30+** | Continuous (auto-merge) | But not without a CS person on-call |

## Friday-15:00 Rule

Do not deploy after 15:00 AST on Friday. The Saudi work-week ends Thursday-Friday and you don't want to triage on weekends.

Exception: security hotfix or active customer-affecting bug. In which case: deploy, then carry the phone all weekend.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Build fails on Railway but green locally | Different Python version | Pin in `runtime.txt` |
| Migration step fails with "Multiple head revisions" | Alembic chain broken | Use `alembic merge -m "merge"` (see PR #226) |
| Health check 500 with "Connection refused" | Redis or DB URL wrong | Verify `REDIS_URL` + `DATABASE_URL` env in Railway |
| Health check 500 with "No module named X" | Dep not in requirements.txt | Add + redeploy |
| Smoke step 2 returns 0 plans | `pricing.py` removed plans accidentally | `git revert` immediately |
| Smoke step 3 returns 200 (should be 401/403) | Webhook signature validator regression | `git revert` immediately |
| CORS smoke passes evil.example.com | CORS allowlist regression | `git revert` immediately |

## On-Call Rotation

| Day | Primary | Backup |
|-----|---------|--------|
| Mon-Thu | Founder | (none until customer #5) |
| Fri 09–15 | Founder | (none) |
| Fri 15+, Sat, Sun | (no deploys; emergencies only) | Founder phone |

Update this matrix when first hire (customer #10) onboards.

---

## Verification of This Runbook

This runbook is verified working if:
- A new contractor can follow it without asking the founder a question
- A rollback completes in < 5 minutes from "smoke failed" to "previous version restored"
- The post-incident folder grows by 1 file every rollback (no rollback without retro)
