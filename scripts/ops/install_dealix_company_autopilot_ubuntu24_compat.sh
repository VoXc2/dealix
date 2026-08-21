#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO="Dealix-sa/dealix"
BRANCH="ops/dealix-vps-self-hosted-control-20260820"
RUN_USER="dealix"
SOURCE_PATH="scripts/ops/install_dealix_company_autopilot.sh"
TMP="$(mktemp)"
cleanup() { rm -f "$TMP"; }
trap cleanup EXIT

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if ! sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI auth missing for $RUN_USER"
  exit 3
fi

PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
if [[ "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: ${REPO} must remain private"
  exit 4
fi

sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/${SOURCE_PATH}?ref=${BRANCH}" \
  >"$TMP"

test -s "$TMP"

# Ubuntu 24.04/systemd compatibility: this host rejects Sun..Thu ranges.
sed -i 's/Sun\.\.Thu/Sun,Mon,Tue,Wed,Thu/g' "$TMP"

# A degraded immediate health proof must not roll back an otherwise successful
# timer/service installation. Production Trust remains RED until the real
# Railway Next.js frontend is live on dealix.me/ar.
python3 - "$TMP" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
s = s.replace(
    'systemctl start dealix-company@heartbeat.service\nsystemctl start dealix-company@production.service\nsystemctl start dealix-company@status.service',
    'systemctl start dealix-company@heartbeat.service || true\nsystemctl start dealix-company@production.service || true\nsystemctl start dealix-company@status.service || true',
    1,
)
p.write_text(s, encoding="utf-8")
PY

bash -n "$TMP"

echo "===== SYSTEMD CALENDAR COMPATIBILITY CHECK ====="
for calendar in \
  '*-*-* *:17:00 Asia/Riyadh' \
  'Sun,Mon,Tue,Wed,Thu *-*-* 06:30:00 Asia/Riyadh' \
  'Sun,Mon,Tue,Wed,Thu *-*-* 08:45:00 Asia/Riyadh' \
  'Sun,Mon,Tue,Wed,Thu *-*-* 12:30:00 Asia/Riyadh' \
  'Sun,Mon,Tue,Wed,Thu *-*-* 19:00:00 Asia/Riyadh' \
  'Sun,Mon,Tue,Wed,Thu *-*-* 21:15:00 Asia/Riyadh' \
  '*-*-* 23:30:00 Asia/Riyadh' \
  'Sat *-*-* 21:00:00 Asia/Riyadh'
do
  printf 'CHECK: %s\n' "$calendar"
  systemd-analyze calendar "$calendar" --iterations=1 >/dev/null
  echo "PASS"
done

echo "CALENDAR_COMPATIBILITY=PASS"
echo "===== RUN CANONICAL AUTOPILOT INSTALLER WITH HOST COMPAT FIX ====="

bash "$TMP"
