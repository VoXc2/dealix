#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
RUN_USER="dealix"
SOURCE="${REPO}/scripts/ops/dealix_project_engineer.sh"
TARGET="/opt/dealix/control/bin/dealix_project_engineer.sh"
ROOT="/opt/dealix/project-engineer"

[[ "$(id -u)" -eq 0 ]] || { echo "BLOCKED: run installer as root"; exit 2; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "BLOCKED: missing user $RUN_USER"; exit 3; }
[[ -x "$SOURCE" ]] || { echo "BLOCKED: source missing or not executable: $SOURCE"; exit 4; }
install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" /opt/dealix/control/bin "$ROOT" "$ROOT/proof" "$ROOT/worktrees"
install -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$SOURCE" "$TARGET"

cat >/etc/systemd/system/dealix-project-engineer.service <<EOF_SERVICE
[Unit]
Description=Dealix Project Engineer daily review loop
After=network-online.target ollama.service
Wants=network-online.target

[Service]
Type=oneshot
User=dealix
Group=dealix
WorkingDirectory=${REPO}
Environment="HOME=/home/dealix"
Environment="TZ=Asia/Riyadh"
Environment="PATH=/home/dealix/.local/bin:/home/dealix/.hermes/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
# Scheduled operation is review-only until Hermes 8K + deterministic Python
# acceptance are proven. AUTOBUILD is an explicit later opt-in, never the default.
Environment="DEALIX_ENGINEER_AUTOBUILD=0"
Environment="DEALIX_EXTERNAL_OUTREACH_ENABLED=false"
Environment="EXTERNAL_OUTREACH_ENABLED=false"
Environment="AUTO_SEND_ENABLED=false"
Environment="WHATSAPP_ALLOW_LIVE_SEND=false"
Environment="DEALIX_LIVE_CHARGE=false"
Environment="DEALIX_AUTO_MERGE=false"
Environment="DEALIX_PRODUCTION_MUTATION=false"
Environment="AGENT_APPROVAL_MODE=required"
ExecStart=${TARGET} daily
TimeoutStartSec=45min
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
ReadWritePaths=/opt/dealix/project-engineer /opt/dealix/workspace/dealix /opt/dealix/control

[Install]
WantedBy=multi-user.target
EOF_SERVICE

cat >/etc/systemd/system/dealix-project-engineer.timer <<'EOF_TIMER'
[Unit]
Description=Dealix Project Engineer daily review timer

[Timer]
OnCalendar=*-*-* 20:30:00 Asia/Riyadh
RandomizedDelaySec=5m
Persistent=true
Unit=dealix-project-engineer.service

[Install]
WantedBy=timers.target
EOF_TIMER

systemd-analyze verify /etc/systemd/system/dealix-project-engineer.service /etc/systemd/system/dealix-project-engineer.timer
systemctl daemon-reload
systemctl enable --now dealix-project-engineer.timer
systemctl is-enabled dealix-project-engineer.timer
systemctl list-timers dealix-project-engineer.timer --all --no-pager
