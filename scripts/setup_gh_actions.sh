#!/usr/bin/env bash
# scripts/setup_github_secrets.sh
# Sets all GitHub Actions secrets required by Dealix workflows.
# Run LOCALLY after `gh auth login` with admin rights on VoXc2/dealix.
#
# Prompts interactively for each value — no secrets are passed via flags
# (avoids them landing in shell history).

set -euo pipefail
REPO="${REPO:-VoXc2/dealix}"

command -v gh >/dev/null || { echo "gh CLI required: https://cli.github.com"; exit 2; }
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login"; exit 2; }

ask_secret() {
  local name="$1" desc="$2"
  echo
  echo "── ${name} ──"
  echo "  ${desc}"
  read -r -s -p "  value (empty to skip): " val
  echo
  if [[ -n "$val" ]]; then
    echo "$val" | gh secret set "$name" --repo "$REPO" --body -
    echo "  ✓ set"
  else
    echo "  • skipped"
  fi
}

cat <<EOF
This sets/updates the following GitHub secrets on ${REPO}.
Each prompt is hidden; press Enter to skip.

Required for full GA readiness:
  RAILWAY_TOKEN              from https://railway.app/account/tokens
  STAGING_REDIS_URL          redis://: pass@host:6379/0
  PRODUCTION_REDIS_URL       redis://: pass@host:6379/0
  PRODUCTION_DATABASE_URL    read-only DB role (for CI smoke tests)
  CODECOV_TOKEN              optional, from codecov.io
  SENTRY_AUTH_TOKEN          for release tagging in CI
  DSAR_NOTIFY_WEBHOOK        Slack/WhatsApp URL for DSAR intake alerts

EOF

ask_secret RAILWAY_TOKEN          "Railway deploy token (account.tokens page)"
ask_secret STAGING_REDIS_URL      "Redis URL for staging DLQ + rate-limit storage"
ask_secret PRODUCTION_REDIS_URL   "Redis URL for production DLQ check workflow"
ask_secret PRODUCTION_DATABASE_URL "Read-only Postgres role for CI smoke checks"
ask_secret CODECOV_TOKEN          "Codecov token (optional)"
ask_secret SENTRY_AUTH_TOKEN      "Sentry auth token for release tagging"
ask_secret DSAR_NOTIFY_WEBHOOK    "Webhook for DSAR intake alerts (optional)"

echo
echo "Done. Verify with: gh secret list --repo ${REPO}"
