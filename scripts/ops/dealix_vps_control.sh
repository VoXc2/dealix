#!/usr/bin/env bash
set -Eeuo pipefail

# Safe allowlisted control surface for the Dealix Command & AI Node.
# Intentionally excludes arbitrary shell, external sends, merges, production mutation,
# payments, secret changes, and destructive actions.

ROOT="/opt/dealix/workspace/dealix"
AUTOPILOT="/opt/dealix/control/bin/dealix_company_autopilot.sh"
PY_BOOTSTRAP="$ROOT/scripts/ops/ensure_founder_automation_python.sh"
PY="$ROOT/.venv/bin/python"
RUNTIME_ENV="/opt/dealix/control/runtime-state.env"
RUNTIME_STATE_READY=0
COMMAND="${1:-status}"

if [[ ! -d "$ROOT/.git" ]]; then
  echo "BLOCKED: canonical Dealix repo not found at $ROOT"
  exit 2
fi

load_runtime_state_env() {
  RUNTIME_STATE_READY=0
  [[ -e "$RUNTIME_ENV" ]] || return 0
  [[ -f "$RUNTIME_ENV" && ! -L "$RUNTIME_ENV" ]] || {
    echo "BLOCKED: runtime-state env must be a regular non-symlink file"
    return 1
  }
  [[ "$(stat -c '%u' "$RUNTIME_ENV")" == "0" ]] || {
    echo "BLOCKED: runtime-state env must be owned by root"
    return 1
  }
  local mode
  mode="$(stat -c '%a' "$RUNTIME_ENV")"
  (( (8#$mode & 022) == 0 )) || {
    echo "BLOCKED: runtime-state env must not be group/world writable"
    return 1
  }

  local key value resolved root_real
  local seen_state=0 seen_money=0 seen_revenue=0
  root_real="$(readlink -f "$ROOT")" || {
    echo "BLOCKED: cannot resolve canonical repository"
    return 1
  }
  while IFS='=' read -r key value || [[ -n "${key:-}${value:-}" ]]; do
    [[ -z "${key:-}" ]] && continue
    [[ "$key" == \#* ]] && continue
    case "$key" in
      DEALIX_RUNTIME_STATE_ROOT|DEALIX_MONEY_REPORT_ROOT|DEALIX_REVENUE_CYCLE_OUT)
        [[ -n "$value" ]] || {
          echo "BLOCKED: runtime-state env value must not be empty"
          return 1
        }
        resolved="$(readlink -m "$value")" || {
          echo "BLOCKED: cannot resolve runtime-state path"
          return 1
        }
        [[ "$resolved" == /opt/dealix/* ]] || {
          echo "BLOCKED: runtime-state path must remain under /opt/dealix"
          return 1
        }
        case "$resolved" in
          "$root_real"|"$root_real"/*)
            echo "BLOCKED: runtime-state path resolves inside canonical repo"
            return 1
            ;;
        esac
        export "$key=$resolved"
        case "$key" in
          DEALIX_RUNTIME_STATE_ROOT) seen_state=1 ;;
          DEALIX_MONEY_REPORT_ROOT) seen_money=1 ;;
          DEALIX_REVENUE_CYCLE_OUT) seen_revenue=1 ;;
        esac
        ;;
      *)
        echo "BLOCKED: unexpected runtime-state env key: $key"
        return 1
        ;;
    esac
  done < "$RUNTIME_ENV"
  if [[ "$seen_state" -ne 1 || "$seen_money" -ne 1 || "$seen_revenue" -ne 1 ]]; then
    echo "BLOCKED: runtime-state env is missing required keys"
    return 1
  fi
  RUNTIME_STATE_READY=1
}

require_runtime_state() {
  if [[ "$RUNTIME_STATE_READY" -ne 1 ]]; then
    echo "BLOCKED: mutable direct command requires validated runtime-state isolation"
    exit 78
  fi
}

# Private Issue-bridge commands execute this script directly rather than inside
# dealix-company@.service. Load the same root-owned, allowlisted runtime-state
# contract here so mutable direct commands cannot silently fall back into Git.
load_runtime_state_env

cd "$ROOT"

safe_service_state() {
  local service="$1"
  printf '%-20s ' "$service"
  systemctl is-active "$service" 2>/dev/null || true
}

ensure_python() {
  if [[ ! -x "$PY_BOOTSTRAP" ]]; then
    echo "BLOCKED: deterministic automation Python bootstrap missing: $PY_BOOTSTRAP"
    return 1
  fi
  DEALIX_REPO_ROOT="$ROOT" "$PY_BOOTSTRAP"
  [[ -x "$PY" ]] || {
    echo "BLOCKED: deterministic automation Python missing after bootstrap: $PY"
    return 1
  }
}

ensure_github_git_auth() {
  command -v gh >/dev/null 2>&1 || {
    echo "BLOCKED: gh CLI unavailable"
    return 1
  }
  gh auth status >/dev/null 2>&1 || {
    echo "BLOCKED: gh CLI is not authenticated"
    return 1
  }
  # Configure Git's GitHub credential helper without printing a token.
  gh auth setup-git >/dev/null 2>&1 || {
    echo "BLOCKED: could not configure non-interactive GitHub git credentials"
    return 1
  }
}

case "$COMMAND" in
  status)
    echo "===== DEALIX VPS STATUS ====="
    date -Is
    echo "user=$(whoami)"
    echo "host=$(hostname)"
    echo "repo_head=$(git rev-parse HEAD)"
    echo "branch=$(git branch --show-current)"
    echo "runtime_state_ready=$RUNTIME_STATE_READY"
    git status -sb
    echo
    safe_service_state docker
    safe_service_state ollama
    safe_service_state tailscaled
    safe_service_state fail2ban
    safe_service_state hermes-dealix
    echo
    docker ps --filter name=dealix-n8n --format 'n8n={{.Status}} {{.Ports}}' 2>/dev/null || true
    echo
    ollama ps 2>/dev/null || true
    echo
    free -h
    ;;

  repo-inspect)
    echo "===== DEALIX REPO INSPECT ====="
    ensure_github_git_auth
    GIT_TERMINAL_PROMPT=0 git fetch origin main --quiet
    echo "local=$(git rev-parse HEAD)"
    echo "origin_main=$(git rev-parse origin/main)"
    git status -sb
    git log -5 --oneline --decorate
    ;;

  verify)
    echo "===== DEALIX SAFE VERIFY ====="
    ensure_python
    if [[ -f scripts/verify_full_autonomous_ops_stack.py ]]; then
      "$PY" scripts/verify_full_autonomous_ops_stack.py --skip-api
    else
      echo "MISSING scripts/verify_full_autonomous_ops_stack.py"
    fi
    if [[ -f scripts/company_ready_verify.sh ]]; then
      bash scripts/company_ready_verify.sh --docs-only --skip-go-live
    else
      echo "MISSING scripts/company_ready_verify.sh"
    fi
    ;;

  autonomous-dry-run)
    echo "===== COMPLETE AUTONOMOUS DAY DRY RUN ====="
    ensure_python
    "$PY" scripts/run_dealix_complete_autonomous_day.py --dry-run
    ;;

  daily)
    echo "===== DEALIX DAILY SAFE RUN ====="
    require_runtime_state
    ensure_python
    if [[ -f scripts/ops/dealix_daily_self_runner.py ]]; then
      "$PY" scripts/ops/dealix_daily_self_runner.py
    else
      echo "MISSING scripts/ops/dealix_daily_self_runner.py"
      exit 3
    fi
    ;;

  sales-arena)
    echo "===== DEALIX SALES ARENA ====="
    require_runtime_state
    ensure_python
    if [[ -f scripts/commercial/run_sales_arena.py ]]; then
      "$PY" scripts/commercial/run_sales_arena.py
    else
      echo "MISSING scripts/commercial/run_sales_arena.py"
      exit 3
    fi
    ;;

  ollama-status)
    echo "===== OLLAMA STATUS ====="
    systemctl is-active ollama
    ollama list
    ollama ps
    ;;

  n8n-status)
    echo "===== N8N STATUS ====="
    docker ps --filter name=dealix-n8n --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
    ;;

  security-status)
    echo "===== SECURITY STATUS ====="
    safe_service_state tailscaled
    safe_service_state fail2ban
    if command -v ufw >/dev/null 2>&1; then
      ufw status 2>/dev/null || echo "UFW status requires elevated read permission"
    fi
    echo
    echo "Listening sockets (process names only; no environment/secrets):"
    ss -lnt 2>/dev/null | head -40 || true
    ;;

  autopilot-status|autopilot-heartbeat|autopilot-production|autopilot-repo-watch|autopilot-preflight|autopilot-morning-fallback|autopilot-midday|autopilot-evening|autopilot-nightly|autopilot-weekly|autopilot-local-ai)
    if [[ ! -x "$AUTOPILOT" ]]; then
      echo "BLOCKED: Dealix Company Autopilot is not installed"
      exit 3
    fi
    exec "$AUTOPILOT" "${COMMAND#autopilot-}"
    ;;

  *)
    echo "DENIED: unsupported command '$COMMAND'"
    echo "Allowed: status repo-inspect verify autonomous-dry-run daily sales-arena ollama-status n8n-status security-status autopilot-status autopilot-heartbeat autopilot-production autopilot-repo-watch autopilot-preflight autopilot-morning-fallback autopilot-midday autopilot-evening autopilot-nightly autopilot-weekly autopilot-local-ai"
    exit 64
    ;;
esac