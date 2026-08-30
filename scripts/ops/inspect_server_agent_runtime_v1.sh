#!/usr/bin/env bash
# Read-only VPS inspection for the existing Dealix agent control plane.
# This script does not install, restart, enable, disable, mutate, or print secrets.
set -u

failures=0
reconcile=0

check_unit() {
  local unit="$1"
  if ! command -v systemctl >/dev/null 2>&1; then
    echo "SKIP systemd_unavailable"
    return
  fi
  if systemctl is-active --quiet "$unit"; then
    echo "PASS unit_active=$unit"
  else
    echo "FAIL unit_inactive=$unit"
    failures=$((failures + 1))
  fi
}

check_tcp() {
  local label="$1"
  local host="$2"
  local port="$3"
  if command -v timeout >/dev/null 2>&1 && timeout 2 bash -c ":</dev/tcp/$host/$port" >/dev/null 2>&1; then
    echo "PASS tcp_open=$label"
  else
    echo "WARN tcp_unverified=$label"
  fi
}

for unit in docker.service tailscaled.service hermes-dealix.service dealix-llm-router.service; do
  check_unit "$unit"
done

check_tcp "ollama" "127.0.0.1" "11434"
check_tcp "openclaw_gateway" "127.0.0.1" "18789"
check_tcp "n8n" "127.0.0.1" "5678"

if command -v docker >/dev/null 2>&1; then
  if docker ps --format '{{.Names}}' 2>/dev/null | rg -q '^n8n$'; then
    echo "PASS container_running=n8n"
  else
    echo "WARN container_unverified=n8n"
  fi
else
  echo "WARN docker_cli_unavailable"
fi

AUTOPILOT="/opt/dealix/control/bin/dealix_company_autopilot.sh"
if [ -x "$AUTOPILOT" ]; then
  echo "PASS canonical_company_autopilot=$AUTOPILOT"
else
  echo "FAIL canonical_company_autopilot_missing=$AUTOPILOT"
  failures=$((failures + 1))
fi

if command -v systemctl >/dev/null 2>&1; then
  echo "--- DEALIX_TIMER_INVENTORY_BEGIN ---"
  timer_inventory="$(systemctl list-timers --all --no-pager 2>/dev/null | grep -E 'dealix-(company|omega|live|supply|vps-issue-bridge)' || true)"
  printf '%s\n' "$timer_inventory"
  echo "--- DEALIX_TIMER_INVENTORY_END ---"

  company_count="$(printf '%s\n' "$timer_inventory" | grep -c 'dealix-company-' || true)"
  adjacent_count="$(printf '%s\n' "$timer_inventory" | grep -Ec 'dealix-(omega|live|supply)' || true)"
  echo "INFO canonical_company_timer_count=$company_count"
  echo "INFO adjacent_timer_count=$adjacent_count"
  if [ "$adjacent_count" -gt 0 ]; then
    echo "WARN scheduler_reconciliation=REQUIRED_CLASSIFY_BEFORE_DISABLE"
    echo "NOTE=adjacent timers may be bounded monitoring; do not disable without ownership/effect evidence"
    reconcile=1
  else
    echo "PASS scheduler_reconciliation=NO_ADJACENT_TIMER_NAMES_DETECTED"
  fi
fi

if command -v ss >/dev/null 2>&1; then
  sensitive="$(ss -lnt 2>/dev/null | grep -E ':(11434|18789|5678)[[:space:]]' || true)"
  printf '%s\n' "$sensitive"
  if printf '%s\n' "$sensitive" | grep -Eq '(^|[[:space:]])(0\.0\.0\.0|\[::\]):(11434|18789|5678)'; then
    echo "FAIL sensitive_listener_public_bind_detected=true"
    failures=$((failures + 1))
  else
    echo "PASS sensitive_listener_public_bind_detected=false"
  fi
fi

if [ "$failures" -eq 0 ]; then
  echo "DEALIX_SERVER_AGENT_RUNTIME_INSPECTION=PASS_OR_UNVERIFIED"
  if [ "$reconcile" -eq 1 ]; then
    echo "SCHEDULER_OWNERSHIP=RECONCILIATION_REQUIRED"
  else
    echo "SCHEDULER_OWNERSHIP=NO_ADJACENT_TIMER_SIGNAL"
  fi
  echo "NOTE=runtime_receipts_and_exact_head_acceptance_are_still_required"
else
  echo "DEALIX_SERVER_AGENT_RUNTIME_INSPECTION=FAIL"
  exit 1
fi
