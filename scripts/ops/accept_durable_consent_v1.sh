#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
PY="${DEALIX_AUTOMATION_PYTHON:-python3}"

if [[ -z "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

ACTUAL="$(git -C "$ROOT" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$ACTUAL"
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_SHA_MISMATCH"
  exit 3
fi

export APP_ENV=test
export PYTHONNOUSERSITE=1
export DEALIX_CONSENT_BACKEND=memory
export DEALIX_SUPPRESSION_BACKEND=memory
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

cd "$ROOT"

"$PY" -m py_compile \
  app/outbound/consent.py \
  db/migrations/versions/20260908_023_consent_events.py

"$PY" -m pytest -q \
  tests/test_postgres_consent_backend.py \
  tests/test_durable_consent_migration_graph.py \
  tests/test_controlled_live_outbound_policy.py \
  tests/test_ops_production_trust_hardening.py \
  tests/test_postgres_suppression_backend.py

"$PY" scripts/ops/verify_secret_literals.py

if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE"
  exit 4
fi

if [[ "$(git -C "$ROOT" rev-parse HEAD)" != "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_HEAD_MOVED"
  exit 5
fi

cat <<EOF
EXACT_SHA=$EXPECTED
SOURCE_COMPILE=PASS
MIGRATION_GRAPH=PASS
FOCUSED_TESTS=PASS
SECRET_LITERAL_VERIFIER=PASS
DURABLE_CONSENT_RUNTIME_BACKEND=NOT_ACTIVATED
PRODUCTION_MIGRATION=NOT_RUN
EXTERNAL_SEND=0
PUBLIC_PUBLISH=0
PAYMENT_EXECUTION=0
PRODUCTION_MUTATION=0
DEALIX_DURABLE_CONSENT_ACCEPTANCE=PASS_SOURCE_ONLY
EOF
