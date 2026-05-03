#!/usr/bin/env bash
# ============================================================
# Dealix — Railway deploy helper
# ============================================================
# Use this AFTER you've created a Railway project and set environment
# variables manually (see docs/RAILWAY_ONE_CLICK.md).
#
# What this script does:
#   1. Confirms `railway` CLI is installed.
#   2. Logs in (interactive prompt — opens browser).
#   3. Triggers a redeploy of the current branch.
#   4. Runs the staging smoke immediately after deploy.
#   5. Optionally seeds demo data.
#
# Usage:
#   chmod +x scripts/deploy_railway.sh
#   ./scripts/deploy_railway.sh                # deploy + smoke
#   ./scripts/deploy_railway.sh --with-seed    # also seed demo data
# ============================================================

set -euo pipefail

# ── Helpers ─────────────────────────────────────────────
err()  { printf "\033[1;31m✗\033[0m %s\n" "$*" >&2; }
ok()   { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
info() { printf "\033[1;34m→\033[0m %s\n" "$*"; }
need() { command -v "$1" >/dev/null 2>&1 || { err "missing $1"; exit 1; }; }

WITH_SEED=false
[[ "${1:-}" == "--with-seed" ]] && WITH_SEED=true

# ── Pre-flight ──────────────────────────────────────────
info "Pre-flight checks"
need git
need python
need curl

if ! command -v railway >/dev/null 2>&1; then
  err "Railway CLI not installed."
  echo "  Install: npm i -g @railway/cli   OR   brew install railway"
  exit 1
fi
ok "railway CLI present"

# ── Confirm we're on the launch branch ──────────────────
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" != "claude/launch-command-center-6P4N0" ]]; then
  err "Current branch is '$BRANCH'. Switch first:"
  echo "  git checkout claude/launch-command-center-6P4N0"
  exit 1
fi
ok "branch: $BRANCH"

# ── Confirm working tree clean ──────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
  err "Working tree dirty. Commit or stash first."
  git status --short
  exit 1
fi
ok "working tree clean"

# ── Local launch checklist ──────────────────────────────
info "Running local launch_checklist.py..."
if ! python scripts/launch_checklist.py >/tmp/dealix_checklist.log 2>&1; then
  err "launch_checklist FAILED. See /tmp/dealix_checklist.log"
  tail -20 /tmp/dealix_checklist.log
  exit 1
fi
ok "launch_checklist: LAUNCH_READY (5/5)"

# ── Login + link ────────────────────────────────────────
info "Logging into Railway (browser may open)..."
railway login || true

info "Linking project (select your Dealix project)..."
railway link

# ── Trigger deploy ──────────────────────────────────────
info "Triggering deploy..."
railway up --detach || true
ok "deploy triggered. Watch progress at:"
echo "  https://railway.app/project/$(railway status --json 2>/dev/null | python -c 'import sys,json; print(json.load(sys.stdin).get("projectId",""))' 2>/dev/null)"

# ── Wait for deploy to settle ───────────────────────────
info "Waiting 90s for deploy to settle..."
sleep 90

# ── Get the public URL ─────────────────────────────────
URL="$(railway variables 2>/dev/null | grep -E 'RAILWAY_PUBLIC_DOMAIN' | head -1 | awk -F= '{print $2}' | tr -d ' ')"
if [[ -z "$URL" ]]; then
  err "Could not detect public URL. Check Railway dashboard manually."
  exit 1
fi
URL="https://$URL"
ok "deployed at: $URL"

# ── Smoke test ──────────────────────────────────────────
info "Running staging smoke against $URL..."
if python scripts/staging_smoke.py --base-url "$URL"; then
  ok "STAGING_SMOKE_PASS"
else
  err "STAGING_SMOKE_FAIL — check Railway logs"
  exit 1
fi

# ── Optional seed ───────────────────────────────────────
if $WITH_SEED; then
  DB_URL="$(railway variables 2>/dev/null | grep -E '^DATABASE_URL=' | head -1 | awk -F= '{$1=""; print substr($0,2)}')"
  if [[ -z "$DB_URL" ]]; then
    err "No DATABASE_URL — skip seed"
  else
    info "Seeding demo data..."
    DATABASE_URL="$DB_URL" python scripts/seed_commercial_demo.py
    ok "demo data seeded"
  fi
fi

# ── Done ────────────────────────────────────────────────
echo ""
echo "═════════════════════════════════════════════"
echo "  DEPLOY COMPLETE"
echo "═════════════════════════════════════════════"
echo "  URL:               $URL"
echo "  Healthz:           $URL/healthz"
echo "  Command Center:    $URL/command-center.html"
echo "  Agency Portal:     $URL/agency-partner.html?partner_id=demo_partner_riyadh"
echo "  Proof Pack:        $URL/proof-pack.html?customer_id=demo_cust_training_co"
echo ""
echo "  Next: open docs/YOUR_TASKS.md → start with task [3]"
echo "═════════════════════════════════════════════"
