#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CANONICAL_REPO="${DEALIX_CANONICAL_REPO:-/opt/dealix/workspace/dealix}"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"

if [[ -n "${DEALIX_AUTOMATION_PYTHON:-}" ]]; then
  PY="$DEALIX_AUTOMATION_PYTHON"
elif [[ -x "$CANONICAL_REPO/.venv/bin/python" ]]; then
  PY="$CANONICAL_REPO/.venv/bin/python"
else
  PY="python3"
fi

git_safe() {
  git -c "safe.directory=$ROOT" -C "$ROOT" "$@"
}

if [[ -z "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

ACTUAL="$(git_safe rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$ACTUAL"
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_SHA_MISMATCH"
  exit 3
fi

# Source acceptance must be deterministic and must never inherit live-send or
# material authority from the host. Keep both canonical Dealix flags and the
# policy-gate compatibility flags explicitly fail-closed.
export APP_ENV=test
export PYTHONNOUSERSITE=1
export DEALIX_CONSENT_BACKEND=memory
export DEALIX_SUPPRESSION_BACKEND=memory
unset DEALIX_CONSENT_DEFAULT_TENANT || true

export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only

export EXTERNAL_SEND_ENABLED=false
export EMAIL_SEND_ENABLED=false
export EMAIL_LIVE_SEND=0
export WHATSAPP_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export WHATSAPP_OUTBOUND=0
export SMS_SEND_ENABLED=false
export OUTBOUND_MODE=draft_only
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
export IDENTITY_MUTATION=0
export VOICE_AI_ENABLED=false
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

"$PY" scripts/ops/verify_secret_literals.py --repo "$ROOT"

if [[ -n "$(git_safe status --porcelain)" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE"
  exit 4
fi

if [[ "$(git_safe rev-parse HEAD)" != "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_ACCEPTANCE=BLOCKED_HEAD_MOVED"
  exit 5
fi

cat <<EOF
EXACT_SHA=$EXPECTED
SOURCE_COMPILE=PASS
MIGRATION_GRAPH=PASS
FOCUSED_TESTS=PASS
SECRET_LITERAL_VERIFIER=PASS
GIT_SAFE_DIRECTORY=PROCESS_LOCAL_EXACT_ROOT
DURABLE_CONSENT_RUNTIME_BACKEND=NOT_ACTIVATED
PRODUCTION_MIGRATION=NOT_RUN
EXTERNAL_SEND=0
PUBLIC_PUBLISH=0
PAYMENT_EXECUTION=0
PRODUCTION_MUTATION=0
DEALIX_DURABLE_CONSENT_ACCEPTANCE=PASS_SOURCE_ONLY
EOF
