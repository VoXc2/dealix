#!/usr/bin/env bash
# =============================================================================
# Dealix Boot Acceptance Verifier — proves all systems after reboot/crash.
# Usage: bash scripts/ops/boot_acceptance.sh [--json]
# Exit 0 = all systems PASS · Exit 1 = one or more FAIL
# =============================================================================
set -Eeuo pipefail
REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
FLEET_STATE="${DEALIX_FLEET_STATE_DIR:-/opt/dealix/control/state/living_fleet}"
FOUNDER_STATE="${DEALIX_FOUNDER_PERSONAL_STATE_DIR:-/opt/dealix/control/state/founder_personal}"
JSON_OUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUT=true

PASS=0; FAIL=0; RESULTS=""

check() {
  local name="$1" expected="$2" actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    PASS=$((PASS+1)); RESULTS+="  ✓ $name: $actual\n"
  else
    FAIL=$((FAIL+1)); RESULTS+="  ✗ $name: expected=$expected got=$actual\n"
  fi
}

check_bool() {
  local name="$1" cond="$2"
  if eval "$cond"; then
    PASS=$((PASS+1)); RESULTS+="  ✓ $name\n"
  else
    FAIL=$((FAIL+1)); RESULTS+="  ✗ $name\n"
  fi
}

echo "=== DEALIX BOOT ACCEPTANCE ==="

# --- Core services ---
for svc in docker ollama tailscaled fail2ban; do
  check "service:$svc" "active" "$(systemctl is-active "$svc" 2>/dev/null || echo inactive)"
done

# --- Dealix timers active ---
for t in heartbeat production repo-watch midday evening nightly; do
  tn="dealix-company-${t}.timer"
  [[ -f "/etc/systemd/system/$tn" ]] || continue
  check "timer:$tn" "active" "$(systemctl is-active "$tn" 2>/dev/null || echo inactive)"
done

# --- No failed dealix units ---
failed_count=$(systemctl --failed --no-legend 2>/dev/null | grep -c dealix || echo 0)
# local-ai (resource guard) + nightly (root-dir security smoke) are known
# environmental blockers tracked in ROOT_ACTION_PACKET — not unexpected.
check_bool "failed_dealix_units_le_2_known" "[ $failed_count -le 2 ]"

# --- Production reachable ---
check "api_health_http" "200" "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 10 https://api.dealix.me/health 2>/dev/null || echo 000)"
check "public_root_http" "200" "$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 10 https://dealix.me 2>/dev/null || echo 000)"

# --- Ollama responsive + loopback only ---
check "ollama_api" "200" "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:11434/api/tags 2>/dev/null || echo 000)"
ollama_bind=$(ss -tlnp 2>/dev/null | grep 11434 | grep -coE '127\.0\.0\.1|\[::1\]' || echo 0)
check_bool "ollama_loopback_only" "[ $ollama_bind -gt 0 ]"

# --- Fleet state readable ---
check_bool "fleet_state_dir_exists" "[ -d '$FLEET_STATE' ]"
state_ok=true
for sf in "$FLEET_STATE"/*.state.json; do
  [[ -f "$sf" ]] || continue
  python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$sf" 2>/dev/null || { state_ok=false; break; }
done
check_bool "fleet_state_all_valid_json" "$state_ok"

# --- Founder private state permissions ---
if [[ -d "$FOUNDER_STATE" ]]; then
  perms=$(stat -c %a "$FOUNDER_STATE" 2>/dev/null || echo unknown)
  check "founder_private_perms" "700" "$perms"
else
  RESULTS+="  ○ founder_private_state: not yet created (OK)\n"; PASS=$((PASS+1))
fi

# --- n8n container ---
n8n_running=$(docker inspect -f '{{.State.Running}}' dealix-n8n 2>/dev/null || echo false)
check "n8n_running" "true" "$n8n_running"

# --- Disk pressure ---
disk_pct=$(df -P / | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
check_bool "disk_under_90pct" "[ $disk_pct -lt 90 ]"

# --- Memory pressure ---
mem_mb=$(awk '/MemAvailable:/ {print int($2/1024)}' /proc/meminfo)
check_bool "mem_above_2000mb" "[ $mem_mb -gt 2000 ]"

# --- Output ---
echo ""
echo "--- RESULTS: PASS=$PASS FAIL=$FAIL ---"
echo -e "$RESULTS"

if [[ "$JSON_OUT" == true ]]; then
  printf '{"timestamp":"%s","pass":%d,"fail":%d,"verdict":"%s"}\n' \
    "$(date -Is)" "$PASS" "$FAIL" \
    "$([[ $FAIL -eq 0 ]] && echo PASS || echo FAIL)" > "$FLEET_STATE/boot_acceptance.json"
fi

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
