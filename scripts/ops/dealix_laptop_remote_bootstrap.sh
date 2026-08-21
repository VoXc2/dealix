#!/usr/bin/env bash
set -Eeuo pipefail

ADMIN_USER="dealix"
REPO_DIR="/opt/dealix/workspace/dealix"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "===== DEALIX LAPTOP REMOTE BOOTSTRAP ====="

if [ "$(id -u)" -ne 0 ]; then
  echo "BLOCKED: run as root via sudo"
  exit 2
fi

id "$ADMIN_USER" >/dev/null 2>&1 || {
  echo "BLOCKED: user $ADMIN_USER does not exist"
  exit 3
}

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y \
  openssh-server \
  tmux \
  git \
  curl \
  jq \
  rsync \
  ripgrep \
  ca-certificates

systemctl enable --now ssh

if command -v tailscale >/dev/null 2>&1; then
  echo "TAILSCALE_PRESENT=yes"
  tailscale status >/dev/null 2>&1 && echo "TAILSCALE_STATUS=PASS" || echo "TAILSCALE_STATUS=DEGRADED"
else
  echo "TAILSCALE_PRESENT=no"
fi

install -d -m 0755 -o "$ADMIN_USER" -g "$ADMIN_USER" /opt/dealix /opt/dealix/workspace /opt/dealix/logs

if [ -d "$REPO_DIR/.git" ]; then
  echo "REPO_PRESENT=PASS"
  sudo -iu "$ADMIN_USER" bash -lc "cd '$REPO_DIR' && git status -sb && git log -1 --oneline"
else
  echo "REPO_PRESENT=NO"
  echo "No clone is performed automatically because the server repository/source-of-truth policy may already be managed elsewhere."
fi

TMUX_CONF="/home/${ADMIN_USER}/.tmux.conf"
if [ -f "$TMUX_CONF" ]; then
  cp -a "$TMUX_CONF" "${TMUX_CONF}.bak-${STAMP}"
fi
cat >"$TMUX_CONF" <<'EOF'
set -g mouse on
set -g history-limit 100000
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -g set-clipboard on
set -g escape-time 10
set -g status-interval 5
EOF
chown "$ADMIN_USER:$ADMIN_USER" "$TMUX_CONF"
chmod 0644 "$TMUX_CONF"

PROFILE="/home/${ADMIN_USER}/.bashrc"
BEGIN="# BEGIN DEALIX FOUNDER COCKPIT"
END="# END DEALIX FOUNDER COCKPIT"
python3 - "$PROFILE" "$BEGIN" "$END" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
begin, end = sys.argv[2], sys.argv[3]
s = p.read_text() if p.exists() else ""
while begin in s and end in s:
    left, rest = s.split(begin, 1)
    _, right = rest.split(end, 1)
    s = left.rstrip() + "\n" + right.lstrip("\n")
block = r'''
# BEGIN DEALIX FOUNDER COCKPIT
export DEALIX_REPO=/opt/dealix/workspace/dealix
export PATH="$HOME/.local/bin:$HOME/.railway/bin:$HOME/.hermes/bin:$PATH"
alias d='cd "$DEALIX_REPO"'
alias dg='cd "$DEALIX_REPO" && git status -sb'
alias dl='cd "$DEALIX_REPO" && git log -10 --oneline --decorate'
alias dpr='cd "$DEALIX_REPO" && gh pr list --limit 30'
alias drw='cd "$DEALIX_REPO" && gh run list --limit 20'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dt='tmux new -As dealix'
alias dmem='free -h && echo && df -h /'
# END DEALIX FOUNDER COCKPIT
'''.strip()
p.write_text(s.rstrip() + "\n\n" + block + "\n")
PY
chown "$ADMIN_USER:$ADMIN_USER" "$PROFILE"

sudo -iu "$ADMIN_USER" tmux has-session -t dealix 2>/dev/null || \
  sudo -iu "$ADMIN_USER" tmux new-session -d -s dealix -n founder

for name in github railway engineering ops agents monitoring; do
  if ! sudo -iu "$ADMIN_USER" tmux list-windows -t dealix -F '#{window_name}' 2>/dev/null | grep -Fxq "$name"; then
    sudo -iu "$ADMIN_USER" tmux new-window -d -t dealix -n "$name"
  fi
done

if [ -d "$REPO_DIR" ]; then
  for window in founder github railway engineering ops agents monitoring; do
    sudo -iu "$ADMIN_USER" tmux send-keys -t "dealix:$window" "cd '$REPO_DIR'" C-m || true
  done
fi

cat >/usr/local/bin/dealix-cockpit-status <<'EOF'
#!/usr/bin/env bash
set -u
printf '%s\n' '===== DEALIX COCKPIT STATUS ====='
date
printf '%s\n' '--- identity ---'
whoami
hostname
printf '%s\n' '--- repo ---'
cd /opt/dealix/workspace/dealix 2>/dev/null && git status -sb && git log -1 --oneline || true
printf '%s\n' '--- github ---'
gh auth status 2>&1 | sed -E 's/(Token:).*/\1 [REDACTED]/I' || true
printf '%s\n' '--- railway ---'
export PATH="$HOME/.railway/bin:$HOME/.local/bin:$PATH"
railway whoami 2>&1 || true
printf '%s\n' '--- docker ---'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>&1 | head -20 || true
printf '%s\n' '--- tmux ---'
tmux list-sessions 2>&1 || true
printf '%s\n' '--- ollama ---'
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && echo OLLAMA_API=PASS || echo OLLAMA_API=DEGRADED
printf '%s\n' '--- services ---'
for unit in ssh docker ollama tailscaled fail2ban; do
  printf '%-20s ' "$unit"
  systemctl is-active "$unit" 2>/dev/null || true
done
printf '%s\n' '--- resources ---'
free -h
df -h /
EOF
chmod 0755 /usr/local/bin/dealix-cockpit-status

cat >/usr/local/bin/dealix-cockpit <<'EOF'
#!/usr/bin/env bash
exec tmux new -As dealix
EOF
chmod 0755 /usr/local/bin/dealix-cockpit

echo "===== SAFE VERIFICATION ====="
sudo -iu "$ADMIN_USER" bash -lc '
set -u
command -v git
command -v gh || true
command -v railway || true
command -v tmux
command -v docker || true
tmux list-sessions || true
cd /opt/dealix/workspace/dealix 2>/dev/null && git status -sb || true
'

systemctl is-active ssh >/dev/null && echo "SSH_SERVICE=PASS" || echo "SSH_SERVICE=FAIL"

echo "REMOTE_BOOTSTRAP=PASS"
echo "Use: ssh dealix"
echo "Then: dealix-cockpit"
