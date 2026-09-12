#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Read-only Dealix VPS posture audit. No package install, service restart,
# firewall mutation, secret read, deployment, or database mutation.

OUT="${1:-/opt/dealix/control/proof/vps-audit-$(date -u +%Y%m%dT%H%M%SZ).txt}"
mkdir -p "$(dirname "$OUT")"
exec > >(tee "$OUT") 2>&1

section() { printf '\n======================================================================\n%s\n======================================================================\n' "$1"; }
run() { printf '\n$ %q' "$1"; shift; printf ' %q' "$@"; printf '\n'; "$@" 2>&1 || true; }

section "IDENTITY / OS"
date -Is
uname -a
[[ -r /etc/os-release ]] && cat /etc/os-release
uptime

section "RESOURCES"
free -h || true
df -hT / /opt 2>/dev/null || df -hT / || true
swapon --show || true

section "REBOOT / UPDATE POSTURE"
[[ -e /var/run/reboot-required ]] && echo "REBOOT_REQUIRED=true" || echo "REBOOT_REQUIRED=false"
command -v apt >/dev/null 2>&1 && apt list --upgradable 2>/dev/null | sed -n '1,120p' || true
systemctl is-enabled unattended-upgrades.service 2>/dev/null || true
systemctl is-active unattended-upgrades.service 2>/dev/null || true
systemctl is-active apparmor.service 2>/dev/null || true
command -v aa-status >/dev/null 2>&1 && aa-status 2>/dev/null | sed -n '1,120p' || true
command -v needrestart >/dev/null 2>&1 && needrestart -b 2>/dev/null | sed -n '1,120p' || true

section "NETWORK EXPOSURE"
ss -lntup 2>/dev/null | sed -n '1,200p' || ss -lnt 2>/dev/null | sed -n '1,200p' || true
command -v ufw >/dev/null 2>&1 && ufw status verbose || true
command -v tailscale >/dev/null 2>&1 && tailscale status 2>/dev/null | sed -n '1,120p' || true

section "FAIL2BAN"
systemctl is-active fail2ban.service 2>/dev/null || true
command -v fail2ban-client >/dev/null 2>&1 && fail2ban-client status 2>/dev/null || true

section "CORE SERVICES"
for unit in \
  docker.service \
  ollama.service \
  tailscaled.service \
  hermes-dealix.service \
  dealix-llm-router.service \
  n8n.service \
  openclaw-gateway.service
do
  printf '\n[%s]\n' "$unit"
  systemctl is-enabled "$unit" 2>/dev/null || true
  systemctl is-active "$unit" 2>/dev/null || true
  systemctl show "$unit" -p FragmentPath -p User -p Group -p Restart -p NoNewPrivileges -p ProtectSystem -p ProtectHome -p PrivateTmp -p MemoryMax -p CPUQuota 2>/dev/null || true
done

section "USER SERVICES"
if id dealix >/dev/null 2>&1; then
  sudo -u dealix -H systemctl --user --no-pager --type=service --state=running 2>/dev/null | sed -n '1,160p' || true
  sudo -u dealix -H systemctl --user --no-pager --type=timer --all 2>/dev/null | sed -n '1,160p' || true
fi

section "SYSTEM TIMERS"
systemctl list-timers --all --no-pager 2>/dev/null | grep -E 'dealix|omega|company|openclaw|n8n|hermes|NEXT|LEFT' | sed -n '1,200p' || true

section "DOCKER POSTURE"
command -v docker >/dev/null 2>&1 && {
  docker version --format 'server={{.Server.Version}} client={{.Client.Version}}' 2>/dev/null || true
  docker info --format 'rootless={{.SecurityOptions}} cgroup={{.CgroupDriver}} storage={{.Driver}}' 2>/dev/null || true
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null | sed -n '1,160p' || true
  docker system df 2>/dev/null || true
}

section "DEALIX REPOSITORY"
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
if [[ -d "$REPO/.git" ]]; then
  git -C "$REPO" status --short || true
  git -C "$REPO" branch --show-current || true
  git -C "$REPO" rev-parse HEAD || true
  git -C "$REPO" rev-parse origin/main 2>/dev/null || true
fi

section "LOCAL ENDPOINT BINDINGS"
for port in 11434 5678 18789; do
  printf 'PORT_%s=' "$port"
  ss -lnt 2>/dev/null | awk -v p=":$port" '$4 ~ p {print $4}' | paste -sd, - || true
  printf '\n'
done

section "AUDIT RESULT"
echo "AUDIT_MODE=READ_ONLY"
echo "SECRETS_READ=false"
echo "PACKAGES_MUTATED=false"
echo "SERVICES_RESTARTED=false"
echo "FIREWALL_MUTATED=false"
echo "PRODUCTION_MUTATED=false"
echo "OUTPUT=$OUT"
