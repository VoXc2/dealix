#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
REPORT_ROOT="${DEALIX_MONEY_REPORT_ROOT:-${REPO_ROOT}/reports/founder_money_command}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="${REPORT_ROOT}/${STAMP}"
MD="${OUT_DIR}/money_command.md"
JSON="${OUT_DIR}/money_command.json"
PY_BOOTSTRAP="$REPO_ROOT/scripts/ops/ensure_founder_automation_python.sh"
PY="${DEALIX_AUTOMATION_PYTHON:-$REPO_ROOT/.venv/bin/python}"

mkdir -p "$OUT_DIR"

section() { printf '\n===== %s =====\n' "$*"; }

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "BLOCKED: Dealix repository not found at $REPO_ROOT"
  exit 20
fi

cd "$REPO_ROOT"
if [ ! -x "$PY_BOOTSTRAP" ]; then
  echo "BLOCKED: deterministic automation Python bootstrap missing: $PY_BOOTSTRAP"
  exit 21
fi
DEALIX_REPO_ROOT="$REPO_ROOT" "$PY_BOOTSTRAP"
if [ ! -x "$PY" ]; then
  echo "BLOCKED: deterministic automation Python missing after bootstrap: $PY"
  exit 22
fi
# Preserve the existing command contract while ensuring every legacy `python`
# invocation resolves to the repository-local verified runtime.
python() { "$PY" "$@"; }

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

run_py_if_exists founder_daily_five scripts/founder_daily_five_metrics.py --json
run_py_if_exists money_truth scripts/commercial/founder_money_truth.py
run_py_if_exists ceo_master_plan scripts/run_ceo_master_plan_status.py
run_py_if_exists first_paid_gate scripts/founder_paid_launch_gate.py
run_py_if_exists first_paid_tracker scripts/verify_first_paid_diagnostic_tracker.py
run_py_if_exists commercial_value_map scripts/commercial_value_map_status.py
run_py_if_exists phase_0_1_close scripts/phase_0_1_close_helper.py
run_py_if_exists commercial_intelligence scripts/commercial/verify_commercial_intelligence.py

if [ -x scripts/ops/dealix_founder_cockpit_full.sh ]; then
  run_capture founder_cockpit bash scripts/ops/dealix_founder_cockpit_full.sh --status-only
elif command -v dealix-cockpit-status >/dev/null 2>&1; then
  run_capture founder_cockpit dealix-cockpit-status
else
  echo "UNKNOWN: founder cockpit status surface unavailable" >"${OUT_DIR}/founder_cockpit.txt"
  echo 127 >"${OUT_DIR}/founder_cockpit.rc"
fi

# Existing autonomous loops are intentionally draft-only.
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
import json, sys
from pathlib import Path

out=Path(sys.argv[1]); head=sys.argv[2]; branch=sys.argv[3]; dirty=sys.argv[4]=="true"
json_path=Path(sys.argv[5]); md_path=Path(sys.argv[6])

def read(name):
    p=out/f"{name}.txt"
    return p.read_text(errors="replace") if p.exists() else "UNKNOWN"

def rc(name):
    p=out/f"{name}.rc"
    try: return int(p.read_text().strip())
    except Exception: return 127

def load_json(name):
    try: return json.loads(read(name).strip())
    except Exception: return None

five=load_json("founder_daily_five") or {}
truth=load_json("money_truth") or {}
metrics=five.get("metrics", {}) if isinstance(five, dict) else {}

def val(key):
    v=metrics.get(key, "UNKNOWN")
    return "UNKNOWN" if v is None else v

cash={
  "paid_revenue_events_today": val("1_new_paid_revenue_events_today"),
  "payment_received_real_total": val("2_payment_received_real_total"),
  "proof_packs_delivered_total": val("3_proof_packs_delivered_total"),
  "open_pipeline_real_leads": val("4_open_pipeline_leads_real"),
  "production_layers_pct": val("5_production_layers_pct"),
  "verified_cash_sar": truth.get("verified_cash_sar", "UNKNOWN"),
  "outstanding_collections_sar": truth.get("outstanding_collections_sar", "UNKNOWN"),
  "cash_on_hand_sar": truth.get("cash_on_hand_sar", "UNKNOWN"),
  "monthly_burn_sar": truth.get("monthly_burn_sar", "UNKNOWN"),
  "runway_months": truth.get("runway_months", "UNKNOWN"),
}

finance={
  "actual_gross_margin_pct": truth.get("gross_margin_actual_pct", "UNKNOWN"),
  "policy": truth.get("commercial_finance_policy", {"status":"UNKNOWN"}),
  "source_schema_has_cash_amount": truth.get("source_schema_has_cash_amount", False),
  "verified_invoice_event_count": truth.get("verified_invoice_event_count", "UNKNOWN"),
  "verified_collection_candidate_count": truth.get("verified_collection_candidate_count", "UNKNOWN"),
}

public_truth=truth.get("public_commercial_truth", {"status":"UNKNOWN","findings":[]})

actions=[]
def add(priority, area, action, evidence):
    actions.append({"priority":priority,"area":area,"action":action,"evidence":evidence})

for blocker in truth.get("top_blockers", []):
    rank={"P0":1,"P1":2,"P2":3}.get(blocker.get("priority"),4)
    add(rank, blocker.get("area","money_truth"), blocker.get("action","Review money-truth blocker."), "money_truth")

if rc("first_paid_gate") != 0:
    add(2,"close_path","Resolve the first-paid-customer gate blocker; do not bypass evidence requirements.","first_paid_gate")
if rc("commercial_intelligence") != 0:
    add(3,"commercial_intelligence","Repair or complete the canonical commercial intelligence verifier before trusting opportunity scoring.","commercial_intelligence")
if rc("railway_status") != 0:
    add(4,"production","Restore Railway visibility/trust before enabling automation that depends on production.","railway_status")
if not actions:
    add(1,"expansion","Use verified customer proof to prioritize renewal/retainer expansion before adding new product surface.","money_truth + founder_daily_five")

# Deduplicate by area/action and preserve highest priority.
seen=set(); unique=[]
for item in sorted(actions,key=lambda x:x["priority"]):
    key=(item["area"],item["action"])
    if key in seen: continue
    seen.add(key); unique.append(item)
actions=unique[:5]
for idx,item in enumerate(actions,1): item["priority"]=idx

approval=[
  {"item":"Send customer/prospect message","type":"external_send","status":"approval_required"},
  {"item":"Issue customer-specific commercial quote","type":"commercial_commitment","status":"approval_required"},
  {"item":"Request/capture payment","type":"payment","status":"approval_required"},
  {"item":"Publish external content","type":"publish","status":"approval_required"},
  {"item":"Merge to main or change production","type":"production_change","status":"approval_required"},
]

blob={
 "generated_at":out.name,
 "repository":{"head":head,"branch":branch,"dirty":dirty},
 "cash_truth":cash,
 "finance_truth":finance,
 "public_commercial_truth":public_truth,
 "phase_0_1":{
   "verdict":five.get("phase_0_1_verdict","UNKNOWN") if isinstance(five,dict) else "UNKNOWN",
   "first_close_ready":five.get("first_close_ready","UNKNOWN") if isinstance(five,dict) else "UNKNOWN",
 },
 "top_actions":actions,
 "approval_queue":approval,
 "planning_scenarios":{
   "phase_a":{"qualified_accounts_month":20,"diagnostics":8,"discoveries":4,"pilot_proposals":2,"paid_pilots":1,"pilot_planning_band_sar":"7500-15000"},
   "phase_b":{"paid_pilots_month":2,"active_retainers":3,"retainer_planning_band_sar_month":"5000-10000","delivery_gross_margin_target":">=70%"},
   "phase_c":{"active_clients":"5-10","monthly_gross_margin_target":">=75% when sufficiently automated"},
   "label":"INTERNAL PLANNING ONLY — not booked revenue, public pricing, quote authority, tax advice, or customer commitment"
 },
 "source_return_codes":{n:rc(n) for n in ["founder_daily_five","money_truth","ceo_master_plan","first_paid_gate","first_paid_tracker","commercial_value_map","phase_0_1_close","commercial_intelligence","company_os_daily","growth_daily","self_improvement","weekly_proof","founder_cockpit","gh_prs","railway_status"]},
 "safety":{"live_send":False,"live_charge":False,"quote_authority":False,"merge":False,"production_mutation":False,"cold_whatsapp":False,"fake_proof":False}
}
json_path.write_text(json.dumps(blob,ensure_ascii=False,indent=2)+"\n")

lines=["# Dealix Founder Money Command","",f"- HEAD: `{head}`",f"- Branch: `{branch}`",f"- Dirty worktree: `{dirty}`","","## Cash truth"]
for k,v in cash.items(): lines.append(f"- {k}: **{v}**")
lines += ["","## Finance truth",f"- actual_gross_margin_pct: **{finance['actual_gross_margin_pct']}**",f"- verified_invoice_event_count: **{finance['verified_invoice_event_count']}**",f"- verified_collection_candidate_count: **{finance['verified_collection_candidate_count']}**",f"- source_schema_has_cash_amount: **{finance['source_schema_has_cash_amount']}**",f"- finance_policy_status: **{finance['policy'].get('status','UNKNOWN')}**","","## Public commercial truth",f"- status: **{public_truth.get('status','UNKNOWN')}**",f"- findings: **{len(public_truth.get('findings',[]))}**",f"- authority: {public_truth.get('authority','UNKNOWN')}","","## Phase 0–1",f"- verdict: **{blob['phase_0_1']['verdict']}**",f"- first_close_ready: **{blob['phase_0_1']['first_close_ready']}**","","## TOP 5"]
for a in actions: lines.append(f"{a['priority']}. **{a['area']}** — {a['action']}  \n   Evidence: `{a['evidence']}`")
lines += ["","## Approval queue"]
for a in approval: lines.append(f"- {a['item']} — `{a['status']}`")
lines += ["","## Internal planning scenarios","Targets only; not actual revenue or quote authority.","- Phase A: 20 qualified accounts -> 8 diagnostics -> 4 discoveries -> 2 proposals -> 1 paid pilot; internal planning band SAR 7.5k–15k after discovery.","- Phase B: 2 paid pilots/month + 3 active retainers; internal planning band SAR 5k–10k/month; delivery gross margin target >=70%.","- Phase C: 5–10 active clients; target >=75% monthly gross margin when sufficiently automated.","","## Guardrails","- Payment event count is not cash amount unless a verified amount source exists.","- Invoice, commitment, pipeline and cash remain separate.","- Gross margin actual stays UNKNOWN without verified payment amount + delivery cost.","- Burn/runway stay UNKNOWN without an approved bank/accounting/spend source.","- No send, publish, quote commitment, charge, merge or production mutation is executed by this command.",""]
md_path.write_text("\n".join(lines))
PY

section "MONEY COMMAND"
cat "$MD"
echo
echo "REPORT_MD=$MD"
echo "REPORT_JSON=$JSON"
echo "DEALIX_FOUNDER_MONEY_COMMAND=COMPLETE"
