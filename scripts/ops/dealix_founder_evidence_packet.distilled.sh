#!/usr/bin/env bash
set -uo pipefail
# HERMES_FOUNDER_INTELLIGENCE — bounded 8192ctx packet (2026-09-14 fix for 14488 overflow)
# Root cause: 32082-char packet + SOUL+AGENTS+skills+tools = 14488 tokens >8192 n_ctx. Single-message compression cannot recover.
# Fix: distill to ~6000 chars (~1500 tok) so total prompt <8192. 8K hardener stays (16Gi node). See docs/ops/HERMES_FOUNDER_INTELLIGENCE_CRON_FIX.md
TODAY=$(date +%F)
echo '# DEALIX CURRENT FOUNDER EVIDENCE PACKET'
echo "generated=$(date -Is)"
echo "budget=8192 n_ctx=8192 distilled=v3 bounded=true"
echo '## founder_os_truth'
for f in LATEST_TRUTH.json ECONOMIC_KPI.json; do
  p="/opt/dealix/company-os/founder-os/current/$f"
  [ -f "$p" ] && { echo "### $f"; head -c 1800 "$p"; echo; }
done
p="/opt/dealix/company-os/founder-os/current/FOUNDER_DAILY_COMMAND.md"
if [ -f "$p" ]; then echo "### FOUNDER_DAILY_COMMAND.md (head 22 lines)"; head -n 22 "$p"; echo; fi
echo '## live_pr1600'
gh api repos/Dealix-sa/dealix/pulls/1600 --jq '{head:.head.sha,base:.base.sha,state,draft,mergeable,merged,commits,changed_files,updated_at}' 2>/dev/null | head -c 700 || true; echo
echo '## current_company_opportunity_summary'
for p in /opt/dealix/control/autonomous-company/gtm/state/opportunity-summary.json; do
 [ -f "$p" ] && {
   echo "### opportunity-summary (top2)"
   if command -v jq >/dev/null 2>&1; then
     jq -c '{records_seen,records_selected,production_green,external_send_authorized,top: (.top // [] | .[0:2] | map({company,score,stage,next}))}' "$p" 2>/dev/null | head -c 1100 || head -c 1100 "$p"
     echo
   else head -c 1100 "$p"; echo; fi
 }
done
for p in /opt/dealix/control/autonomous-company/gtm/queues/material-approval-queue.json; do
 [ -f "$p" ] && {
   echo "### approval-queue (top2)"
   if command -v jq >/dev/null 2>&1; then
     jq -c 'map({action,target,evidence_score,relationship_state,authority_required}) | .[0:2]' "$p" 2>/dev/null | head -c 900 || head -c 900 "$p"
     echo
   else head -c 900 "$p"; echo; fi
 }
done
echo '## today_self_operating_company'
for p in "/opt/dealix/workspace/dealix/reports/self_operating_company_os/daily/$TODAY.md"; do
 [ -f "$p" ] && { echo "### $(basename "$p") (first 30 lines)"; head -n 30 "$p"; echo; }
done
if [ -f "/opt/dealix/workspace/dealix/reports/probability_revenue_engine/$TODAY.json" ]; then
  p="/opt/dealix/workspace/dealix/reports/probability_revenue_engine/$TODAY.json"
  echo "### probability_revenue_engine (top3 distilled)"
  if command -v jq >/dev/null 2>&1; then
    jq -c '{generated_at,mode,target_count,top3: (.ranked_targets | sort_by(-.evidence_priority) | .[0:3] | map({rank,company_name,commercial_stage,evidence_priority,next_action}))}' "$p" 2>/dev/null | head -c 1300 || head -c 1300 "$p"
    echo
  else head -c 1300 "$p"; echo; fi
fi
exit 0
