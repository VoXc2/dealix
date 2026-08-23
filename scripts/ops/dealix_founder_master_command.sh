#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO_SLUG="${DEALIX_REPO_SLUG:-Dealix-sa/dealix}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
PROOF_ROOT="${DEALIX_EXECUTIVE_PROOF_ROOT:-/opt/dealix/executive-proof}"
PROMPT_ROOT="${DEALIX_EXECUTIVE_PROMPT_ROOT:-/opt/dealix/executive-prompts}"
LOG_ROOT="${DEALIX_LOG_ROOT:-/opt/dealix/logs}"
LOCK_FILE="${DEALIX_MASTER_LOCK:-/run/lock/dealix-founder-master.lock}"
STAMP="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="${PROOF_ROOT}/${STAMP}"
LOG_FILE="${LOG_ROOT}/founder-master-${STAMP}.log"
SUMMARY_MD="${RUN_DIR}/FOUNDER_MASTER_SUMMARY.md"
SUMMARY_JSON="${RUN_DIR}/founder_master_summary.json"
SYNC_MAIN="${DEALIX_SYNC_MAIN:-1}"
RUN_LOCAL_AI="${DEALIX_RUN_LOCAL_AI:-1}"
RUN_PROD_VERIFY="${DEALIX_RUN_PROD_VERIFY:-0}"
RUN_COMMERCIAL_GATE="${DEALIX_RUN_COMMERCIAL_GATE:-1}"
RUN_REVENUE_DAILY="${DEALIX_RUN_REVENUE_DAILY:-1}"
RUN_WEEKLY_PROOF="${DEALIX_RUN_WEEKLY_PROOF:-1}"
MAX_SECONDS="${DEALIX_COMMAND_TIMEOUT:-900}"

mkdir -p "$RUN_DIR" "$PROMPT_ROOT" "$LOG_ROOT"
chmod 0700 "$RUN_DIR" "$PROMPT_ROOT" 2>/dev/null || true
exec > >(tee -a "$LOG_FILE") 2>&1

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }
section() { printf '\n============================================================\n%s\n============================================================\n' "$*"; }
kv() { printf '%-34s %s\n' "$1" "$2"; }

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root on the Dealix VPS."
  exit 2
fi
if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing OS user: $RUN_USER"
  exit 3
fi
if [[ ! -d "$REPO/.git" ]]; then
  echo "BLOCKED: canonical Dealix repository missing at $REPO"
  exit 4
fi

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "BLOCKED: another Dealix Founder Master cycle is already running."
  exit 5
fi

# L5 kill switches. Internal analysis may run; external/irreversible actions stay closed.
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0
export DEALIX_LIVE_CHARGE=false
export DEALIX_AUTO_MERGE=false
export DEALIX_PRODUCTION_MUTATION=false
export AGENT_APPROVAL_MODE=required
export DEALIX_PROOF_MODE=verified_only

safe_capture() {
  local name="$1"; shift
  local out="${RUN_DIR}/${name}.txt"
  local rcfile="${RUN_DIR}/${name}.rc"
  log "RUN[$name]: $*"
  set +e
  timeout "$MAX_SECONDS" "$@" >"$out" 2>&1
  local rc=$?
  set -e
  printf '%s\n' "$rc" >"$rcfile"
  log "RC[$name]=$rc"
  return 0
}

safe_capture_user() {
  local name="$1"; shift
  local out="${RUN_DIR}/${name}.txt"
  local rcfile="${RUN_DIR}/${name}.rc"
  log "RUN_USER[$name]: $*"
  set +e
  timeout "$MAX_SECONDS" sudo -iu "$RUN_USER" bash -lc "$*" >"$out" 2>&1
  local rc=$?
  set -e
  printf '%s\n' "$rc" >"$rcfile"
  log "RC[$name]=$rc"
  return 0
}

find_hermes() {
  local candidate
  for candidate in \
    "/home/${RUN_USER}/.local/bin/hermes" \
    "/home/${RUN_USER}/.hermes/bin/hermes" \
    "/usr/local/bin/hermes" \
    "/usr/bin/hermes"
  do
    if [[ -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  sudo -iu "$RUN_USER" bash -lc 'command -v hermes 2>/dev/null || true'
}

read_repo_head() {
  sudo -iu "$RUN_USER" git -C "$REPO" rev-parse HEAD 2>/dev/null || true
}

resolve_github_main() {
  sudo -iu "$RUN_USER" gh api "repos/${REPO_SLUG}/commits/main" --jq '.sha' 2>/dev/null || true
}

section "DEALIX FOUNDER MASTER - SAFETY & IDENTITY"
kv "timestamp" "$STAMP"
kv "repo" "$REPO"
kv "proof_dir" "$RUN_DIR"
kv "log" "$LOG_FILE"
kv "NO_MERGE" "YES"
kv "NO_PRODUCTION_MUTATION" "YES"
kv "NO_DNS_MUTATION" "YES"
kv "NO_EXTERNAL_SEND" "YES"
kv "NO_PAYMENT" "YES"
kv "NO_FAKE_PROOF" "YES"

safe_capture_user github_auth 'gh auth status'
safe_capture_user github_identity 'gh api user --jq "{login:.login}"'
safe_capture_user github_repo "gh repo view ${REPO_SLUG} --json nameWithOwner,isPrivate,defaultBranchRef,url"

GITHUB_MAIN="$(resolve_github_main)"
LOCAL_BEFORE="$(read_repo_head)"
BRANCH_BEFORE="$(sudo -iu "$RUN_USER" git -C "$REPO" branch --show-current 2>/dev/null || true)"
DIRTY_BEFORE="false"
[[ -n "$(sudo -iu "$RUN_USER" git -C "$REPO" status --porcelain 2>/dev/null || true)" ]] && DIRTY_BEFORE="true"
kv "github_main" "${GITHUB_MAIN:-UNKNOWN}"
kv "local_head_before" "${LOCAL_BEFORE:-UNKNOWN}"
kv "branch_before" "${BRANCH_BEFORE:-UNKNOWN}"
kv "dirty_before" "$DIRTY_BEFORE"

section "1. SAFE MAIN SYNCHRONIZATION"
if [[ "$SYNC_MAIN" == "1" ]]; then
  if [[ -z "$GITHUB_MAIN" ]]; then
    echo "SYNC_MAIN=BLOCKED_GITHUB_MAIN_UNKNOWN"
  elif [[ "$LOCAL_BEFORE" == "$GITHUB_MAIN" && "$BRANCH_BEFORE" == "main" && "$DIRTY_BEFORE" == "false" ]]; then
    echo "SYNC_MAIN=ALREADY_CURRENT"
  elif [[ -x "$REPO/scripts/ops/activate_dealix_from_main.sh" ]]; then
    safe_capture activate_main env DEALIX_SOURCE_REF=main DEALIX_REPO_ROOT="$REPO" bash "$REPO/scripts/ops/activate_dealix_from_main.sh"
  else
    echo "SYNC_MAIN=BLOCKED_CANONICAL_ACTIVATOR_MISSING"
  fi
else
  echo "SYNC_MAIN=SKIPPED_BY_CONFIG"
fi

LOCAL_HEAD="$(read_repo_head)"
GITHUB_MAIN_AFTER="$(resolve_github_main)"
kv "github_main_after" "${GITHUB_MAIN_AFTER:-UNKNOWN}"
kv "local_head_after" "${LOCAL_HEAD:-UNKNOWN}"
if [[ -n "$GITHUB_MAIN_AFTER" && "$LOCAL_HEAD" == "$GITHUB_MAIN_AFTER" ]]; then
  echo "MAIN_SYNC_PROOF=PASS"
else
  echo "MAIN_SYNC_PROOF=DEGRADED"
fi

section "2. VPS / SECURITY / RESOURCE BASELINE"
safe_capture uname uname -a
safe_capture uptime uptime
safe_capture memory free -h
safe_capture swap swapon --show
safe_capture disk df -h / /opt
safe_capture system_failed systemctl --failed --no-pager
safe_capture tailscale systemctl is-active tailscaled
safe_capture tailscale_status tailscale status
safe_capture ssh systemctl is-active ssh
safe_capture ufw ufw status verbose
safe_capture fail2ban systemctl is-active fail2ban
safe_capture docker systemctl is-active docker
safe_capture docker_ps docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
safe_capture timers systemctl list-timers 'dealix-*' --all --no-pager

section "3. LOCAL AI - OLLAMA 8K TRUST"
safe_capture ollama_service systemctl is-active ollama
if curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "OLLAMA_API=PASS"
  safe_capture ollama_ps ollama ps
  safe_capture ollama_list ollama list
else
  echo "OLLAMA_API=DEGRADED"
fi
safe_capture ollama_unit systemctl cat ollama

section "4. N8N / OPENCLAW / HERMES CONTROL PLANE"
safe_capture n8n_ps docker ps --filter name=dealix-n8n --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
if docker ps --format '{{.Names}}' | grep -Fxq dealix-n8n; then
  safe_capture n8n_audit docker exec dealix-n8n n8n audit
fi

OPENCLAW="/home/${RUN_USER}/.openclaw/bin/openclaw"
if [[ -x "$OPENCLAW" ]]; then
  safe_capture_user openclaw_status '"$HOME/.openclaw/bin/openclaw" status --all'
  safe_capture_user openclaw_gateway '"$HOME/.openclaw/bin/openclaw" gateway status --require-rpc'
  safe_capture_user openclaw_channels '"$HOME/.openclaw/bin/openclaw" channels status --probe'
  safe_capture_user openclaw_security '"$HOME/.openclaw/bin/openclaw" security audit --deep'
else
  echo "OPENCLAW=UNKNOWN_NOT_INSTALLED"
fi

HERMES="$(find_hermes | tail -1)"
if [[ -n "$HERMES" && -x "$HERMES" ]]; then
  kv "hermes_binary" "$HERMES"
  safe_capture_user hermes_version "'$HERMES' --version || '$HERMES' version"
  safe_capture_user hermes_config "'$HERMES' config check"
  safe_capture_user hermes_guardrails "'$HERMES' config set terminal.cwd '$REPO' >/dev/null 2>&1 || true; '$HERMES' config set approvals.mode manual >/dev/null 2>&1 || true; '$HERMES' config set approvals.cron_mode deny >/dev/null 2>&1 || true; '$HERMES' config set checkpoints.enabled true >/dev/null 2>&1 || true; echo HERMES_GUARDRAILS=APPLIED"
else
  echo "HERMES=DEGRADED_NOT_FOUND"
fi

section "5. GITHUB EXECUTION / CI TRUTH"
safe_capture_user git_status "cd '$REPO' && git status -sb"
safe_capture_user git_recent "cd '$REPO' && git log -10 --oneline --decorate"
safe_capture_user gh_open_prs "gh pr list --repo '$REPO_SLUG' --state open --limit 50 --json number,title,isDraft,mergeable,headRefOid,updatedAt,url"
safe_capture_user gh_open_issues "gh issue list --repo '$REPO_SLUG' --state open --limit 50 --json number,title,labels,updatedAt,url"
safe_capture_user gh_runs "gh run list --repo '$REPO_SLUG' --limit 30 --json databaseId,name,event,status,conclusion,headSha,headBranch,createdAt,updatedAt,url"

section "6. RAILWAY READ-ONLY TRUST"
if sudo -iu "$RUN_USER" bash -lc 'command -v railway >/dev/null 2>&1'; then
  safe_capture_user railway_whoami 'railway whoami'
  safe_capture_user railway_status "cd '$REPO' && railway status"
  safe_capture_user railway_services "cd '$REPO' && railway service list"
else
  echo "RAILWAY=UNKNOWN_CLI_NOT_FOUND"
fi

section "7. CANONICAL REPOSITORY VERIFICATION"
if [[ -f "$REPO/Makefile" ]] && make -C "$REPO" -n prod-verify >/dev/null 2>&1; then
  if [[ "$RUN_PROD_VERIFY" == "1" ]]; then
    safe_capture_user prod_verify "cd '$REPO' && make prod-verify"
  else
    echo "PROD_VERIFY=AVAILABLE_SKIPPED_DEFAULT_HEAVY"
  fi
fi

if [[ "$RUN_COMMERCIAL_GATE" == "1" ]]; then
  if [[ -x "$REPO/scripts/verify_dealix_commercial_go_live.sh" ]]; then
    safe_capture_user commercial_go_live "cd '$REPO' && bash scripts/verify_dealix_commercial_go_live.sh"
  elif [[ -f "$REPO/scripts/verify_commercial_launch_ready.py" ]]; then
    safe_capture_user commercial_go_live "cd '$REPO' && python3 scripts/verify_commercial_launch_ready.py"
  else
    echo "COMMERCIAL_GATE=UNKNOWN_MISSING"
  fi
fi

if [[ -x "$REPO/scripts/dealix_local_stack_verify.sh" ]]; then
  safe_capture_user local_stack_verify "cd '$REPO' && bash scripts/dealix_local_stack_verify.sh"
fi
if [[ -f "$REPO/scripts/ops/verify_canonical_company_autopilot.py" ]]; then
  safe_capture_user canonical_autopilot "cd '$REPO' && python3 scripts/ops/verify_canonical_company_autopilot.py"
fi

section "8. CANONICAL REVENUE + MONEY COMMAND"
if [[ -x "$REPO/scripts/ops/dealix_canonical_revenue_cycle.sh" ]]; then
  safe_capture_user revenue_status "cd '$REPO' && DEALIX_REPO_ROOT='$REPO' bash scripts/ops/dealix_canonical_revenue_cycle.sh status"
  if [[ "$RUN_REVENUE_DAILY" == "1" ]]; then
    safe_capture_user revenue_daily "cd '$REPO' && DEALIX_REPO_ROOT='$REPO' bash scripts/ops/dealix_canonical_revenue_cycle.sh daily"
  fi
else
  echo "REVENUE_CYCLE=UNKNOWN_MISSING"
fi

if [[ -x "$REPO/scripts/ops/dealix_founder_money_command.sh" ]]; then
  safe_capture_user founder_money "cd '$REPO' && DEALIX_REPO_ROOT='$REPO' bash scripts/ops/dealix_founder_money_command.sh"
else
  echo "FOUNDER_MONEY=UNKNOWN_MISSING"
fi

section "9. PROOF + SELF-IMPROVEMENT LOOPS"
for spec in \
  "company_os_daily|scripts/commercial/run_company_os_daily.py|--client dealix --mode draft-only --limit 50" \
  "autonomous_growth|scripts/commercial/run_autonomous_growth_daily.py|--autonomy-level 3 --mode draft-only --limit 50" \
  "self_improvement|scripts/commercial/run_self_improvement_daily.py|--client dealix --mode draft-only" \
  "weekly_proof|scripts/commercial/run_weekly_proof_pack.py|--client dealix --mode draft-only"
do
  IFS='|' read -r name rel args <<<"$spec"
  if [[ -f "$REPO/$rel" ]]; then
    if [[ "$name" == "weekly_proof" && "$RUN_WEEKLY_PROOF" != "1" ]]; then
      echo "$name=SKIPPED_BY_CONFIG"
    else
      safe_capture_user "$name" "cd '$REPO' && python3 '$rel' $args"
    fi
  else
    echo "$name=UNKNOWN_MISSING"
  fi
done

section "10. EXECUTIVE AI SYNTHESIS - OPTIONAL, ONE-SHOT, NO TERMINAL TOOLS"
MASTER_PROMPT="$REPO/docs/ops/DEALIX_EXECUTIVE_AUTOPILOT_MASTER_PROMPT.md"
if [[ "$RUN_LOCAL_AI" == "1" && -n "$HERMES" && -x "$HERMES" && -f "$MASTER_PROMPT" ]]; then
  SYNTH_DIR="/home/${RUN_USER}/.cache/dealix-founder-master"
  install -d -o "$RUN_USER" -g "$RUN_USER" -m 0700 "$SYNTH_DIR"
  AI_CONTEXT="${SYNTH_DIR}/evidence-${STAMP}.txt"
  AI_PROMPT="${SYNTH_DIR}/synthesis-${STAMP}.prompt"
  : >"$AI_CONTEXT"
  for name in \
    system_failed memory disk openclaw_security git_status gh_open_prs gh_runs \
    railway_status railway_services commercial_go_live local_stack_verify canonical_autopilot \
    revenue_status revenue_daily founder_money company_os_daily autonomous_growth self_improvement weekly_proof
  do
    src="${RUN_DIR}/${name}.txt"
    if [[ -f "$src" ]]; then
      printf '\n===== %s =====\n' "$name" >>"$AI_CONTEXT"
      tail -40 "$src" >>"$AI_CONTEXT" 2>/dev/null || true
    fi
  done
  # Keep the one-shot request inside the confirmed 8K operating envelope.
  if [[ "$(wc -c <"$AI_CONTEXT")" -gt 24000 ]]; then
    tail -c 24000 "$AI_CONTEXT" >"${AI_CONTEXT}.trim"
    mv "${AI_CONTEXT}.trim" "$AI_CONTEXT"
  fi
  chown "$RUN_USER:$RUN_USER" "$AI_CONTEXT"
  chmod 0600 "$AI_CONTEXT"
  {
    cat <<__AI_PROMPT__
You are the Dealix executive synthesis layer.
You have NO terminal or mutation tools in this run. Use only the evidence embedded below.
Do not claim anything that is not supported by that evidence.

Operating contract summary:
- Historical plans are not execution proof.
- Synthetic/demo evidence never becomes real customer, payment, revenue, delivery, or production proof.
- Revenue is real only with verified payment evidence.
- Delivery is real only with delivery evidence.
- External send, publish, payment, merge, DNS, DB, secret, and production changes remain approval-gated.
- Public/commercial truth must follow the repository's canonical first-launch offer gate.

Return exactly these sections:
1. EXECUTED
2. EVIDENCE
3. TOP_5_NEXT_ACTIONS ranked by impact x urgency x ease x risk
4. APPROVAL_QUEUE (L5 only)
5. BLOCKED_AND_WHY
6. PROOF_GAPS
7. HIGHEST_NEXT_ACTION

Evidence bundle excerpt follows.
__AI_PROMPT__
    cat "$AI_CONTEXT"
  } >"$AI_PROMPT"
  chown "$RUN_USER:$RUN_USER" "$AI_PROMPT"
  chmod 0600 "$AI_PROMPT"

  log "RUN_USER[executive_ai]: Hermes chat one-shot with clarify-only tool schema"
  set +e
  timeout "$MAX_SECONDS" sudo -iu "$RUN_USER" env \
    PATH="/home/${RUN_USER}/.local/bin:/home/${RUN_USER}/.hermes/bin:/usr/local/bin:/usr/bin:/bin" \
    "$HERMES" chat -Q --ignore-rules --toolsets clarify --max-turns 1 --query-file "$AI_PROMPT" \
    >"${RUN_DIR}/executive_ai.txt" 2>&1
  EXECUTIVE_AI_RC=$?
  set -e
  printf '%s\n' "$EXECUTIVE_AI_RC" >"${RUN_DIR}/executive_ai.rc"
  log "RC[executive_ai]=$EXECUTIVE_AI_RC"
else
  echo "EXECUTIVE_AI=SKIPPED_OR_UNAVAILABLE"
fi

section "11. FINAL PROOF SYNTHESIS"
python3 - "$RUN_DIR" "$SUMMARY_JSON" "$SUMMARY_MD" "$REPO_SLUG" "$GITHUB_MAIN_AFTER" "$LOCAL_HEAD" <<'__PY_SUMMARY__'
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone

run = Path(sys.argv[1])
json_path = Path(sys.argv[2])
md_path = Path(sys.argv[3])
repo = sys.argv[4]
gh_main = sys.argv[5] or "UNKNOWN"
local = sys.argv[6] or "UNKNOWN"

def rc(name: str) -> int:
    p = run / f"{name}.rc"
    try:
        return int(p.read_text().strip())
    except Exception:
        return 127

def tail(name: str, n: int = 40) -> str:
    p = run / f"{name}.txt"
    if not p.exists():
        return ""
    lines = p.read_text(errors="replace").splitlines()
    return "\n".join(lines[-n:])

critical = [
    "github_auth", "github_repo", "git_status", "railway_status",
    "canonical_autopilot", "commercial_go_live", "revenue_status",
    "revenue_daily", "founder_money", "company_os_daily",
    "self_improvement", "weekly_proof",
]
statuses = {name: rc(name) for name in critical if (run / f"{name}.rc").exists()}
missing = [name for name in critical if not (run / f"{name}.rc").exists()]
failed = [name for name, code in statuses.items() if code != 0]
passed = [name for name, code in statuses.items() if code == 0]
heads_verified = gh_main != "UNKNOWN" and local != "UNKNOWN" and gh_main == local
overall = "PASS" if not failed and not missing and heads_verified else "DEGRADED"

blob = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "repository": repo,
    "github_main": gh_main,
    "local_head": local,
    "overall": overall,
    "passed": passed,
    "failed_or_blocked": failed,
    "missing_critical_evidence": missing,
    "return_codes": statuses,
    "safety": {
        "merge": False,
        "production_mutation": False,
        "dns_mutation": False,
        "external_send": False,
        "payment": False,
        "fake_proof": False,
        "cold_whatsapp": False,
    },
}
json_path.write_text(json.dumps(blob, ensure_ascii=False, indent=2) + "\n")

lines = [
    "# Dealix Founder Master - Proof Summary", "",
    f"- Overall: **{overall}**",
    f"- GitHub main: `{gh_main}`",
    f"- VPS local HEAD: `{local}`",
    f"- Passed bounded checks: **{len(passed)}**",
    f"- Failed/blocked bounded checks: **{len(failed)}**",
    f"- Missing critical evidence: **{len(missing)}**",
    "", "## Executed",
]
for name in passed:
    lines.append(f"- PASS - `{name}`")
if not passed:
    lines.append("- No bounded check recorded PASS.")
lines += ["", "## Failed / blocked"]
for name in failed:
    lines.append(f"- `{name}` - rc={statuses[name]}")
for name in missing:
    lines.append(f"- `{name}` - evidence missing")
if not failed and not missing:
    lines.append("- None in the bounded critical set.")
lines += [
    "", "## Safety boundary",
    "- NO merge to main.",
    "- NO production / DNS / DB / secret mutation.",
    "- NO external send or publish.",
    "- NO payment or live checkout.",
    "- NO fake proof; synthetic stays synthetic.",
    "", "## Evidence files",
]
for p in sorted(run.iterdir()):
    if p.is_file() and p.name != md_path.name:
        lines.append(f"- `{p.name}`")
if (run / "executive_ai.txt").exists():
    lines += ["", "## Executive AI synthesis", "```text", tail("executive_ai", 120), "```"]
if (run / "founder_money.txt").exists():
    lines += ["", "## Founder Money Command tail", "```text", tail("founder_money", 80), "```"]
lines += [
    "", "## Highest next action",
    "Use the first evidence-backed blocker from Executive AI synthesis; if unavailable, close the highest-priority failed or missing critical check without reducing a gate.", "",
]
md_path.write_text("\n".join(lines))
__PY_SUMMARY__

cat "$SUMMARY_MD"

section "12. FOUNDER SHORTCUTS"
cat > /usr/local/bin/dealix-master <<__MASTER_SHORTCUT__
#!/usr/bin/env bash
exec bash "$REPO/scripts/ops/dealix_founder_master_command.sh" "\$@"
__MASTER_SHORTCUT__
chmod 0755 /usr/local/bin/dealix-master

cat > /usr/local/bin/dealix-proof <<'__PROOF_SHORTCUT__'
#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="/opt/dealix/executive-proof"
latest="$(find "$ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [[ -z "$latest" ]]; then
  echo "No Dealix executive proof bundle found."
  exit 1
fi
cat "$latest/FOUNDER_MASTER_SUMMARY.md" 2>/dev/null || find "$latest" -maxdepth 1 -type f -print
__PROOF_SHORTCUT__
chmod 0755 /usr/local/bin/dealix-proof

cat <<__FINAL__

============================================================
DEALIX FOUNDER MASTER COMPLETE
============================================================
OVERALL_SUMMARY=$SUMMARY_MD
PROOF_DIR=$RUN_DIR
LOG=$LOG_FILE
GITHUB_MAIN=${GITHUB_MAIN_AFTER:-UNKNOWN}
LOCAL_HEAD=${LOCAL_HEAD:-UNKNOWN}

Founder commands:
  dealix-master
  dealix-proof

Optional heavy verification:
  DEALIX_RUN_PROD_VERIFY=1 dealix-master

Read-only / no-sync cycle:
  DEALIX_SYNC_MAIN=0 dealix-master

Hard safety boundary:
  NO_MERGE=YES
  NO_PRODUCTION_MUTATION=YES
  NO_DNS_MUTATION=YES
  NO_EXTERNAL_SEND=YES
  NO_PAYMENT=YES
  NO_FAKE_PROOF=YES
============================================================
__FINAL__
