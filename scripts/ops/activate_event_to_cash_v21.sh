#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

###############################################################################
# DEALIX V21 — V18.1 ACTIVATE + TRUTH FIREWALL ROOT-CAUSE + EVENT WAR ROOM
#
# PURPOSE
#   1. Stop only stale foreground V18 Hermes calls.
#   2. Fetch exact current PR #1281 head and verify/activate V18.1.
#   3. Forensically remove the known founder/self-test from live runtime indexes
#      when (and only when) the source is untracked runtime state.
#   4. Preserve all audit/quarantine evidence and all tracked Git source.
#   5. Install a safe event-evidence inbox for Big 5 / LEAP field capture.
#   6. Write durable Event-to-Cash directive + receipt.
#
# DOES NOT
#   - merge main
#   - deploy production
#   - mutate DNS/DB/secrets
#   - create timer/cron/agent
#   - send email/WhatsApp/LinkedIn
#   - submit tender
#   - make payment
###############################################################################

[[ "$(id -u)" -eq 0 ]] || { echo "ERROR=RUN_AS_ROOT"; exit 20; }

RUN_USER=dealix
RUN_GROUP=dealix
RUN_HOME=/home/dealix
RUN_UID="$(id -u "$RUN_USER")"
REPO=/opt/dealix/workspace/dealix
REPO_SLUG=Dealix-sa/dealix
BRANCH=ops/revenue-portfolio-v18-server-control
WT=/opt/dealix/worktrees/v18-server-control-v21
CURRENT=/opt/dealix/company-os/current
FOUNDER=/opt/dealix/company-os/founder-os
PROMPTS=/opt/dealix/executive-prompts
PROOF_ROOT=/opt/dealix/executive-proof/v21-event-to-cash
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PROOF="$PROOF_ROOT/$STAMP"
LOCK=/run/lock/dealix-v21.lock
BAD_ID=5a6cd75618e385625ae8
BAD_MARKER_A='hige'
BAD_MARKER_B='text me'
REV=/usr/local/bin/dealix-revenue

install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 \
  /opt/dealix/worktrees "$CURRENT" "$FOUNDER" "$PROMPTS" "$PROOF"

exec 9>"$LOCK"
flock -n 9 || { echo "V21=SKIPPED_LOCKED"; exit 0; }

section(){ printf '\n================================================================\n %s\n================================================================\n' "$*"; }
as_dealix(){ runuser -u "$RUN_USER" -- env HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" XDG_RUNTIME_DIR="/run/user/$RUN_UID" PATH="$RUN_HOME/.local/bin:$RUN_HOME/.openclaw/bin:/usr/local/bin:/usr/bin:/bin" "$@"; }

###############################################################################
# 1. HOST / RUNTIME TRUTH
###############################################################################
section "1. HOST / RUNTIME TRUTH"
date -Is
hostname
FAILED_UNITS="$(systemctl --failed --no-legend --plain 2>/dev/null | awk 'NF{n++} END{print n+0}')"
echo "FAILED_SYSTEM_UNITS=$FAILED_UNITS"
for svc in docker ollama tailscaled hermes-dealix.service dealix-llm-router.service; do
  printf '%s=' "$svc"
  systemctl is-active "$svc" 2>/dev/null || true
done

###############################################################################
# 2. STOP ONLY STALE FOREGROUND V18 HERMES
###############################################################################
section "2. FOREGROUND V18 HERMES GUARD"
: >"$PROOF/v18-foreground-before.txt"
pgrep -af 'DEALIX_V18_REVENUE_PORTFOLIO_CONTROL_PLANE\.md' \
  >"$PROOF/v18-foreground-before.txt" 2>/dev/null || true
cat "$PROOF/v18-foreground-before.txt" || true
KILLED=0
while read -r pid rest; do
  [[ "${pid:-}" =~ ^[0-9]+$ ]] || continue
  cmd="$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null || true)"
  [[ -n "$cmd" ]] || continue
  if grep -q 'DEALIX_V18_REVENUE_PORTFOLIO_CONTROL_PLANE.md' <<<"$cmd" && \
     ! grep -qE 'hermes-dealix|gateway' <<<"$cmd"; then
    kill -TERM "$pid" 2>/dev/null || true
    KILLED=$((KILLED+1))
  fi
done <"$PROOF/v18-foreground-before.txt"
sleep 1
echo "STALE_V18_FOREGROUND_PROCESSES_TERMINATED=$KILLED"
echo "PERSISTENT_HERMES_SERVICE=$(systemctl is-active hermes-dealix.service 2>/dev/null || true)"

###############################################################################
# 3. FETCH + VERIFY EXACT UPDATED PR #1281
###############################################################################
section "3. ACTIVATE EXACT PR1281 V18.1"
as_dealix git -C "$REPO" fetch --quiet origin "$BRANCH"
PR1281_HEAD="$(as_dealix git -C "$REPO" rev-parse "origin/$BRANCH")"
echo "PR1281_HEAD=$PR1281_HEAD"

if [[ -d "$WT" ]]; then
  as_dealix git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true
fi
as_dealix git -C "$REPO" worktree add --detach "$WT" "$PR1281_HEAD" \
  >"$PROOF/worktree.txt" 2>&1

python3 "$WT/scripts/ops/verify_revenue_portfolio_v18_server_control.py" \
  | tee "$PROOF/v18-verifier.txt"

DEALIX_REPO_ROOT="$REPO" \
  timeout 300 bash "$WT/scripts/ops/activate_revenue_portfolio_v18.sh" \
  | tee "$PROOF/v18-activation.txt"

V18_STATUS="$CURRENT/REVENUE_PORTFOLIO_V18_STATUS.json"
[[ -s "$V18_STATUS" ]] || { echo "ERROR=V18_STATUS_NOT_WRITTEN"; exit 30; }
jq . "$V18_STATUS" | tee "$PROOF/v18-status.json"
AUTHORITY_MODE="$(jq -r '.active_commercial_authority_mode // "UNKNOWN"' "$V18_STATUS")"
echo "ACTIVE_COMMERCIAL_AUTHORITY_MODE=$AUTHORITY_MODE"

###############################################################################
# 4. BASELINE ECONOMIC TRUTH
###############################################################################
section "4. ECONOMIC TRUTH BEFORE ROOT-CAUSE CLEANUP"
[[ -x "$REV" ]] || { echo "ERROR=DEALIX_REVENUE_CLI_MISSING"; exit 31; }
for sub in today interactions candidates money; do
  set +e
  timeout 60 runuser -u "$RUN_USER" -- env \
    HOME="$RUN_HOME" \
    USER="$RUN_USER" \
    LOGNAME="$RUN_USER" \
    XDG_RUNTIME_DIR="/run/user/$RUN_UID" \
    PATH="$RUN_HOME/.local/bin:$RUN_HOME/.openclaw/bin:/usr/local/bin:/usr/bin:/bin" \
    "$REV" "$sub" >"$PROOF/before-$sub.txt" 2>&1
  rc=$?
  set -e
  echo "BEFORE_${sub^^}_RC=$rc"
  tail -30 "$PROOF/before-$sub.txt" || true
done
REAL_CONTACTS_BEFORE="$(awk -F= '/^REAL_CONTACTS=/{v=$2} END{print (v==""?"UNKNOWN":v)}' "$PROOF/before-money.txt")"

###############################################################################
# 5. FIND SELF-TEST SOURCE BY ID OR UNIQUE FINGERPRINT
###############################################################################
section "5. SELF-TEST ROOT-CAUSE DISCOVERY"
SEARCH_ROOTS=(
  "$FOUNDER"
  /opt/dealix/company-os
  "$REPO/business/autonomy"
  "$REPO/business/commercial"
)
: >"$PROOF/selftest-candidates.txt"
for root in "${SEARCH_ROOTS[@]}"; do
  [[ -e "$root" ]] || continue
  rg --hidden --no-messages --files-with-matches --fixed-strings "$BAD_ID" "$root" \
    >>"$PROOF/selftest-candidates.txt" || true
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    if grep -Fq "$BAD_MARKER_B" "$f" 2>/dev/null; then
      echo "$f" >>"$PROOF/selftest-candidates.txt"
    fi
  done < <(rg --hidden --no-messages --files-with-matches --fixed-strings "$BAD_MARKER_A" "$root" 2>/dev/null || true)
done
sort -u -o "$PROOF/selftest-candidates.txt" "$PROOF/selftest-candidates.txt"
cat "$PROOF/selftest-candidates.txt" || true

###############################################################################
# 6. SAFE QUARANTINE FROM LIVE INDEXES ONLY
###############################################################################
section "6. SAFE SELF-TEST QUARANTINE"
BACKUPS="$PROOF/selftest-backups"
mkdir -p "$BACKUPS"
: >"$PROOF/selftest-mutated.txt"
: >"$PROOF/selftest-preserved.txt"
: >"$PROOF/selftest-tracked-blockers.txt"
MUTATED=0
TRACKED=0
PRESERVED=0

is_mutable_runtime_path(){
  local f="$1"
  [[ "$f" == "$FOUNDER/big5-2026/"* ]] && return 0
  [[ "$f" == "$FOUNDER/event-intake/"* ]] && return 0
  [[ "$f" == "$FOUNDER/relationships/"* ]] && return 0
  [[ "$f" == "$FOUNDER/pipeline/"* ]] && return 0
  [[ "$f" == "$REPO/business/autonomy/"* ]] && return 0
  [[ "$f" == "$REPO/business/commercial/"* ]] && return 0
  return 1
}

while IFS= read -r file; do
  [[ -f "$file" ]] || continue

  case "$file" in
    "$FOUNDER/evidence/quarantined/"*|"$FOUNDER/evidence/rejected/"*|"$CURRENT/"*|*.md|*.log)
      echo "$file" >>"$PROOF/selftest-preserved.txt"
      PRESERVED=$((PRESERVED+1))
      continue
      ;;
  esac

  if [[ "$file" == "$REPO/"* ]]; then
    rel="${file#$REPO/}"
    if as_dealix git -C "$REPO" ls-files --error-unmatch "$rel" >/dev/null 2>&1; then
      echo "$rel" >>"$PROOF/selftest-tracked-blockers.txt"
      TRACKED=$((TRACKED+1))
      continue
    fi
  fi

  if ! is_mutable_runtime_path "$file"; then
    echo "$file" >>"$PROOF/selftest-preserved.txt"
    PRESERVED=$((PRESERVED+1))
    continue
  fi

  case "$file" in
    *.json|*.jsonl|*.csv|*.tsv|*.txt)
      backup_name="$(printf '%s' "$file" | sed 's#^/##; s#/#__#g')"
      cp -a "$file" "$BACKUPS/$backup_name"

      python3 - "$file" "$BAD_ID" "$BAD_MARKER_A" "$BAD_MARKER_B" <<'PY'
import json, pathlib, sys
path = pathlib.Path(sys.argv[1])
bad, a, b = sys.argv[2:]
raw = path.read_text(errors="replace")

def contaminated(obj):
    try:
        s = json.dumps(obj, ensure_ascii=False).lower()
    except Exception:
        s = str(obj).lower()
    return bad.lower() in s or (a.lower() in s and b.lower() in s)

def clean(obj, top=False):
    if isinstance(obj, list):
        return [clean(x) for x in obj if not contaminated(x)]
    if isinstance(obj, dict):
        if top and contaminated(obj):
            out = dict(obj)
            out.update({
                "synthetic_or_self_test": True,
                "do_not_count": True,
                "real_interaction": False,
                "real_contact": False,
                "warm": False,
                "qualified": False,
                "paid": False,
                "revenue_sar": 0,
                "state": "SELF_TEST_QUARANTINED",
            })
            return out
        out = {}
        for k, v in obj.items():
            if contaminated(v):
                if isinstance(v, (list, dict)):
                    out[k] = clean(v)
                continue
            out[k] = clean(v)
        return out
    return obj

suffix = path.suffix.lower()
if suffix == ".json":
    try:
        data = json.loads(raw)
        new = json.dumps(clean(data, top=True), ensure_ascii=False, indent=2) + "\n"
    except Exception:
        new = "\n".join(x for x in raw.splitlines() if not (bad in x or (a in x and b in x))) + "\n"
elif suffix == ".jsonl":
    rows=[]
    for line in raw.splitlines():
        try:
            obj=json.loads(line)
            if contaminated(obj):
                continue
            rows.append(json.dumps(obj, ensure_ascii=False))
        except Exception:
            if bad not in line and not (a in line and b in line): rows.append(line)
    new="\n".join(rows) + ("\n" if rows else "")
else:
    rows=[x for x in raw.splitlines() if bad not in x and not (a in x and b in x)]
    new="\n".join(rows) + ("\n" if rows else "")

tmp=path.with_name(path.name + ".v21.tmp")
tmp.write_text(new, encoding="utf-8")
tmp.replace(path)
PY
      echo "$file" >>"$PROOF/selftest-mutated.txt"
      MUTATED=$((MUTATED+1))
      ;;
    *)
      echo "$file" >>"$PROOF/selftest-preserved.txt"
      PRESERVED=$((PRESERVED+1))
      ;;
  esac
done <"$PROOF/selftest-candidates.txt"

echo "SELF_TEST_RUNTIME_FILES_MUTATED=$MUTATED"
echo "SELF_TEST_TRACKED_SOURCE_BLOCKERS=$TRACKED"
echo "SELF_TEST_EVIDENCE_PRESERVED=$PRESERVED"
cat "$PROOF/selftest-mutated.txt" || true

###############################################################################
# 7. RE-PROVE ECONOMIC TRUTH
###############################################################################
section "7. ECONOMIC TRUTH AFTER ROOT-CAUSE CLEANUP"
for sub in today interactions candidates money; do
  set +e
  timeout 60 runuser -u "$RUN_USER" -- env \
    HOME="$RUN_HOME" \
    USER="$RUN_USER" \
    LOGNAME="$RUN_USER" \
    XDG_RUNTIME_DIR="/run/user/$RUN_UID" \
    PATH="$RUN_HOME/.local/bin:$RUN_HOME/.openclaw/bin:/usr/local/bin:/usr/bin:/bin" \
    "$REV" "$sub" >"$PROOF/after-$sub.txt" 2>&1
  rc=$?
  set -e
  echo "AFTER_${sub^^}_RC=$rc"
  tail -30 "$PROOF/after-$sub.txt" || true
done

REAL_CONTACTS="$(awk -F= '/^REAL_CONTACTS=/{v=$2} END{print (v==""?"UNKNOWN":v)}' "$PROOF/after-money.txt")"
VERIFIED_PAID_PILOTS="$(awk -F= '/^VERIFIED_PAID_PILOTS=/{v=$2} END{print (v==""?"UNKNOWN":v)}' "$PROOF/after-money.txt")"
VERIFIED_REVENUE_SAR="$(awk -F= '/^VERIFIED_REVENUE_SAR=/{v=$2} END{print (v==""?"UNKNOWN":v)}' "$PROOF/after-money.txt")"
INTERACTION_ROWS="$(awk -F'\t' 'NF>=3{c++} END{print c+0}' "$PROOF/after-interactions.txt")"
CANDIDATE_ROWS="$(awk -F'\t' 'NF>=3{c++} END{print c+0}' "$PROOF/after-candidates.txt")"
TRUTH_FIREWALL=PASS
if [[ "$REAL_CONTACTS" == "0" ]] && { [[ "$INTERACTION_ROWS" -gt 0 ]] || [[ "$CANDIDATE_ROWS" -gt 0 ]]; }; then
  TRUTH_FIREWALL=BLOCKED_UNVERIFIED_MARKERS_STILL_VISIBLE
fi
if grep -Fiq "$BAD_MARKER_A" "$PROOF/after-interactions.txt" "$PROOF/after-candidates.txt" 2>/dev/null || \
   grep -Fiq "$BAD_MARKER_B" "$PROOF/after-interactions.txt" "$PROOF/after-candidates.txt" 2>/dev/null; then
  TRUTH_FIREWALL=BLOCKED_SELF_TEST_FINGERPRINT_STILL_VISIBLE
fi

echo "TRUTH_FIREWALL=$TRUTH_FIREWALL"
echo "REAL_CONTACTS=$REAL_CONTACTS"
echo "VERIFIED_PAID_PILOTS=$VERIFIED_PAID_PILOTS"
echo "VERIFIED_REVENUE_SAR=$VERIFIED_REVENUE_SAR"

###############################################################################
# 8. SAFE FIELD EVIDENCE INTAKE — STAGING ONLY
###############################################################################
section "8. FIELD EVIDENCE INTAKE"
INTAKE_ROOT="$FOUNDER/event-intake"
INBOX="$INTAKE_ROOT/inbox"
REJECTED="$INTAKE_ROOT/rejected"
install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 "$INBOX" "$REJECTED"

cat >/usr/local/bin/dealix-event-intake <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
umask 027
ROOT=/opt/dealix/company-os/founder-os/event-intake
INBOX="$ROOT/inbox"
REJECTED="$ROOT/rejected"
mkdir -p "$INBOX" "$REJECTED"

read -r -p 'Event/source [Big5|LEAP|Referral|Inbound|Other]: ' source
read -r -p 'Company: ' company
read -r -p 'Person: ' person
read -r -p 'Role: ' role
read -r -p 'Problem actually discussed: ' problem
read -r -p 'Current workflow / handling: ' workflow
read -r -p 'Interest [none|low|medium|high]: ' interest
read -r -p 'Follow-up permission [yes|no|unknown]: ' followup
read -r -p 'Agreed next action: ' next_action

interest="${interest,,}"
followup="${followup,,}"
case "$interest" in none|low|medium|high) ;; *) echo 'REJECT=INVALID_INTEREST'; exit 20;; esac
case "$followup" in yes|no|unknown) ;; *) echo 'REJECT=INVALID_FOLLOWUP_PERMISSION'; exit 21;; esac
[[ -n "$source" && -n "$company" && -n "$person" && -n "$problem" ]] || { echo 'REJECT=MISSING_REQUIRED_EVIDENCE'; exit 22; }
case "${company,,}" in dealix|dealix-sa|"dealix sa") echo 'REJECT=SELF_TEST_COMPANY'; exit 23;; esac
case "${person,,}" in founder) echo 'REJECT=SELF_TEST_PERSON'; exit 24;; esac

id="$(date -u +%Y%m%dT%H%M%SZ)-$(printf '%s|%s|%s' "$company" "$person" "$problem" | sha256sum | cut -c1-12)"
out="$INBOX/$id.json"
python3 - "$out" "$id" "$source" "$company" "$person" "$role" "$problem" "$workflow" "$interest" "$followup" "$next_action" <<'PY'
import json,sys
from datetime import datetime,timezone
(out,eid,source,company,person,role,problem,workflow,interest,followup,next_action)=sys.argv[1:]
data={
 'schema':'dealix.event-evidence-staging.v1',
 'evidence_id':eid,
 'captured_at':datetime.now(timezone.utc).isoformat(),
 'source':source,'company':company,'person':person,'role':role,
 'problem_evidence':problem,'current_workflow':workflow,'interest':interest,
 'followup_permission':followup,'agreed_next_action':next_action,
 'state':'STAGED_UNVERIFIED','real_relationship':False,'qualified':False,
 'customer':False,'paid':False,'revenue_sar':0,
 'promotion_rule':'canonical_revenue_truth_review_required'
}
with open(out,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
PY
chown dealix:dealix "$out" 2>/dev/null || true
chmod 0640 "$out"
echo "STAGED_EVIDENCE=$id"
echo "FILE=$out"
echo 'STATE=STAGED_UNVERIFIED'
echo 'NEXT=canonical review/capture; this staging item does not count as relationship or revenue'
EOF
chmod 0755 /usr/local/bin/dealix-event-intake

cat >/usr/local/bin/dealix-event-queue <<'EOF'
#!/usr/bin/env bash
ROOT=/opt/dealix/company-os/founder-os/event-intake/inbox
shopt -s nullglob
files=("$ROOT"/*.json)
echo "STAGED_COUNT=${#files[@]}"
for f in "${files[@]}"; do jq -r '[.evidence_id,.source,.company,.person,.interest,.followup_permission,.state] | @tsv' "$f"; done
EOF
chmod 0755 /usr/local/bin/dealix-event-queue

echo 'FIELD_INTAKE=/usr/local/bin/dealix-event-intake'
echo 'FIELD_QUEUE=/usr/local/bin/dealix-event-queue'

###############################################################################
# 9. EVENT-TO-CASH DIRECTIVE
###############################################################################
section "9. EVENT-TO-CASH DIRECTIVE"
DIRECTIVE="$PROMPTS/DEALIX_V21_EVENT_TO_CASH.md"
cat >"$DIRECTIVE" <<'EOF'
# Dealix V21 — Live Event-to-Cash War Room

North Star: FIRST VERIFIED PAID PILOT.

## Window
Big 5 Construct Saudi: 30 Aug–2 Sep 2026, 16:00–22:00, ROSHN Front.
LEAP x DeepFest: 31 Aug–3 Sep 2026, RECC Malham; general admission 13:00–21:00.

## Truth firewall
Research != relationship.
Networking request observed != verified relationship.
Business card != consent.
Staged event evidence != canonical pipeline.
Draft != send.
Provider accepted != delivered.
Proposal != payment.
Payment proof is required for verified revenue.
Self-test never counts.

## Conversion
STAGED_FIELD_EVIDENCE
-> VALIDATE / DEDUPE / PROVENANCE
-> CANONICAL REVENUE CAPTURE
-> REAL INTERACTION
-> VERIFIED RELATIONSHIP
-> QUALIFIED PROBLEM
-> MINI DIAGNOSTIC
-> DISCOVERY
-> CUSTOMER-SPECIFIC PROPOSAL
-> ELIGIBILITY / APPROVAL
-> 30-DAY REVENUE COMMAND PILOT
-> PAYMENT EVIDENCE
-> DELIVERY
-> PROOF PACK
-> RENEW / EXPAND / REFERRAL

## Field objective
Optimize for meaningful conversations, not booth count.
For each real conversation record what was actually said, problem/workflow, stakeholder role, urgency, follow-up permission, next action and provenance.

## Active authority
Always resolve the active checkout before customer-facing execution. Draft PR #1276 is not active authority by itself. If active authority is channel-governed, consent/relationship/suppression/cadence/channel gates still decide recipient eligibility. Named quote/price, contract, tender, payment and sensitive commitments retain their specific gates.

## Systems
Use existing Dealix Company Brain / Opportunity / Approval / Proof / Revenue systems. `dealix-event-intake` is only an anti-corruption staging inbox for field evidence, not a new CRM or source of truth.
EOF
chown "$RUN_USER:$RUN_GROUP" "$DIRECTIVE"
chmod 0640 "$DIRECTIVE"

###############################################################################
# 10. DURABLE V21 RECEIPT
###############################################################################
section "10. V21 RECEIPT"
STATUS="$CURRENT/V21_EVENT_TO_CASH_STATUS.json"
python3 - "$STATUS" "$STAMP" "$PR1281_HEAD" "$AUTHORITY_MODE" "$FAILED_UNITS" "$KILLED" "$MUTATED" "$TRACKED" "$PRESERVED" "$TRUTH_FIREWALL" "$REAL_CONTACTS" "$VERIFIED_PAID_PILOTS" "$VERIFIED_REVENUE_SAR" <<'PY'
import json,sys
from datetime import datetime,timezone
(p,stamp,head,auth,failed,killed,mutated,tracked,preserved,firewall,contacts,pilots,revenue)=sys.argv[1:]
data={
 'schema':'dealix.v21.event-to-cash.v1','generated_at':datetime.now(timezone.utc).isoformat(),'run_id':stamp,
 'north_star':'FIRST_VERIFIED_PAID_PILOT','pr1281_head':head,'active_commercial_authority_mode':auth,
 'failed_system_units':int(failed),'stale_foreground_v18_terminated':int(killed),
 'self_test_cleanup':{'runtime_files_mutated':int(mutated),'tracked_source_blockers':int(tracked),'evidence_preserved':int(preserved),'truth_firewall':firewall},
 'economic_truth':{'real_contacts':contacts,'verified_paid_pilots':pilots,'verified_revenue_sar':revenue},
 'field_runtime':{'intake':'/usr/local/bin/dealix-event-intake','queue':'/usr/local/bin/dealix-event-queue','staging_is_canonical_pipeline':False},
 'infrastructure_freeze':True,
 'authority':{'new_timer':False,'new_cron':False,'new_agent':False,'external_send_from_v21':False,'merge_main':False,'production_mutation':False,'payment':False,'tender_submission':False},
 'next':'REAL_EVENT_INTERACTION_TO_VERIFIED_RELATIONSHIP_TO_DIAGNOSTIC_TO_DISCOVERY_TO_PAID_PILOT'
}
with open(p,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
PY
chown "$RUN_USER:$RUN_GROUP" "$STATUS"
chmod 0640 "$STATUS"
jq . "$STATUS" | tee "$PROOF/final-receipt.json"

cat >/usr/local/bin/dealix-v21-status <<'EOF'
#!/usr/bin/env bash
jq . /opt/dealix/company-os/current/V21_EVENT_TO_CASH_STATUS.json 2>/dev/null || true
echo
/usr/local/bin/dealix-event-queue 2>/dev/null || true
EOF
chmod 0755 /usr/local/bin/dealix-v21-status

###############################################################################
# 11. FINAL
###############################################################################
section "11. FINAL VERDICT"
echo 'DEALIX_V21=COMPLETE'
echo "PR1281_HEAD=$PR1281_HEAD"
echo "ACTIVE_COMMERCIAL_AUTHORITY_MODE=$AUTHORITY_MODE"
echo "FAILED_SYSTEM_UNITS=$FAILED_UNITS"
echo "STALE_V18_FOREGROUND_TERMINATED=$KILLED"
echo "SELF_TEST_RUNTIME_FILES_MUTATED=$MUTATED"
echo "SELF_TEST_TRACKED_SOURCE_BLOCKERS=$TRACKED"
echo "TRUTH_FIREWALL=$TRUTH_FIREWALL"
echo "REAL_CONTACTS=$REAL_CONTACTS"
echo "VERIFIED_PAID_PILOTS=$VERIFIED_PAID_PILOTS"
echo "VERIFIED_REVENUE_SAR=$VERIFIED_REVENUE_SAR"
echo 'FIELD_INTAKE=dealix-event-intake'
echo 'FIELD_QUEUE=dealix-event-queue'
echo 'NEW_TIMER=NO'
echo 'NEW_CRON=NO'
echo 'NEW_AGENT=NO'
echo 'EXTERNAL_SEND_FROM_V21=NO'
echo 'MERGE_MAIN=NO'
echo 'PRODUCTION_MUTATION=NO'
echo "STATUS=$STATUS"
echo "PROOF=$PROOF"
if [[ "$TRUTH_FIREWALL" == PASS ]]; then
  echo 'NEXT_PHASE=LIVE_BIG5_LEAP_EVENT_TO_CASH'
else
  echo 'NEXT_BLOCKER=CANONICAL_REVENUE_CAPTURE_CODE_PATH_REPAIR_REQUIRED'
fi
