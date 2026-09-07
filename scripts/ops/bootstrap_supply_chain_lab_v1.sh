#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export GIT_TERMINAL_PROMPT=0
export GH_PROMPT_DISABLED=1

# Dealix Supply-Chain Lab V1
# Installs pinned scanner/SBOM binaries into an isolated lab only.
# It never changes Production PATH, dependencies, deployments, DNS, DB, secrets,
# customer communication, payment state, or public surfaces.

[[ "${EUID:-$(id -u)}" -eq 0 ]] || { echo "[FAIL] run as root"; exit 2; }

DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
LAB_ROOT="${DEALIX_SUPPLY_CHAIN_LAB_ROOT:-/opt/dealix/labs/supply-chain}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
BIN="$LAB_ROOT/bin"
STAMP="$(date '+%Y%m%dT%H%M%S%z')"
PROOF="$CONTROL/proof/supply-chain-lab-v1/$STAMP"
TMP="$(mktemp -d)"

OSV_VERSION="v2.5.1"
SYFT_VERSION="v1.51.1"
GRYPE_VERSION="v0.118.0"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

install -d -m 0750 -o "$DEALIX_USER" -g "$DEALIX_GROUP" "$LAB_ROOT" "$BIN"
install -d -m 0700 "$PROOF"

case "$(uname -m)" in
  x86_64|amd64) ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
  *) echo "[FAIL] unsupported architecture: $(uname -m)"; exit 3 ;;
esac

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "[FAIL] required command missing: $1"; exit 4; }
}
need_cmd curl
need_cmd sha256sum
need_cmd tar

fetch() {
  local url="$1" out="$2"
  curl --fail --location --silent --show-error \
    --connect-timeout 15 --max-time 300 \
    "$url" -o "$out"
}

verify_checksum_line() {
  local sums="$1" artifact="$2" basename
  basename="$(basename "$artifact")"
  local line
  line="$(grep -E "[[:space:]]\\*?${basename//./\\.}$" "$sums" | head -n 1 || true)"
  [[ -n "$line" ]] || { echo "[FAIL] checksum entry missing for $basename"; exit 5; }
  local expected actual
  expected="$(printf '%s\n' "$line" | awk '{print $1}')"
  actual="$(sha256sum "$artifact" | awk '{print $1}')"
  [[ "$expected" == "$actual" ]] || {
    echo "[FAIL] checksum mismatch for $basename"
    exit 6
  }
  printf '%s  %s\n' "$actual" "$basename" >> "$PROOF/verified_sha256.txt"
}

install_osv() {
  local artifact="osv-scanner_linux_${ARCH}"
  local base="https://github.com/google/osv-scanner/releases/download/${OSV_VERSION}"
  fetch "$base/$artifact" "$TMP/$artifact"
  fetch "$base/osv-scanner_SHA256SUMS" "$TMP/osv-scanner_SHA256SUMS"
  verify_checksum_line "$TMP/osv-scanner_SHA256SUMS" "$TMP/$artifact"
  install -m 0750 -o "$DEALIX_USER" -g "$DEALIX_GROUP" "$TMP/$artifact" "$BIN/osv-scanner"
}

install_syft() {
  local v="${SYFT_VERSION#v}"
  local artifact="syft_${v}_linux_${ARCH}.tar.gz"
  local sums="syft_${v}_checksums.txt"
  local base="https://github.com/anchore/syft/releases/download/${SYFT_VERSION}"
  fetch "$base/$artifact" "$TMP/$artifact"
  fetch "$base/$sums" "$TMP/$sums"
  verify_checksum_line "$TMP/$sums" "$TMP/$artifact"
  tar -xzf "$TMP/$artifact" -C "$TMP" syft
  install -m 0750 -o "$DEALIX_USER" -g "$DEALIX_GROUP" "$TMP/syft" "$BIN/syft"
}

install_grype() {
  local v="${GRYPE_VERSION#v}"
  local artifact="grype_${v}_linux_${ARCH}.tar.gz"
  local sums="grype_${v}_checksums.txt"
  local base="https://github.com/anchore/grype/releases/download/${GRYPE_VERSION}"
  fetch "$base/$artifact" "$TMP/$artifact"
  fetch "$base/$sums" "$TMP/$sums"
  verify_checksum_line "$TMP/$sums" "$TMP/$artifact"
  tar -xzf "$TMP/$artifact" -C "$TMP" grype
  install -m 0750 -o "$DEALIX_USER" -g "$DEALIX_GROUP" "$TMP/grype" "$BIN/grype"
}

install_osv
install_syft
install_grype

{
  echo "OSV_VERSION=$($BIN/osv-scanner --version 2>&1 | head -n 1)"
  echo "SYFT_VERSION=$($BIN/syft version 2>&1 | head -n 1)"
  echo "GRYPE_VERSION=$($BIN/grype version 2>&1 | head -n 1)"
} | tee "$PROOF/versions.env"

cat > "$PROOF/receipt.env" <<EOF
SCHEMA_VERSION=1
TIMESTAMP=$STAMP
LAB_ROOT=$LAB_ROOT
ARCH=$ARCH
SERVICES_STARTED=false
PORTS_EXPOSED=false
PRODUCTION_MUTATION=false
DEPLOYMENT=false
DNS_MUTATION=false
DB_MUTATION=false
SECRET_MUTATION=false
CUSTOMER_EFFECTS=false
PAYMENT_EXECUTION=false
EOF

cat > "$PROOF/rollback.sh" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
rm -f "$BIN/osv-scanner" "$BIN/syft" "$BIN/grype"
EOF
chmod 0700 "$PROOF/rollback.sh"

printf 'DEALIX_SUPPLY_CHAIN_LAB_V1=PASS\n'
printf 'BIN=%s\n' "$BIN"
printf 'PROOF=%s\n' "$PROOF"
printf 'PRODUCTION_MUTATION=false\nCUSTOMER_EFFECTS=false\n'
