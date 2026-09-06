#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
PROFILE="${DEALIX_OSS_PROFILE:-full}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-smoke-v2/$STAMP"

install -d -o root -g "$DEALIX_GROUP" -m 0750 "$PROOF"
exec > >(tee -a "$PROOF/smoke.log") 2>&1
PASS=0; FAIL=0; HOLD=0
R="$PROOF/results.tsv"; printf 'component\tstatus\tdetail\n' >"$R"
pass(){ PASS=$((PASS+1)); printf '%s\tPASS\t%s\n' "$1" "$2" >>"$R"; }
fail(){ FAIL=$((FAIL+1)); printf '%s\tFAIL\t%s\n' "$1" "$2" >>"$R"; }
hold(){ HOLD=$((HOLD+1)); printf '%s\tHOLD\t%s\n' "$1" "$2" >>"$R"; }
as_dealix(){ sudo -u "$DEALIX_USER" -H "$@"; }
check_py(){ local n="$1" s="$2" py="$LAB_ROOT/$n/venv/bin/python"; [[ -x "$py" ]] || { hold "$n" not_installed; return; }; if as_dealix "$py" -c "$s" >"$PROOF/$n.out" 2>"$PROOF/$n.err"; then pass "$n" import_ok; else fail "$n" import_failed; fi; }

case "$PROFILE" in
 core|full)
  check_py presidio 'import presidio_analyzer,presidio_anonymizer'
  check_py schemathesis 'import schemathesis'
  check_py checkdmarc 'import checkdmarc'
  check_py docling 'import docling'
  check_py rapidfuzz 'from rapidfuzz import fuzz; assert fuzz.ratio("Dealix","Dealix")==100'
  check_py trafilatura 'import trafilatura'
 ;;&
 research|full)
  check_py rapidfuzz 'from rapidfuzz import fuzz; assert fuzz.ratio("Dealix","Dealix")==100'
  check_py trafilatura 'import trafilatura'
  check_py crawl4ai 'import crawl4ai'
 ;;&
 arabic|full)
  check_py camel-tools 'import camel_tools'
  check_py surya-ocr 'import surya'
 ;;&
 voice|full)
  check_py faster-whisper 'import faster_whisper'
  check_py silero-vad 'import silero_vad'
  check_py livekit-agents 'from livekit import agents'
  check_py pipecat 'import pipecat'
 ;;
 *) echo '[FAIL] invalid profile'; exit 2;;
esac

if command -v docker >/dev/null 2>&1 && [[ "$PROFILE" == full ]]; then
  for spec in 'changedetection|ghcr.io/dgtlmoon/changedetection.io:latest' 'zaproxy|ghcr.io/zaproxy/zaproxy:stable' 'mailpit|axllent/mailpit:latest'; do
    n="${spec%%|*}"; image="${spec#*|}"; if docker image inspect "$image" >/dev/null 2>&1; then pass "$n-image" present_not_running; else hold "$n-image" not_pulled; fi
  done
fi

cat >"$PROOF/receipt.json" <<EOF
{"schema_version":2,"timestamp":"$STAMP","profile":"$PROFILE","pass":$PASS,"fail":$FAIL,"hold":$HOLD,"services_started":false,"ports_exposed":false,"active_security_scan_executed":false,"customer_effects":false}
EOF
cat "$R"
echo "PASS=$PASS FAIL=$FAIL HOLD=$HOLD PROOF_ROOT=$PROOF"
[[ "$FAIL" -eq 0 ]]
