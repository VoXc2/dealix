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

"$PY" -m py_compile \
  scripts/commercial/verify_dealix_control_kernel_v2.py \
  scripts/commercial/dealix_control_kernel_v2.py \
  scripts/commercial/verify_dealix_operating_constitution.py \
  scripts/commercial/verify_dealix_arm_registry.py \
  scripts/commercial/verify_dealix_arm_execution_playbooks.py \
  scripts/ops/dealix_north_star_status.py

"$PY" scripts/commercial/verify_dealix_control_kernel_v2.py
"$PY" scripts/commercial/verify_dealix_operating_constitution.py
"$PY" scripts/commercial/verify_dealix_arm_registry.py
"$PY" scripts/commercial/verify_dealix_arm_execution_playbooks.py
"$PY" scripts/ops/dealix_north_star_status.py
"$PY" -m pytest -q \
  tests/test_dealix_control_kernel_v2.py \
  tests/test_dealix_operating_constitution.py \
  tests/test_dealix_arm_registry.py \
  tests/test_dealix_arm_execution_playbooks.py

# The compatibility entrypoint must evaluate the constitutional superlayer
# first, then company law and arm governance before one canonical runner.
"$PY" - <<'PY'
from pathlib import Path
root = Path.cwd()
text = (root / "scripts/commercial/run_company_os_daily.py").read_text(encoding="utf-8")
for needle in (
    "verify_dealix_control_kernel_v2.py",
    "verify_dealix_operating_constitution.py",
    "verify_dealix_arm_registry.py",
    "verify_dealix_arm_execution_playbooks.py",
    "run_self_operating_company_os.py",
    "BLOCKED_CONTROL_KERNEL_INVALID",
    "BLOCKED_CONSTITUTION_INVALID",
    "BLOCKED_ARM_REGISTRY_INVALID",
    "BLOCKED_ARM_EXECUTION_INVALID",
    "DELEGATED_TO_CANONICAL_COMPANY_OS",
):
    assert needle in text
assert text.index("CONTROL_KERNEL_VERIFY") < text.index("CONSTITUTION_VERIFY") < text.index("ARM_REGISTRY_VERIFY") < text.index("ARM_EXECUTION_VERIFY")
assert text.index("control_kernel_rc") < text.index("constitution_rc") < text.index("arm_registry_rc") < text.index("arm_execution_rc")

constitution = (root / "config/company/dealix_operating_constitution.json").read_text(encoding="utf-8")
registry = (root / "config/company/dealix_arm_registry.json").read_text(encoding="utf-8")
for needle in ('"constitution_version": "2.0-fast-compression"','"compress_time": true','"compress_truth": false','"deep_wip_max": 3','"path": "config/company/dealix_arm_registry.json"'):
    assert needle in constitution
for needle in ('"id": "ARM-001"','"id": "ARM-044"','"state": "ACTIVE_DEEP"','"engine": "VENTURE_AND_ASSET_ENGINE"'):
    assert needle in registry

kernel = (root / "config/company/dealix_control_kernel_v2.json").read_text(encoding="utf-8")
for needle in ('"kernel_version": "2.0-control-kernel"','"objective": "AUTONOMOUS_BUSINESS_THROUGHPUT"','"prediction_is_not_fact": true','"never_authorize_by_agent_name_only": true','"universal_l5_autonomy_forbidden": true','"global_uncontrolled_customer_sensitive_memory_forbidden": true','"do_not_install_spire_without_trigger": true'):
    assert needle in kernel

agent_directive = root / "prompts/company/DEALIX_CONTROL_KERNEL_V2_AGENT_DIRECTIVE.md"
assert agent_directive.is_file()
directive = agent_directive.read_text(encoding="utf-8")
for agent in ("dealix-pm","dealix-sales","dealix-delivery","dealix-engineer","dealix-content"):
    assert f"`{agent}`" in directive
for needle in ("does not create a new agent, scheduler, brain, policy store, approval system, or proof ledger","agent name alone never grants authority","BUDGET_BLOCKED","Never self-heal via production DB mutation, secret replacement, DNS change, external commitment, payment, privilege expansion, or approval bypass"):
    assert needle in directive

scorecard = root / "docs/ops/DEALIX_PERMANENT_NORTH_STAR_SCORECARD.md"
assert scorecard.is_file()
score_text = scorecard.read_text(encoding="utf-8")
for needle in (
    "VERIFIED_CASH_SAR",
    "CUSTOMER_ACCEPTED_PROOF_PACKS",
    "M5 — Q1 Revenue",
    "No stage may be inferred from the stage before it.",
):
    assert needle in score_text
print("CONTROL_KERNEL_V2_PREFLIGHT=PASS")
print("FIVE_AGENT_DIRECTIVE=PASS")
print("COMPANY_OS_CONSTITUTION_PREFLIGHT=PASS")
print("ARM_REGISTRY_PREFLIGHT=PASS")
print("ARM_EXECUTION_PREFLIGHT=PASS")
print("NORTH_STAR_SCORECARD_CONTRACT=PASS")
PY

git_safe diff --check

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
CONTROL_KERNEL_VERSION=2.0-control-kernel
CONTROL_KERNEL_VERIFIER=PASS
CONTROL_KERNEL_RUNTIME_PRIMITIVES=PASS
FIVE_AGENT_DIRECTIVE=PASS
CONSTITUTION_VERSION=2.0-fast-compression
CONSTITUTION_VERIFIER=PASS
ARM_REGISTRY_VERIFIER=PASS
ARM_EXECUTION_VERIFIER=PASS
NORTH_STAR_STATUS=PASS
NORTH_STAR_SCORECARD_CONTRACT=PASS
FOCUSED_TESTS=PASS
CONTROL_KERNEL_V2_PREFLIGHT=PASS
COMPANY_OS_CONSTITUTION_PREFLIGHT=PASS
ARM_REGISTRY_PREFLIGHT=PASS
ARM_EXECUTION_PREFLIGHT=PASS
PERMANENT_AGENTS=5
PORTFOLIOS=TRUST,MONEY_NOW,COMPOUNDING
STRATEGIC_ENGINES=9
ACTIVE_GTM_WEDGE_LIMIT=3
DEEP_WIP_MAX=3
MATERIAL_AUTHORITY=FAIL_CLOSED
UNIVERSAL_L5_AUTONOMY=false
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
