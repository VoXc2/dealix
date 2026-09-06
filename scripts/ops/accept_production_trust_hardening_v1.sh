#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Dealix Production Trust Hardening — source acceptance only.
# No merge, deploy, DNS/DB/secret mutation, outbound, payment, or public publish.

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export PYTHONNOUSERSITE=1
export APP_ENV=test

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
export VOICE_AI_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CANONICAL_REPO="${DEALIX_CANONICAL_REPO:-/opt/dealix/workspace/dealix}"
PY="${DEALIX_PYTHON:-$CANONICAL_REPO/.venv/bin/python}"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
PROOF="${DEALIX_PROOF_DIR:-/tmp/dealix-production-trust-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$PROOF"

exec > >(tee -a "$PROOF/acceptance.log") 2>&1

cd "$ROOT"
ACTUAL_SHA="$(git rev-parse HEAD)"

echo "======================================================================"
echo " DEALIX — PRODUCTION TRUST HARDENING V1"
echo "======================================================================"
echo "ROOT=$ROOT"
echo "ACTUAL_SHA=$ACTUAL_SHA"
echo "EXPECTED_SHA=${EXPECTED_SHA:-UNSET}"
echo "PROOF=$PROOF"
echo "MATERIAL_EFFECTS=false"

if [[ -n "$EXPECTED_SHA" && "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "EXACT_HEAD=FAIL"
  exit 10
fi
echo "EXACT_HEAD=PASS"

if [[ ! -x "$PY" ]]; then
  echo "PYTHON_RUNTIME=FAIL path=$PY"
  exit 11
fi
"$PY" --version

run() {
  local name="$1"
  shift
  echo
  echo "--- RUN $name ---"
  if "$@"; then
    echo "PASS: $name"
  else
    local rc=$?
    echo "FAIL: $name rc=$rc"
    return "$rc"
  fi
}

run "git metadata integrity" \
  "$PY" scripts/ops/git_metadata_permission_guard.py --repo "$CANONICAL_REPO"
run "secret literal scan" \
  "$PY" scripts/ops/verify_secret_literals.py --repo "$ROOT"
run "Railway API watch contract" \
  "$PY" scripts/ops/verify_railway_api_watch_contract.py
run "self-improvement truth quarantine" \
  "$PY" scripts/ops/verify_self_improvement_truth_quarantine.py
run "Voice Front Desk verifier" \
  "$PY" scripts/ops/verify_voice_front_desk_realtime_2_1.py
run "autonomous quarantine" \
  "$PY" scripts/ops/verify_autonomous_quarantine.py
run "launch readiness" \
  "$PY" scripts/verify_dealix_launch_readiness.py
run "enterprise layer readiness" \
  "$PY" scripts/verify_enterprise_layer_readiness.py
run "focused pytest" \
  "$PY" -m pytest -q \
    tests/test_ops_production_trust_hardening.py \
    tests/test_postgres_suppression_backend.py \
    tests/test_controlled_live_outbound_policy.py

# Default state must remain fail-closed.  A durable Postgres proof is a separate
# production-like acceptance and is deliberately not auto-enabled here.
unset DEALIX_SUPPRESSION_BACKEND || true
unset DEALIX_SUPPRESSION_ALLOW_REMOVE || true

echo
echo "--- CONTROLLED LIVE DEFAULT POSTURE ---"
set +e
"$PY" scripts/ops/verify_controlled_live_readiness.py \
  >"$PROOF/controlled-live-default.log" 2>&1
CONTROLLED_RC=$?
set -e
cat "$PROOF/controlled-live-default.log"
if [[ "$CONTROLLED_RC" -eq 0 ]]; then
  echo "CONTROLLED_LIVE_DEFAULT=FAIL reason=unexpected_live_readiness"
  exit 12
fi
if ! grep -q 'CONTROLLED_LIVE_READINESS=NOT_READY' "$PROOF/controlled-live-default.log"; then
  echo "CONTROLLED_LIVE_DEFAULT=FAIL reason=expected_not_ready_marker_missing"
  exit 13
fi
echo "CONTROLLED_LIVE_DEFAULT=PASS_FAIL_CLOSED"

{
  echo "timestamp=$(date --iso-8601=seconds)"
  echo "actual_sha=$ACTUAL_SHA"
  echo "expected_sha=${EXPECTED_SHA:-UNSET}"
  echo "source_acceptance=PASS"
  echo "controlled_live_default=FAIL_CLOSED"
  echo "merge=false"
  echo "deploy=false"
  echo "dns_mutation=false"
  echo "db_mutation=false"
  echo "secret_mutation=false"
  echo "outbound=false"
  echo "payment=false"
  echo "public_publish=false"
} >"$PROOF/receipt.env"

sha256sum "$PROOF/receipt.env"
echo "PRODUCTION_TRUST_HARDENING_SOURCE_ACCEPTANCE=PASS"
echo "NEXT=ISOLATED_POSTGRES_SUPPRESSION_PROOF_THEN_REVIEW"
