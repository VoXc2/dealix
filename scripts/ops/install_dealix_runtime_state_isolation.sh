#!/usr/bin/env bash
# Keep mutable Dealix VPS operating state outside the canonical Git worktree.
set -Eeuo pipefail
umask 027

REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
STATE_ROOT="${DEALIX_RUNTIME_STATE_ROOT:-/opt/dealix/company-autopilot/state}"
CONTROL_ROOT="${DEALIX_CONTROL_ROOT:-/opt/dealix/control}"
ENV_FILE="${CONTROL_ROOT}/runtime-state.env"
DROPIN_DIR="/etc/systemd/system/dealix-company@.service.d"
DROPIN="${DROPIN_DIR}/20-runtime-state.conf"
TMP=""
ENV_EXISTED=0
DROPIN_EXISTED=0
CONFIG_ARMED=0
SUCCESS=0
CREATED_REPORT_TARGETS=()

fail() {
  echo "DEALIX_RUNTIME_STATE_ISOLATION=FAIL_CLOSED"
  echo "$*"
  exit 1
}

rollback_config() {
  [[ "$CONFIG_ARMED" -eq 1 && "$SUCCESS" -ne 1 ]] || return 0
  echo "runtime_state_config_rollback=START"
  if [[ "$ENV_EXISTED" -eq 1 ]]; then
    install -D -m 0640 -o root -g "$RUN_USER" "$TMP/env.before" "$ENV_FILE" || true
  else
    rm -f "$ENV_FILE" || true
  fi
  if [[ "$DROPIN_EXISTED" -eq 1 ]]; then
    install -D -m 0644 -o root -g root "$TMP/dropin.before" "$DROPIN" || true
  else
    rm -f "$DROPIN" || true
  fi
  systemctl daemon-reload >/dev/null 2>&1 || true
  for target in "${CREATED_REPORT_TARGETS[@]}"; do
    rmdir "$target" >/dev/null 2>&1 || true
  done
  echo "runtime_state_config_rollback=COMPLETE"
}

cleanup() {
  local rc=$?
  set +e
  rollback_config
  [[ -n "$TMP" ]] && rm -rf "$TMP"
  set -e
  exit "$rc"
}
trap cleanup EXIT

[[ "$(id -u)" -eq 0 ]] || fail "run as root"
id "$RUN_USER" >/dev/null 2>&1 || fail "missing OS user: $RUN_USER"
[[ -d "$REPO_ROOT/.git" ]] || fail "canonical repository missing: $REPO_ROOT"
[[ -x "$REPO_ROOT/.venv/bin/python" ]] || fail "canonical repository Python missing: $REPO_ROOT/.venv/bin/python"
command -v git >/dev/null 2>&1 || fail "git missing"
command -v systemctl >/dev/null 2>&1 || fail "systemctl missing"
command -v sha256sum >/dev/null 2>&1 || fail "sha256sum missing"

# Overrides must never turn the isolation root back into repository state.
# Resolve before creating anything so an invalid override cannot partially
# write directories/drop-ins and then fail only at the later Python proof.
REPO_ROOT_REAL="$(readlink -f "$REPO_ROOT")" || fail "cannot resolve canonical repository path"
STATE_ROOT_REAL="$(readlink -m "$STATE_ROOT")" || fail "cannot resolve runtime-state path"
CONTROL_ROOT_REAL="$(readlink -m "$CONTROL_ROOT")" || fail "cannot resolve control path"
[[ "$STATE_ROOT_REAL" != "/" ]] || fail "runtime-state root must not be filesystem root"
[[ "$CONTROL_ROOT_REAL" != "/" ]] || fail "control root must not be filesystem root"
case "$STATE_ROOT_REAL" in
  "$REPO_ROOT_REAL"|"$REPO_ROOT_REAL"/*)
    fail "runtime-state root must remain outside canonical repository: $STATE_ROOT_REAL"
    ;;
esac
case "$CONTROL_ROOT_REAL" in
  "$REPO_ROOT_REAL"|"$REPO_ROOT_REAL"/*)
    fail "control root must remain outside canonical repository: $CONTROL_ROOT_REAL"
    ;;
esac
STATE_ROOT="$STATE_ROOT_REAL"
CONTROL_ROOT="$CONTROL_ROOT_REAL"
ENV_FILE="${CONTROL_ROOT}/runtime-state.env"

# Namespace adoption must be atomic. daemon-reload cannot retrofit an already
# running process, and active timers can start a legacy writer mid-install.
ACTIVE_COMPANY_SERVICES="$(
  systemctl list-units 'dealix-company@*.service' \
    --type=service --state=active,activating --no-legend --plain 2>/dev/null \
    | awk '{print $1}' | sed '/^$/d' || true
)"
ACTIVE_WRITER_TIMERS="$(
  systemctl list-units \
    'dealix-company-*.timer' 'dealix-agent-council.timer' 'dealix-vps-issue-bridge.timer' \
    --type=timer --state=active --no-legend --plain 2>/dev/null \
    | awk '{print $1}' | sed '/^$/d' || true
)"
if [[ -n "$ACTIVE_COMPANY_SERVICES" || -n "$ACTIVE_WRITER_TIMERS" ]]; then
  echo "active_company_services=${ACTIVE_COMPANY_SERVICES//$'\n'/,}"
  echo "active_writer_timers=${ACTIVE_WRITER_TIMERS//$'\n'/,}"
  fail "runtime namespace adoption pending: quiesce Dealix repo writers before installation"
fi
echo "RUNTIME_NAMESPACE_ADOPTION=PREFLIGHT_QUIESCED"

TMP="$(mktemp -d /tmp/dealix-runtime-isolation.XXXXXX)"
chmod 0700 "$TMP"

install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" \
  "$STATE_ROOT" \
  "$STATE_ROOT/commercial" \
  "$STATE_ROOT/commercial/founder_briefs" \
  "$STATE_ROOT/commercial/founder_debriefs" \
  "$STATE_ROOT/commercial/founder_weekly" \
  "$STATE_ROOT/reports" \
  "$STATE_ROOT/reports/founder_money_command" \
  "$STATE_ROOT/reports/canonical_revenue_cycle"
install -d -m 0750 "$CONTROL_ROOT"

file_sha() {
  local path="$1"
  [[ -f "$path" ]] && sha256sum "$path" | awk '{print $1}' || printf 'absent\n'
}

seed_or_preserve() {
  local relative="$1"
  local target="$2"
  local source="$REPO_ROOT/$relative"
  local source_sha target_sha dirty

  source_sha="$(file_sha "$source")"
  target_sha="$(file_sha "$target")"
  dirty="$(git -C "$REPO_ROOT" status --porcelain -- "$relative" 2>/dev/null || true)"

  if [[ -e "$target" ]]; then
    if [[ -n "$dirty" && -f "$source" && "$source_sha" != "$target_sha" ]]; then
      echo "runtime_seed=$relative status=CONFLICT source_sha=$source_sha target_sha=$target_sha"
      fail "dirty canonical/runtime conflict requires recovery reconciliation before isolation: $relative"
    fi
    echo "runtime_seed=$relative status=PRESERVED_EXISTING source_sha=$source_sha target_sha=$target_sha"
    return 0
  fi
  if [[ ! -f "$source" ]]; then
    echo "runtime_seed=$relative status=SOURCE_ABSENT_SKIP source_sha=absent target_sha=absent"
    return 0
  fi
  install -D -m 0640 -o "$RUN_USER" -g "$RUN_USER" "$source" "$target"
  target_sha="$(file_sha "$target")"
  echo "runtime_seed=$relative status=SEEDED_FROM_CURRENT_SOURCE source_sha=$source_sha target_sha=$target_sha"
}

# Preserve an already-authoritative runtime copy. If the canonical worktree is
# dirty and differs, fail closed so the full recovery can reconcile it first.
seed_or_preserve \
  "docs/commercial/operations/evidence_events_tracker.csv" \
  "$STATE_ROOT/commercial/evidence_events_tracker.csv"
seed_or_preserve \
  "dealix/config/social_content_queue.yaml" \
  "$STATE_ROOT/commercial/social_content_queue.yaml"
seed_or_preserve \
  "docs/commercial/operations/soft_launch_meetings_tracker.yaml" \
  "$STATE_ROOT/commercial/soft_launch_meetings_tracker.yaml"
seed_or_preserve \
  "data/war_room_today.json" \
  "$STATE_ROOT/commercial/war_room_today.json"
seed_or_preserve \
  "data/dealix_dogfooding_war_room.json" \
  "$STATE_ROOT/commercial/dealix_dogfooding_war_room.json"
seed_or_preserve \
  "data/founder_agent_queue_today.json" \
  "$STATE_ROOT/commercial/founder_agent_queue_today.json"

# Generated report roots are absent from Git main. Create only these exact mount
# targets; never shadow the tracked top-level reports/ tree. Remember which ones
# were created so a failed config transaction can remove them if still empty.
for target in \
  "$REPO_ROOT/reports/founder_money_command" \
  "$REPO_ROOT/reports/canonical_revenue_cycle"
do
  if [[ ! -d "$target" ]]; then
    install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$target"
    CREATED_REPORT_TARGETS+=("$target")
  fi
done

ENV_STAGE="$TMP/runtime-state.env"
DROPIN_STAGE="$TMP/20-runtime-state.conf"
cat >"$ENV_STAGE" <<EOF
DEALIX_RUNTIME_STATE_ROOT=$STATE_ROOT
DEALIX_MONEY_REPORT_ROOT=$STATE_ROOT/reports/founder_money_command
DEALIX_REVENUE_CYCLE_OUT=$STATE_ROOT/reports/canonical_revenue_cycle
EOF
chmod 0600 "$ENV_STAGE"

cat >"$DROPIN_STAGE" <<EOF
[Service]
EnvironmentFile=-$ENV_FILE
ReadWritePaths=$STATE_ROOT
EOF

append_bind() {
  local source="$1"
  local target="$2"
  if [[ -e "$source" && -e "$target" ]]; then
    printf 'BindPaths=%s:%s\n' "$source" "$target" >>"$DROPIN_STAGE"
    echo "bind_isolation=$(basename "$target") status=ENABLED"
  else
    echo "bind_isolation=$(basename "$target") status=SKIPPED_MISSING_ENDPOINT"
  fi
}

# Private mount namespace compatibility layer: isolate legacy current-main code
# until every consumer uses the env-aware paths directly.
append_bind \
  "$STATE_ROOT/commercial/evidence_events_tracker.csv" \
  "$REPO_ROOT/docs/commercial/operations/evidence_events_tracker.csv"
append_bind \
  "$STATE_ROOT/commercial/social_content_queue.yaml" \
  "$REPO_ROOT/dealix/config/social_content_queue.yaml"
append_bind \
  "$STATE_ROOT/commercial/soft_launch_meetings_tracker.yaml" \
  "$REPO_ROOT/docs/commercial/operations/soft_launch_meetings_tracker.yaml"
append_bind \
  "$STATE_ROOT/commercial/war_room_today.json" \
  "$REPO_ROOT/data/war_room_today.json"
append_bind \
  "$STATE_ROOT/commercial/dealix_dogfooding_war_room.json" \
  "$REPO_ROOT/data/dealix_dogfooding_war_room.json"
append_bind \
  "$STATE_ROOT/commercial/founder_agent_queue_today.json" \
  "$REPO_ROOT/data/founder_agent_queue_today.json"
append_bind "$STATE_ROOT/commercial/founder_briefs" "$REPO_ROOT/data/founder_briefs"
append_bind "$STATE_ROOT/commercial/founder_debriefs" "$REPO_ROOT/data/founder_debriefs"
append_bind "$STATE_ROOT/commercial/founder_weekly" "$REPO_ROOT/data/founder_weekly"
append_bind \
  "$STATE_ROOT/reports/founder_money_command" \
  "$REPO_ROOT/reports/founder_money_command"
append_bind \
  "$STATE_ROOT/reports/canonical_revenue_cycle" \
  "$REPO_ROOT/reports/canonical_revenue_cycle"
chmod 0600 "$DROPIN_STAGE"

BIND_COUNT="$(grep -c '^BindPaths=' "$DROPIN_STAGE" || true)"
[[ "$BIND_COUNT" -ge 4 ]] || fail "too few runtime bind-isolation paths in staged config: $BIND_COUNT"
grep -Fxq "DEALIX_RUNTIME_STATE_ROOT=$STATE_ROOT" "$ENV_STAGE" \
  || fail "staged runtime-state env verification failed"
grep -Fxq "ReadWritePaths=$STATE_ROOT" "$DROPIN_STAGE" \
  || fail "staged systemd drop-in verification failed"

# Back up prior armed configuration before atomic replacement. The EXIT trap
# restores it and reloads systemd if any post-install verification fails.
if [[ -f "$ENV_FILE" ]]; then
  cp -a "$ENV_FILE" "$TMP/env.before"
  ENV_EXISTED=1
fi
if [[ -f "$DROPIN" ]]; then
  cp -a "$DROPIN" "$TMP/dropin.before"
  DROPIN_EXISTED=1
fi
CONFIG_ARMED=1
install -D -m 0640 -o root -g "$RUN_USER" "$ENV_STAGE" "$ENV_FILE"
install -D -m 0644 -o root -g root "$DROPIN_STAGE" "$DROPIN"
systemctl daemon-reload

if command -v systemd-analyze >/dev/null 2>&1; then
  systemd-analyze verify /etc/systemd/system/dealix-company@.service >/dev/null \
    || fail "systemd unit verification failed after runtime-state drop-in"
fi

# The patch-aware code must resolve *all* exported mutable targets outside Git.
if grep -q 'DEALIX_RUNTIME_STATE_ROOT' "$REPO_ROOT/dealix/commercial_ops/paths.py" 2>/dev/null; then
  sudo -u "$RUN_USER" -H env \
    DEALIX_RUNTIME_STATE_ROOT="$STATE_ROOT" \
    DEALIX_REPO_ROOT="$REPO_ROOT" \
    PYTHONPATH="$REPO_ROOT" \
    "$REPO_ROOT/.venv/bin/python" - <<'PY'
import os
from dealix.commercial_ops import paths
root = paths.REPO_ROOT.resolve()
mutable = (
    paths.EVIDENCE_TRACKER_CSV,
    paths.SOCIAL_QUEUE_YAML,
    paths.WAR_ROOM_TODAY_JSON,
    paths.SOFT_LAUNCH_TRACKER_YAML,
    paths.FOUNDER_BRIEFS_DIR,
    paths.FOUNDER_DEBRIEFS_DIR,
    paths.FOUNDER_WEEKLY_DECISION_DIR,
    paths.DEALIX_DOGFOODING_WAR_ROOM_JSON,
    paths.FOUNDER_AGENT_QUEUE_TODAY_JSON,
)
for path in mutable:
    resolved = path.resolve(strict=False)
    if resolved == root or root in resolved.parents:
        raise SystemExit(f"runtime path still inside canonical repo: {resolved}")
print("RUNTIME_PATH_REDIRECTION=PASS")
PY
else
  echo "RUNTIME_PATH_REDIRECTION=COMPAT_BIND_UNTIL_PATCH_MERGED"
fi

# No old namespace may still be running when we declare the config armed.
POST_ACTIVE="$(
  systemctl list-units 'dealix-company@*.service' \
    --type=service --state=active,activating --no-legend --plain 2>/dev/null \
    | awk '{print $1}' | sed '/^$/d' || true
)"
[[ -z "$POST_ACTIVE" ]] || fail "company service became active before namespace acceptance: $POST_ACTIVE"

SUCCESS=1
CONFIG_ARMED=0
echo "runtime_state_root=$STATE_ROOT"
echo "runtime_env_file=$ENV_FILE"
echo "systemd_dropin=$DROPIN"
echo "bind_paths=$BIND_COUNT"
echo "tracked_reports_tree_shadowed=false"
echo "RUNTIME_NAMESPACE_ADOPTION=READY_FOR_NEXT_INVOCATION"
echo "external_send=DISABLED_UNCHANGED"
echo "payment=DISABLED_UNCHANGED"
echo "merge_to_main=DISABLED_UNCHANGED"
echo "production_mutation=DISABLED_UNCHANGED"
echo "DEALIX_RUNTIME_STATE_ISOLATION=PASS"
