#!/usr/bin/env bash
# Founder cadence — morning default, optional evening / weekly
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${1:-}" == "--evening" ]]; then
  python3 scripts/run_founder_strongest_ops.py --evening
  exec python3 scripts/founder_evening_evidence.py "${@:2}"
fi

if [[ "${1:-}" == "--complete" ]]; then
  shift || true
  exec python3 scripts/run_dealix_complete_autonomous_day.py "$@"
fi

if [[ "${1:-}" == "--weekly" ]]; then
  python3 scripts/run_founder_strongest_ops.py --weekly --run-checks
  python3 scripts/founder_weekly_scorecard.py
  python3 scripts/founder_all_motions_pipeline.py --top-n 5
  python3 scripts/founder_comprehensive_plan_status.py
  exit 0
fi

python3 scripts/run_founder_strongest_ops.py --morning
python3 scripts/run_full_commercial_ops_autopilot.py --execute --top-n 15
python3 scripts/founder_dogfooding_war_room_sync.py
bash scripts/run_founder_commercial_day.sh "$@"
rc=$?
python3 scripts/founder_comprehensive_plan_status.py
exit $rc
