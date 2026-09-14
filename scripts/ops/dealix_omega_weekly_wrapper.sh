#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

source /usr/local/lib/dealix-omega-env

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN="$PROOF_ROOT/weekly/$STAMP"
mkdir -p "$RUN"
chmod 0750 "$RUN"

PYTHON="$REPO/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON="$(command -v python3)"

export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export DEALIX_LIVE_CHARGE=false
export DEALIX_AUTO_MERGE=false

as_dealix() {
  runuser -u "$RUN_USER" -- env \
    HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" \
    PATH="$RUN_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    "$@"
}
RC=0
if [[ -f "$REPO/scripts/commercial/run_weekly_proof_pack.py" ]]; then
  set +e
  as_dealix timeout 1800 \
    "$PYTHON" \
    "$REPO/scripts/commercial/run_weekly_proof_pack.py" \
    --client dealix \
    --mode draft-only \
    >"$RUN/weekly-proof.log" 2>&1
  RC=$?
  set -e
else
  echo "WEEKLY_PROOF_SCRIPT=NOT_FOUND" >"$RUN/weekly-proof.log"
fi

echo "$RC" >"$RUN/rc"
if [[ "$RC" -eq 0 ]]; then
  echo "WEEKLY_PROOF=PASS"
else
  echo "WEEKLY_PROOF=FAIL rc=$RC"
fi
exit "$RC"
