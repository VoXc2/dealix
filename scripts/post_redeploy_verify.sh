#!/usr/bin/env bash
# Dealix — Post-Redeploy Verifier
#
# One command the founder runs after Railway "Deploy Latest Commit".
# Bundles: running git_sha + staging smoke + 4 unsafe Arabic operator
# probes. Read-only. Never sends money. Never sends a real
# WhatsApp/email/LinkedIn message.
#
# Usage:
#   bash scripts/post_redeploy_verify.sh
#   STAGING_URL=https://api.dealix.me bash scripts/post_redeploy_verify.sh
#
# Exit code:
#   0 → OUTREACH_GO=yes (smoke green AND PR #132 wiring is live)
#   1 → OUTREACH_GO=no  (anything else; specific reason printed)

set -u
B="${STAGING_URL:-https://api.dealix.me}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXPECTED_PREFIX="${EXPECTED_GIT_SHA:-}"

hr() { echo "────────────────────────────────────────────────────────────"; }

echo "Dealix — Post-Redeploy Verifier"
echo "  base: $B"
hr

# 1. Running git_sha
echo "[1/3] /health git_sha"
HEALTH=$(curl -sS -m 15 "$B/health" 2>/dev/null || echo "")
GIT_SHA=$(echo "$HEALTH" | python -c "import json,sys; \
  d=(json.load(sys.stdin) if sys.stdin else {}); \
  print(d.get('git_sha') or 'absent')" 2>/dev/null || echo "absent")
echo "  running git_sha = $GIT_SHA"
if [ "$GIT_SHA" = "absent" ] || [ "$GIT_SHA" = "unknown" ]; then
  echo "  ⚠ /health does not expose git_sha — Railway built before the GIT_SHA build-arg landed."
  echo "    First-time bootstrap: Railway → Deployments → Deploy Latest Commit (NOT Redeploy)."
fi
if [ -n "$EXPECTED_PREFIX" ] && [ "$GIT_SHA" != "$EXPECTED_PREFIX" ] && [ -n "${GIT_SHA##$EXPECTED_PREFIX*}" ]; then
  echo "  ⚠ git_sha mismatch: expected to start with '$EXPECTED_PREFIX', got '$GIT_SHA'"
fi
hr

# 2. Full staging smoke
echo "[2/3] Staging smoke"
STAGING_URL="$B" bash "$SCRIPT_DIR/staging_smoke.sh"
SMOKE_RC=$?
hr

# 3. Verdict
echo "[3/3] Verdict"
if [ "$SMOKE_RC" = "0" ] && [ "$GIT_SHA" != "absent" ] && [ "$GIT_SHA" != "unknown" ]; then
  echo "  OUTREACH_GO=yes"
  echo "  DEALIX_FINAL_VERDICT=FIRST_CUSTOMER_READY_REALISTIC"
  echo "  Next: docs/FIRST_CUSTOMER_EXECUTION_PACK.md"
  exit 0
elif [ "$SMOKE_RC" = "0" ]; then
  echo "  OUTREACH_GO=yes (smoke green)"
  echo "  ⚠ git_sha is '$GIT_SHA' — verify the running commit matches the deploy branch HEAD before sending the first DMs."
  exit 0
else
  echo "  OUTREACH_GO=no"
  echo "  Reason: staging smoke failed. See output above for the specific failed check."
  echo "  If the failure mentions 'PR #132 wiring fields' or 'production has not redeployed':"
  echo "    Railway is serving a stale image — use 'Deploy Latest Commit', not 'Redeploy'."
  exit 1
fi
