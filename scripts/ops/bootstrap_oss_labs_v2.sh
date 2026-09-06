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

# Dealix OSS Lab Bootstrap V2
# Profiles: core | research | arabic | voice | full
# Isolation only: no service start, no public port, no Production mutation.

[[ "${EUID:-$(id -u)}" -eq 0 ]] || { echo '[FAIL] run as root'; exit 2; }

PROFILE="${DEALIX_OSS_PROFILE:-full}"
UPDATE_EXISTING="${DEALIX_OSS_UPDATE:-0}"
PULL_IMAGES="${DEALIX_OSS_PULL_IMAGES:-1}"
LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-bootstrap-v2/$STAMP"
LOCK="$CONTROL/locks/oss-bootstrap-v2.lock"
BIN="$LAB_ROOT/bin"

case "$PROFILE" in core|research|arabic|voice|full) ;; *) echo '[FAIL] invalid profile'; exit 3;; esac

install -d -o root -g "$DEALIX_GROUP" -m 0750 "$PROOF" "$CONTROL/locks"
install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$LAB_ROOT" "$BIN"
exec 9>"$LOCK"; flock -n 9 || { echo '[FAIL] bootstrap already running'; exit 10; }
exec > >(tee -a "$PROOF/bootstrap.log") 2>&1

PASS=0; FAIL=0; SKIP=0
RESULTS="$PROOF/components.tsv"
printf 'component\tstatus\trc\n' > "$RESULTS"

as_dealix(){ sudo -u "$DEALIX_USER" -H "$@"; }
run(){ local n="$1"; shift; set +e; "$@" >"$PROOF/$n.log" 2>&1; rc=$?; set -e; if [[ $rc -eq 0 ]]; then PASS=$((PASS+1)); printf '%s\tPASS\t0\n' "$n" >>"$RESULTS"; else FAIL=$((FAIL+1)); printf '%s\tFAIL\t%s\n' "$n" "$rc" >>"$RESULTS"; fi; tail -n 20 "$PROOF/$n.log" || true; }
skip(){ SKIP=$((SKIP+1)); printf '%s\tSKIP\t0\n' "$1" >>"$RESULTS"; echo "[SKIP] $1: $2"; }

apt-get update
apt-get install -y --no-install-recommends python3 python3-venv python3-pip git jq curl ca-certificates build-essential pkg-config

ensure_venv(){ local n="$1" d="$LAB_ROOT/$1"; if [[ ! -x "$d/venv/bin/python" ]]; then install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$d"; as_dealix python3 -m venv "$d/venv"; fi; as_dealix "$d/venv/bin/python" -m pip install -U pip wheel setuptools >/dev/null; }
py_component(){ local n="$1" smoke="$2"; shift 2; local d="$LAB_ROOT/$n"; ensure_venv "$n"; if [[ "$UPDATE_EXISTING" == 1 || ! -s "$d/.installed" ]]; then as_dealix "$d/venv/bin/python" -m pip install -U "$@"; as_dealix touch "$d/.installed"; fi; as_dealix "$d/venv/bin/python" -m pip freeze >"$PROOF/$n.freeze.txt"; cp "$PROOF/$n.freeze.txt" "$d/requirements.lock.txt"; chown "$DEALIX_USER:$DEALIX_GROUP" "$d/requirements.lock.txt"; as_dealix "$d/venv/bin/python" -c "$smoke"; }

core(){
 run presidio py_component presidio 'import presidio_analyzer,presidio_anonymizer' presidio-analyzer presidio-anonymizer
 run schemathesis py_component schemathesis 'import schemathesis' schemathesis
 run checkdmarc py_component checkdmarc 'import checkdmarc' checkdmarc
 run docling py_component docling 'import docling' docling
 run rapidfuzz py_component rapidfuzz 'from rapidfuzz import fuzz; assert fuzz.ratio("Dealix","Dealix")==100' rapidfuzz
 run trafilatura py_component trafilatura 'import trafilatura' trafilatura
}
research(){
 run rapidfuzz py_component rapidfuzz 'from rapidfuzz import fuzz; assert fuzz.ratio("Dealix","Dealix")==100' rapidfuzz
 run trafilatura py_component trafilatura 'import trafilatura' trafilatura
 run crawl4ai-package py_component crawl4ai 'import crawl4ai' crawl4ai
}
arabic(){
 run camel-tools py_component camel-tools 'import camel_tools' camel-tools
 run surya-ocr-package py_component surya-ocr 'import surya' surya-ocr
}
voice(){
 run faster-whisper py_component faster-whisper 'import faster_whisper' faster-whisper
 run silero-vad-package py_component silero-vad 'import silero_vad' silero-vad
 run livekit-agents py_component livekit-agents 'from livekit import agents' livekit-agents
 run pipecat py_component pipecat 'import pipecat' pipecat-ai
}

case "$PROFILE" in
 core) core;; research) research;; arabic) arabic;; voice) voice;; full) core; research; arabic; voice;;
esac

if [[ "$PROFILE" == full && "$PULL_IMAGES" == 1 ]] && command -v docker >/dev/null 2>&1; then
 run changedetection-image docker pull ghcr.io/dgtlmoon/changedetection.io:latest
 run zap-image docker pull ghcr.io/zaproxy/zaproxy:stable
 run mailpit-image docker pull axllent/mailpit:latest
else
 skip docker-images 'not requested or Docker unavailable'
fi

cat >"$PROOF/receipt.json" <<EOF
{"schema_version":2,"timestamp":"$STAMP","profile":"$PROFILE","pass":$PASS,"fail":$FAIL,"skip":$SKIP,"services_started":false,"ports_exposed":false,"production_mutation":false,"dns_mutation":false,"db_mutation":false,"secret_mutation":false,"customer_send":false,"payment_execution":false}
EOF
cat >"$PROOF/rollback.sh" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
rm -rf "$LAB_ROOT/presidio" "$LAB_ROOT/schemathesis" "$LAB_ROOT/checkdmarc" "$LAB_ROOT/docling" "$LAB_ROOT/rapidfuzz" "$LAB_ROOT/trafilatura" "$LAB_ROOT/crawl4ai" "$LAB_ROOT/camel-tools" "$LAB_ROOT/surya-ocr" "$LAB_ROOT/faster-whisper" "$LAB_ROOT/silero-vad" "$LAB_ROOT/livekit-agents" "$LAB_ROOT/pipecat"
EOF
chmod 0750 "$PROOF/rollback.sh"

cat "$RESULTS"
echo "PASS=$PASS FAIL=$FAIL SKIP=$SKIP"
echo "PROOF_ROOT=$PROOF"
echo 'SERVICES_STARTED=false PORTS_EXPOSED=false CUSTOMER_EFFECTS=false'
[[ "$FAIL" -eq 0 ]]
