#!/usr/bin/env bash
# scripts/generate_production_env.sh
# Generates a Railway-compatible production env block with fresh secrets in
# place of placeholders. Run LOCALLY, paste the output into Railway → Variables
# → Raw Editor. Store the same values in 1Password vault "Dealix Production".
#
# This script does NOT call any API and does NOT push anywhere. It's a
# generator + checklist combined.
#
# Usage:
#   bash scripts/generate_production_env.sh > dealix.prod.env
#   # Review, paste into Railway, then `shred dealix.prod.env` (don't commit!)

set -euo pipefail

gen() { python -c "import secrets; print(secrets.token_hex(32))"; }

APP_SECRET=$(gen)
JWT_SECRET=$(gen)
API_KEY_TENANT=$(gen)
API_KEY_ADMIN=$(gen)
MOYASAR_WEBHOOK=$(gen)
BACKUP_ENC=$(gen)
WHATSAPP_VERIFY_TOKEN=$(gen)

cat <<EOF
# ─────────────────────────────────────────────────────────────────
# Dealix — Production env block
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# REPLACE every <fill-from-…> placeholder with the real value, then
# paste this into Railway → Variables → Raw Editor.
# After pasting, save these values in 1Password vault "Dealix Production".
# ─────────────────────────────────────────────────────────────────

# ── App identity ──
ENVIRONMENT=production
APP_ENV=production
LOG_LEVEL=INFO
APP_URL=https://dealix.sa
APP_SECRET_KEY=${APP_SECRET}
JWT_SECRET_KEY=${JWT_SECRET}

# ── API auth ──
API_KEYS=${API_KEY_TENANT}
ADMIN_API_KEYS=${API_KEY_ADMIN}
# (Generate one extra per enterprise tenant when needed; add comma-separated.)

# ── CORS (strict, no wildcard) ──
CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa,https://dashboard.dealix.me

# ── Database (already exists in your Railway env — keep as-is) ──
# DATABASE_URL=<keep current value>

# ── Redis (DLQ + rate-limit) ──
REDIS_URL=<fill-from-Railway-Redis-addon-or-Upstash>
RL_STORAGE_URI=\${REDIS_URL}

# ── Moyasar ──
MOYASAR_MODE=production
MOYASAR_SECRET_KEY=<fill-with-sk_live_xxxxx-from-Moyasar-dashboard>
MOYASAR_WEBHOOK_SECRET=${MOYASAR_WEBHOOK}
# ☝️ Copy the same value into Moyasar dashboard → Webhooks → Secret.

# ── Sentry ──
SENTRY_DSN=<fill-from-Sentry-project-dealix-backend>
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.05

# ── PostHog ──
POSTHOG_API_KEY=<fill-with-phc_xxxxx-from-PostHog>
POSTHOG_HOST=https://us.i.posthog.com

# ── Calendly ──
CALENDLY_URL=https://calendly.com/sami-assiri11/dealix-demo
CALENDLY_WEBHOOK_SECRET=<fill-with-secret-from-Calendly-webhook>

# ── WhatsApp (Meta Cloud, after Meta verification completes) ──
# Until WhatsApp_ALLOW_LIVE_SEND=true, the multi-provider fallback chain runs.
WHATSAPP_VERIFY_TOKEN=${WHATSAPP_VERIFY_TOKEN}
WHATSAPP_APP_SECRET=<fill-from-Meta-App-Settings-Basic>
WHATSAPP_ACCESS_TOKEN=<fill-from-Meta-System-User-permanent-token>
WHATSAPP_PHONE_NUMBER_ID=<fill-from-Meta-WhatsApp-API-Setup>
META_APP_SECRET=\${WHATSAPP_APP_SECRET}
WHATSAPP_ALLOW_LIVE_SEND=false

# ── Gmail OAuth ──
GMAIL_CLIENT_ID=<fill-from-Google-Cloud-Console>
GMAIL_CLIENT_SECRET=<fill-from-Google-Cloud-Console>
GMAIL_REFRESH_TOKEN=<fill-via-docs/ops/GMAIL_OAUTH_SETUP_CHECKLIST.md>
GMAIL_SENDER_EMAIL=sami@dealix.sa
DAILY_EMAIL_LIMIT=50
EMAIL_BATCH_SIZE=10
EMAIL_BATCH_INTERVAL_MINUTES=90

# ── AWS S3 backup (run scripts/setup_aws_backup.sh first) ──
BACKUP_S3_BUCKET=dealix-backups-ksa
BACKUP_S3_PREFIX=dealix/hourly
BACKUP_RETENTION_HOURS=48
BACKUP_ENCRYPTION_KEY=${BACKUP_ENC}
AWS_ACCESS_KEY_ID=<fill-from-setup_aws_backup-output>
AWS_SECRET_ACCESS_KEY=<fill-from-setup_aws_backup-output>
AWS_DEFAULT_REGION=me-south-1

# ── Reconciliation alert webhook (optional) ──
RECONCILE_ALERT_WEBHOOK=<fill-with-Slack-or-WhatsApp-webhook-url>

# ─────────────────────────────────────────────────────────────────
# Notes
#  1. After pasting into Railway, click Deploy.
#  2. The app will refuse to boot if APP_SECRET_KEY, JWT_SECRET_KEY,
#     API_KEYS, or ADMIN_API_KEYS are missing/insecure.
#  3. Shred this file: shred -u dealix.prod.env
# ─────────────────────────────────────────────────────────────────
EOF
