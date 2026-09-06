#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(git rev-parse --show-toplevel)"
EXPECTED_SHA="${1:-}"
ACTUAL_SHA="$(git -C "$ROOT" rev-parse HEAD)"
PYTHON_BIN="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"

block() {
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_$1"
  exit 2
}

[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || block EXACT_SHA_REQUIRED
[[ "$ACTUAL_SHA" == "$EXPECTED_SHA" ]] || block HEAD_MISMATCH
[[ -x "$PYTHON_BIN" ]] || block PYTHON_NOT_EXECUTABLE
[[ -z "$(git -C "$ROOT" status --porcelain)" ]] || block DIRTY_WORKTREE

# Never reuse a proof directory: a failed retry must not inherit an old PASS.
if [[ -n "${DEALIX_E2E_PROOF_ROOT:-}" ]]; then
  PROOF_ROOT="$(realpath -m -- "$DEALIX_E2E_PROOF_ROOT")"
  case "$PROOF_ROOT/" in "$ROOT/"*) block PROOF_INSIDE_WORKTREE ;; esac
  [[ ! -e "$DEALIX_E2E_PROOF_ROOT" && ! -L "$DEALIX_E2E_PROOF_ROOT" ]] || block PROOF_PATH_EXISTS
  mkdir -m 0700 -- "$PROOF_ROOT"
else
  PROOF_PARENT="$(realpath -e -- "${TMPDIR:-/tmp}")"
  case "$PROOF_PARENT/" in "$ROOT/"*) block PROOF_INSIDE_WORKTREE ;; esac
  PROOF_ROOT="$(mktemp -d "$PROOF_PARENT/dealix-e2e-company-$ACTUAL_SHA.XXXXXXXX")"
fi

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
export APP_ENV=test
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"

cd "$ROOT"
STAGE=initialization
RESULT=FAIL

finish() {
  local rc=$?
  trap - EXIT
  set +e
  [[ "$rc" -eq 0 && "$RESULT" == PASS ]] || RESULT=FAIL
  "$PYTHON_BIN" - "$PROOF_ROOT" "$ACTUAL_SHA" "$RESULT" "$STAGE" "$rc" <<'PY_RECEIPT'
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
result = sys.argv[3]
receipt = {
    "schema": "dealix.end-to-end-company-acceptance-receipt.v1",
    "git_sha": sys.argv[2],
    "created_at": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "result": result,
    "last_stage": sys.argv[4],
    "exit_code": int(sys.argv[5]),
    "authority_class": "L4_INTERNAL_VERIFICATION",
    "external_effects": "FAIL_CLOSED_FLAGS_CONFIGURED_NOT_AN_EGRESS_ATTESTATION",
    "agents": 5,
    "runtime_specialist_roles": 12,
    "operating_company_specialist_roles": 15,
    "revenue_factory_specialist_roles": 15,
    "automation_plays": 30,
    "systems": 12,
    "lifecycle_stages": 18,
    "counts_semantics": "CONTRACT_EXPECTATIONS_VALIDATED_ONLY_ON_PASS",
    "autonomous_quarantine": "PASS" if result == "PASS" else "NOT_ATTESTED",
    "acceptance_ceiling": "A0_A1_ONLY",
    "quarantine_scope": "TEST_ENV_IMPORTED_APPLICATION_ONLY",
    "deployed_production_verified": False,
    "tenant_isolation_verified": False,
    "founder_control": "TELEGRAM_OPENCLAW_E2E_RECEIPT_REQUIRED_SEPARATELY",
    "next_action": "independent_same_head_review_then_runtime_and_production_gates",
    "log_sha256": {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.glob("*.log"))
    },
}
temporary = root / "receipt.json.tmp"
temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
os.replace(temporary, root / "receipt.json")
digest = hashlib.sha256((root / "receipt.json").read_bytes()).hexdigest()
(root / "receipt.sha256").write_text(digest + "  receipt.json\n", encoding="ascii")
PY_RECEIPT
  local receipt_rc=$?
  if [[ "$receipt_rc" -ne 0 ]]; then
    RESULT=FAIL_RECEIPT_WRITE
    rm -f -- "$PROOF_ROOT/receipt.json" "$PROOF_ROOT/receipt.sha256"
    [[ "$rc" -ne 0 ]] || rc=1
  fi
  echo "DEALIX_E2E_ACCEPTANCE=$RESULT"
  echo "git_sha=$ACTUAL_SHA"
  echo "proof_root=$PROOF_ROOT"
  exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

run() {
  STAGE="$1"
  shift
  echo "[$STAGE]"
  "$@" 2>&1 | tee "$PROOF_ROOT/$STAGE.log"
}

run quarantine_logic_tests \
  "$PYTHON_BIN" -m unittest discover -s tests -p test_autonomous_quarantine_verifier.py
run autonomous_quarantine \
  "$PYTHON_BIN" scripts/ops/verify_autonomous_quarantine.py
run composite_contract \
  "$PYTHON_BIN" scripts/ops/verify_end_to_end_company_acceptance_v1.py
run company_machine \
  "$PYTHON_BIN" scripts/ops/verify_autonomous_company_machine_v2.py --source-sha "$ACTUAL_SHA"
run continuous_operations \
  "$PYTHON_BIN" scripts/verify_continuous_company_operations_v1.py
run governed_channels \
  "$PYTHON_BIN" scripts/verify_governed_channel_runtime_v1.py
run commercial_fabric \
  "$PYTHON_BIN" scripts/verify_commercial_execution_fabric_v2.py
run focused_tests \
  "$PYTHON_BIN" -m pytest -q \
    tests/test_end_to_end_company_acceptance_v1.py \
    tests/test_ai_workforce_canonical_delegation.py \
    tests/test_ai_workforce_revenue_factory_blueprint.py \
    tests/test_autonomous_company_machine_source_awareness.py \
    tests/test_end_to_end_acceptance_runner_integrity.py

STAGE=final_worktree_integrity
[[ "$(git -C "$ROOT" rev-parse HEAD)" == "$EXPECTED_SHA" ]] || block HEAD_MOVED_DURING_RUN
[[ -z "$(git -C "$ROOT" status --porcelain)" ]] || block WORKTREE_CHANGED_DURING_RUN
RESULT=PASS
STAGE=complete
