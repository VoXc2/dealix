#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
CANONICAL_REPO="${DEALIX_CANONICAL_REPO:-/opt/dealix/workspace/dealix}"

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
  echo "DEALIX_OPERATING_CONSTITUTION_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

ACTUAL="$(git_safe rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$ACTUAL"
  echo "DEALIX_OPERATING_CONSTITUTION_ACCEPTANCE=BLOCKED_SHA_MISMATCH"
  exit 3
fi

# Source acceptance must never inherit material authority from the host.
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
export VOICE_OUTBOUND_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export PYTHONNOUSERSITE=1

cd "$ROOT"

"$PY" -m py_compile scripts/commercial/verify_dealix_operating_constitution.py
"$PY" scripts/commercial/verify_dealix_operating_constitution.py
"$PY" -m pytest -q tests/test_dealix_operating_constitution.py

# The compatibility entrypoint must delegate to exactly one canonical runner
# and must enforce constitution verification before delegation.
"$PY" - <<'PY'
from pathlib import Path
root = Path.cwd()
text = (root / "scripts/commercial/run_company_os_daily.py").read_text(encoding="utf-8")
assert "verify_dealix_operating_constitution.py" in text
assert "run_self_operating_company_os.py" in text
assert "BLOCKED_CONSTITUTION_INVALID" in text
assert "DELEGATED_TO_CANONICAL_COMPANY_OS" in text
print("COMPANY_OS_CONSTITUTION_PREFLIGHT=PASS")
PY

if [[ -n "$(git_safe status --porcelain)" ]]; then
  echo "DEALIX_OPERATING_CONSTITUTION_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE"
  exit 4
fi

if [[ "$(git_safe rev-parse HEAD)" != "$EXPECTED" ]]; then
  echo "DEALIX_OPERATING_CONSTITUTION_ACCEPTANCE=BLOCKED_HEAD_MOVED"
  exit 5
fi

cat <<EOF
EXACT_SHA=$EXPECTED
CONSTITUTION_VERIFIER=PASS
FOCUSED_TESTS=PASS
COMPANY_OS_CONSTITUTION_PREFLIGHT=PASS
PERMANENT_AGENTS=5
PORTFOLIOS=TRUST,MONEY_NOW,COMPOUNDING
ACTIVE_GTM_WEDGE_LIMIT=3
MATERIAL_AUTHORITY=FAIL_CLOSED
MERGE=false
DEPLOY=false
DNS_MUTATION=false
DB_MUTATION=false
SECRET_MUTATION=false
EXTERNAL_SEND=false
PAYMENT=false
PUBLIC_PUBLISH=false
DEALIX_OPERATING_CONSTITUTION_ACCEPTANCE=PASS_SOURCE_ONLY
EOF
