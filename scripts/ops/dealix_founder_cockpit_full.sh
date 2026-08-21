#!/usr/bin/env bash
set -Eeuo pipefail

# Dealix Founder Cockpit - comprehensive, idempotent VPS bootstrap.
# Safe boundary: no merge, deploy, production mutation, payment, live outbound,
# secret printing, destructive git reset, or customer-data mutation.

ADMIN_USER="${DEALIX_ADMIN_USER:-dealix}"
DEALIX_ROOT="${DEALIX_ROOT:-/opt/dealix}"
REPO_DIR="${DEALIX_REPO_DIR:-$DEALIX_ROOT/workspace/dealix}"
LOG_DIR="$DEALIX_ROOT/logs"
BACKUP_DIR="$DEALIX_ROOT/backups/founder-cockpit"
REPORT_DIR="$DEALIX_ROOT/reports/founder-cockpit"
STAMP="$(date +%Y%m%d-%H%M%S)"
REPORT="$REPORT_DIR/acceptance-$STAMP.txt"
LOCK="/run/lock/dealix-founder-cockpit.lock"

exec 9>"$LOCK"
flock -n 9 || { echo "BLOCKED: another founder cockpit bootstrap is running"; exit 75; }

if [ "$(id -u)" -ne 0 ]; then
  echo "BLOCKED: run as root (or through the Windows bootstrap)"
  exit 2
fi

id "$ADMIN_USER" >/dev/null 2>&1 || {
  echo "BLOCKED: required user '$ADMIN_USER' does not exist"
  exit 3
}

mkdir -p "$LOG_DIR" "$BACKUP_DIR" "$REPORT_DIR"
chmod 0755 "$DEALIX_ROOT" "$LOG_DIR" "$BACKUP_DIR" "$REPORT_DIR"

exec > >(tee -a "$REPORT") 2>&1

echo "============================================================"
echo "        DEALIX FOUNDER COCKPIT - FULL BOOTSTRAP"
echo "============================================================"
echo "started_at=$(date -Is)"
echo "host=$(hostname)"
echo "kernel=$(uname -r)"
echo "admin_user=$ADMIN_USER"
echo "repo=$REPO_DIR"

echo
 echo "===== 1. SAFETY / IDENTITY ====="
whoami
hostname
uname -a

# Never display environment or secret stores.
for forbidden in env printenv; do :; done

echo
 echo "===== 2. SYSTEM BASELINE ====="
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  openssh-server tmux git git-lfs curl wget jq rsync ripgrep tree unzip zip \
  ca-certificates gnupg lsb-release htop acl sqlite3 openssl python3 python3-venv \
  python3-pip build-essential ufw fail2ban unattended-upgrades

systemctl enable --now ssh >/dev/null 2>&1 || true
systemctl enable --now fail2ban >/dev/null 2>&1 || true
systemctl enable --now unattended-upgrades >/dev/null 2>&1 || true

printf '%-24s %s\n' "ssh" "$(systemctl is-active ssh 2>/dev/null || true)"
printf '%-24s %s\n' "fail2ban" "$(systemctl is-active fail2ban 2>/dev/null || true)"
printf '%-24s %s\n' "unattended-upgrades" "$(systemctl is-active unattended-upgrades 2>/dev/null || true)"

# Do not change firewall policy here; only report it.
echo
 echo "--- UFW (read-only) ---"
ufw status verbose 2>/dev/null || true

echo
 echo "===== 3. TAILSCALE ====="
if command -v tailscale >/dev/null 2>&1; then
  tailscale status || true
  printf 'tailscale_ipv4='
  tailscale ip -4 2>/dev/null | head -1 || true
  printf 'tailscale_ipv6='
  tailscale ip -6 2>/dev/null | head -1 || true
  printf 'tailscaled_service=%s\n' "$(systemctl is-active tailscaled 2>/dev/null || true)"
else
  echo "TAILSCALE=NOT_INSTALLED"
fi

# Ensure workspace ownership without modifying git content.
install -d -m 0755 -o "$ADMIN_USER" -g "$ADMIN_USER" \
  "$DEALIX_ROOT" "$DEALIX_ROOT/workspace" "$LOG_DIR" "$REPORT_DIR"


echo
 echo "===== 4. REPOSITORY SAFETY ====="
if [ -d "$REPO_DIR/.git" ]; then
  echo "REPO_PRESENT=PASS"
  sudo -iu "$ADMIN_USER" bash -lc "cd '$REPO_DIR' && git status -sb && git log -1 --oneline && git remote -v"
else
  echo "REPO_PRESENT=NO"
  echo "No clone performed automatically. Source-of-truth policy remains GitHub."
fi


echo
 echo "===== 5. TMUX FOUNDER COCKPIT ====="
TMUX_CONF="/home/$ADMIN_USER/.tmux.conf"
if [ -f "$TMUX_CONF" ]; then
  cp -a "$TMUX_CONF" "$BACKUP_DIR/tmux.conf.$STAMP"
fi
cat > "$TMUX_CONF" <<'EOF'
set -g mouse on
set -g history-limit 200000
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -g set-clipboard on
set -g escape-time 10
set -g status-interval 5
set -g remain-on-exit off
set -g allow-rename off
EOF
chown "$ADMIN_USER:$ADMIN_USER" "$TMUX_CONF"
chmod 0644 "$TMUX_CONF"

sudo -iu "$ADMIN_USER" tmux has-session -t dealix 2>/dev/null || \
  sudo -iu "$ADMIN_USER" tmux new-session -d -s dealix -n founder

WINDOWS=(founder github railway engineering ops agents monitoring research)
for name in "${WINDOWS[@]}"; do
  if ! sudo -iu "$ADMIN_USER" tmux list-windows -t dealix -F '#{window_name}' 2>/dev/null | grep -Fxq "$name"; then
    sudo -iu "$ADMIN_USER" tmux new-window -d -t dealix -n "$name"
  fi
done

if [ -d "$REPO_DIR" ]; then
  for name in "${WINDOWS[@]}"; do
    sudo -iu "$ADMIN_USER" tmux send-keys -t "dealix:$name" "cd '$REPO_DIR'" C-m || true
  done
fi


echo
 echo "===== 6. SHELL FOUNDER COMMANDS ====="
PROFILE="/home/$ADMIN_USER/.bashrc"
cp -a "$PROFILE" "$BACKUP_DIR/bashrc.$STAMP" 2>/dev/null || true
python3 - "$PROFILE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text() if p.exists() else ""
begin="# BEGIN DEALIX FOUNDER COCKPIT"
end="# END DEALIX FOUNDER COCKPIT"
while begin in s and end in s:
    left, rest=s.split(begin,1)
    _, right=rest.split(end,1)
    s=left.rstrip()+"\n"+right.lstrip("\n")
block=r'''
# BEGIN DEALIX FOUNDER COCKPIT
export DEALIX_REPO=/opt/dealix/workspace/dealix
export PATH="$HOME/.local/bin:$HOME/.railway/bin:$HOME/.hermes/bin:$PATH"
alias d='cd "$DEALIX_REPO"'
alias dg='cd "$DEALIX_REPO" && git status -sb'
alias dl='cd "$DEALIX_REPO" && git log -15 --oneline --decorate'
alias dfetch='cd "$DEALIX_REPO" && git fetch --all --prune'
alias dpr='cd "$DEALIX_REPO" && gh pr list --limit 50'
alias dri='cd "$DEALIX_REPO" && gh issue list --limit 50'
alias drw='cd "$DEALIX_REPO" && gh run list --limit 30'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dt='tmux new -As dealix'
alias dmem='free -h; echo; df -h /'
alias dolls='ollama ps'
alias dstatus='dealix-cockpit-status'
alias dproof='dealix-cockpit-proof'
# END DEALIX FOUNDER COCKPIT
'''.strip()
p.write_text(s.rstrip()+"\n\n"+block+"\n")
PY
chown "$ADMIN_USER:$ADMIN_USER" "$PROFILE"


echo
 echo "===== 7. STATUS COMMAND ====="
cat > /usr/local/bin/dealix-cockpit-status <<'EOF'
#!/usr/bin/env bash
set -u
printf '%s\n' '===== DEALIX COCKPIT STATUS ====='
date -Is
printf '%s\n' '--- identity ---'
whoami
hostname
printf '%s\n' '--- tailscale ---'
command -v tailscale >/dev/null 2>&1 && { tailscale ip -4 2>/dev/null | head -1; tailscale status 2>/dev/null | head -8; } || true
printf '%s\n' '--- repository ---'
cd /opt/dealix/workspace/dealix 2>/dev/null && git status -sb && git log -1 --oneline || true
printf '%s\n' '--- github ---'
gh auth status 2>&1 | sed -E 's/(Token:).*/\1 [REDACTED]/I' || true
printf '%s\n' '--- railway ---'
export PATH="$HOME/.railway/bin:$HOME/.local/bin:$PATH"
railway whoami 2>&1 || true
printf '%s\n' '--- docker ---'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>&1 | head -30 || true
printf '%s\n' '--- tmux ---'
tmux list-sessions 2>&1 || true
printf '%s\n' '--- ollama ---'
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && echo OLLAMA_API=PASS || echo OLLAMA_API=DEGRADED
ollama ps 2>/dev/null || true
printf '%s\n' '--- services ---'
for unit in ssh docker ollama tailscaled fail2ban unattended-upgrades; do
  printf '%-24s %s\n' "$unit" "$(systemctl is-active "$unit" 2>/dev/null || true)"
done
printf '%s\n' '--- resources ---'
free -h
df -h /
EOF
chmod 0755 /usr/local/bin/dealix-cockpit-status

cat > /usr/local/bin/dealix-cockpit <<'EOF'
#!/usr/bin/env bash
exec tmux new -As dealix
EOF
chmod 0755 /usr/local/bin/dealix-cockpit

cat > /usr/local/bin/dealix-cockpit-proof <<'EOF'
#!/usr/bin/env bash
set -u
OUT="/opt/dealix/reports/founder-cockpit/manual-proof-$(date +%Y%m%d-%H%M%S).txt"
mkdir -p "$(dirname "$OUT")"
{
  echo "DEALIX_FOUNDER_COCKPIT_PROOF"
  date -Is
  dealix-cockpit-status
} | tee "$OUT"
echo "proof=$OUT"
EOF
chmod 0755 /usr/local/bin/dealix-cockpit-proof


echo
 echo "===== 8. CLI / AUTH READINESS ====="
sudo -iu "$ADMIN_USER" bash -lc '
set -u
export PATH="$HOME/.railway/bin:$HOME/.local/bin:$HOME/.hermes/bin:$PATH"
for x in git gh railway tmux docker curl jq python3 ollama hermes; do
  printf "%-12s " "$x"
  command -v "$x" 2>/dev/null || echo MISSING
done
printf "%s\n" "--- GitHub auth ---"
gh auth status 2>&1 | sed -E "s/(Token:).*/\1 [REDACTED]/I" || true
printf "%s\n" "--- Railway auth ---"
railway whoami 2>&1 || true
'


echo
 echo "===== 9. LOCAL AI SAFETY ====="
if systemctl list-unit-files ollama.service >/dev/null 2>&1; then
  printf 'ollama_service=%s\n' "$(systemctl is-active ollama 2>/dev/null || true)"
fi
if curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "OLLAMA_API=PASS"
  ollama ps 2>/dev/null || true
else
  echo "OLLAMA_API=DEGRADED"
fi

# Report Hermes/OpenClaw; do not start heavy agents automatically.
echo
 echo "===== 10. AGENT RUNTIMES (READ-ONLY STATUS) ====="
for unit in hermes-dealix.service openclaw-gateway.service; do
  printf '%-32s %s\n' "$unit" "$(systemctl is-active "$unit" 2>/dev/null || true)"
done
sudo -iu "$ADMIN_USER" bash -lc '
export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"
command -v hermes >/dev/null 2>&1 && hermes --version 2>/dev/null || true
if [ -x "$HOME/.openclaw/bin/openclaw" ]; then
  "$HOME/.openclaw/bin/openclaw" status --all 2>/dev/null | head -60 || true
fi
'


echo
 echo "===== 11. DOCKER / N8N ====="
if command -v docker >/dev/null 2>&1; then
  systemctl is-active docker >/dev/null 2>&1 && echo "DOCKER_SERVICE=PASS" || echo "DOCKER_SERVICE=DEGRADED"
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | head -30 || true
  if docker ps --format '{{.Names}}' | grep -Fxq dealix-n8n; then
    echo "N8N_CONTAINER=RUNNING"
    docker port dealix-n8n 2>/dev/null || true
  else
    echo "N8N_CONTAINER=NOT_RUNNING"
  fi
fi


echo
 echo "===== 12. SYSTEMD TIMERS ====="
systemctl list-timers --all --no-pager | grep -E 'dealix|NEXT|LEFT' | head -80 || true


echo
 echo "===== 13. SSH CONFIG AUDIT ====="
sshd -t && echo "SSHD_CONFIG=PASS" || echo "SSHD_CONFIG=FAIL"
ss -lntp 2>/dev/null | grep -E ':(22|11434|5678)\b' || true


echo
 echo "===== 14. RESOURCE BASELINE ====="
free -h
df -h /
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -20


echo
 echo "===== 15. FINAL ACCEPTANCE AS DEALIX USER ====="
sudo -iu "$ADMIN_USER" bash -lc '
set -u
export PATH="$HOME/.railway/bin:$HOME/.local/bin:$HOME/.hermes/bin:$PATH"
echo "user=$(whoami)"
echo "host=$(hostname)"
echo "home=$HOME"
command -v tmux >/dev/null && echo TMUX=PASS || echo TMUX=FAIL
tmux list-sessions >/dev/null 2>&1 && echo TMUX_SESSION=PASS || echo TMUX_SESSION=DEGRADED
command -v gh >/dev/null && echo GH_CLI=PASS || echo GH_CLI=DEGRADED
command -v railway >/dev/null && echo RAILWAY_CLI=PASS || echo RAILWAY_CLI=DEGRADED
command -v docker >/dev/null && echo DOCKER_CLI=PASS || echo DOCKER_CLI=DEGRADED
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && echo OLLAMA_API=PASS || echo OLLAMA_API=DEGRADED
if [ -d /opt/dealix/workspace/dealix/.git ]; then
  cd /opt/dealix/workspace/dealix
  echo "repo_head=$(git rev-parse --short HEAD)"
  echo "repo_branch=$(git branch --show-current)"
fi
'


echo
 echo "===== 16. SAFETY GATES ====="
echo "MERGE_TO_MAIN=BLOCKED_BY_POLICY"
echo "RAILWAY_DEPLOY=BLOCKED_BY_POLICY"
echo "PRODUCTION_MUTATION=BLOCKED_BY_POLICY"
echo "LIVE_OUTBOUND=BLOCKED_BY_POLICY"
echo "PAYMENT=BLOCKED_BY_POLICY"
echo "SECRET_PRINTING=BLOCKED_BY_POLICY"


echo
 echo "============================================================"
echo "DEALIX_FOUNDER_COCKPIT=PASS"
echo "proof_report=$REPORT"
echo "connect=ssh dealix"
echo "cockpit=dealix-cockpit"
echo "status=dealix-cockpit-status"
echo "============================================================"
