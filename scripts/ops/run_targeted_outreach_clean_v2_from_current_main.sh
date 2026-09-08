#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export DEALIX_EXTERNAL_SEND=0 DEALIX_EMAIL_LIVE_SEND=0 DEALIX_WHATSAPP_OUTBOUND=0 DEALIX_PUBLIC_PUBLISH=0 DEALIX_PAID_SPEND=0 DEALIX_PAYMENT_EXECUTION=0 DEALIX_PRODUCTION_MUTATION=0 DEALIX_DNS_MUTATION=0 DEALIX_DB_MUTATION=0 DEALIX_SECRET_MUTATION=0 DEALIX_AUTONOMY_LEVEL=4 DEALIX_MODE=draft-only
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"; CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"; RUN_USER="${DEALIX_RUN_USER:-dealix}"; STAMP="$(date -u +%Y%m%dT%H%M%SZ)"; WT="$CONTROL/worktrees/targeted-outreach-clean-$STAMP"; PROOF="$CONTROL/proof/targeted-outreach-clean/$STAMP"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$CONTROL/worktrees" "$PROOF"
cleanup(){ set +e; sudo -u "$RUN_USER" git -c safe.directory="$REPO" -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true; }
trap cleanup EXIT
sudo -u "$RUN_USER" git -c safe.directory="$REPO" -C "$REPO" fetch origin main --quiet
MAIN="$(sudo -u "$RUN_USER" git -c safe.directory="$REPO" -C "$REPO" rev-parse origin/main)"
sudo -u "$RUN_USER" git -c safe.directory="$REPO" -C "$REPO" worktree add --detach "$WT" "$MAIN" >/dev/null
sudo -u "$RUN_USER" git -c safe.directory="$WT" -C "$WT" diff --check
sudo -u "$RUN_USER" env HOME="/home/$RUN_USER" DEALIX_EXTERNAL_SEND=0 DEALIX_EMAIL_LIVE_SEND=0 python3 "$WT/scripts/commercial/render_company_profile_pdf.py" | tee "$PROOF/profile.log"
sudo -u "$RUN_USER" env HOME="/home/$RUN_USER" DEALIX_EXTERNAL_SEND=0 DEALIX_EMAIL_LIVE_SEND=0 DEALIX_OUTREACH_MAX_DRAFTS=3 DEALIX_GMAIL_DRAFTS="${DEALIX_GMAIL_DRAFTS:-0}" GMAIL_TOKEN_PATH="${GMAIL_TOKEN_PATH:-$WT/token.json}" python3 "$WT/scripts/commercial/run_targeted_outreach_clean_v2.py" --max-drafts 3 | tee "$PROOF/outreach.log"
printf 'MAIN=%s\nEXTERNAL_SEND=0\nMAX_DRAFTS=3\nL5_EXECUTED=NONE\n' "$MAIN" | tee "$PROOF/summary.env"
echo "PROOF=$PROOF"
