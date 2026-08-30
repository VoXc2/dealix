#!/usr/bin/env bash
# Read-only VPS inspection for the existing Dealix agent control plane.
# This script does not install, restart, enable, disable, mutate, or print secrets.
set -u

failures=0

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

if [ "$failures" -eq 0 ]; then
  echo "DEALIX_SERVER_AGENT_RUNTIME_INSPECTION=PASS_OR_UNVERIFIED"
  echo "NOTE=runtime_receipts_and_exact_head_acceptance_are_still_required"
else
  echo "DEALIX_SERVER_AGENT_RUNTIME_INSPECTION=FAIL"
  exit 1
fi
