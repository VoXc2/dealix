#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONNOUSERSITE=1

LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-smoke/$STAMP"
EMAIL_DOMAIN="${DEALIX_OSS_EMAIL_DOMAIN:-dealix.me}"

install -d -o root -g "$DEALIX_GROUP" -m 0750 "$PROOF"
exec > >(tee -a "$PROOF/smoke.log") 2>&1

PASS=0
FAIL=0
HOLD=0
RESULTS="$PROOF/results.tsv"
printf 'component\tstatus\tdetail\n' > "$RESULTS"

pass(){ PASS=$((PASS+1)); printf '%s\tPASS\t%s\n' "$1" "${2:-ok}" >> "$RESULTS"; echo "[PASS] $1 ${2:-}"; }
fail(){ FAIL=$((FAIL+1)); printf '%s\tFAIL\t%s\n' "$1" "${2:-failed}" >> "$RESULTS"; echo "[FAIL] $1 ${2:-}"; }
hold(){ HOLD=$((HOLD+1)); printf '%s\tHOLD\t%s\n' "$1" "${2:-hold}" >> "$RESULTS"; echo "[HOLD] $1 ${2:-}"; }

as_dealix(){ sudo -u "$DEALIX_USER" -H "$@"; }

check_py_import(){
  local name="$1" import_stmt="$2"
  local py="$LAB_ROOT/$name/venv/bin/python"
  if [[ ! -x "$py" ]]; then hold "$name" "not_installed"; return 0; fi
  if as_dealix "$py" -c "$import_stmt" >"$PROOF/$name.out" 2>"$PROOF/$name.err"; then
    pass "$name" "import_ok"
  else
    fail "$name" "import_failed"
  fi
}

check_cmd(){
  local name="$1" cmd="$2"
  if [[ ! -x "$cmd" ]]; then hold "$name" "not_installed"; return 0; fi
  if as_dealix "$cmd" --version >"$PROOF/$name.out" 2>"$PROOF/$name.err"; then
    pass "$name" "version_ok"
  else
    fail "$name" "version_failed"
  fi
}

check_py_import presidio 'import presidio_analyzer, presidio_anonymizer'
check_cmd schemathesis "$LAB_ROOT/schemathesis/venv/bin/schemathesis"
check_py_import docling 'import docling'
check_py_import faster-whisper 'import faster_whisper'
check_py_import camel-tools 'import camel_tools'
check_py_import livekit-agents 'from livekit import agents'
check_py_import pipecat 'import pipecat'
check_cmd promptfoo "$LAB_ROOT/promptfoo/node_modules/.bin/promptfoo"

CHECKDMARC="$LAB_ROOT/checkdmarc/venv/bin/checkdmarc"
if [[ -x "$CHECKDMARC" ]]; then
  set +e
  as_dealix "$CHECKDMARC" "$EMAIL_DOMAIN" --format json \
    > "$PROOF/checkdmarc-$EMAIL_DOMAIN.json" \
    2> "$PROOF/checkdmarc-$EMAIL_DOMAIN.err"
  rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    pass checkdmarc "domain_read_only_ok"
  else
    # Invalid/missing DNS records are evidence, not an installer failure.
    hold checkdmarc "domain_findings_or_cli_nonzero_rc=$rc"
  fi
else
  hold checkdmarc "not_installed"
fi

if command -v docker >/dev/null 2>&1; then
  for spec in \
    'changedetection|ghcr.io/dgtlmoon/changedetection.io:latest' \
    'zaproxy|ghcr.io/zaproxy/zaproxy:stable' \
    'mailpit|axllent/mailpit:latest'
  do
    name="${spec%%|*}"
    image="${spec#*|}"
    if docker image inspect "$image" >/dev/null 2>&1; then
      docker image inspect "$image" --format '{{json .RepoDigests}}' \
        > "$PROOF/$name-image.json" 2>/dev/null || true
      pass "$name-image" "present_not_running"
    else
      hold "$name-image" "not_pulled"
    fi
  done
else
  hold docker-images "docker_unavailable"
fi

cat > "$PROOF/receipt.json" <<EOF
{
  "schema_version": 1,
  "timestamp": "$STAMP",
  "pass": $PASS,
  "fail": $FAIL,
  "hold": $HOLD,
  "email_domain": "$EMAIL_DOMAIN",
  "services_started": false,
  "ports_exposed": false,
  "active_security_scan_executed": false,
  "customer_effects": false
}
EOF

cat "$RESULTS"
echo "PASS=$PASS"
echo "FAIL=$FAIL"
echo "HOLD=$HOLD"
echo "PROOF_ROOT=$PROOF"
echo "ACTIVE_SCAN_EXECUTED=false"
echo "SERVICES_STARTED=false"

[[ "$FAIL" -eq 0 ]]
