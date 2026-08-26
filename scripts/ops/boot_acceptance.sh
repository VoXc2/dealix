#!/usr/bin/env bash
set -Eeuo pipefail
FLEET_STATE="${DEALIX_FLEET_STATE_DIR:-/opt/dealix/control/state/living_fleet}"
FOUNDER_STATE="${DEALIX_FOUNDER_PERSONAL_STATE_DIR:-/opt/dealix/control/state/founder_personal}"
PASS=0;FAIL=0;R=""
ck(){ local n="$1" e="$2" a="$3"; if [[ "$a" == "$e" ]]; then PASS=$((PASS+1)); R+="  ✓ $n: $a\n"; else FAIL=$((FAIL+1)); R+="  ✗ $n: want=$e got=$a\n"; fi; }
for s in docker ollama tailscaled; do ck "svc:$s" active "$(systemctl is-active $s 2>/dev/null||echo inactive)"; done
check(){ local n="$1" c="$2"; if eval "$c"; then PASS=$((PASS+1)); R+="  ✓ $n\n"; else FAIL=$((FAIL+1)); R+="  ✗ $n\n"; fi; }
check "api_200" "curl -so /dev/null -w %{http_code} --max-time 10 https://api.dealix.me/health | grep -q 200"
check "root_200" "curl -so /dev/null -w %{http_code} -L --max-time 10 https://dealix.me | grep -q 200"
check "ollama_api" "curl -so /dev/null -w %{http_code} --max-time 5 http://127.0.0.1:11434/api/tags | grep -q 200"
check "ollama_loopback" "ss -tlnp | grep 11434 | grep -q 127.0.0.1"
[[ -d "$FLEET_STATE" ]] && check "fleet_state_exists" "true" || check "fleet_state_exists" "false"
check "n8n_running" "docker inspect -f {{.State.Running}} dealix-n8n 2>/dev/null | grep -q true"
disk=$(df -P / | awk 'NR==2{gsub(/%/,"",$5);print $5}'); check "disk_lt_90" "[ $disk -lt 90 ]"
mem=$(awk '/MemAvailable:/{print int($2/1024)}' /proc/meminfo); check "mem_gt_2g" "[ $mem -gt 2000 ]"
if [[ -d "$FOUNDER_STATE" ]]; then p=$(stat -c %a "$FOUNDER_STATE"); check "founder_0700" "[ $p == 700 ]"; fi
echo "=== BOOT ACCEPTANCE: PASS=$PASS FAIL=$FAIL ==="; echo -e "$R"; [[ $FAIL -eq 0 ]] && exit 0 || exit 1
