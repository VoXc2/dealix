# Go-Live — Master Index

> Entry point for everything related to Dealix's GA launch. Pre-launch / Launch day / Post-launch.
> Last updated: 2026-05-12. Owner: founder.

## Status at a glance

| Workstream | Code/docs ready | External action remaining |
|------------|-----------------|---------------------------|
| **A — Legal & PDPL** | 🟢 templates + breach runbook + retention + sub-processors | 🟡 DPO registration, DPA signature, SDAIA portal account |
| **B — Payments (Moyasar)** | 🟢 reconciliation script + KYC checklist + webhook code | 🟡 KYC submission, `sk_live_` issuance, webhook registration in dashboard |
| **C — Channels (WhatsApp + Gmail)** | 🟢 Meta verification checklist + email deliverability | 🟡 Meta business verification, Gmail OAuth refresh token |
| **D — Infrastructure (DB + Backups)** | 🟢 hourly_backup + restore_test + alembic check + index audit | 🟡 cron schedule on Railway, BACKUP_ENCRYPTION_KEY in 1Password |
| **E — Observability** | 🟢 UptimeRobot + Sentry + PostHog runbooks + on-call rotation | 🟡 account creation + DSN + alert wiring |
| **F — Security** | 🟢 RATE_LIMITS + KEY_ROTATION + CORS_POLICY | 🟡 first rotation execution + 1Password vault setup |
| **G — CI/CD** | 🟢 DLQ check workflow + Railway post-deploy smoke | 🟡 STAGING_REDIS_URL + PRODUCTION_REDIS_URL secrets in GH |
| **H — Marketing** | 🟢 press releases AR/EN + content checklist + sitemap | 🟡 reporter list, partner signatures, scheduled posts |

Code-side: **DONE**. External vendor + legal actions: see per-workstream checklists for owners + dates.

---

## Documents created / updated for GA

### Planning
- `/root/.claude/plans/go-lovely-gem.md` — the source plan
- `docs/ops/GO_LIVE_INDEX.md` — this file

### Workstream A — Legal & PDPL
- `docs/ops/PDPL_BREACH_RUNBOOK.md` 🆕
- `docs/ops/PDPL_RETENTION_POLICY.md` 🆕
- `docs/ops/PDPL_CLOSURE_CHECKLIST_AR.md` (existing)
- `landing/sub-processors.html` 🆕

### Workstream B — Payments
- `docs/ops/MOYASAR_KYC_CHECKLIST.md` 🆕
- `scripts/reconcile_moyasar.py` 🆕
- `docs/ops/MANUAL_PAYMENT_SOP.md` (existing; will be deprecated post-Phase 5 of MOYASAR_KYC_CHECKLIST)
- `docs/ops/WEBHOOK_RETRY_DLQ.md` (existing)

### Workstream C — Channels
- `docs/ops/WHATSAPP_META_VERIFICATION.md` 🆕
- `docs/ops/EMAIL_DELIVERABILITY.md` (existing — already SPF/DKIM/DMARC ready)
- `docs/ops/GMAIL_OAUTH_SETUP_CHECKLIST.md` (existing)

### Workstream D — Infrastructure
- `docs/ops/BACKUP_RESTORE.md` ♻️ (TODO closed — now references hourly_backup.sh)
- `docs/ops/RESTORE_DRILL_LOG.md` 🆕
- `scripts/hourly_backup.sh` 🆕
- `scripts/restore_test.sh` 🆕
- `scripts/check_alembic_heads.sh` 🆕
- `scripts/db_index_audit.py` 🆕
- `docs/ops/ALEMBIC_MIGRATION_POLICY.md` (existing)

### Workstream E — Observability
- `docs/ops/UPTIMEROBOT_SETUP.md` 🆕 (replaces ref to GitHub Issue #85)
- `docs/ops/SENTRY_SETUP.md` 🆕
- `docs/ops/POSTHOG_EVENTS.md` 🆕
- `docs/ops/ON_CALL_ROTATION.md` 🆕
- `docs/ops/UPTIME_AND_ALERTS.md` (existing — superseded by UPTIMEROBOT_SETUP.md)
- `docs/ops/INCIDENT_RUNBOOK.md` (existing)

### Workstream F — Security
- `docs/security/RATE_LIMITS.md` 🆕
- `docs/security/KEY_ROTATION.md` 🆕
- `docs/security/key_rotation_log.md` 🆕
- `docs/security/CORS_POLICY.md` 🆕

### Workstream G — CI/CD
- `.github/workflows/dlq_check.yml` 🆕
- `.github/workflows/railway_deploy.yml` ♻️ (added post-deploy smoke pack + fail-on-healthz)
- `scripts/check_dlq_size.py` 🆕

### Workstream H — Marketing
- `docs/business/PRESS_RELEASE_AR.md` 🆕
- `docs/business/PRESS_RELEASE_EN.md` 🆕
- `docs/business/LAUNCH_MARKETING_CHECKLIST.md` 🆕
- `landing/sitemap.xml` ♻️ (added privacy/terms/sub-processors/launch-readiness)
- `docs/ops/launch_content_queue.md` (existing)
- `docs/ops/agency_partner_kit.md` (existing)

### Cutover + post-launch
- `docs/ops/RELEASE_DAY_RUNBOOK.md` 🆕
- `docs/ops/ROLLBACK_RUNBOOK.md` 🆕
- `docs/ops/POST_LAUNCH_SCORECARD.md` 🆕

Legend: 🆕 new this round, ♻️ modified, otherwise pre-existing.

---

## What still needs human / external action

Items only the founder can complete (sequenced for fastest unblock):

### This week (T-21 → T-14)
1. Submit Moyasar KYC (`docs/ops/MOYASAR_KYC_CHECKLIST.md` Phase 1) → 1-3 business days
2. Submit Meta business verification (`docs/ops/WHATSAPP_META_VERIFICATION.md` Phase 1-2) → 1-7 business days
3. Identify and onboard the DPO (`docs/ops/ON_CALL_ROTATION.md` + `PDPL_BREACH_RUNBOOK.md` contact table)
4. Create 1Password vault `Dealix Production` and seed with all secrets from `docs/security/KEY_ROTATION.md` table

### Next week (T-14 → T-7)
5. UptimeRobot account + 5 monitors (`docs/ops/UPTIMEROBOT_SETUP.md`)
6. Sentry account + 2 projects + alerts (`docs/ops/SENTRY_SETUP.md`)
7. PostHog account + ingest test (`docs/ops/POSTHOG_EVENTS.md`)
8. AWS S3 bucket `dealix-backups-ksa` in `me-south-1` + IAM keys + Railway cron for `scripts/hourly_backup.sh`
9. Add `STAGING_REDIS_URL` + `PRODUCTION_REDIS_URL` to GitHub secrets (for `dlq_check.yml`)

### Closer to launch (T-7 → T-1)
10. Sign 3 agency partners (`docs/ops/agency_partner_kit.md`)
11. Draft & schedule social posts (`docs/business/LAUNCH_MARKETING_CHECKLIST.md`)
12. Pre-brief 10 reporters with embargoed press release
13. Run the quarterly **restore drill** at least once before launch (`scripts/restore_test.sh`)
14. Run **abuse drill**: kill Railway service for 3 minutes → verify UptimeRobot alert (`docs/ops/UPTIMEROBOT_SETUP.md` "Drill — kill-switch test")

### Launch day (T-0)
Follow `docs/ops/RELEASE_DAY_RUNBOOK.md`. Roles + hours + abort criteria + comms all there.

### After launch
- T+1 / T+7 / T+30: fill `docs/ops/POST_LAUNCH_SCORECARD.md`
- On any incident: `docs/ops/ROLLBACK_RUNBOOK.md` then `INCIDENT_RUNBOOK.md` for post-mortem

---

## Single-command verification

When you've ticked all the boxes above, this is the smoke sequence to run before declaring GA:

```bash
# 1. Local smoke pack
bash scripts/revenue_os_master_verify.sh

# 2. Single Alembic head
bash scripts/check_alembic_heads.sh

# 3. DLQ healthy
REDIS_URL=<staging-redis> python scripts/check_dlq_size.py --max 5

# 4. Health endpoints
curl https://api.dealix.me/healthz                            # → {"status":"ok"}
curl https://api.dealix.me/api/v1/pricing/plans | jq '.plans | length'  # → 4

# 5. Real 1 SAR test
curl -X POST https://api.dealix.me/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"plan":"pilot_1sar","email":"sami@dealix.sa"}'
# follow payment_url, verify webhook + DB

# 6. Reconciliation drill
MOYASAR_SECRET_KEY=$LIVE DATABASE_URL=$PROD_DB \
  python scripts/reconcile_moyasar.py --since 1h

# 7. CORS strictness
curl -i -X OPTIONS https://api.dealix.me/api/v1/pricing/plans \
  -H "Origin: https://evil.example.com" -H "Access-Control-Request-Method: GET"
# Expect: no Access-Control-Allow-Origin header

# 8. Webhook bad signature rejection
curl -i -X POST https://api.dealix.me/api/v1/webhooks/moyasar \
  -H "X-Moyasar-Signature: bogus" -d '{}'
# Expect: 401

# 9. Lighthouse + Pa11y on landing
npx @lhci/cli autorun
npx pa11y https://dealix.sa

# 10. Backup drill
bash scripts/hourly_backup.sh  # produces local backup
RESTORE_DATABASE_URL=$SCRATCH bash scripts/restore_test.sh  # restores it
```

All 10 must pass before GA. Record results in `docs/ops/release_logs/pre-ga-smoke.md`.

---

## When in doubt

- Operational question → `docs/ops/`
- Security question → `docs/security/`
- Marketing question → `docs/business/`
- Architecture question → `docs/architecture/`
- "What's blocking launch?" → this file's "What still needs human / external action" section

Maintainer: founder. Reviewed weekly until T+30, monthly thereafter.
