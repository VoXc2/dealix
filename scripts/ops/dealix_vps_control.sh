#!/usr/bin/env bash
set -Eeuo pipefail

# Safe allowlisted control surface for the Dealix Command & AI Node.
# Intentionally excludes arbitrary shell, external sends, merges, production mutation,
# payments, secret changes, and destructive actions.

ROOT="/opt/dealix/workspace/dealix"
AUTOPILOT="/opt/dealix/control/bin/dealix_company_autopilot.sh"
PY_BOOTSTRAP="$ROOT/scripts/ops/ensure_founder_automation_python.sh"
PY="$ROOT/.venv/bin/python"
COMMAND="${1:-status}"

if [[ ! -d "$ROOT/.git" ]]; then
  echo "BLOCKED: canonical Dealix repo not found at $ROOT"
  exit 2
fi

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
