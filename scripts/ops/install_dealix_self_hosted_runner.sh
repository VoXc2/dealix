#!/usr/bin/env bash
set -Eeuo pipefail

# Install the Dealix GitHub Actions self-hosted runner on the Command & AI Node.
# Security properties:
# - requires the canonical repository to be PRIVATE
# - requires authenticated GitHub CLI access for the dealix OS user
# - registration token is fetched locally, used once, never printed, and unset
# - runner service executes as the non-root `dealix` user
# - pinned release archive is verified by the official GitHub SHA-256 checksum
# - an already-configured but stopped runner is recovered fail-closed instead of
#   being reported as a successful installation
# - proof distinguishes the installed runner version from the desired pinned version

REPO="Dealix-sa/dealix"
REPO_URL="https://github.com/${REPO}"
RUNNER_USER="dealix"
RUNNER_NAME="dealix-vps"
RUNNER_DIR="/opt/dealix/actions-runner"
RUNNER_VERSION="2.337.0"
RUNNER_ARCHIVE="actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
RUNNER_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${RUNNER_ARCHIVE}"
RUNNER_SHA256="70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run this installer as root."
  exit 2
fi

if ! id "$RUNNER_USER" >/dev/null 2>&1; then
  echo "BLOCKED: OS user '$RUNNER_USER' does not exist."
  exit 3
fi

if ! command -v curl >/dev/null 2>&1 || ! command -v sha256sum >/dev/null 2>&1; then
  echo "BLOCKED: curl and sha256sum are required."
  exit 4
fi

if ! sudo -iu "$RUNNER_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for user '$RUNNER_USER'."
  exit 5
fi

PRIVATE="$(sudo -iu "$RUNNER_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
if [[ "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: ${REPO} must be private before a self-hosted runner is registered."
  exit 6
fi

LOGIN="$(sudo -iu "$RUNNER_USER" gh api user --jq '.login' 2>/dev/null || true)"
if [[ "$LOGIN" != "VoXc2" ]]; then
  echo "BLOCKED: expected authenticated founder login VoXc2; got '${LOGIN:-unknown}'."
  exit 7
fi

mkdir -p "$RUNNER_DIR"
chown "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"
cd "$RUNNER_DIR"

actual_runner_version() {
  if [[ -x ./bin/Runner.Listener ]]; then
    ./bin/Runner.Listener --version 2>/dev/null | tail -n 1 | tr -d '\r' || true
  else
    printf 'unknown\n'
  fi
}

print_runner_proof() {
  local recovered="$1"
  local actual upgrade_required
  actual="$(actual_runner_version)"
  [[ -n "$actual" ]] || actual="unknown"
  if [[ "$actual" == "$RUNNER_VERSION" ]]; then
    upgrade_required=false
  else
    upgrade_required=true
  fi

  echo
  echo "===== DEALIX SELF-HOSTED RUNNER PROOF ====="
  printf 'runner_name=%s\n' "$RUNNER_NAME"
  printf 'runner_dir=%s\n' "$RUNNER_DIR"
  printf 'runner_user=%s\n' "$RUNNER_USER"
  printf 'runner_version_actual=%s\n' "$actual"
  printf 'runner_version_target=%s\n' "$RUNNER_VERSION"
  printf 'runner_upgrade_required=%s\n' "$upgrade_required"
  printf 'repository_private=true\n'
  printf 'configured_runner_recovered=%s\n' "$recovered"
  printf 'secret_values_printed=false\n'
  echo "===== END ====="
}

if [[ -f .runner ]]; then
  echo "Runner is already configured at $RUNNER_DIR."
  if [[ ! -x ./svc.sh ]]; then
    echo "BLOCKED: configured runner is missing executable svc.sh."
    exit 10
  fi

  if ! ./svc.sh status; then
    echo "Runner service is not healthy; attempting bounded recovery."
    if ! ./svc.sh start; then
      echo "Runner service start failed; attempting one service install + start."
      ./svc.sh install "$RUNNER_USER"
      ./svc.sh start
    fi
  fi

  if ! ./svc.sh status; then
    echo "BLOCKED: configured runner service is still not healthy after recovery."
    exit 11
  fi

  print_runner_proof true
  exit 0
fi

TMP_ARCHIVE="$(mktemp --tmpdir "${RUNNER_ARCHIVE}.XXXXXX")"
cleanup() {
  rm -f "$TMP_ARCHIVE"
  unset TOKEN || true
}
trap cleanup EXIT

printf 'Downloading GitHub Actions runner v%s...\n' "$RUNNER_VERSION"
curl --fail --location --silent --show-error "$RUNNER_URL" --output "$TMP_ARCHIVE"

echo "${RUNNER_SHA256}  ${TMP_ARCHIVE}" | sha256sum --check --status || {
  echo "BLOCKED: runner archive SHA-256 verification failed."
  exit 8
}
echo "Runner archive checksum verified."
tar xzf "$TMP_ARCHIVE" -C "$RUNNER_DIR"
chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"

if [[ -x "$RUNNER_DIR/bin/installdependencies.sh" ]]; then
  "$RUNNER_DIR/bin/installdependencies.sh"
fi

if getent group docker >/dev/null 2>&1; then
  usermod -aG docker "$RUNNER_USER"
fi

mkdir -p /etc/needrestart/conf.d
cat >/etc/needrestart/conf.d/actions_runner_services.conf <<'EOF'
$nrconf{override_rc}{qr(^actions\.runner\..+\.service$)} = 0;
EOF

TOKEN="$(sudo -iu "$RUNNER_USER" gh api \
  --method POST \
  "repos/${REPO}/actions/runners/registration-token" \
  --jq '.token')"

if [[ -z "$TOKEN" ]]; then
  echo "BLOCKED: GitHub did not return a runner registration token."
  exit 9
fi

sudo -iu "$RUNNER_USER" bash -c '
  set -Eeuo pipefail
  cd "$1"
  ./config.sh \
    --unattended \
    --replace \
    --url "$2" \
    --token "$3" \
    --name "$4" \
    --labels "dealix-vps,dealix-command,ollama,n8n" \
    --work "_work"
' _ "$RUNNER_DIR" "$REPO_URL" "$TOKEN" "$RUNNER_NAME"
unset TOKEN

cd "$RUNNER_DIR"
./svc.sh install "$RUNNER_USER"
./svc.sh start

if ! ./svc.sh status; then
  echo "BLOCKED: newly installed runner service is not healthy."
  exit 12
fi

print_runner_proof false
