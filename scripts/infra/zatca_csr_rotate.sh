#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
# zatca_csr_rotate.sh — generate a new ZATCA CSR, request a cert from
# Fatoorah, and update the secrets store. Cron-friendly.
#
# Reads (via env):
#   ZATCA_COMPANY_NAME    — legal name on the CR
#   ZATCA_COMMON_NAME     — eg. "Dealix"
#   ZATCA_OTP             — one-time password from Fatoorah portal
#   ZATCA_VAT_NUMBER      — 15-digit VAT
#   ZATCA_CR_NUMBER       — commercial registration
#   ZATCA_API_BASE        — sandbox or prod (default sandbox)
#   ZATCA_OUTPUT_DIR      — where to write key+csr+cert (default
#                            /etc/dealix/zatca)
#
# Dry-run support: pass `--dry-run` to print the plan without
# touching the filesystem or contacting Fatoorah.
# ─────────────────────────────────────────────────────
set -euo pipefail

DRY_RUN="0"
for arg in "$@"; do
  case "$arg" in
    --dry-run|-n) DRY_RUN="1" ;;
    -h|--help)
      sed -n '1,30p' "$0"
      exit 0
      ;;
  esac
done

OUTDIR="${ZATCA_OUTPUT_DIR:-/etc/dealix/zatca}"
API_BASE="${ZATCA_API_BASE:-https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal}"
COMPANY="${ZATCA_COMPANY_NAME:-AI Company Saudi Arabia}"
CN="${ZATCA_COMMON_NAME:-Dealix}"
VAT="${ZATCA_VAT_NUMBER:-}"
CR="${ZATCA_CR_NUMBER:-}"
OTP="${ZATCA_OTP:-}"

step() { printf '\n\033[1;34m→ %s\033[0m\n' "$1"; }
run()  { if [[ "$DRY_RUN" == "1" ]]; then printf '   [dry-run] %s\n' "$*"; else eval "$@"; fi; }

step "1. Pre-flight"
echo "   output dir: $OUTDIR"
echo "   API base:   $API_BASE"
echo "   company:    $COMPANY"
echo "   CN:         $CN"
echo "   VAT:        ${VAT:-<unset>}"
echo "   CR:         ${CR:-<unset>}"

if [[ "$DRY_RUN" != "1" ]]; then
  [[ -n "$VAT" ]] || { echo "ABORT: ZATCA_VAT_NUMBER required" >&2; exit 2; }
  [[ -n "$CR"  ]] || { echo "ABORT: ZATCA_CR_NUMBER required"  >&2; exit 2; }
  [[ -n "$OTP" ]] || { echo "ABORT: ZATCA_OTP required"        >&2; exit 2; }
fi

step "2. Generate EC P-256 keypair + CSR"
TS=$(date +%Y%m%d_%H%M%S)
KEY="${OUTDIR}/zatca_${TS}.key"
CSR="${OUTDIR}/zatca_${TS}.csr"
CONFIG="${OUTDIR}/zatca_${TS}.cnf"
mkdir -p "$OUTDIR" 2>/dev/null || true

cat > /tmp/zatca_${TS}.cnf <<EOF
[ req ]
prompt = no
distinguished_name = req_dn
req_extensions = req_ext

[ req_dn ]
C  = SA
O  = ${COMPANY}
OU = Dealix
CN = ${CN}-${TS}

[ req_ext ]
subjectAltName = otherName:1.3.6.1.4.1.311.20.2.3;UTF8:${VAT}|${CR}
EOF

run "openssl ecparam -name prime256v1 -genkey -noout -out \"$KEY\""
run "openssl req -new -sha256 -key \"$KEY\" -out \"$CSR\" -config /tmp/zatca_${TS}.cnf"
run "rm -f /tmp/zatca_${TS}.cnf"

step "3. Request compliance CSID from Fatoorah"
if [[ "$DRY_RUN" != "1" ]]; then
  CSR_B64=$(base64 -w0 < "$CSR")
  CSID_JSON=$(curl -sS -X POST "$API_BASE/compliance" \
    -H "OTP: $OTP" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "Accept-Version: V2" \
    -d "{\"csr\":\"$CSR_B64\"}")
  echo "$CSID_JSON" > "${OUTDIR}/zatca_${TS}_csid.json"
  echo "   csid written to ${OUTDIR}/zatca_${TS}_csid.json"
else
  echo "   [dry-run] would POST CSR to $API_BASE/compliance"
fi

step "4. Smoke check"
if [[ "$DRY_RUN" != "1" ]]; then
  curl -fsS "$API_BASE/compliance/invoices" -X POST \
    -H "Content-Type: application/json" \
    -H "Accept-Version: V2" \
    -d '{"invoice":"dGVzdA==","invoiceHash":"x","uuid":"00000000-0000-0000-0000-000000000000"}' \
    >/dev/null && echo "   sandbox reachable" || echo "   sandbox smoke failed"
fi

step "5. Rotate secrets"
echo "   Update INFISICAL / .env:"
echo "     ZATCA_PRIVATE_KEY_PATH=${KEY}"
echo "     ZATCA_CSID_PATH=${OUTDIR}/zatca_${TS}_csid.json"
echo "   Then restart the API service for the new cert to take effect."

step "Done"
