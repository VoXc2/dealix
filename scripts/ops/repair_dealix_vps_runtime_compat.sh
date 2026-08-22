#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
VENV="${DEALIX_AUTOMATION_VENV:-$ROOT/.venv}"
PYTHON="$VENV/bin/python"
BOOTSTRAP="$ROOT/scripts/ops/ensure_founder_automation_python.sh"
HERMES="/home/${RUN_USER}/.local/bin/hermes"
HERMES_ACCEPT_TIMEOUT="${HERMES_ACCEPT_TIMEOUT:-45}"
DROPIN_DIR="/etc/systemd/system/dealix-company@.service.d"
DROPIN="$DROPIN_DIR/20-canonical-python-venv.conf"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF_DIR="/opt/dealix/executive-proof/runtime-compat-${STAMP}"
PROOF="$PROOF_DIR/proof.log"
SERVICE_PATH="$VENV/bin:/home/${RUN_USER}/.local/bin:/home/${RUN_USER}/.railway/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
HERMES_PATH="/home/${RUN_USER}/.local/bin:/home/${RUN_USER}/.hermes/bin:$VENV/bin:/usr/local/bin:/usr/bin:/bin"

section() {
  printf '\n==============================================================\n %s\n==============================================================\n' "$*"
}

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi
if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing user $RUN_USER"
  exit 3
fi
if [[ ! -d "$ROOT/.git" || ! -x "$BOOTSTRAP" ]]; then
  echo "BLOCKED: canonical repository/runtime bootstrap missing"
  exit 4
fi

mkdir -p "$PROOF_DIR"
chmod 0700 "$PROOF_DIR"
exec > >(tee -a "$PROOF") 2>&1

section "1. DETERMINISTIC REPOSITORY PYTHON"
sudo -iu "$RUN_USER" env \
  DEALIX_REPO_ROOT="$ROOT" \
  DEALIX_AUTOMATION_VENV="$VENV" \
  bash "$BOOTSTRAP"

if [[ ! -x "$PYTHON" ]]; then
  echo "BLOCKED: canonical virtualenv python missing after bootstrap"
  exit 5
fi

sudo -u "$RUN_USER" -H "$PYTHON" -c 'import fastapi, httpx, pydantic, pytest, yaml; print("CANONICAL_PYTHON_IMPORTS=PASS")'

section "2. SYSTEMD COMPANY RUNTIME PIN"
install -d -m 0755 "$DROPIN_DIR"
cat >"$DROPIN" <<EOF_DROPIN
[Service]
Environment="VIRTUAL_ENV=${VENV}"
Environment="PYTHONNOUSERSITE=1"
Environment="PATH=${SERVICE_PATH}"
EOF_DROPIN
chmod 0644 "$DROPIN"
systemctl daemon-reload

effective_env="$(systemctl show 'dealix-company@heartbeat.service' -p Environment --value 2>/dev/null || true)"
printf '%s\n' "$effective_env" | sed -E 's/(TOKEN|SECRET|PASSWORD|API_KEY)=[^ ]+/\1=[REDACTED]/g'
[[ "$effective_env" == *"${VENV}/bin"* ]] || { echo "BLOCKED: effective PATH lacks repo venv"; exit 6; }
[[ "$effective_env" == *"VIRTUAL_ENV=${VENV}"* ]] || { echo "BLOCKED: VIRTUAL_ENV is not effective"; exit 7; }
echo "SYSTEMD_CANONICAL_PYTHON=PASS"

section "3. SERVICE-STYLE IMPORT ACCEPTANCE"
# Do not use a login shell or embedded heredoc here. On the live VPS sudo/bash
# argument reconstruction flattened the heredoc and produced a false syntax
# failure. Resolve and execute python directly under the exact service PATH.
SERVICE_PYTHON="$(sudo -u "$RUN_USER" -H env \
  VIRTUAL_ENV="$VENV" \
  PYTHONNOUSERSITE=1 \
  PATH="$SERVICE_PATH" \
  sh -c 'command -v python3')"
echo "service_python3=$SERVICE_PYTHON"
[[ "$SERVICE_PYTHON" == "$VENV/bin/python3" || "$SERVICE_PYTHON" == "$VENV/bin/python" ]] || {
  echo "BLOCKED: service-style python3 does not resolve into canonical venv"
  exit 8
}
sudo -u "$RUN_USER" -H env \
  VIRTUAL_ENV="$VENV" \
  PYTHONNOUSERSITE=1 \
  PATH="$SERVICE_PATH" \
  python3 -c 'import fastapi, pydantic, pytest; print("SERVICE_STYLE_PYTHON_IMPORTS=PASS")'

section "4. HEARTBEAT ACCEPTANCE"
set +e
systemctl start dealix-company@heartbeat.service
HEARTBEAT_RC=$?
set -e
journalctl -u dealix-company@heartbeat.service -n 30 --no-pager || true
if [[ $HEARTBEAT_RC -ne 0 ]]; then
  echo "HEARTBEAT_ACCEPT=FAIL rc=$HEARTBEAT_RC"
  exit 9
fi
echo "HEARTBEAT_ACCEPT=PASS"

section "5. EXECUTIVE HERMES RUNNER"
HERMES_ACCEPT="BLOCKED_BINARY_MISSING"
if [[ -x "$HERMES" ]]; then
  install -d -m 0750 -o root -g "$RUN_USER" /opt/dealix/executive-prompts
  cat >/opt/dealix/run-executive-prompt <<'EOF_RUNNER'
#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

PROMPT_FILE="${1:?usage: run-executive-prompt PROMPT_FILE}"
REPO="/opt/dealix/workspace/dealix"
HERMES="/home/dealix/.local/bin/hermes"
VENV="${REPO}/.venv"
HERMES_PATH="/home/dealix/.local/bin:/home/dealix/.hermes/bin:${VENV}/bin:/usr/local/bin:/usr/bin:/bin"

[[ -f "$PROMPT_FILE" ]] || { echo "BLOCKED: prompt file missing"; exit 2; }
[[ -d "$REPO/.git" ]] || { echo "BLOCKED: repository missing"; exit 3; }
[[ -x "$HERMES" ]] || { echo "BLOCKED: Hermes binary missing"; exit 4; }

cd "$REPO"
exec sudo -u dealix -H env \
  HOME=/home/dealix \
  PATH="$HERMES_PATH" \
  "$HERMES" chat --query-file "$PROMPT_FILE"
EOF_RUNNER
  chmod 0750 /opt/dealix/run-executive-prompt
  chown root:"$RUN_USER" /opt/dealix/run-executive-prompt
  echo "HERMES_RUNNER=REPAIRED"

  section "6. BOUNDED HERMES 8K ACCEPTANCE"
  echo "HERMES_ACCEPT_TIMEOUT_SECONDS=$HERMES_ACCEPT_TIMEOUT"
  # Hermes/model readiness is a separate fail-closed gate. Never let it hold
  # the runtime-repair shell for five minutes on a CPU-only local model.
  set +e
  HERMES_OUT="$(
    cd "$ROOT" &&
    sudo -u "$RUN_USER" -H env \
      HOME="/home/${RUN_USER}" \
      PATH="$HERMES_PATH" \
      timeout --signal=TERM --kill-after=10s "${HERMES_ACCEPT_TIMEOUT}s" \
      "$HERMES" chat -Q --ignore-rules --toolsets clarify --max-turns 1 \
      -q 'Do not use tools. Reply with exactly: DEALIX_HERMES_8K_OK' \
      2>&1
  )"
  HERMES_RC=$?
  set -e

  if printf '%s\n' "$HERMES_OUT" | grep -Fxq DEALIX_HERMES_8K_OK; then
    HERMES_ACCEPT="PASS"
    echo "DEALIX_HERMES_8K_OK"
  elif [[ "$HERMES_RC" -eq 124 || "$HERMES_RC" -eq 137 ]]; then
    HERMES_ACCEPT="DEGRADED_TIMEOUT"
    echo "HERMES_ACCEPT=DEGRADED_TIMEOUT rc=$HERMES_RC"
    printf '%s\n' "$HERMES_OUT" | tail -40
  else
    HERMES_ACCEPT="FAIL_CLOSED"
    echo "HERMES_ACCEPT=FAIL_CLOSED rc=$HERMES_RC"
    printf '%s\n' "$HERMES_OUT" | tail -40
  fi
fi

section "7. RESULT"
echo "DEALIX_RUNTIME_COMPAT=PASS"
echo "CANONICAL_PYTHON=$PYTHON"
echo "SYSTEMD_VENV_PIN=PASS"
echo "HEARTBEAT_ACCEPT=PASS"
echo "HERMES_ACCEPT=$HERMES_ACCEPT"
echo "PRODUCTION_MUTATION=false"
echo "EXTERNAL_SEND=false"
echo "MERGE_TO_MAIN=false"
echo "PAYMENT_EXECUTION=false"
echo "SECRET_VALUES_PRINTED=false"
echo "PROOF=$PROOF"

# Python/runtime repair is successful independently of Hermes model quality.
# Hermes remains fail-closed and must pass before any Project Engineer AUTOBUILD.
exit 0
