#!/usr/bin/env bash
# Bootstrap a fresh Ubuntu server for Dealix Docker production hosting.
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root: sudo bash scripts/server_bootstrap_ubuntu.sh"
  exit 1
fi

DEPLOY_USER="${DEPLOY_USER:-dealix}"
SSH_PORT="${SSH_PORT:-22}"

apt-get update
apt-get install -y --no-install-recommends ca-certificates curl gnupg git ufw fail2ban unattended-upgrades htop jq rsync
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
. /etc/os-release
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

if ! id "$DEPLOY_USER" >/dev/null 2>&1; then
  adduser --disabled-password --gecos "Dealix deploy user" "$DEPLOY_USER"
fi
usermod -aG docker "$DEPLOY_USER"

mkdir -p /srv/dealix /srv/dealix/backups /srv/dealix/logs
chown -R "$DEPLOY_USER:$DEPLOY_USER" /srv/dealix

ufw allow "${SSH_PORT}/tcp"
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

systemctl enable --now docker
systemctl enable --now fail2ban
systemctl enable --now unattended-upgrades || true

echo "DEALIX_SERVER_BOOTSTRAP_OK user=${DEPLOY_USER} root=/srv/dealix"
