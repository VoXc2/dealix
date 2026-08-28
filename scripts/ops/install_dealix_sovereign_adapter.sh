#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
STATE_ROOT="${DEALIX_SOVEREIGN_CI_ROOT:-/opt/dealix/sovereign-ci}"
CONTROL_BIN="${DEALIX_CONTROL_BIN_DIR:-/opt/dealix/control/bin}"
SOURCE_ADAPTER="$REPO_ROOT/scripts/ops/dealix_sovereign_adapter.py"
ADAPTER="$CONTROL_BIN/dealix_sovereign_adapter.py"
ENV_FILE="/etc/dealix/sovereign-adapter.env"
POLL_SERVICE="/etc/systemd/system/dealix-sovereign-adapter.service"
POLL_TIMER="/etc/systemd/system/dealix-sovereign-adapter.timer"
TRUST_SERVICE="/etc/systemd/system/dealix-sovereign-trusted.service"
TRUST_TIMER="/etc/systemd/system/dealix-sovereign-trusted.timer"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="/root/dealix-sovereign-adapter-$STAMP"

[[ "$(id -u)" -eq 0 ]] || { echo "ERROR: run as root"; exit 1; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "ERROR: missing user $RUN_USER"; exit 1; }
[[ -f "$SOURCE_ADAPTER" ]] || { echo "ERROR: missing adapter source $SOURCE_ADAPTER"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 missing"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "ERROR: gh missing"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "ERROR: git missing"; exit 1; }

install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$STATE_ROOT"
install -d -m 0755 "$CONTROL_BIN"
install -d -m 0750 /etc/dealix
mkdir -p "$BACKUP"
chmod 0700 "$BACKUP"

for path in "$ADAPTER" "$ENV_FILE" "$POLL_SERVICE" "$POLL_TIMER" "$TRUST_SERVICE" "$TRUST_TIMER"; do
  [[ -e "$path" ]] && cp -a "$path" "$BACKUP/"
done

# Pin the scheduler to a root-owned runtime copy. Verification policy itself is
# still loaded from the dedicated tool checkout through bin/dealix verify.
install -m 0755 -o root -g root "$SOURCE_ADAPTER" "$ADAPTER"

cat > "$ENV_FILE" <<EOF
DEALIX_REPO_SLUG=Dealix-sa/dealix
DEALIX_SOVEREIGN_CI_ROOT=$STATE_ROOT
DEALIX_SOVEREIGN_TOOL_REF=main
DEALIX_CI_MAX_PRS_PER_POLL=2
DEALIX_CI_MAX_LOAD1=2.75
DEALIX_CI_MIN_AVAILABLE_MB=4096
EOF
chmod 0640 "$ENV_FILE"
chown root:"$RUN_USER" "$ENV_FILE"

cat > "$POLL_SERVICE" <<EOF
[Unit]
Description=Dealix Sovereign Verification Adapter Poller
After=network-online.target
Wants=network-online.target
ConditionPathExists=$ADAPTER

[Service]
Type=oneshot
User=$RUN_USER
Group=$RUN_USER
WorkingDirectory=$STATE_ROOT
EnvironmentFile=$ENV_FILE
ExecStart=/usr/bin/python3 $ADAPTER poll
TimeoutStartSec=45min
Nice=10
CPUQuota=200%
CPUWeight=20
MemoryHigh=5G
MemoryMax=6G
TasksMax=512
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$STATE_ROOT
ReadOnlyPaths=$ADAPTER
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true

[Install]
WantedBy=multi-user.target
EOF

cat > "$POLL_TIMER" <<EOF
[Unit]
Description=Dealix Sovereign Verification Poll Timer

[Timer]
OnBootSec=3min
OnUnitInactiveSec=5min
AccuracySec=15s
RandomizedDelaySec=30s
Unit=dealix-sovereign-adapter.service

[Install]
WantedBy=timers.target
EOF

cat > "$TRUST_SERVICE" <<EOF
[Unit]
Description=Dealix Sovereign Trusted Runtime/Production/Commercial Verification
After=network-online.target
Wants=network-online.target
ConditionPathExists=$ADAPTER

[Service]
Type=oneshot
User=$RUN_USER
Group=$RUN_USER
WorkingDirectory=$STATE_ROOT
EnvironmentFile=$ENV_FILE
ExecStart=/usr/bin/python3 $ADAPTER trusted-cycle
TimeoutStartSec=45min
Nice=15
CPUQuota=150%
CPUWeight=10
MemoryHigh=4G
MemoryMax=5G
TasksMax=384
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$STATE_ROOT
ReadOnlyPaths=$ADAPTER
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true

[Install]
WantedBy=multi-user.target
EOF

cat > "$TRUST_TIMER" <<EOF
[Unit]
Description=Dealix Sovereign Trusted Verification Timer

[Timer]
OnCalendar=*-*-* 04:20:00
Persistent=true
AccuracySec=1min
RandomizedDelaySec=10min
Unit=dealix-sovereign-trusted.service

[Install]
WantedBy=timers.target
EOF

systemd-analyze verify "$POLL_SERVICE" "$POLL_TIMER" "$TRUST_SERVICE" "$TRUST_TIMER"
systemctl daemon-reload
systemctl enable --now dealix-sovereign-adapter.timer dealix-sovereign-trusted.timer

sudo -iu "$RUN_USER" env \
  DEALIX_SOVEREIGN_CI_ROOT="$STATE_ROOT" \
  DEALIX_SOVEREIGN_TOOL_REF="main" \
  /usr/bin/python3 "$ADAPTER" doctor

echo "INSTALL=PASS"
echo "BACKUP=$BACKUP"
echo "ADAPTER=$ADAPTER"
echo "STATE_ROOT=$STATE_ROOT"
echo "NOTE=#1264 must be merged before TOOL_REF=main can provide bin/dealix verify"
echo "ROLLBACK=disable timers; restore files from $BACKUP; daemon-reload"
echo "NO_MERGE=1 NO_DEPLOY=1 NO_DNS=1 NO_DB_MUTATION=1 NO_EXTERNAL_SEND=1"
