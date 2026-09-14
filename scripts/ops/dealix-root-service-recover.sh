#!/usr/bin/env bash
# dealix-root-service-recover — narrow allowlist for Dealix service recovery
# Only allows specific Dealix services, no arbitrary root
set -Eeuo pipefail
SERVICE="${1:?usage: dealix-root-service-recover <service> [status|restart|start]}"
ACTION="${2:-status}"
ALLOWED=(
  "dealix-omega-weekly.service"
  "dealix-omega-weekly.timer"
  "dealix-autonomous-company.service"
  "dealix-autonomous-company.timer"
  "hermes-dealix.service"
  "dealix-llm-router.service"
  "ollama.service"
)
ok=false
for a in "${ALLOWED[@]}"; do
  [[ "$SERVICE" == "$a" ]] && ok=true
done
if ! $ok; then
  echo "BLOCKED: $SERVICE not in allowlist"
  printf 'ALLOWED: %s\n' "${ALLOWED[@]}"
  exit 1
fi
case "$ACTION" in
  status) exec systemctl status "$SERVICE" --no-pager ;;
  is-active) exec systemctl is-active "$SERVICE" ;;
  restart) echo "RECOVER: $SERVICE restart requested — requires L5 approval, preparing command:"
           echo "  sudo systemctl restart $SERVICE && systemctl is-active $SERVICE"
           echo "Run with exact approval packet: sha256(L5|systemd|$SERVICE|restart)[:16]"
           exit 0
           ;;
  *) echo "BLOCKED: action $ACTION not allowed (use status/is-active/restart)"; exit 1 ;;
esac
