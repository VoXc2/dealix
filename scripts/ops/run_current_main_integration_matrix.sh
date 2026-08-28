#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Dealix current-main integration acceptance harness.
# L0-L4 only. It never merges main, deploys production, publishes, sends customer
# messages, mutates DNS/DB/secrets, or spends money.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_GROUP="${DEALIX_RUN_GROUP:-dealix}"
RUN_HOME="${DEALIX_RUN_HOME:-/home/dealix}"
PY="${DEALIX_PYTHON:-$REPO/.venv/bin/python}"
[[ -x "$PY" ]] || PY=/usr/bin/python3

BR1301="fix/current-main-truth-repair-20260828"
BR1297="feat/growth-council-morning-command-20260828"
BR1298="fix/public-commercial-truth-current-main-20260828"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
WTROOT="/opt/dealix/worktrees/current-main-matrix-$STAMP"
PROOF="/opt/dealix/executive-proof/current-main-matrix/$STAMP"
CURRENT="/opt/dealix/company-os/current"
FAIL=0

section() {
  printf '\n================================================================\n %s\n================================================================\n' "$*"
}

as_dealix() {
  runuser -u "$RUN_USER" -- env \
    HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" \
    PATH="$RUN_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    "$@"
}

gitd() { as_dealix git "$@"; }
fail() { echo "FAIL=$*"; FAIL=$((FAIL+1)); }

cleanup() {
  set +e
  for wt in "$WTROOT/1301" "$WTROOT/1297" "$WTROOT/1298"; do
    [[ -e "$wt" || -L "$wt" ]] && gitd -C "$REPO" worktree remove --force "$wt" >/dev/null 2>&1
  done
  gitd -C "$REPO" worktree prune >/dev/null 2>&1
}
trap cleanup EXIT

section "1. PRECONDITIONS"
[[ "$(id -u)" -eq 0 ]] || { echo "ERROR=RUN_AS_ROOT"; exit 10; }
[[ -d "$REPO/.git" ]] || { echo "ERROR=REPO_NOT_FOUND"; exit 11; }

install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 /opt/dealix/worktrees
install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 "$WTROOT"
install -d -o root -g "$RUN_GROUP" -m 0750 "$PROOF" "$CURRENT"
runuser -u "$RUN_USER" -- test -x "$WTROOT" || { echo "ERROR=WORKTREE_PARENT_NOT_TRAVERSABLE"; exit 12; }

echo "WORKTREE_PARENT=$(stat -c '%U:%G %a' "$WTROOT")"
echo "ACCEPTANCE_HARNESS_PERMISSION=PASS"

section "2. SOURCE TRUTH"
as_dealix gh auth status >/dev/null || { echo "ERROR=GH_AUTH"; exit 13; }
as_dealix gh auth setup-git >/dev/null 2>&1 || true

gitd -C "$REPO" fetch origin main "$BR1301" "$BR1297" "$BR1298"
MAIN="$(gitd -C "$REPO" rev-parse origin/main)"
H1301="$(gitd -C "$REPO" rev-parse origin/$BR1301)"
H1297="$(gitd -C "$REPO" rev-parse origin/$BR1297)"
H1298="$(gitd -C "$REPO" rev-parse origin/$BR1298)"

printf 'MAIN=%s\nPR1301=%s\nPR1297=%s\nPR1298=%s\n' "$MAIN" "$H1301" "$H1297" "$H1298" | tee "$PROOF/source-truth.txt"

make_wt() {
  local name="$1" wt="$WTROOT/$name"
  gitd -C "$REPO" worktree add --detach "$wt" origin/main >/dev/null
  [[ "$(stat -c '%U' "$wt")" == "$RUN_USER" ]] || { echo "ERROR=WORKTREE_OWNER:$name"; exit 20; }
  printf '%s\n' "$wt"
}

merge_ref() {
  local wt="$1" ref="$2"
  gitd -C "$wt" -c user.name='Dealix Acceptance Operator' -c user.email='dealix-bot@users.noreply.github.com' merge --no-ff --no-edit "$ref"
}

verify() {
  local wt="$1" script="$2"
  if [[ ! -f "$wt/$script" ]]; then
    echo "SKIP_NOT_PRESENT=$script" | tee -a "$PROOF/verifiers.log"
    return 0
  fi
  set +e
  (cd "$wt" && as_dealix "$PY" "$script") 2>&1 | tee -a "$PROOF/verifiers.log"
  local rc=${PIPESTATUS[0]}
  set -e
  echo "VERIFY=$script RC=$rc" | tee -a "$PROOF/verifiers.log"
  [[ "$rc" -eq 0 ]] || fail "$script:$rc"
}

section "3. PR1301 ON CURRENT MAIN"
WT1301="$(make_wt 1301)"
merge_ref "$WT1301" "origin/$BR1301"
verify "$WT1301" scripts/verify_brand_authority.py
verify "$WT1301" scripts/verify_hubspot_mirror_contract.py
verify "$WT1301" scripts/verify_brand_distribution_wave2.py
verify "$WT1301" scripts/verify_marketing_distribution_os.py
verify "$WT1301" scripts/verify_marketing_attribution_contract.py
verify "$WT1301" scripts/verify_public_marketing_surface.py
verify "$WT1301" scripts/ops/verify_revenue_portfolio_v18_server_control.py

section "4. PR1297 + PR1301"
WT1297="$(make_wt 1297)"
merge_ref "$WT1297" "origin/$BR1301"
merge_ref "$WT1297" "origin/$BR1297"
verify "$WT1297" scripts/verify_brand_authority.py
verify "$WT1297" scripts/verify_hubspot_mirror_contract.py
verify "$WT1297" scripts/verify_growth_council_morning_command.py
verify "$WT1297" scripts/verify_brand_distribution_wave2.py
verify "$WT1297" scripts/verify_marketing_distribution_os.py
verify "$WT1297" scripts/verify_marketing_attribution_contract.py
verify "$WT1297" scripts/verify_public_marketing_surface.py

if [[ -f "$WT1297/scripts/generate_morning_revenue_command.py" ]]; then
  set +e
  (cd "$WT1297" && as_dealix "$PY" scripts/generate_morning_revenue_command.py --stdout) 2>&1 | tee "$PROOF/morning-command.txt"
  rc=${PIPESTATUS[0]}; set -e
  [[ "$rc" -eq 0 ]] || fail "morning-command:$rc"
fi

if [[ -f "$WT1297/scripts/run_dealix_daily_ops.py" ]]; then
  set +e
  (cd "$WT1297" && as_dealix "$PY" scripts/run_dealix_daily_ops.py --dry-run) 2>&1 | tee "$PROOF/daily-ops.txt"
  rc=${PIPESTATUS[0]}; set -e
  [[ "$rc" -eq 0 ]] || fail "daily-ops:$rc"
fi

section "5. PR1298 + PR1301"
WT1298="$(make_wt 1298)"
merge_ref "$WT1298" "origin/$BR1301"
merge_ref "$WT1298" "origin/$BR1298"
verify "$WT1298" scripts/verify_brand_authority.py
verify "$WT1298" scripts/verify_hubspot_mirror_contract.py
verify "$WT1298" scripts/verify_public_marketing_surface.py
verify "$WT1298" scripts/verify_marketing_distribution_os.py
verify "$WT1298" scripts/verify_marketing_attribution_contract.py

WEB="$WT1298/apps/web"
if [[ -f "$WEB/package.json" && -f "$WEB/package-lock.json" ]]; then
  set +e
  (cd "$WEB" && as_dealix npm ci) >"$PROOF/npm-ci.log" 2>&1
  rc=$?; set -e
  echo "NPM_CI_RC=$rc"
  if [[ "$rc" -eq 0 ]]; then
    if (cd "$WEB" && as_dealix npm run 2>/dev/null | grep -qE '(^|[[:space:]])typecheck'); then
      set +e; (cd "$WEB" && as_dealix npm run typecheck) >"$PROOF/typecheck.log" 2>&1; trc=$?; set -e
      [[ "$trc" -eq 0 ]] || fail "typecheck:$trc"
    fi
    set +e; (cd "$WEB" && as_dealix npm run build) >"$PROOF/build.log" 2>&1; brc=$?; set -e
    [[ "$brc" -eq 0 ]] || fail "next-build:$brc"
  else
    fail "npm-ci:$rc"
  fi
else
  fail "web-lockfiles-missing"
fi

section "6. OPTIONAL EXISTING SECURITY TOOLS"
for tool in actionlint zizmor syft trivy osv-scanner; do
  command -v "$tool" >/dev/null 2>&1 && echo "$tool=AVAILABLE" || echo "$tool=ABSENT_NO_AUTO_INSTALL"
done
if command -v actionlint >/dev/null 2>&1; then
  set +e; (cd "$WT1301" && as_dealix actionlint) >"$PROOF/actionlint.log" 2>&1; arc=$?; set -e
  [[ "$arc" -eq 0 ]] || fail "actionlint:$arc"
fi

section "7. READ-ONLY PUBLIC HEALTH"
set +e
HTTP="$(curl -L -sS --connect-timeout 5 --max-time 15 -o "$PROOF/public-root.html" -w '%{http_code}' https://dealix.me/)"
crc=$?
set -e
printf 'PUBLIC_ROOT_HTTP=%s CURL_RC=%s\n' "$HTTP" "$crc"
[[ "$crc" -eq 0 && "$HTTP" == 200 ]] || fail "public-root:$crc/$HTTP"

section "8. RECEIPT"
VERDICT=PASS
[[ "$FAIL" -eq 0 ]] || VERDICT=BLOCKED
"$PY" - "$PROOF/receipt.json" "$VERDICT" "$FAIL" "$MAIN" "$H1301" "$H1297" "$H1298" "$HTTP" <<'PY'
import json, sys
from datetime import datetime, timezone
from pathlib import Path
out, verdict, failures, main, p1301, p1297, p1298, http = sys.argv[1:]
payload = {
  "schema": "dealix.current-main-integration-matrix.v1",
  "generated_at": datetime.now(timezone.utc).isoformat(),
  "verdict": verdict,
  "failure_count": int(failures),
  "main": main,
  "prs": {"1301": p1301, "1297": p1297, "1298": p1298},
  "public_root_http": http,
  "north_star": "FIRST_VERIFIED_PAID_DEALIX_PILOT",
  "infrastructure_freeze": True,
  "truth": {
    "research_is_relationship": False,
    "crm_is_commercial_truth": False,
    "analytics_is_payment": False,
    "proposal_is_revenue": False,
    "invoice_is_payment": False,
    "verified_revenue_requires_payment_evidence": True
  },
  "authority": {
    "l0_l4_internal": True,
    "merge_main": False,
    "production_mutation": False,
    "external_send": False,
    "public_publish": False,
    "payment_spend": False
  }
}
Path(out).write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
PY
cat "$PROOF/receipt.json"
install -m 0640 "$PROOF/receipt.json" "$CURRENT/CURRENT_MAIN_INTEGRATION_ACCEPTANCE.json"

echo "FINAL_VERDICT=$VERDICT"
echo "FAIL_COUNT=$FAIL"
echo "PROOF=$PROOF"
echo "MERGE_MAIN=NO"
echo "PRODUCTION_DEPLOY=NO"
echo "EXTERNAL_SEND=NO"
echo "PUBLIC_PUBLISH=NO"
echo "PAYMENT_SPEND=NO"

[[ "$FAIL" -eq 0 ]] || exit 1
