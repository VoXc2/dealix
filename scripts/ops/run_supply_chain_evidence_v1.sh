#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export GIT_TERMINAL_PROMPT=0
export GH_PROMPT_DISABLED=1

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
LAB_ROOT="${DEALIX_SUPPLY_CHAIN_LAB_ROOT:-/opt/dealix/labs/supply-chain}"
BIN="$LAB_ROOT/bin"
STAMP="$(date '+%Y%m%dT%H%M%S%z')"
RUN="$CONTROL/proof/supply-chain-evidence-v1/$STAMP"

install -d -m 0700 "$RUN"

for tool in osv-scanner syft grype; do
  [[ -x "$BIN/$tool" ]] || {
    echo "DEALIX_SUPPLY_CHAIN_EVIDENCE_V1=BLOCKED_TOOL_MISSING"
    echo "missing=$BIN/$tool"
    exit 2
  }
done

[[ -d "$REPO/.git" || -f "$REPO/.git" ]] || {
  echo "DEALIX_SUPPLY_CHAIN_EVIDENCE_V1=BLOCKED_REPO_MISSING"
  exit 3
}

SOURCE_SHA="$(git -C "$REPO" rev-parse HEAD 2>/dev/null || printf UNKNOWN)"
STARTED="$(date --iso-8601=seconds)"

# SBOM is bound to the current source tree identity. It is evidence only.
"$BIN/syft" "dir:$REPO" -o cyclonedx-json="$RUN/source.cdx.json" \
  >"$RUN/syft.out" 2>"$RUN/syft.err"
SYFT_RC=$?

set +e
"$BIN/osv-scanner" scan source -r "$REPO" --format json \
  >"$RUN/osv.json" 2>"$RUN/osv.err"
OSV_RC=$?

"$BIN/grype" "sbom:$RUN/source.cdx.json" -o json \
  >"$RUN/grype.json" 2>"$RUN/grype.err"
GRYPE_RC=$?
set -e

COMPLETED="$(date --iso-8601=seconds)"

for f in source.cdx.json osv.json grype.json; do
  if [[ -s "$RUN/$f" ]]; then
    sha256sum "$RUN/$f" >> "$RUN/result_digests.sha256"
  fi
done

cat > "$RUN/receipt.env" <<EOF
SCHEMA_VERSION=1
SOURCE_SHA=$SOURCE_SHA
TARGET_KIND=source_tree
TARGET_IDENTITY=$REPO@$SOURCE_SHA
STARTED_AT=$STARTED
COMPLETED_AT=$COMPLETED
SYFT_RC=$SYFT_RC
OSV_RC=$OSV_RC
GRYPE_RC=$GRYPE_RC
PRODUCTION_MUTATION=false
DEPLOYMENT=false
DNS_MUTATION=false
DB_MUTATION=false
SECRET_MUTATION=false
CUSTOMER_EFFECTS=false
PAYMENT_EXECUTION=false
EOF

# Vulnerability scanners may return non-zero when findings exist. Preserve that as
# evidence rather than silently rewriting dependencies or Production.
echo "DEALIX_SUPPLY_CHAIN_EVIDENCE_V1=COMPLETE"
echo "SOURCE_SHA=$SOURCE_SHA"
echo "SYFT_RC=$SYFT_RC OSV_RC=$OSV_RC GRYPE_RC=$GRYPE_RC"
echo "PROOF=$RUN"
echo "AUTO_REMEDIATION=false"
echo "PRODUCTION_MUTATION=false"
echo "CUSTOMER_EFFECTS=false"
