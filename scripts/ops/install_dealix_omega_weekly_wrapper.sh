#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${DEALIX_REPO_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd -P)}"
SOURCE="$ROOT/scripts/ops/dealix_omega_weekly_wrapper.sh"
TARGET="${DEALIX_OMEGA_WEEKLY_TARGET:-/usr/local/sbin/dealix-omega-weekly}"
MODE="${1:---check}"

[[ -f "$SOURCE" ]] || { echo "OMEGA_WEEKLY_REPAIR=BLOCKED_SOURCE_MISSING"; exit 2; }
bash -n "$SOURCE"

source_sha="$(sha256sum "$SOURCE" | awk '{print $1}')"
target_sha="MISSING"
if [[ -f "$TARGET" ]]; then
  target_sha="$(sha256sum "$TARGET" | awk '{print $1}')"
fi

if [[ "$MODE" == "--check" ]]; then
  echo "OMEGA_WEEKLY_SOURCE_SHA=$source_sha"
  echo "OMEGA_WEEKLY_TARGET_SHA=$target_sha"
  [[ "$source_sha" == "$target_sha" ]] && { echo "OMEGA_WEEKLY_REPAIR=PASS_CURRENT"; exit 0; }
  echo "OMEGA_WEEKLY_REPAIR=NEEDED"
  exit 1
fi
[[ "$MODE" == "--install" ]] || { echo "OMEGA_WEEKLY_REPAIR=BLOCKED_BAD_MODE"; exit 2; }
[[ "$(id -u)" -eq 0 ]] || { echo "OMEGA_WEEKLY_REPAIR=BLOCKED_ROOT_REQUIRED"; exit 2; }

if [[ -f "$TARGET" && "$source_sha" != "$target_sha" ]]; then
  backup="${TARGET}.bak-$(date -u +%Y%m%dT%H%M%SZ)"
  cp -a "$TARGET" "$backup"
  echo "OMEGA_WEEKLY_BACKUP=$backup"
fi

install -m 0755 -o root -g root "$SOURCE" "$TARGET"
installed_sha="$(sha256sum "$TARGET" | awk '{print $1}')"
[[ "$installed_sha" == "$source_sha" ]] || { echo "OMEGA_WEEKLY_REPAIR=FAIL_HASH_MISMATCH"; exit 3; }

echo "OMEGA_WEEKLY_REPAIR=PASS_INSTALLED"
echo "OMEGA_WEEKLY_TARGET=$TARGET"
echo "SYSTEMD_RESTART_EXECUTED=false"
echo "SCHEDULER_CREATED=false"
echo "EXTERNAL_EFFECT_EXECUTED=false"
