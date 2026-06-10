#!/usr/bin/env bash
# Founder commercial morning — canonical daily command (governed: drafts + approval, no auto-send)
# Usage:
#   bash scripts/run_founder_commercial_day.sh
#   bash scripts/run_founder_commercial_day.sh --dry-run
#   bash scripts/run_founder_commercial_day.sh --with-business-now
#   bash scripts/run_founder_commercial_day.sh --full   # business_now + sync evidence
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi
if [[ -z "${DEALIX_ADMIN_API_KEY:-}" && -n "${ADMIN_API_KEYS:-}" ]]; then
  DEALIX_ADMIN_API_KEY="${ADMIN_API_KEYS%%,*}"
  export DEALIX_ADMIN_API_KEY
fi
export DEALIX_API_BASE="${DEALIX_API_BASE:-${DEALIX_API_URL:-${NEXT_PUBLIC_API_URL:-}}}"

DRY_RUN=0
WITH_BIZ_NOW=0
SYNC_EVIDENCE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --with-business-now) WITH_BIZ_NOW=1 ;;
    --full)
      WITH_BIZ_NOW=1
      SYNC_EVIDENCE=1
      ;;
  esac
done

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "FOUNDER_COMMERCIAL_DAY: FAIL — python3 not found"
  exit 1
fi

API_URL="${DEALIX_API_URL:-${NEXT_PUBLIC_API_URL:-http://localhost:8000}}"
API_URL="${API_URL%/}"
ADMIN_KEY="${DEALIX_ADMIN_API_KEY:-}"
DATE="$(date -u +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)"
TOP_N=15

echo "== Dealix Founder Commercial Day (canonical) =="
echo "  repo: $ROOT"
echo "  date: $DATE"
echo "  dry_run: $DRY_RUN"
echo ""

echo "== 0a/7 Agent work packets (today) =="
$PYTHON_BIN "$ROOT/scripts/print_agent_work_packets.py" --cadence daily || true
echo ""

echo "== 0b/7 GTM public surfaces (repo) =="
$PYTHON_BIN "$ROOT/scripts/verify_gtm_public_surfaces.py" --skip-live || true
echo ""

PROD_API="${DEALIX_API_BASE:-https://api.dealix.me}"
echo "== 0c/7 Production gates (Railway + live API) =="
$PYTHON_BIN "$ROOT/scripts/run_founder_production_gates.py" --api-base "$PROD_API" || true
echo ""

echo "== Expand stack (targeting + social + content) =="
$PYTHON_BIN "$ROOT/scripts/expand_commercial_operating_stack.py" --daily || true
echo ""

if [[ "$DRY_RUN" -eq 1 ]]; then
  exec "$PYTHON_BIN" "$ROOT/scripts/founder_revenue_day_runner.py" --dry-run
fi

DAILY_ARGS=(--api-only)
if [[ -z "$ADMIN_KEY" ]]; then
  DAILY_ARGS=(--skip-api)
fi
echo "== 0/7 Dealix daily ops (bridge + health) =="
$PYTHON_BIN "$ROOT/scripts/run_dealix_daily_ops.py" "${DAILY_ARGS[@]}"
echo ""

echo "== 1/7 Founder daily brief =="
$PYTHON_BIN "$ROOT/scripts/dealix_founder_daily_brief.py" --out "data/founder_briefs/brief_${DATE}.md"
echo ""

echo "== 2/7 KPI commercial status =="
$PYTHON_BIN "$ROOT/scripts/bootstrap_founder_kpi_import.py" || true
$PYTHON_BIN "$ROOT/scripts/apply_kpi_founder_commercial.py" --status || true
echo ""

if [[ "$WITH_BIZ_NOW" -eq 1 ]]; then
  echo "== optional: Business NOW =="
  if [[ -f "$ROOT/scripts/run_business_now.sh" ]]; then
    bash "$ROOT/scripts/run_business_now.sh" || echo "  (business_now warning — continuing)"
  fi
  echo ""
fi

echo "== 3/8 War Room sync (P0 rotation) =="
$PYTHON_BIN "$ROOT/scripts/commercial_war_room_sync.py"
echo ""

echo "== 4/8 War Room CSV import (skips duplicates) =="
if [[ -n "$ADMIN_KEY" ]]; then
  export DEALIX_API_BASE="${DEALIX_API_BASE:-$API_URL}"
  $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply --via-api \
    || $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply \
    || echo "  (import warning — continuing)"
else
  $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply || echo "  (import warning — continuing)"
fi
echo ""

echo "== 5/8 Commercial digest =="
SYNC_ARGS=()
if [[ "$SYNC_EVIDENCE" -eq 1 || "${DEALIX_SYNC_EVIDENCE:-}" == "1" ]]; then
  SYNC_ARGS+=(--sync-evidence --pull-evidence)
fi
$PYTHON_BIN "$ROOT/scripts/founder_commercial_digest.py" --out "data/founder_briefs/commercial_${DATE}.md" "${SYNC_ARGS[@]}"
echo ""

echo "== 5b/8 War Room touch drafts (governed, no send) =="
$PYTHON_BIN "$ROOT/scripts/generate_war_room_touch_drafts.py" --top-n "$TOP_N" || echo "  (touch drafts warning — continuing)"
echo ""

echo "== 6/9 Social queue today =="
$PYTHON_BIN "$ROOT/scripts/social_queue_today.py" || true
echo ""

echo "== 7/10 SOAEN + doctrine block =="
$PYTHON_BIN "$ROOT/scripts/founder_soaen_daily.py" --out "data/founder_briefs/soaen_${DATE}.md" || true
echo ""

echo "== 8/10 AEO + War Room summary + verdict =="
$PYTHON_BIN "$ROOT/scripts/founder_revenue_day_runner.py" --skip-substeps
echo ""

echo "== 9/12 Expand social queue (idempotent weeks 9–12) =="
$PYTHON_BIN "$ROOT/scripts/expand_social_queue_12w.py" --cycle-weeks 28 || true
echo ""

echo "== 10/12 Soft Launch meeting packs =="
$PYTHON_BIN "$ROOT/scripts/prepare_soft_launch_meetings.py" --top-n 10 || true
echo ""

echo "== 11/14 Motion A pipeline (P0 close path) =="
$PYTHON_BIN "$ROOT/scripts/founder_motion_a_pipeline.py" --top-n "$TOP_N" || true
$PYTHON_BIN "$ROOT/scripts/founder_all_motions_pipeline.py" --top-n 5 || true
echo ""

echo "== 12/14 First paid Diagnostic tracker =="
$PYTHON_BIN "$ROOT/scripts/verify_first_paid_diagnostic_tracker.py" || true
echo ""

echo "== 13/14 Content approval queue (dry-run) =="
$PYTHON_BIN "$ROOT/scripts/queue_content_drafts_for_approval.py" --dry-run || true
echo ""

DOW=$(date +%u)
if [[ "$DOW" -eq 5 ]]; then
  echo "== 14/14 Weekly scorecard (Friday) =="
  $PYTHON_BIN "$ROOT/scripts/founder_weekly_scorecard.py" || true
else
  echo "== 14/14 Weekly scorecard (skip - Friday or founder_weekly_scorecard.py) =="
fi
echo ""

echo "== Evening (founder) =="
echo "  bash: python3 scripts/founder_evening_evidence.py"
echo "  Or: --append --event-type message_sent_manual --company 'Agency'"
echo ""

echo "== 15/17 Value Plan snapshot =="
$PYTHON_BIN "$ROOT/scripts/export_value_plan_snapshot.py" || true
echo ""

echo "== 16/18 Strongest ops (مهام اليوم + قرار أسبوعي) =="
$PYTHON_BIN "$ROOT/scripts/run_founder_strongest_ops.py" --morning --run-checks || true
echo ""

echo "== 17/18 Full autonomous ops (snapshot + morning core) =="
$PYTHON_BIN "$ROOT/scripts/run_full_commercial_ops_autopilot.py" --execute --json > "data/founder_briefs/full_autonomous_ops_${DATE}.json" 2>/dev/null || \
  $PYTHON_BIN "$ROOT/scripts/run_full_commercial_ops_autopilot.py" --execute || true
echo ""

echo "== 18/19 GTM + comprehensive gates =="
$PYTHON_BIN "$ROOT/scripts/verify_gtm_stack.py" || true
$PYTHON_BIN "$ROOT/scripts/founder_comprehensive_plan_status.py" || true
echo ""

echo "== 19/19 Full autonomous ops stack =="
$PYTHON_BIN "$ROOT/scripts/verify_full_autonomous_ops_stack.py" --skip-api || true
echo ""

echo "== Daily pack index =="
echo "  See data/founder_briefs/index.json and data/war_room_today.json"
echo "  Ops UI: /ar/ops/founder · /ar/ops/war-room · /ar/ops/approvals"
echo ""

echo "== Automated drafts (production) =="
echo "  GitHub: .github/workflows/daily-revenue-machine.yml (04:00 UTC, draft_only)"
echo "  GitHub: .github/workflows/founder_commercial_daily.yml (05:00 UTC Sun-Thu)"
echo "  Weekly content: python scripts/generate_weekly_content_drafts.py"
echo "  Queue approvals: python scripts/queue_content_drafts_for_approval.py --dry-run"
if [[ -n "$ADMIN_KEY" ]]; then
  echo "  War Room API: ${API_URL}/api/v1/ops-autopilot/war-room?needs_follow_up=true"
else
  echo "  Set DEALIX_ADMIN_API_KEY for live War Room API fetch."
fi
echo ""

echo "== Operating evidence (if none today) =="
$PYTHON_BIN "$ROOT/scripts/log_founder_commercial_day_evidence.py" || true
echo ""

echo "FOUNDER_COMMERCIAL_DAY: OK"
echo "Soft launch verify: python3 scripts/verify_commercial_launch_ready.py"
echo "Extended morning (+ Business NOW): bash scripts/run_founder_revenue_day.sh"
echo "Company ready: docs/company/DEALIX_COMPANY_READY_MASTER_AR.md"
echo "5 min ops: docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md"
echo "Launch checklist: docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md"
