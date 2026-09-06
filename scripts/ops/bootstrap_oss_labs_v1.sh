#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONNOUSERSITE=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export GIT_TERMINAL_PROMPT=0
export GH_PROMPT_DISABLED=1

###############################################################################
# Dealix OSS Lab Bootstrap V1
#
# Purpose:
# - Install high-value open-source capabilities in isolated lab directories.
# - Record exact resolved versions and rollback evidence.
# - Start NO service, expose NO port, mutate NO Production DB/DNS/secret state.
#
# Default profile: full
#   core -> Presidio, Schemathesis, checkdmarc, Docling, Promptfoo
#   full -> core + faster-whisper, CAMeL Tools, LiveKit Agents, Pipecat,
#           changedetection.io image, ZAP image, Mailpit image
#
# This bootstrap deliberately does NOT install parallel CRM/database/scheduler
# systems and does NOT activate outbound/customer effects.
###############################################################################

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "[FAIL] run as root"
  exit 2
fi

PROFILE="${DEALIX_OSS_PROFILE:-full}"
UPDATE_EXISTING="${DEALIX_OSS_UPDATE:-0}"
INSTALL_PREREQS="${DEALIX_OSS_INSTALL_PREREQS:-1}"
PULL_IMAGES="${DEALIX_OSS_PULL_IMAGES:-1}"

case "$PROFILE" in
  core|full) ;;
  *) echo "[FAIL] DEALIX_OSS_PROFILE must be core or full"; exit 3 ;;
esac

LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-bootstrap/$STAMP"
STATE="$CONTROL/state/oss-harvest"
BIN="$LAB_ROOT/bin"
LOCK="$CONTROL/locks/oss-bootstrap.lock"

install -d -o root -g "$DEALIX_GROUP" -m 0750 \
  "$PROOF" "$STATE" "$CONTROL/locks"
install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 \
  "$LAB_ROOT" "$BIN"

exec 9>"$LOCK"
flock -n 9 || {
  echo "[FAIL] another OSS bootstrap is active"
  exit 10
}

exec > >(tee -a "$PROOF/bootstrap.log") 2>&1

RESULTS="$PROOF/components.tsv"
printf 'component\tstatus\trc\n' > "$RESULTS"

PASS=0
FAIL=0
SKIP=0

section() {
  echo
  echo "======================================================================"
  echo " $*"
  echo "======================================================================"
}

run_component() {
  local name="$1"
  shift
  local log="$PROOF/${name}.log"
  local rc=0

  echo "[START] $name"
  set +e
  "$@" >"$log" 2>&1
  rc=$?
  set -e

  if [[ "$rc" -eq 0 ]]; then
    PASS=$((PASS + 1))
    printf '%s\tPASS\t0\n' "$name" >> "$RESULTS"
    echo "[PASS] $name"
  else
    FAIL=$((FAIL + 1))
    printf '%s\tFAIL\t%s\n' "$name" "$rc" >> "$RESULTS"
    echo "[FAIL] $name rc=$rc"
  fi

  tail -n 25 "$log" 2>/dev/null || true
  return 0
}

skip_component() {
  local name="$1"
  local why="$2"
  SKIP=$((SKIP + 1))
  printf '%s\tSKIP\t0\n' "$name" >> "$RESULTS"
  echo "[SKIP] $name: $why"
}

as_dealix() {
  sudo -u "$DEALIX_USER" -H "$@"
}

ensure_prereqs() {
  if [[ "$INSTALL_PREREQS" != "1" ]]; then
    command -v python3 >/dev/null
    command -v git >/dev/null
    command -v jq >/dev/null
    return 0
  fi

  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    git jq curl ca-certificates build-essential pkg-config
}

ensure_venv() {
  local name="$1"
  local dir="$LAB_ROOT/$name"
  if [[ ! -x "$dir/venv/bin/python" ]]; then
    install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$dir"
    as_dealix python3 -m venv "$dir/venv"
  fi
  if [[ "$UPDATE_EXISTING" == "1" || ! -s "$dir/.pip-ready" ]]; then
    as_dealix "$dir/venv/bin/python" -m pip install -U pip wheel setuptools
    as_dealix touch "$dir/.pip-ready"
  fi
  printf '%s' "$dir"
}

install_python_component() {
  local name="$1"
  local smoke="$2"
  shift 2
  local dir
  dir="$(ensure_venv "$name")"

  if [[ "$UPDATE_EXISTING" == "1" || ! -s "$dir/.installed" ]]; then
    as_dealix "$dir/venv/bin/python" -m pip install -U "$@"
    as_dealix touch "$dir/.installed"
  fi

  as_dealix "$dir/venv/bin/python" -m pip freeze \
    > "$PROOF/${name}.freeze.txt"
  cp "$PROOF/${name}.freeze.txt" "$dir/requirements.lock.txt"
  chown "$DEALIX_USER:$DEALIX_GROUP" "$dir/requirements.lock.txt"
  chmod 0640 "$dir/requirements.lock.txt"

  as_dealix "$dir/venv/bin/python" -c "$smoke"
}

install_presidio() {
  install_python_component \
    presidio \
    'import importlib.metadata as m; import presidio_analyzer, presidio_anonymizer; print("presidio-analyzer=" + m.version("presidio-analyzer")); print("presidio-anonymizer=" + m.version("presidio-anonymizer"))' \
    presidio-analyzer presidio-anonymizer
}

install_schemathesis() {
  install_python_component \
    schemathesis \
    'import importlib.metadata as m; import schemathesis; print("schemathesis=" + m.version("schemathesis"))' \
    schemathesis
  ln -sfn "$LAB_ROOT/schemathesis/venv/bin/schemathesis" "$BIN/schemathesis"
}

install_checkdmarc() {
  install_python_component \
    checkdmarc \
    'import importlib.metadata as m; import checkdmarc; print("checkdmarc=" + m.version("checkdmarc"))' \
    checkdmarc
  ln -sfn "$LAB_ROOT/checkdmarc/venv/bin/checkdmarc" "$BIN/checkdmarc"
}

install_docling() {
  install_python_component \
    docling \
    'import importlib.metadata as m; import docling; print("docling=" + m.version("docling"))' \
    docling
  if [[ -x "$LAB_ROOT/docling/venv/bin/docling" ]]; then
    ln -sfn "$LAB_ROOT/docling/venv/bin/docling" "$BIN/docling"
  fi
}

install_faster_whisper() {
  install_python_component \
    faster-whisper \
    'import importlib.metadata as m; import faster_whisper; print("faster-whisper=" + m.version("faster-whisper"))' \
    faster-whisper
}

install_camel_tools() {
  install_python_component \
    camel-tools \
    'import importlib.metadata as m; import camel_tools; print("camel-tools=" + m.version("camel-tools"))' \
    camel-tools
}

install_livekit_agents() {
  install_python_component \
    livekit-agents \
    'import importlib.metadata as m; from livekit import agents; print("livekit-agents=" + m.version("livekit-agents"))' \
    livekit-agents
}

install_pipecat() {
  install_python_component \
    pipecat \
    'import importlib.metadata as m; import pipecat; print("pipecat-ai=" + m.version("pipecat-ai"))' \
    pipecat-ai
}

install_promptfoo() {
  command -v node >/dev/null
  command -v npm >/dev/null

  local dir="$LAB_ROOT/promptfoo"
  install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$dir"

  if [[ "$UPDATE_EXISTING" == "1" || ! -x "$dir/node_modules/.bin/promptfoo" ]]; then
    as_dealix npm install \
      --prefix "$dir" \
      --no-fund \
      --no-audit \
      promptfoo@latest
  fi

  as_dealix "$dir/node_modules/.bin/promptfoo" --version
  as_dealix npm ls --prefix "$dir" --depth=0 --json \
    > "$PROOF/promptfoo.npm-lock-summary.json" || true
  set +e
  as_dealix npm audit --prefix "$dir" --omit=dev --json \
    > "$PROOF/promptfoo.audit.json" 2> "$PROOF/promptfoo.audit.err"
  set -e
  ln -sfn "$dir/node_modules/.bin/promptfoo" "$BIN/promptfoo"
}

pull_image() {
  local image="$1"
  docker pull "$image"
  docker image inspect "$image" \
    --format '{{json .RepoDigests}}' || true
}

pull_changedetection() {
  pull_image ghcr.io/dgtlmoon/changedetection.io:latest
}

pull_zap() {
  pull_image ghcr.io/zaproxy/zaproxy:stable
}

pull_mailpit() {
  pull_image axllent/mailpit:latest
}

write_runtime_receipt() {
  local disk_free
  disk_free="$(df -B1 --output=avail "$LAB_ROOT" | tail -1 | tr -d ' ')"

  cat > "$PROOF/runtime-receipt.json" <<EOF
{
  "schema_version": 1,
  "timestamp": "$STAMP",
  "profile": "$PROFILE",
  "lab_root": "$LAB_ROOT",
  "pass": $PASS,
  "fail": $FAIL,
  "skip": $SKIP,
  "disk_free_bytes_after": ${disk_free:-0},
  "services_started": false,
  "ports_exposed": false,
  "production_mutation": false,
  "dns_mutation": false,
  "db_mutation": false,
  "secret_mutation": false,
  "customer_send": false,
  "payment_execution": false
}
EOF
  chmod 0640 "$PROOF/runtime-receipt.json"
}

write_rollback() {
  cat > "$PROOF/rollback.sh" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
# Removes only Dealix OSS lab files. It does not prune shared Docker images.
rm -rf \
  "$LAB_ROOT/presidio" \
  "$LAB_ROOT/schemathesis" \
  "$LAB_ROOT/checkdmarc" \
  "$LAB_ROOT/docling" \
  "$LAB_ROOT/promptfoo" \
  "$LAB_ROOT/faster-whisper" \
  "$LAB_ROOT/camel-tools" \
  "$LAB_ROOT/livekit-agents" \
  "$LAB_ROOT/pipecat" \
  "$LAB_ROOT/bin"
echo "Dealix OSS lab files removed. Docker images, if pulled, were intentionally left in the shared Docker cache."
EOF
  chmod 0750 "$PROOF/rollback.sh"
}

section "0. SAFETY CONTRACT"
echo "NORTH_STAR=CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
echo "PROFILE=$PROFILE"
echo "LAB_ROOT=$LAB_ROOT"
echo "SERVICES_WILL_START=false"
echo "PORTS_WILL_OPEN=false"
echo "PRODUCTION_MUTATION=false"
echo "CUSTOMER_EFFECTS=false"

section "1. HOST CAPACITY"
df -h "$LAB_ROOT" || true
free -h || true

section "2. PREREQUISITES"
run_component prerequisites ensure_prereqs

section "3. CORE CAPABILITIES"
run_component presidio install_presidio
run_component schemathesis install_schemathesis
run_component checkdmarc install_checkdmarc
run_component docling install_docling
run_component promptfoo install_promptfoo

if [[ "$PROFILE" == "full" ]]; then
  section "4. FULL LANGUAGE / VOICE LAB"
  run_component faster-whisper install_faster_whisper
  run_component camel-tools install_camel_tools
  run_component livekit-agents install_livekit_agents
  run_component pipecat install_pipecat

  section "5. DOCKER IMAGES ONLY — NO CONTAINERS STARTED"
  if [[ "$PULL_IMAGES" == "1" ]] && command -v docker >/dev/null 2>&1; then
    run_component changedetection-image pull_changedetection
    run_component zap-image pull_zap
    run_component mailpit-image pull_mailpit
  else
    skip_component changedetection-image "Docker unavailable or DEALIX_OSS_PULL_IMAGES=0"
    skip_component zap-image "Docker unavailable or DEALIX_OSS_PULL_IMAGES=0"
    skip_component mailpit-image "Docker unavailable or DEALIX_OSS_PULL_IMAGES=0"
  fi
fi

section "6. INVENTORY"
find "$LAB_ROOT" -maxdepth 3 -type f \( \
  -name requirements.lock.txt -o \
  -name package.json -o \
  -name package-lock.json \
\) -printf '%p\n' | sort || true

if command -v docker >/dev/null 2>&1; then
  docker image inspect \
    ghcr.io/dgtlmoon/changedetection.io:latest \
    ghcr.io/zaproxy/zaproxy:stable \
    axllent/mailpit:latest \
    --format '{{.RepoTags}} {{.RepoDigests}}' \
    > "$PROOF/docker-images.txt" 2>/dev/null || true
fi

write_runtime_receipt
write_rollback

section "7. SUMMARY"
cat "$RESULTS"
echo "PASS=$PASS"
echo "FAIL=$FAIL"
echo "SKIP=$SKIP"
echo "PROOF_ROOT=$PROOF"
echo "LAB_ROOT=$LAB_ROOT"
echo "SERVICES_STARTED=false"
echo "PORTS_EXPOSED=false"
echo "NEXT=RUN_BOUNDED_BENCHMARKS_AND_PROMOTE_ONLY_WINNERS"

# Installation failures are surfaced in receipts but do not roll back successful,
# isolated components. Return non-zero so automation cannot call a partial lab Green.
if [[ "$FAIL" -gt 0 ]]; then
  exit 20
fi
