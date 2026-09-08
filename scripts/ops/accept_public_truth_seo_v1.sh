#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
PY="${DEALIX_AUTOMATION_PYTHON:-python3}"

if [[ -z "$EXPECTED" ]]; then
  echo "DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

ACTUAL="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$ACTUAL"
  echo "DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=BLOCKED_SHA_MISMATCH"
  exit 3
fi

export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_OUTBOUND=0
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
export VOICE_OUTBOUND_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export PYTHONNOUSERSITE=1

cd "$ROOT"

"$PY" -m py_compile scripts/ops/verify_public_truth_seo.py
"$PY" scripts/ops/verify_public_truth_seo.py --repo "$ROOT"
"$PY" -m pytest -q tests/test_public_truth_seo_contract.py

if [[ ! -d apps/web/node_modules ]]; then
  echo "DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=BLOCKED_WEB_DEPENDENCIES_NOT_INSTALLED"
  exit 4
fi

npm --prefix apps/web run verify

if [[ -n "$(git -c safe.directory="$ROOT" -C "$ROOT" status --porcelain)" ]]; then
  echo "DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE"
  exit 5
fi

if [[ "$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD)" != "$EXPECTED" ]]; then
  echo "DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=BLOCKED_HEAD_MOVED"
  exit 6
fi

cat <<EOF
EXACT_SHA=$EXPECTED
PUBLIC_TRUTH_VERIFIER=PASS
FOCUSED_TESTS=PASS
WEB_TYPECHECK=PASS
WEB_BUILD=PASS
PUBLIC_PUBLISH=false
PRODUCTION_DEPLOY=false
DNS_MUTATION=false
DEALIX_PUBLIC_TRUTH_SEO_ACCEPTANCE=PASS_SOURCE_ONLY
EOF
