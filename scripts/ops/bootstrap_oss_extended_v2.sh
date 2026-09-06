#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONNOUSERSITE=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Extended packages are deliberately isolated from the existing full OSS profile.
# This script starts no service, downloads no model weights or browser runtimes,
# opens no ports, and performs no customer/Production/DNS/DB/secret effect.

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "[FAIL] run as root"
  exit 2
fi

LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-extended-bootstrap/$STAMP"
LOCK="$CONTROL/locks/oss-extended-bootstrap.lock"

install -d -o root -g "$DEALIX_GROUP" -m 0750 "$PROOF" "$CONTROL/locks"
install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$LAB_ROOT"

exec 9>"$LOCK"
flock -n 9 || { echo "[FAIL] another extended OSS bootstrap is active"; exit 10; }
exec > >(tee -a "$PROOF/bootstrap.log") 2>&1

PASS=0
FAIL=0
RESULTS="$PROOF/components.tsv"
printf 'component\tstatus\trc\n' > "$RESULTS"

as_dealix() { sudo -u "$DEALIX_USER" -H "$@"; }

run_component() {
  local name="$1"; shift
  local log="$PROOF/$name.log" rc=0
  set +e
  "$@" >"$log" 2>&1
  rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    PASS=$((PASS+1)); printf '%s\tPASS\t0\n' "$name" >> "$RESULTS"; echo "[PASS] $name"
  else
    FAIL=$((FAIL+1)); printf '%s\tFAIL\t%s\n' "$name" "$rc" >> "$RESULTS"; echo "[FAIL] $name rc=$rc"
  fi
  tail -n 30 "$log" || true
}

ensure_venv() {
  local name="$1" dir="$LAB_ROOT/$1"
  if [[ ! -x "$dir/venv/bin/python" ]]; then
    install -d -o "$DEALIX_USER" -g "$DEALIX_GROUP" -m 0750 "$dir"
    as_dealix python3 -m venv "$dir/venv"
  fi
  as_dealix "$dir/venv/bin/python" -m pip install -U pip wheel setuptools
}

install_pkg() {
  local name="$1" import_name="$2" package_name="$3"
  local dir="$LAB_ROOT/$name"
  ensure_venv "$name"
  as_dealix "$dir/venv/bin/python" -m pip install -U "$package_name"
  as_dealix "$dir/venv/bin/python" -c "import importlib.metadata as m; import ${import_name}; print(m.version('${package_name}'))"
  as_dealix "$dir/venv/bin/python" -m pip freeze > "$PROOF/$name.freeze.txt"
  cp "$PROOF/$name.freeze.txt" "$dir/requirements.lock.txt"
  chown "$DEALIX_USER:$DEALIX_GROUP" "$dir/requirements.lock.txt"
  chmod 0640 "$dir/requirements.lock.txt"
}

install_crawl4ai() { install_pkg crawl4ai crawl4ai crawl4ai; }
install_paddleocr() { install_pkg paddleocr paddleocr paddleocr; }
install_flagembedding() { install_pkg flagembedding FlagEmbedding FlagEmbedding; }
install_splink() { install_pkg splink splink splink; }

cat <<'EOF'
======================================================================
 DEALIX OSS EXTENDED LAB V2
======================================================================
NORTH_STAR=CASH_READY_AUTONOMOUS_DEALIX_COMPANY
SERVICES_STARTED=false
PORTS_EXPOSED=false
MODEL_DOWNLOADS=false
BROWSER_DOWNLOADS=false
CRAWLS_EXECUTED=false
PRODUCTION_MUTATION=false
CUSTOMER_EFFECTS=false

Extended candidates:
- Crawl4AI: public-web evidence extraction challenger
- PaddleOCR: Arabic/English OCR/document challenger
- FlagEmbedding: BGE-M3 multilingual retrieval package; no model download
- Splink: probabilistic entity-linkage package; adoption remains scale-gated
EOF

run_component crawl4ai install_crawl4ai
run_component paddleocr install_paddleocr
run_component flagembedding install_flagembedding
run_component splink install_splink

cat > "$PROOF/receipt.json" <<EOF
{
  "schema_version": 1,
  "timestamp": "$STAMP",
  "pass": $PASS,
  "fail": $FAIL,
  "services_started": false,
  "ports_exposed": false,
  "model_downloads": false,
  "browser_downloads": false,
  "crawls_executed": false,
  "production_mutation": false,
  "customer_effects": false
}
EOF
chmod 0640 "$PROOF/receipt.json"

cat > "$PROOF/rollback.sh" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
rm -rf \
  "$LAB_ROOT/crawl4ai" \
  "$LAB_ROOT/paddleocr" \
  "$LAB_ROOT/flagembedding" \
  "$LAB_ROOT/splink"
echo "Extended Dealix OSS lab packages removed."
EOF
chmod 0750 "$PROOF/rollback.sh"

cat "$RESULTS"
echo "PASS=$PASS"
echo "FAIL=$FAIL"
echo "PROOF_ROOT=$PROOF"
echo "NEXT=RUN_EXTENDED_SMOKE_THEN_BOUNDED_ARABIC_BENCHMARKS"

[[ "$FAIL" -eq 0 ]]
