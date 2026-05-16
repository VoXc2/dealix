#!/usr/bin/env bash
# One-session CEO readiness: weekly proof + platform KPI signals + full verify bundle + session report.
# See docs/transformation/CEO_ONE_SESSION_MASTER_PLAN_AR.md
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"
DATE_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
REPORT="${ROOT}/docs/transformation/evidence/session_report_${DATE_UTC:0:10}.md"

cd "$ROOT"

echo "== Phase A: Executive weekly checklist =="
bash "${ROOT}/scripts/run_executive_weekly_checklist.sh"

echo ""
echo "== Phase B: Platform KPI signals (not CRM) =="
"$PYTHON_BIN" "${ROOT}/scripts/populate_kpi_baselines_platform_signals.py"

echo ""
echo "== Phase C: Pre-scale gate bundle =="
bash "${ROOT}/scripts/run_pre_scale_gate_bundle.sh"

echo ""
echo "== Phase D: Full transformation + control plane =="
bash "${ROOT}/scripts/verify_global_ai_transformation.sh"

echo ""
echo "== Phase E: Alembic single head =="
"$PYTHON_BIN" "${ROOT}/scripts/check_alembic_single_head.py"

echo ""
echo "== Phase F: Reliability scorecard =="
"$PYTHON_BIN" "${ROOT}/scripts/reliability_drills_scorecard.py" | tee /tmp/dealix_drills_scorecard.txt

echo ""
echo "== Phase G: Session report =="
mkdir -p "$(dirname "$REPORT")"
{
  echo "# CEO one-session readiness report — ${DATE_UTC:0:10}"
  echo ""
  echo "## Commands executed"
  echo ""
  echo "- run_executive_weekly_checklist.sh"
  echo "- populate_kpi_baselines_platform_signals.py"
  echo "- run_pre_scale_gate_bundle.sh"
  echo "- verify_global_ai_transformation.sh"
  echo "- check_alembic_single_head.py"
  echo "- reliability_drills_scorecard.py"
  echo ""
  echo "## Platform signals"
  echo ""
  echo '```text'
  "$PYTHON_BIN" -c "
from dealix.execution.weekly_cross_os_snapshot import weekly_cross_os_snapshot
s = weekly_cross_os_snapshot()
print(f'reliability_posture_score={s.reliability_posture_score} status={s.reliability_posture_status}')
print(f'gross_margin_pct={s.gross_margin_pct} flywheel={s.flywheel_overall} delivery_risk={s.delivery_risk_score}')
"
  echo '```'
  echo ""
  echo "## Drills scorecard (trimmed)"
  echo ""
  echo '```text'
  head -20 /tmp/dealix_drills_scorecard.txt
  echo '```'
  echo ""
  echo "## Founder-only (still required for commercial truth)"
  echo ""
  echo "- Fill CRM/finance nulls in dealix/transformation/kpi_baselines.yaml with real source_ref."
  echo "- Update ownership_matrix executive_review.last_ownership_matrix_review_iso after hiring review."
  echo "- Engineering cutover only with external_signal per ENGINEERING_CUTOVER_RUNBOOK_AR.md."
  echo ""
  echo "## Next command"
  echo ""
  echo '```bash'
  echo "bash scripts/verify_ceo_signal_readiness.sh revenue_os   # when GTM/pipeline changed"
  echo '```'
} >"$REPORT"

echo ""
echo "CEO_ONE_SESSION_READINESS: PASS"
echo "Session report: $REPORT"
echo "Arabic master plan: docs/transformation/CEO_ONE_SESSION_MASTER_PLAN_AR.md"
