#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
MODE="${1:-daily}"
OUT_ROOT="${DEALIX_REVENUE_CYCLE_OUT:-$ROOT/reports/canonical_revenue_cycle}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="$OUT_ROOT/$STAMP"
GATE="$ROOT/dealix/config/first_launch_offer_gate.yaml"

export TZ="${TZ:-Asia/Riyadh}"
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export AGENT_APPROVAL_MODE=required
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0

if [[ ! -d "$ROOT/.git" ]]; then
  echo "BLOCKED: canonical repository not found at $ROOT"
  exit 2
fi
cd "$ROOT"
mkdir -p "$OUT_DIR"

if [[ ! -f "$GATE" ]]; then
  echo "BLOCKED: canonical launch gate missing: $GATE"
  exit 3
fi

case "$MODE" in
  daily|weekly|status) ;;
  *) echo "DENIED: mode must be daily, weekly, or status"; exit 64 ;;
esac

python3 - "$GATE" "$OUT_DIR/gate.json" <<'PY'
import json
import sys
from pathlib import Path
import yaml

src = Path(sys.argv[1])
out = Path(sys.argv[2])
payload = yaml.safe_load(src.read_text(encoding="utf-8"))
primary = payload.get("primary_motion") or {}
pricing = payload.get("pricing_experiment") or {}
conversation = payload.get("conversation_policy") or {}
icp = payload.get("icp_hypothesis") or {}
summary = {
    "status": payload.get("status"),
    "motion_id": primary.get("id"),
    "motion_name": primary.get("name_en"),
    "duration_days": primary.get("duration_days"),
    "quote_only_after_discovery": primary.get("quote_only_after_discovery"),
    "checkout_enabled": primary.get("checkout_enabled"),
    "pricing_status": pricing.get("status"),
    "public_amount_sar": pricing.get("public_amount_sar"),
    "qualified_conversations_required": pricing.get("qualified_conversations_required"),
    "audience": conversation.get("audience"),
    "external_send_allowed": conversation.get("external_send_allowed"),
    "icp_status": icp.get("status"),
    "icp_segment": icp.get("segment"),
}
violations = []
if summary["motion_id"] != "revenue_command_pilot_30d":
    violations.append("unexpected_primary_motion")
if summary["checkout_enabled"] is not False:
    violations.append("checkout_must_remain_disabled")
if summary["public_amount_sar"] is not None:
    violations.append("public_price_not_authorized")
if summary["external_send_allowed"] is not False:
    violations.append("external_send_must_remain_disabled")
if summary["audience"] != "warm_consented_only":
    violations.append("audience_must_be_warm_consented_only")
summary["violations"] = violations
out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if violations:
    print("CANONICAL_LAUNCH_GATE=FAIL " + ",".join(violations))
    raise SystemExit(4)
print("CANONICAL_LAUNCH_GATE=PASS")
print(f"PRIMARY_MOTION={summary['motion_name']}")
print(f"PRICING_STATUS={summary['pricing_status']}")
print(f"QUALIFIED_CONVERSATIONS_REQUIRED={summary['qualified_conversations_required']}")
PY

run_optional() {
  local label="$1"
  shift
  echo
  echo "===== $label ====="
  if "$@"; then
    echo "${label// /_}=PASS"
  else
    local rc=$?
    echo "${label// /_}=DEGRADED rc=$rc"
    return "$rc"
  fi
}

if [[ "$MODE" == "status" ]]; then
  cat "$OUT_DIR/gate.json"
  echo "CANONICAL_REVENUE_CYCLE_STATUS=PASS"
  exit 0
fi

# Canonical governed operating board: reads the launch gate and source registry,
# creates no external actions, and records truth state when real signals are absent.
run_optional "commercial_intelligence" \
  python3 scripts/commercial/run_commercial_intelligence_founder_cycle.py \
  --output "$OUT_DIR/commercial_intelligence" || true

# Revenue Lab runs only when a caller supplies an explicit evidence-backed input.
# Never silently substitute demo signals in the daily company cycle.
if [[ -n "${DEALIX_REVENUE_LAB_INPUT:-}" ]]; then
  INPUT="$DEALIX_REVENUE_LAB_INPUT"
  if [[ ! -f "$INPUT" ]]; then
    echo "REVENUE_LAB=BLOCKED input_missing=$INPUT"
  else
    run_optional "revenue_lab" \
      python3 scripts/commercial/run_revenue_lab_daily.py \
      --input "$INPUT" \
      --mode draft-only \
      --output-dir "$OUT_DIR/revenue_lab" || true
  fi
else
  echo "REVENUE_LAB=SKIPPED reason=no_evidence_backed_input"
fi

# Market-entry lane is opt-in and requires an explicit governed signal file.
if [[ -n "${DEALIX_MARKET_ENTRY_SIGNALS:-}" ]]; then
  SIGNALS="$DEALIX_MARKET_ENTRY_SIGNALS"
  if [[ ! -f "$SIGNALS" ]]; then
    echo "MARKET_ENTRY=BLOCKED signals_missing=$SIGNALS"
  else
    run_optional "market_entry" \
      python3 scripts/commercial/run_founder_market_entry.py \
      --signals "$SIGNALS" \
      --output-dir "$OUT_DIR/market_entry" || true
  fi
else
  echo "MARKET_ENTRY=SKIPPED reason=no_explicit_governed_signals"
fi

# Lead-to-cash is only used as a structural safety/proof rehearsal here.
# draft_only must block at the first external effect.
run_optional "lead_to_cash_draft_only" \
  python3 scripts/commercial/run_company_loop_simulation.py \
  --loop lead_to_cash \
  --mode draft_only \
  --output "$OUT_DIR/lead_to_cash.json" || true

if [[ "$MODE" == "weekly" && -f scripts/run_weekly_proof_pack.py ]]; then
  run_optional "weekly_proof_pack" python3 scripts/run_weekly_proof_pack.py || true
fi

python3 - "$OUT_DIR" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
gate = json.loads((root / "gate.json").read_text(encoding="utf-8"))
summary = {
    "mode": "draft_only",
    "primary_motion": gate.get("motion_name"),
    "pricing_status": gate.get("pricing_status"),
    "public_amount_sar": gate.get("public_amount_sar"),
    "qualified_conversations_required": gate.get("qualified_conversations_required"),
    "audience": gate.get("audience"),
    "external_actions_executed_by_wrapper": 0,
    "approval_required_for_external_actions": True,
    "next_operating_goal": "five qualified first-party conversations -> bounded pilot decision -> accepted proof",
}
(root / "cycle_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("CANONICAL_REVENUE_CYCLE=PASS")
print(f"OUTPUT_DIR={root}")
PY
