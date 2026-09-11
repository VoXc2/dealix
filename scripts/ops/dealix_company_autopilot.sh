#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Release-truth guard for the canonical Company Autopilot.
# All modes except production/status are delegated byte-for-byte to the
# previously canonical implementation. Production may be GREEN only when
# liveness AND immutable Web/API release identity match current origin/main.

MODE="${1:-status}"
ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
AUTOPILOT_ROOT="${DEALIX_AUTOPILOT_ROOT:-/opt/dealix/company-autopilot}"
STATE_DIR="${AUTOPILOT_ROOT}/state"
PYTHON="${DEALIX_PYTHON:-python3}"
ISSUE_REPO="${DEALIX_ISSUE_REPO:-Dealix-sa/dealix}"
ISSUE_NUMBER="${DEALIX_ISSUE_NUMBER:-1604}"
API_BASE="${DEALIX_PUBLIC_API_BASE:-https://api.dealix.me}"
WEB_BASE="${DEALIX_PUBLIC_WEB_BASE:-https://dealix.me}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LEGACY="${SCRIPT_DIR}/dealix_company_autopilot_legacy.sh"
if [[ ! -x "$LEGACY" ]]; then
  LEGACY="${ROOT}/scripts/ops/dealix_company_autopilot_legacy.sh"
fi

if [[ "$MODE" != "production" && "$MODE" != "status" ]]; then
  if [[ ! -x "$LEGACY" ]]; then
    echo "BLOCKED: canonical legacy autopilot implementation is unavailable"
    exit 2
  fi
  exec "$LEGACY" "$@"
fi

mkdir -p "$STATE_DIR"
chmod 0750 "$AUTOPILOT_ROOT" "$STATE_DIR" 2>/dev/null || true

http_code() {
  local url="$1" code
  code="$(curl -L -sS -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 15 "$url" 2>/dev/null || true)"
  printf '%s\n' "${code:-000}"
}

is_http_ok() {
  [[ "${1:-000}" =~ ^[23][0-9][0-9]$ ]]
}

fetch_json() {
  local url="$1"
  curl -L -fsS --connect-timeout 5 --max-time 15 "$url" 2>/dev/null || true
}

extract_git_sha() {
  "$PYTHON" -c '
import json, re, sys
try:
    value = json.load(sys.stdin)
except Exception:
    raise SystemExit(0)

def find(obj):
    if isinstance(obj, dict):
        candidate = obj.get("git_sha")
        if isinstance(candidate, str) and re.fullmatch(r"[0-9a-fA-F]{40}", candidate):
            return candidate.lower()
        for child in obj.values():
            found = find(child)
            if found:
                return found
    elif isinstance(obj, list):
        for child in obj:
            found = find(child)
            if found:
                return found
    return ""

print(find(value))
' 2>/dev/null || true
}

valid_sha() {
  [[ "${1:-}" =~ ^[0-9a-f]{40}$ ]]
}

write_state() {
  local state="$1" file="${STATE_DIR}/production.state" tmp
  tmp="${file}.tmp.$$"
  printf '%s\n' "$state" >"$tmp"
  chmod 0640 "$tmp" 2>/dev/null || true
  mv -f "$tmp" "$file"
}

notify_transition() {
  local previous="$1" state="$2" reason="$3" expected="$4" api_sha="$5" web_sha="$6"
  [[ "$previous" != "$state" ]] || return 0
  [[ "${DEALIX_DISABLE_TRANSITION_NOTIFY:-0}" != "1" ]] || return 0
  command -v gh >/dev/null 2>&1 || return 0
  gh auth status >/dev/null 2>&1 || return 0
  local body
  body="DEALIX_AUTOPILOT_TRANSITION

- check: production
- from: ${previous}
- to: ${state}
- time: $(date -Is)
- expected_main_sha: ${expected:-UNKNOWN_NOT_EVIDENCE_BACKED}
- api_release_sha: ${api_sha:-UNKNOWN_NOT_EVIDENCE_BACKED}
- web_release_sha: ${web_sha:-UNKNOWN_NOT_EVIDENCE_BACKED}
- reason: ${reason}

No production mutation was attempted."
  gh api --method POST "repos/${ISSUE_REPO}/issues/${ISSUE_NUMBER}/comments" -f "body=${body}" >/dev/null 2>&1 || true
}

production_truth() {
  exec 9>"${STATE_DIR}/production-truth.lock"
  if command -v flock >/dev/null 2>&1 && ! flock -n 9; then
    echo "PRODUCTION_TRUTH=SKIP_ALREADY_RUNNING"
    return 0
  fi

  local previous="unknown" state="HOLD" reason="unknown"
  local state_file="${STATE_DIR}/production.state"
  [[ -f "$state_file" ]] && previous="$(cat "$state_file" 2>/dev/null || echo unknown)"

  local api_http web_http
  api_http="$(http_code "${API_BASE%/}/healthz")"
  web_http="$(http_code "${WEB_BASE%/}/")"

  local failure_file="${STATE_DIR}/production_failures" failures=0
  if [[ -f "$failure_file" ]]; then
    failures="$(cat "$failure_file" 2>/dev/null || echo 0)"
  fi
  [[ "$failures" =~ ^[0-9]+$ ]] || failures=0

  local source_ok=0 branch="" local_head="" expected=""
  if git -C "$ROOT" fetch origin main --quiet >/dev/null 2>&1; then
    branch="$(git -C "$ROOT" branch --show-current 2>/dev/null || true)"
    local_head="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || true)"
    expected="$(git -C "$ROOT" rev-parse origin/main 2>/dev/null || true)"
    expected="${expected,,}"
    local_head="${local_head,,}"
    if [[ "$branch" == "main" ]] && valid_sha "$local_head" && valid_sha "$expected" && [[ "$local_head" == "$expected" ]]; then
      source_ok=1
    fi
  fi

  local api_sha="" web_sha=""
  api_sha="$(fetch_json "${API_BASE%/}/version" | extract_git_sha)"
  web_sha="$(fetch_json "${WEB_BASE%/}/healthz" | extract_git_sha)"
  api_sha="${api_sha,,}"
  web_sha="${web_sha,,}"

  if ! is_http_ok "$api_http" || ! is_http_ok "$web_http"; then
    failures=$((failures + 1))
    printf '%s\n' "$failures" >"$failure_file"
    if (( failures >= 3 )); then
      state="RED"
      reason="public_liveness_failed_three_consecutive_probes"
    else
      state="HOLD"
      reason="public_liveness_failed_pending_hysteresis"
    fi
  else
    printf '0\n' >"$failure_file"
    if (( source_ok != 1 )); then
      state="HOLD"
      reason="canonical_source_not_exact_current_main"
    elif ! valid_sha "$api_sha" || ! valid_sha "$web_sha"; then
      state="HOLD"
      reason="immutable_release_identity_missing"
    elif [[ "$api_sha" != "$expected" || "$web_sha" != "$expected" ]]; then
      state="HOLD"
      reason="running_release_not_equal_current_main"
    else
      state="GREEN"
      reason="liveness_and_exact_web_api_release_identity_match_current_main"
    fi
  fi

  write_state "$state"
  notify_transition "$previous" "$state" "$reason" "$expected" "$api_sha" "$web_sha"

  echo "===== PRODUCTION RELEASE TRUTH ====="
  echo "api_healthz_http=${api_http}"
  echo "web_root_http=${web_http}"
  echo "canonical_branch=${branch:-UNKNOWN_NOT_EVIDENCE_BACKED}"
  echo "canonical_local_sha=${local_head:-UNKNOWN_NOT_EVIDENCE_BACKED}"
  echo "expected_main_sha=${expected:-UNKNOWN_NOT_EVIDENCE_BACKED}"
  echo "api_release_sha=${api_sha:-UNKNOWN_NOT_EVIDENCE_BACKED}"
  echo "web_release_sha=${web_sha:-UNKNOWN_NOT_EVIDENCE_BACKED}"
  echo "production_state=${state}"
  echo "production_reason=${reason}"
  if [[ "$state" == "GREEN" ]]; then
    echo "PRODUCTION_GREEN=true"
  else
    echo "PRODUCTION_GREEN=false"
  fi
}

production_truth

if [[ "$MODE" == "status" ]]; then
  if [[ ! -x "$LEGACY" ]]; then
    echo "BLOCKED: canonical legacy autopilot implementation is unavailable"
    exit 2
  fi
  exec "$LEGACY" status
fi