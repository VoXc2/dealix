#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPORT_ROOT="/opt/dealix/company-agents/reports"
OPENCLAW="/home/dealix/.openclaw/bin/openclaw"
HERMES="/home/dealix/.local/bin/hermes"

redact_stream() {
  python3 -u -c '
import re, sys
patterns = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"(?i)\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*)\s*[=:]\s*[^\s]+"),
]
email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
phone = re.compile(r"(?<!\d)(?:\+?966|0)?5\d{8}(?!\d)")
for line in sys.stdin:
    for p in patterns:
        if p.groups:
            line = p.sub(lambda m: f"{m.group(1)}[REDACTED]", line)
        else:
            line = p.sub("[REDACTED]", line)
    line = re.sub(r"(?i)([?&](?:token|key|secret|password|signature)=)[^&\s]+", r"\1[REDACTED]", line)
    line = email.sub("[EMAIL_REDACTED]", line)
    line = phone.sub("[PHONE_REDACTED]", line)
    sys.stdout.write(line)
'
}

safe_run() {
  set +e
  "$@" 2>&1 | redact_stream
  local rc=${PIPESTATUS[0]}
  set -e
  return "$rc"
}

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

FAIL=0

echo "===== DEALIX COMPANY AGENTS LIVE VERIFICATION ====="
echo "time=$(date -Is)"
echo "host=$(hostname)"

echo
echo "===== 1. COUNCIL TIMER ====="
printf 'enabled='; systemctl is-enabled dealix-agent-council.timer 2>/dev/null || true
printf 'active='; systemctl is-active dealix-agent-council.timer 2>/dev/null || true
systemctl list-timers dealix-agent-council.timer --all --no-pager | redact_stream || true
[[ "$(systemctl is-enabled dealix-agent-council.timer 2>/dev/null || true)" == "enabled" ]] || FAIL=1
[[ "$(systemctl is-active dealix-agent-council.timer 2>/dev/null || true)" == "active" ]] || FAIL=1

echo
echo "===== 2. MANUAL COUNCIL PROOF RUN ====="
systemctl reset-failed dealix-agent-council.service 2>/dev/null || true
set +e
systemctl start dealix-agent-council.service
START_RC=$?
set -e
echo "start_rc=${START_RC}"
systemctl show dealix-agent-council.service -p Result -p ExecMainStatus -p ActiveState -p SubState --no-pager | redact_stream || true
RESULT="$(systemctl show dealix-agent-council.service -p Result --value 2>/dev/null || true)"
STATUS="$(systemctl show dealix-agent-council.service -p ExecMainStatus --value 2>/dev/null || true)"
if [[ "$START_RC" -eq 0 && "$RESULT" == "success" && "$STATUS" == "0" ]]; then
  echo "COUNCIL_SERVICE=PASS"
else
  echo "COUNCIL_SERVICE=FAIL"
  FAIL=1
  journalctl -u dealix-agent-council.service -n 80 --no-pager 2>/dev/null \
    | grep -Eai 'error|fail|blocked|timeout|hermes|ollama|memory|resource|permission|result|exit' \
    | tail -60 \
    | redact_stream || true
fi

echo
echo "===== 3. DAILY COMMAND ====="
DAILY="${REPORT_ROOT}/LATEST_DAILY_COMMAND.md"
if [[ -s "$DAILY" ]]; then
  echo "daily_command=present"
  echo "daily_command_bytes=$(wc -c < "$DAILY")"
  sed -n '1,80p' "$DAILY" | redact_stream
else
  echo "daily_command=MISSING"
  FAIL=1
fi

echo
echo "===== 4. PROOF JSON ====="
LATEST_PROOF="$(find "$REPORT_ROOT" -name PROOF.json -type f -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [[ -n "${LATEST_PROOF:-}" && -s "$LATEST_PROOF" ]]; then
  echo "proof_path=${LATEST_PROOF}"
  set +e
  python3 - "$LATEST_PROOF" <<'PY' | redact_stream
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    d = json.load(f)
for k in ("run_id", "timestamp", "status", "result", "external_actions_executed", "approval_items", "reports_generated"):
    if k in d:
        print(f"{k}={d[k]}")
if d.get("external_actions_executed") != 0:
    raise SystemExit("FAIL: external_actions_executed must be 0")
print("PROOF_EXTERNAL_EFFECTS=PASS")
PY
  PROOF_RC=${PIPESTATUS[0]}
  set -e
  [[ "$PROOF_RC" -eq 0 ]] || FAIL=1
else
  echo "proof=MISSING"
  FAIL=1
fi

echo
echo "===== 5. OPENCLAW GATEWAY ====="
if [[ -x "$OPENCLAW" ]]; then
  safe_run sudo -iu dealix "$OPENCLAW" gateway status --require-rpc || FAIL=1
else
  echo "OPENCLAW=MISSING"
  FAIL=1
fi

echo
echo "===== 6. TELEGRAM LIVE PROBE ====="
if [[ -x "$OPENCLAW" ]]; then
  safe_run sudo -iu dealix "$OPENCLAW" channels status --channel telegram --probe || true
else
  echo "TELEGRAM_PROBE=SKIP"
fi

echo
echo "===== 7. TELEGRAM TRANSPORT DIAGNOSTICS ====="
if [[ -x "$OPENCLAW" ]]; then
  safe_run sudo -iu dealix "$OPENCLAW" channels logs --channel telegram --lines 160 \
    | grep -Eai 'poll|getUpdates|webhook|stall|disconnect|connect|401|409|timeout|fetch failed|network|dns|ipv6|error|retry|works' \
    | tail -100 || true
fi
printf 'telegram_api_ipv4='; getent ahostsv4 api.telegram.org 2>/dev/null | awk 'NR==1 {print $1}' || true
printf 'telegram_api_ipv6='; getent ahostsv6 api.telegram.org 2>/dev/null | awk 'NR==1 {print $1}' || true
TG_HTTP="$(curl -4 -sS -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 https://api.telegram.org/ 2>/dev/null || true)"
echo "telegram_https_ipv4=${TG_HTTP:-000}"

if [[ -x "$HERMES" ]]; then
  echo
  echo "===== 8. HERMES ====="
  sudo -iu dealix "$HERMES" --version 2>&1 | head -8 | redact_stream || true
fi

echo
echo "===== 9. RESOURCE POSTURE ====="
free -h | redact_stream
ollama ps 2>/dev/null | redact_stream || true
docker ps --filter name=dealix-n8n --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null | redact_stream || true

echo
echo "===== 10. HARD SAFETY ====="
echo "external_send=false"
echo "merge_to_main=false"
echo "production_mutation=false"
echo "payment_execution=false"
echo "secret_values_printed=false"

if [[ "$FAIL" -eq 0 ]]; then
  echo "DEALIX_COMPANY_AGENTS_LIVE_VERIFY=PASS"
  exit 0
fi

echo "DEALIX_COMPANY_AGENTS_LIVE_VERIFY=DEGRADED"
exit 1
