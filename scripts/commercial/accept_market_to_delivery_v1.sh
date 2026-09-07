#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
EXPECTED="${1:-}"

if [[ "$EUID" -eq 0 ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_RUN_AS_REPOSITORY_OWNER_NOT_ROOT'
  exit 2
fi

if [[ ! "$EXPECTED" =~ ^[0-9a-f]{40}$ ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_EXPECTED_SHA_REQUIRED'
  exit 2
fi

ACTUAL="$(git -C "$ROOT" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_HEAD_MISMATCH' "EXPECTED_SHA=$EXPECTED" "ACTUAL_SHA=$ACTUAL"
  exit 2
fi

if [[ -n "$(git -C "$ROOT" status --porcelain --untracked-files=no)" ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_TRACKED_SOURCE_DIRTY'
  exit 2
fi

export PYTHONDONTWRITEBYTECODE=1
PY="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PY" ]] || PY="$(command -v python3)"

printf '%s\n' '=== MARKET-TO-DELIVERY EXACT-HEAD ACCEPTANCE ===' "SOURCE_SHA=$ACTUAL"

"$PY" "$ROOT/scripts/commercial/verify_market_to_delivery_wedge_policy_v1.py"
"$PY" -m unittest discover -s "$ROOT/tests" -p 'test_market_to_delivery_preparation.py' -v
"$PY" -m unittest discover -s "$ROOT/tests" -p 'test_market_to_delivery_http.py' -v
"$PY" -m pytest -q "$ROOT/tests/test_market_to_delivery_intake_bridge.py"
"$PY" "$ROOT/scripts/commercial/generate_market_to_delivery_projection.py" --check
node --check "$ROOT/apps/web/public/market-to-delivery-workspace.js"

WEB_STATUS='NOT_RUN_MISSING_INSTALLED_DEPENDENCIES'
if [[ -f "$ROOT/apps/web/node_modules/next/dist/bin/next" ]]; then
  (
    cd "$ROOT/apps/web"
    npm run typecheck
    npm run build
  )
  WEB_STATUS='PASS'
fi

if [[ "$(git -C "$ROOT" rev-parse HEAD)" != "$EXPECTED" ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_HEAD_MOVED_DURING_ACCEPTANCE'
  exit 2
fi

if [[ -n "$(git -C "$ROOT" status --porcelain --untracked-files=no)" ]]; then
  printf '%s\n' 'MTD_ACCEPTANCE=HOLD_SOURCE_CHANGED_DURING_ACCEPTANCE'
  exit 2
fi

printf '%s\n' \
  'MTD_SOURCE_ACCEPTANCE=PASS' \
  "SOURCE_SHA=$ACTUAL" \
  "NEXT_TYPECHECK_BUILD=$WEB_STATUS" \
  'WEDGE_POLICY=SOURCE_VERIFIED' \
  'ACTIVE_GTM_WEDGES_MAX=3' \
  'SCALE_POLICY=EVIDENCE_GATED' \
  'CANONICAL_SIGNAL_INTAKE=SOURCE_VERIFIED' \
  'RELATIONSHIP_AUTO_CREATE=false' \
  'CONSENT_AUTO_CREATE=false' \
  'OPPORTUNITY_AUTO_CREATE=false' \
  'BROWSER_QA=SEPARATE_PLAYWRIGHT_GATE' \
  'LIVE_EXECUTION=false' \
  'PRODUCTION_READY=UNPROVEN'
