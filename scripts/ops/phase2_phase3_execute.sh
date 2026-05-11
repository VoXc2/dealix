#!/usr/bin/env bash
set -euo pipefail

# Phase 2 + 3 execution helper:
# - Phase 2: verify Tier-1 no-horizontal-overflow smoke on homepage
# - Phase 3: verify deploy parity + smoke against target base URL
#
# Usage:
#   bash scripts/ops/phase2_phase3_execute.sh \
#     --base-url https://api.dealix.me \
#     --expected-sha 8099b00
#
# Optional:
#   --skip-playwright
#   --full-playwright
#   --skip-readiness-json

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BASE_URL="https://api.dealix.me"
EXPECTED_SHA=""
SKIP_PLAYWRIGHT=0
FULL_PLAYWRIGHT=0
SKIP_READINESS_JSON=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url)
      BASE_URL="${2:?missing value for --base-url}"
      shift 2
      ;;
    --expected-sha)
      EXPECTED_SHA="${2:?missing value for --expected-sha}"
      shift 2
      ;;
    --skip-playwright)
      SKIP_PLAYWRIGHT=1
      shift
      ;;
    --full-playwright)
      FULL_PLAYWRIGHT=1
      shift
      ;;
    --skip-readiness-json)
      SKIP_READINESS_JSON=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

echo "== Phase 2+3 execution =="
echo "BASE_URL=${BASE_URL}"
if [[ -n "${EXPECTED_SHA}" ]]; then
  echo "EXPECTED_SHA=${EXPECTED_SHA}"
fi

SERVER_PID=""
cleanup() {
  if [[ -n "${SERVER_PID}" ]]; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

if [[ "${SKIP_PLAYWRIGHT}" -eq 0 ]]; then
  echo "== Phase 2: Playwright overflow smoke =="
  pushd "${REPO_ROOT}/tests/playwright" >/dev/null

  # Keep install explicit and deterministic for environments where
  # playwright deps are not pre-installed.
  if [[ ! -d node_modules ]]; then
    npm install
  fi

  python3 -m http.server 8765 --directory "${REPO_ROOT}/landing" >/tmp/dealix_phase2_http.log 2>&1 &
  SERVER_PID="$!"
  sleep 2

  PLAYWRIGHT_BASE_URL="http://localhost:8765" \
    npx playwright test tier1_smoke.spec.js \
      --config playwright.config.js \
      --project=tablet-768 \
      --project=desktop-1280 \
      --grep "no horizontal scroll"

  if [[ "${FULL_PLAYWRIGHT}" -eq 1 ]]; then
    PLAYWRIGHT_BASE_URL="http://localhost:8765" \
      npx playwright test --config playwright.config.js
  fi

  popd >/dev/null
  cleanup
  SERVER_PID=""
else
  echo "== Phase 2 skipped (--skip-playwright) =="
fi

echo "== Phase 3: deploy parity + smoke =="
READINESS_CMD=(
  python3 "${REPO_ROOT}/scripts/launch_readiness_check.py"
  --base-url "${BASE_URL}"
)
if [[ -n "${EXPECTED_SHA}" ]]; then
  READINESS_CMD+=(--expect-git-sha "${EXPECTED_SHA}")
fi
if [[ "${SKIP_READINESS_JSON}" -eq 1 ]]; then
  READINESS_CMD+=(--skip-readiness-json)
fi
"${READINESS_CMD[@]}"

echo "PHASE2_PHASE3_EXECUTION_OK"
