#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
PROOF_ROOT="${DEALIX_OPENSHIP_PROOF_ROOT:-/opt/dealix/executive-proof/openship}"
PILOT_ROOT="${DEALIX_OPENSHIP_PILOT_ROOT:-/opt/dealix/openship-pilot}"
OPENSHIP_VERSION="0.4.8"
MIN_AVAILABLE_MB="${DEALIX_OPENSHIP_MIN_AVAILABLE_MB:-6144}"
READY_TIMEOUT="${DEALIX_OPENSHIP_READY_TIMEOUT:-60}"
STOP_TIMEOUT="${DEALIX_OPENSHIP_STOP_TIMEOUT:-30}"
MODE="${1:-status}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF_DIR="${PROOF_ROOT}/${MODE}-${STAMP}"
LOCK="/run/lock/dealix-openship-private-pilot.lock"
SYNTH_STAGE=""

section() {
  printf '\n================================================================\n %s\n================================================================\n' "$*"
}

fail() {
  echo "BLOCKED: $*" >&2
  exit 1
}

redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#(opsh_pat_[A-Za-z0-9_-]+)#[REDACTED_OPENSHIP_TOKEN]#g' \
    -e 's#(ghp_[A-Za-z0-9]+)#[REDACTED_GITHUB_TOKEN]#g' \
    -e 's#(github_pat_[A-Za-z0-9_]+)#[REDACTED_GITHUB_TOKEN]#g' \
    -e 's#(sk-[A-Za-z0-9_-]+)#[REDACTED_API_KEY]#g' \
    -e 's#((TOKEN|SECRET|PASSWORD|API_KEY)[=: ][^ ]+)#\2=[REDACTED]#Ig'
}

as_dealix() {
  sudo -u "$RUN_USER" -H "$@"
}

cleanup_temp() {
  if [[ -n "${SYNTH_STAGE:-}" && -d "$SYNTH_STAGE" ]]; then
    rm -rf -- "$SYNTH_STAGE"
  fi
}
trap cleanup_temp EXIT

find_openship() {
  local p
  for p in \
    "/home/${RUN_USER}/.local/bin/openship" \
    "/home/${RUN_USER}/.bun/bin/openship" \
    "/home/${RUN_USER}/.openship/bin/openship" \
    "/usr/local/bin/openship" \
    "/usr/bin/openship"
  do
    if [[ -x "$p" ]]; then
      printf '%s\n' "$p"
      return 0
    fi
  done
  return 1
}

available_mb() {
  awk '/MemAvailable:/ {printf "%d\n", $2/1024}' /proc/meminfo
}

capture_ports() {
  ss -ltnp 2>/dev/null \
    | grep -E ':(22|80|443|3001|4000|5678|11434|18789)[[:space:]]' \
    || true
}

control_listener_lines() {
  ss -H -ltnp 2>/dev/null \
    | awk '$4 ~ /:3001$/ || $4 ~ /:4000$/ {print}'
}

control_port_occupied() {
  control_listener_lines | grep -q .
}

non_loopback_control_listener_present() {
  local addr
  while IFS= read -r addr; do
    [[ -z "$addr" ]] && continue
    case "$addr" in
      127.0.0.1:3001|127.0.0.1:4000|\[::1\]:3001|\[::1\]:4000)
        ;;
      *)
        echo "unsafe_control_listener=$addr"
        return 0
        ;;
    esac
  done < <(control_listener_lines | awk '{print $4}')
  return 1
}

loopback_port_present() {
  local port="$1"
  control_listener_lines \
    | awk '{print $4}' \
    | grep -Eq "^(127\\.0\\.0\\.1|\\[::1\\]):${port}$"
}

control_listener_owner_is_dealix() {
  local line pid owner seen=0
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    seen=1
    pid="$(sed -nE 's/.*pid=([0-9]+).*/\1/p' <<<"$line" | head -1)"
    if [[ -z "$pid" ]]; then
      echo "listener_owner=UNKNOWN line=$(redact <<<"$line")"
      return 1
    fi
    owner="$(ps -o user= -p "$pid" 2>/dev/null | xargs || true)"
    if [[ "$owner" != "$RUN_USER" ]]; then
      echo "listener_owner=FAIL pid=$pid owner=${owner:-UNKNOWN}"
      return 1
    fi
  done < <(control_listener_lines)
  [[ "$seen" -eq 1 ]] || return 1
  echo "listener_owner=PASS user=$RUN_USER"
}

validate_status_json() {
  local path="$1"
  /usr/bin/python3 - "$path" <<'PY'
import json
import sys
from urllib.parse import urlparse

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)

if data.get("reachable") is not True:
    raise SystemExit("reachable is not true")
service = data.get("service") or {}
if service.get("running") is not True:
    raise SystemExit("service.running is not true")
ports = data.get("ports") or {}
if int(ports.get("api") or 0) != 4000:
    raise SystemExit("API port is not 4000")
if int(ports.get("dashboard") or 0) != 3001:
    raise SystemExit("dashboard port is not 3001")
health = data.get("health") or {}
status = str(health.get("status") or "").lower()
if status not in {"ok", "healthy"}:
    raise SystemExit(f"unexpected health status: {status!r}")
api_url = str(data.get("apiUrl") or "")
parsed = urlparse(api_url)
if parsed.hostname not in {"127.0.0.1", "localhost", "::1"} or parsed.port != 4000:
    raise SystemExit(f"active API context is not local loopback: {api_url!r}")
PY
}

verify_direct_health() {
  local body code rc
  body="$PROOF_DIR/api-health.json"
  set +e
  code="$(curl -sS -o "$body" -w '%{http_code}' --max-time 5 \
    http://127.0.0.1:4000/api/health)"
  rc=$?
  set -e
  [[ "$rc" -eq 0 && "$code" == "200" ]] || return 1
  /usr/bin/python3 - "$body" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
status = str(data.get("status") or "").lower()
if status not in {"ok", "healthy"}:
    raise SystemExit(1)
PY
}

ensure_root_and_paths() {
  [[ "$(id -u)" -eq 0 ]] || fail "run as root"
  id "$RUN_USER" >/dev/null 2>&1 || fail "missing OS user: $RUN_USER"
  [[ -d "$REPO/.git" ]] || fail "canonical Dealix repository missing: $REPO"
  for cmd in sudo curl ss flock python3 ps sha256sum; do
    command -v "$cmd" >/dev/null 2>&1 || fail "$cmd missing"
  done
  [[ "$READY_TIMEOUT" =~ ^[0-9]+$ ]] && (( READY_TIMEOUT >= 10 && READY_TIMEOUT <= 180 )) \
    || fail "DEALIX_OPENSHIP_READY_TIMEOUT must be 10..180"
  [[ "$STOP_TIMEOUT" =~ ^[0-9]+$ ]] && (( STOP_TIMEOUT >= 5 && STOP_TIMEOUT <= 120 )) \
    || fail "DEALIX_OPENSHIP_STOP_TIMEOUT must be 5..120"
  install -d -m 0750 -o root -g "$RUN_USER" "$PROOF_ROOT" "$PILOT_ROOT"
  install -d -m 0700 "$PROOF_DIR"
  exec 9>"$LOCK"
  flock -n 9 || fail "another OpenShip pilot operation is running"
}

record_baseline() {
  section "BASELINE"
  echo "time=$(date -Is)"
  echo "mode=$MODE"
  echo "host=$(hostname)"
  echo "repo_head=$(as_dealix git -C "$REPO" rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
  echo "repo_branch=$(as_dealix git -C "$REPO" branch --show-current 2>/dev/null || echo UNKNOWN)"
  echo "available_mb=$(available_mb)"
  free -h || true
  swapon --show || true
  df -h / || true
  echo
  capture_ports
}

preflight() {
  section "PREFLIGHT"
  local avail
  avail="$(available_mb)"
  if (( avail < MIN_AVAILABLE_MB )); then
    echo "available_mb=$avail"
    echo "required_mb=$MIN_AVAILABLE_MB"
    fail "insufficient memory headroom; unload local AI before starting OpenShip"
  fi

  if control_port_occupied; then
    fail "reserved OpenShip control port 3001 or 4000 is occupied; refuse dynamic-port fallback"
  fi

  if ss -ltnH 2>/dev/null | awk '{print $4}' | grep -Eq ':(80|443)$'; then
    echo "ports_80_443=OCCUPIED"
    echo "This pilot does not take ownership of 80/443."
  else
    echo "ports_80_443=FREE"
  fi

  echo "resource_guard=PASS"
  echo "network_guard=PASS"
  echo "production_mutation=DISABLED"
  echo "dns_mutation=DISABLED"
  echo "public_domain=DISABLED"
  echo "production_secrets_copy=DISABLED"
}

verify_cli() {
  section "VERIFY PINNED OPENSHIP CLI"
  local openship version_out
  openship="$(find_openship || true)"
  [[ -n "$openship" ]] || fail \
    "OpenShip CLI is not installed. Governed pilot refuses mutable network installers; install reviewed openship@${OPENSHIP_VERSION} first."

  version_out="$(as_dealix "$openship" --version 2>&1 | redact)"
  echo "$version_out"
  grep -Eq "(^|[^0-9])${OPENSHIP_VERSION//./\\.}([^0-9]|$)" <<<"$version_out" \
    || fail "OpenShip CLI version is not pinned ${OPENSHIP_VERSION}"
  echo "openship_bin=$openship"
  echo "openship_version=${OPENSHIP_VERSION}"
  echo "openship_provenance=PINNED_PREINSTALLED"
  echo "openship_cli=PASS"
}

verified_stop() {
  local openship rc deadline
  openship="$(find_openship || true)"
  [[ -n "$openship" ]] || {
    control_port_occupied && return 1
    echo "OPENSHIP_STOP=ALREADY_ABSENT"
    return 0
  }

  set +e
  as_dealix "$openship" stop >"$PROOF_DIR/openship-stop.log" 2>&1
  rc=$?
  set -e
  redact <"$PROOF_DIR/openship-stop.log" || true

  deadline=$((SECONDS + STOP_TIMEOUT))
  while (( SECONDS < deadline )); do
    if ! control_port_occupied; then
      if (( rc != 0 )); then
        echo "OPENSHIP_STOP=COMMAND_FAILED rc=$rc"
        return 1
      fi
      echo "OPENSHIP_STOP=COMPLETE"
      return 0
    fi
    sleep 1
  done

  echo "OPENSHIP_STOP=LISTENERS_REMAIN"
  capture_ports
  return 1
}

fail_closed_stop() {
  local reason="$1"
  echo "FAIL_CLOSED_REASON=$reason"
  if verified_stop; then
    echo "FAIL_CLOSED_ROLLBACK=PASS"
  else
    echo "FAIL_CLOSED_ROLLBACK=FAIL"
  fi
  fail "$reason"
}

wait_for_ready() {
  local openship deadline status_json status_err
  openship="$(find_openship)"
  status_json="$PROOF_DIR/openship-status.json"
  status_err="$PROOF_DIR/openship-status.err"
  deadline=$((SECONDS + READY_TIMEOUT))

  while (( SECONDS < deadline )); do
    if as_dealix "$openship" status --json >"$status_json" 2>"$status_err" \
      && validate_status_json "$status_json" \
      && verify_direct_health \
      && ! non_loopback_control_listener_present \
      && loopback_port_present 3001 \
      && loopback_port_present 4000 \
      && control_listener_owner_is_dealix; then
      echo "openship_readiness=PASS"
      return 0
    fi
    sleep 2
  done

  echo "openship_readiness=TIMEOUT seconds=$READY_TIMEOUT"
  redact <"$status_err" 2>/dev/null || true
  return 1
}

start_private() {
  section "START PRIVATE BARE CONTROL PLANE"
  preflight
  verify_cli

  local openship rc
  openship="$(find_openship)"
  set +e
  timeout 180 sudo -u "$RUN_USER" -H "$openship" up --bare \
    >"$PROOF_DIR/openship-up.log" 2>&1
  rc=$?
  set -e
  echo "openship_up_rc=$rc"

  # A timeout may be a benign foreground/service-manager behavior, but it is
  # never accepted by listener presence alone. Only rc=0/124 may proceed and
  # both must pass strict CLI/API health plus loopback ownership readiness.
  if (( rc != 0 && rc != 124 )); then
    redact <"$PROOF_DIR/openship-up.log" || true
    fail_closed_stop "openship up --bare failed rc=$rc"
  fi

  if ! wait_for_ready; then
    fail_closed_stop "OpenShip did not reach healthy deterministic private readiness"
  fi

  capture_ports | tee "$PROOF_DIR/ports-after-start.txt"
  echo "OPENSHIP_MODE=BARE"
  echo "OPENSHIP_DASHBOARD=http://127.0.0.1:3001"
  echo "OPENSHIP_API=http://127.0.0.1:4000"
  echo "OPENSHIP_NETWORK=LOOPBACK_ONLY"
  echo "OPENSHIP_PRIVATE_PILOT=PASS"
}

status_private() {
  section "OPENSHIP STATUS"
  local openship
  openship="$(find_openship || true)"
  if [[ -z "$openship" ]]; then
    echo "OPENSHIP=NOT_INSTALLED"
    return 0
  fi
  verify_cli
  if as_dealix "$openship" status --json >"$PROOF_DIR/openship-status.json" \
       2>"$PROOF_DIR/openship-status.err" \
     && validate_status_json "$PROOF_DIR/openship-status.json" \
     && verify_direct_health \
     && ! non_loopback_control_listener_present \
     && loopback_port_present 3001 \
     && loopback_port_present 4000 \
     && control_listener_owner_is_dealix; then
    echo "OPENSHIP_NETWORK=LOOPBACK_ONLY"
    echo "OPENSHIP_STATUS=HEALTHY"
    return 0
  fi
  redact <"$PROOF_DIR/openship-status.err" 2>/dev/null || true
  capture_ports
  echo "OPENSHIP_STATUS=UNHEALTHY_OR_NONPRIVATE"
  return 2
}

stop_private() {
  section "STOP OPENSHIP"
  verified_stop || fail "OpenShip stop did not complete cleanly"
}

mcp_auth_guard() {
  section "MCP ANONYMOUS ACCESS GUARD"
  local code rc
  set +e
  code="$(curl -sS -o "$PROOF_DIR/mcp-anonymous-body.txt" -w '%{http_code}' \
    --max-time 10 \
    -X POST http://127.0.0.1:4000/api/mcp \
    -H 'Content-Type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"dealix-guard","version":"1"}}}')"
  rc=$?
  set -e

  echo "mcp_transport_rc=$rc"
  echo "mcp_anonymous_http=${code:-000}"
  if (( rc != 0 )); then
    fail_closed_stop "anonymous MCP guard had a transport error rc=$rc"
  fi

  case "$code" in
    401|403)
      echo "MCP_ANONYMOUS_ACCESS=EXPLICITLY_DENIED"
      ;;
    *)
      fail_closed_stop "anonymous MCP must return explicit 401/403; received ${code:-000}"
      ;;
  esac
}

scaffold_synthetic() {
  section "SYNTHETIC APP SCAFFOLD"
  local app_dir="$PILOT_ROOT/synthetic-app-$STAMP"
  [[ ! -e "$app_dir" && ! -L "$app_dir" ]] || fail "synthetic destination already exists"

  SYNTH_STAGE="$(mktemp -d "$PILOT_ROOT/.synthetic-stage-${STAMP}.XXXXXX")"
  [[ -d "$SYNTH_STAGE" && ! -L "$SYNTH_STAGE" ]] || fail "unsafe synthetic staging directory"
  [[ "$(stat -c '%u' "$SYNTH_STAGE")" -eq 0 ]] || fail "synthetic staging directory must be root-owned"

  cat >"$SYNTH_STAGE/package.json" <<'JSON'
{
  "name": "dealix-openship-synthetic",
  "private": true,
  "version": "0.0.1",
  "scripts": {
    "start": "node server.mjs"
  }
}
JSON
  cat >"$SYNTH_STAGE/server.mjs" <<'JS'
import http from "node:http";
const port = Number(process.env.PORT || 8080);
const server = http.createServer((req, res) => {
  if (req.url === "/healthz") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true, service: "dealix-openship-synthetic" }));
    return;
  }
  res.writeHead(200, { "content-type": "text/plain" });
  res.end("Dealix OpenShip synthetic staging probe\n");
});
server.listen(port, "127.0.0.1");
JS
  cat >"$SYNTH_STAGE/README.md" <<'MD'
# Dealix OpenShip Synthetic Staging Probe

Disposable local-only fixture for Issue #1171. It contains no customer data, secrets, production URLs, or production database settings.

The pilot intentionally stops before OpenShip project initialization or deployment until the private OpenShip admin/context is initialized and a staging-only deployment packet is approved by policy.
MD

  chmod 0640 "$SYNTH_STAGE/package.json" "$SYNTH_STAGE/server.mjs" "$SYNTH_STAGE/README.md"
  mv -- "$SYNTH_STAGE" "$app_dir"
  SYNTH_STAGE=""
  chown -R "$RUN_USER:$RUN_USER" "$app_dir"
  echo "synthetic_app=$app_dir"
  echo "SYNTHETIC_SCAFFOLD=PASS"
}

proof_manifest() {
  section "PROOF MANIFEST"
  record_baseline >"$PROOF_DIR/baseline.txt" 2>&1 || true
  find "$PROOF_DIR" -maxdepth 1 -type f \
    ! -name 'SHA256SUMS' ! -name 'run.log' -print0 \
    | sort -z \
    | xargs -0 -r sha256sum >"$PROOF_DIR/SHA256SUMS"
  cat "$PROOF_DIR/SHA256SUMS" || true
  echo "proof=$PROOF_DIR"
}

ensure_root_and_paths
exec > >(tee -a "$PROOF_DIR/run.log") 2>&1

case "$MODE" in
  preflight)
    record_baseline
    preflight
    verify_cli
    ;;
  install)
    record_baseline
    preflight
    verify_cli
    echo "OPENSHIP_INSTALL=EXTERNAL_PINNED_PREREQUISITE_VERIFIED"
    ;;
  start)
    record_baseline
    start_private
    ;;
  status)
    record_baseline
    status_private
    ;;
  stop)
    record_baseline
    stop_private
    ;;
  mcp-guard)
    record_baseline
    mcp_auth_guard
    ;;
  synthetic-scaffold)
    record_baseline
    scaffold_synthetic
    ;;
  full-private-pilot)
    record_baseline
    preflight
    verify_cli
    start_private
    mcp_auth_guard
    scaffold_synthetic
    ;;
  *)
    echo "usage: $0 {preflight|install|start|status|stop|mcp-guard|synthetic-scaffold|full-private-pilot}" >&2
    exit 64
    ;;
esac

proof_manifest

echo
if [[ "$MODE" == "full-private-pilot" ]]; then
  echo "DEALIX_OPENSHIP_PRIVATE_PILOT=PASS"
fi
echo "PRODUCTION_MUTATION=false"
echo "PUBLIC_DOMAIN=false"
echo "DNS_MUTATION=false"
echo "PRODUCTION_SECRET_COPY=false"
echo "EXTERNAL_SEND=false"
echo "PAYMENT=false"
