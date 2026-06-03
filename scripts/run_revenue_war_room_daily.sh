#!/usr/bin/env bash
# Daily Revenue War Room — prints ops snapshot + 30-day tracker reminder
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Dealix Revenue War Room (daily) ==="
echo "Tracker: docs/ops/REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml"
echo "SOP: docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md"
echo ""

if command -v curl >/dev/null 2>&1; then
  BASE="${DEALIX_API_URL:-http://localhost:8000}"
  echo "--- Public services catalog ---"
  curl -sf "${BASE}/api/v1/public/services" | head -c 1200 || echo "(API unreachable)"
  echo ""
  if [[ -n "${DEALIX_ADMIN_API_KEY:-}" ]]; then
    echo "--- Founder ops dashboard ---"
    curl -sf -H "X-Admin-API-Key: ${DEALIX_ADMIN_API_KEY}" \
      "${BASE}/api/v1/ops-autopilot/founder-dashboard" | head -c 2000 || true
    echo ""
    echo "--- Sales pipeline ---"
    curl -sf -H "X-Admin-API-Key: ${DEALIX_ADMIN_API_KEY}" \
      "${BASE}/api/v1/sales/pipeline" | head -c 1200 || true
    echo ""
  else
    echo "(Set DEALIX_ADMIN_API_KEY for founder-dashboard + pipeline)"
  fi
fi

echo ""
echo "UI: /ar/ops/founder · /ar/ops/sales · /ar/ops/evidence · /ar/approvals"
echo "Funnel: /ar/risk-score → /ar/proof-pack → /ar/business-now#strategy"
echo "Done."
