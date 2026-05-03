#!/usr/bin/env bash
# ============================================================
# Dealix — Go Live (full verification of a fresh Railway deploy)
# ============================================================
# Run AFTER the new deployment is up. Performs:
#   1. staging_smoke (13 probes)
#   2. seed_commercial_demo (only if DATABASE_URL is exported)
#   3. Live `dealix today` against the URL
#   4. Final summary with 5 URLs to open in browser
#
# Usage:
#   export DEALIX_BASE_URL=https://web-dealix.up.railway.app
#   export DATABASE_URL=postgresql://...    # from Railway dashboard
#   bash scripts/go_live.sh
#
# Or skip seeding (for read-only verification):
#   DEALIX_BASE_URL=$URL bash scripts/go_live.sh --no-seed
# ============================================================

set -uo pipefail

SKIP_SEED=false
[[ "${1:-}" == "--no-seed" ]] && SKIP_SEED=true

URL="${DEALIX_BASE_URL:-https://web-dealix.up.railway.app}"
echo "═══════════════════════════════════════════════════"
echo "  DEALIX — GO LIVE  →  $URL"
echo "═══════════════════════════════════════════════════"

# ── Step 1: smoke ────────────────────────────────────────
echo ""
echo "[1/4] Running staging_smoke (13 probes)..."
python scripts/staging_smoke.py --base-url "$URL"
SMOKE_RC=$?
if [ $SMOKE_RC -ne 0 ]; then
  echo ""
  echo "✗ Smoke FAILED — investigate Railway logs before continuing."
  exit 1
fi

# ── Step 2: seed (optional) ──────────────────────────────
echo ""
if $SKIP_SEED; then
  echo "[2/4] Skipping seed (--no-seed flag)"
elif [ -z "${DATABASE_URL:-}" ]; then
  echo "[2/4] DATABASE_URL not set — skipping seed."
  echo "    To seed: get DATABASE_URL from Railway dashboard → Variables → DATABASE_URL"
  echo "    Then re-run: DATABASE_URL=... bash scripts/go_live.sh"
else
  echo "[2/4] Seeding 68 demo rows..."
  python scripts/seed_commercial_demo.py
  SEED_RC=$?
  [ $SEED_RC -ne 0 ] && { echo "✗ Seed FAILED"; exit 1; }
fi

# ── Step 3: dealix today against live ────────────────────
echo ""
echo "[3/4] Running 'dealix today' against live URL..."
DEALIX_BASE_URL="$URL" python scripts/dealix_cli.py today

# ── Step 4: final summary ────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo "[4/4] LIVE — open these in browser to verify:"
echo "═══════════════════════════════════════════════════"
echo "  Homepage:         $URL/index.html"
echo "  Command Center:   $URL/command-center.html"
echo "  Operator (chat):  $URL/operator.html"
echo "  Agency Portal:    $URL/agency-partner.html?partner_id=demo_partner_riyadh"
echo "  Proof Pack:       $URL/proof-pack.html?customer_id=demo_cust_training_co"
echo "  Login:            $URL/login.html"
echo ""
echo "  API docs:         $URL/docs"
echo "  Health:           $URL/healthz"
echo "  Founder today:    $URL/api/v1/founder/today"
echo ""
echo "═══════════════════════════════════════════════════"
echo "  REAL_LAUNCH_LIVE  — proceed to docs/YOUR_TASKS.md task [7] (Outreach)"
echo "═══════════════════════════════════════════════════"
