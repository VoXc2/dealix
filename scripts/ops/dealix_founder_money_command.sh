#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
REPORT_ROOT="${DEALIX_MONEY_REPORT_ROOT:-${REPO_ROOT}/reports/founder_money_command}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="${REPORT_ROOT}/${STAMP}"
MD="${OUT_DIR}/money_command.md"
JSON="${OUT_DIR}/money_command.json"

mkdir -p "$OUT_DIR"

log() { printf '%s\n' "$*"; }
section() { printf '\n===== %s =====\n' "$*"; }

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "BLOCKED: Dealix repository not found at $REPO_ROOT"
  exit 20
fi

cd "$REPO_ROOT"

BRANCH="$(git branch --show-current 2>/dev/null || true)"
HEAD="$(git rev-parse HEAD)"
DIRTY="false"
if [ -n "$(git status --porcelain)" ]; then DIRTY="true"; fi

run_capture() {
  local name="$1"; shift
  local path="${OUT_DIR}/${name}.txt"
  set +e
  "$@" >"$path" 2>&1
  local rc=$?
  set -e
  printf '%s' "$rc" >"${OUT_DIR}/${name}.rc"
  return 0
}

run_py_if_exists() {
  local name="$1"; local script="$2"; shift 2
  if [ -f "$script" ]; then
    run_capture "$name" python "$script" "$@"
  else
    printf 'UNKNOWN: missing %s\n' "$script" >"${OUT_DIR}/${name}.txt"
    printf '127' >"${OUT_DIR}/${name}.rc"
  fi
}

section "FOUNDATION"
echo "branch=$BRANCH"
echo "head=$HEAD"
echo "dirty=$DIRTY"

# Existing canonical founder/revenue surfaces. Missing inputs are UNKNOWN, never silently zero.
run_py_if_exists founder_daily_five scripts/founder_daily_five_metrics.py --json
run_py_if_exists ceo_master_plan scripts/run_ceo_master_plan_status.py
run_py_if_exists first_paid_gate scripts/founder_paid_launch_gate.py
run_py_if_exists first_paid_tracker scripts/verify_first_paid_diagnostic_tracker.py
run_py_if_exists commercial_value_map scripts/commercial_value_map_status.py
run_py_if_exists phase_0_1_close scripts/phase_0_1_close_helper.py

if [ -x scripts/ops/dealix_founder_cockpit_full.sh ]; then
  run_capture founder_cockpit bash scripts/ops/dealix_founder_cockpit_full.sh --status-only
elif command -v dealix-cockpit-status >/dev/null 2>&1; then
  run_capture founder_cockpit dealix-cockpit-status
else
  echo "UNKNOWN: founder cockpit status surface unavailable" >"${OUT_DIR}/founder_cockpit.txt"
  echo 127 >"${OUT_DIR}/founder_cockpit.rc"
fi

# Draft-only autonomous loops. Never promote failure to success.
for spec in \
  "company_os_daily:scripts/commercial/run_company_os_daily.py:--client dealix --mode draft-only --limit 50" \
  "growth_daily:scripts/commercial/run_autonomous_growth_daily.py:--autonomy-level 3 --mode draft-only --limit 50" \
  "self_improvement:scripts/commercial/run_self_improvement_daily.py:--client dealix --mode draft-only" \
  "weekly_proof:scripts/commercial/run_weekly_proof_pack.py:--client dealix --mode draft-only"
do
  IFS=: read -r name script args <<<"$spec"
  if [ -f "$script" ]; then
    # shellcheck disable=SC2086
    run_capture "$name" python "$script" $args
  else
    echo "UNKNOWN: missing $script" >"${OUT_DIR}/${name}.txt"
    echo 127 >"${OUT_DIR}/${name}.rc"
  fi
done

# Read-only infrastructure posture.
run_capture git_status git status -sb
run_capture git_recent git log -5 --oneline
if command -v gh >/dev/null 2>&1; then
  run_capture gh_prs gh pr list --repo Dealix-sa/dealix --state open --limit 30 --json number,title,isDraft,mergeable,updatedAt,url
else
  echo "UNKNOWN: gh not installed" >"${OUT_DIR}/gh_prs.txt"; echo 127 >"${OUT_DIR}/gh_prs.rc"
fi
if command -v railway >/dev/null 2>&1; then
  run_capture railway_status railway status
else
  echo "UNKNOWN: railway CLI not installed" >"${OUT_DIR}/railway_status.txt"; echo 127 >"${OUT_DIR}/railway_status.rc"
fi

python - "$OUT_DIR" "$HEAD" "$BRANCH" "$DIRTY" "$JSON" "$MD" <<'PY'
from __future__ import annotations
import json, re, sys
from pathlib import Path

out = Path(sys.argv[1]); head=sys.argv[2]; branch=sys.argv[3]; dirty=sys.argv[4] == "true"
json_path=Path(sys.argv[5]); md_path=Path(sys.argv[6])

def read(name):
    p=out/f"{name}.txt"
    return p.read_text(errors="replace") if p.exists() else "UNKNOWN"

def rc(name):
    p=out/f"{name}.rc"
    try: return int(p.read_text().strip())
    except Exception: return 127

def load_json_text(name):
    txt=read(name).strip()
    try: return json.loads(txt)
    except Exception: return None

five=load_json_text("founder_daily_five")
metrics=(five or {}).get("metrics", {}) if isinstance(five, dict) else {}

def val(k):
    v=metrics.get(k, "UNKNOWN")
    return "UNKNOWN" if v is None else v

cash={
  "paid_revenue_events_today": val("1_new_paid_revenue_events_today"),
  "payment_received_real_total": val("2_payment_received_real_total"),
  "proof_packs_delivered_total": val("3_proof_packs_delivered_total"),
  "open_pipeline_real_leads": val("4_open_pipeline_leads_real"),
  "production_layers_pct": val("5_production_layers_pct"),
}

# Conservative action ranking: cash/proof/collections first, then pipeline, then production blockers.
actions=[]
def add(priority, area, action, evidence): actions.append({"priority":priority,"area":area,"action":action,"evidence":evidence})

pmt=cash["payment_received_real_total"]
proof=cash["proof_packs_delivered_total"]
pipeline=cash["open_pipeline_real_leads"]

if pmt in (0,"0","UNKNOWN"):
    add(1,"cash","Move one qualified company through discovery -> quote-only 30-day Revenue Command Pilot -> verified payment evidence.","founder_daily_five")
if proof in (0,"0","UNKNOWN"):
    add(2,"proof","Prepare/deliver the next evidence-backed Proof Pack only after real delivery evidence exists.","founder_daily_five / weekly_proof")
if pipeline in (0,"0","UNKNOWN"):
    add(3,"pipeline","Build/refresh qualified Saudi target accounts with source, reason, score, stage and next action; do not count synthetic rows.","founder_daily_five / growth_daily")
if rc("first_paid_gate") != 0:
    add(4,"close_path","Resolve the first-paid-customer gate blocker shown by founder_paid_launch_gate.py.","first_paid_gate")
if rc("railway_status") != 0:
    add(5,"production","Resolve Railway visibility/trust blocker before enabling growth automation that depends on production.","railway_status")
if not actions:
    add(1,"expansion","Prioritize expansion/retainer conversion from verified customer proof before adding new product surface.","daily metrics")

actions=sorted(actions,key=lambda x:x["priority"])[:5]

approval=[]
# Fixed safety posture: these always require founder approval.
for item, typ in [
    ("Send customer/prospect message","external_send"),
    ("Issue customer-specific commercial quote","commercial_commitment"),
    ("Request/capture payment","payment"),
    ("Publish external content","publish"),
    ("Merge to main or change production","production_change"),
]: approval.append({"item":item,"type":typ,"status":"approval_required"})

blob={
 "generated_at": out.name,
 "repository":{"head":head,"branch":branch,"dirty":dirty},
 "cash_truth":cash,
 "phase_0_1": {
   "verdict": (five or {}).get("phase_0_1_verdict","UNKNOWN") if isinstance(five,dict) else "UNKNOWN",
   "first_close_ready": (five or {}).get("first_close_ready","UNKNOWN") if isinstance(five,dict) else "UNKNOWN",
 },
 "top_actions":actions,
 "approval_queue":approval,
 "planning_scenarios": {
   "phase_a":{"qualified_accounts_month":20,"diagnostics":8,"discoveries":4,"pilot_proposals":2,"paid_pilots":1,"pilot_planning_band_sar":"7500-15000"},
   "phase_b":{"paid_pilots_month":2,"active_retainers":3,"retainer_planning_band_sar_month":"5000-10000","delivery_gross_margin_target":">=70%"},
   "phase_c":{"active_clients":"5-10","monthly_gross_margin_target":">=75% when sufficiently automated"},
   "label":"INTERNAL PLANNING ONLY — not booked revenue, public pricing, quote authority, tax advice, or customer commitment"
 },
 "source_return_codes": {n:rc(n) for n in ["founder_daily_five","ceo_master_plan","first_paid_gate","first_paid_tracker","commercial_value_map","phase_0_1_close","company_os_daily","growth_daily","self_improvement","weekly_proof","founder_cockpit","gh_prs","railway_status"]},
 "safety":{"live_send":False,"live_charge":False,"merge":False,"production_mutation":False,"cold_whatsapp":False,"fake_proof":False}
}
json_path.write_text(json.dumps(blob,ensure_ascii=False,indent=2)+"\n")

lines=[
"# Dealix Founder Money Command",
"",
f"- HEAD: `{head}`",
f"- Branch: `{branch}`",
f"- Dirty worktree: `{dirty}`",
"",
"## Cash truth",
]
for k,v in cash.items(): lines.append(f"- {k}: **{v}**")
lines += ["", "## Phase 0–1", f"- verdict: **{blob['phase_0_1']['verdict']}**", f"- first_close_ready: **{blob['phase_0_1']['first_close_ready']}**", "", "## TOP 5",]
for a in actions: lines.append(f"{a['priority']}. **{a['area']}** — {a['action']}  \n   Evidence: `{a['evidence']}`")
lines += ["", "## Approval queue"]
for a in approval: lines.append(f"- {a['item']} — `{a['status']}`")
lines += ["", "## Internal planning scenarios", "These are targets for prioritization only; they are not actual revenue or quote authority.", "- Phase A: 20 qualified accounts -> 8 diagnostics -> 4 discoveries -> 2 proposals -> 1 paid pilot; internal pilot planning band SAR 7.5k–15k after discovery.", "- Phase B: 2 paid pilots/month + 3 active retainers; internal retainer planning band SAR 5k–10k/month; delivery gross margin target >=70%.", "- Phase C: 5–10 active clients; target >=75% monthly gross margin where sufficiently automated.", "", "## Guardrails", "- Revenue requires verified payment evidence.", "- Commitments, invoices, pipeline and cash remain separate.", "- Unknown inputs remain UNKNOWN, never silently zero.", "- No send, publish, quote commitment, charge, merge or production mutation is executed by this command.", ""]
md_path.write_text("\n".join(lines))
PY

section "MONEY COMMAND"
cat "$MD"

echo
echo "REPORT_MD=$MD"
echo "REPORT_JSON=$JSON"
echo "DEALIX_FOUNDER_MONEY_COMMAND=COMPLETE"
