#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Safely decommission the companion `ai-company-saudi` Docker stack.
#
# This script touches ONLY resources whose names start with `ai-company-` and
# the compose project checked out at the path provided via --path (default:
# /root/ai-company-saudi). It never touches:
#   - the `dealix-api.service` systemd unit
#   - host Postgres / host Redis
#   - any container, volume, or network named `dealix-*` or prefixed `dealix_`
#
# By default the script is DRY-RUN: it prints the commands it would run and
# exits 0. Pass --apply to actually execute them. Volumes are never removed
# unless you also pass --purge-volumes.
#
# Usage:
#   scripts/server/decommission_ai_company_saudi.sh                 # dry-run
#   scripts/server/decommission_ai_company_saudi.sh --apply
#   scripts/server/decommission_ai_company_saudi.sh --apply --purge-volumes
#   scripts/server/decommission_ai_company_saudi.sh --path /root/ai-company-saudi --apply
#
# See docs/project-merge-ai-company-saudi.md for the full runbook.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

COMPOSE_PATH="/root/ai-company-saudi"
APPLY=0
PURGE_VOLUMES=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --path)           COMPOSE_PATH="$2"; shift 2 ;;
        --apply)          APPLY=1; shift ;;
        --purge-volumes)  PURGE_VOLUMES=1; shift ;;
        -h|--help)
            sed -n '2,20p' "$0"; exit 0 ;;
        *)
            echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

say()  { printf '%s\n' "$*"; }
warn() { printf '\033[33m[warn]\033[0m %s\n' "$*" >&2; }
fail() { printf '\033[31m[fail]\033[0m %s\n' "$*" >&2; exit 1; }

run() {
    # run or echo a command depending on --apply
    if [[ $APPLY -eq 1 ]]; then
        say "+ $*"
        eval "$@"
    else
        say "[dry-run] $*"
    fi
}

# ── preflight ────────────────────────────────────────────────────────────────

command -v docker >/dev/null 2>&1 || fail "docker not installed"

if [[ $APPLY -eq 1 && $EUID -ne 0 ]]; then
    warn "you are not root — some docker/systemd commands may fail"
fi

# Refuse to proceed if the canonical Dealix API looks unhealthy.
if ! curl -fsS --max-time 3 http://127.0.0.1:8000/health >/dev/null 2>&1; then
    warn "Dealix API at http://127.0.0.1:8000/health is not responding."
    warn "Aborting — bring dealix-api.service up first, then re-run."
    [[ $APPLY -eq 1 ]] && exit 3 || say "(dry-run: continuing anyway to show what would happen)"
fi

# ── inventory ────────────────────────────────────────────────────────────────

say "== companion containers =="
docker ps -a --filter 'name=^ai-company-' --format '{{.Names}}\t{{.Status}}\t{{.Image}}' || true

say "== companion volumes =="
docker volume ls --filter 'name=ai-company' --format '{{.Name}}' || true
# the companion compose uses anonymous project-named volumes; also inspect by path
if [[ -f "$COMPOSE_PATH/docker-compose.yml" ]]; then
    project_name="$(basename "$COMPOSE_PATH" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '_')"
    docker volume ls --filter "name=^${project_name}_" --format '{{.Name}}' || true
fi

# ── backup .env ──────────────────────────────────────────────────────────────

if [[ -f "$COMPOSE_PATH/.env" ]]; then
    ts="$(date +%Y%m%d%H%M%S)"
    backup="/root/ai-company-saudi.env.bak.${ts}"
    run "cp -a '$COMPOSE_PATH/.env' '$backup'"
    run "chmod 600 '$backup'"
    say "backed up .env → $backup"
else
    warn "no .env found at $COMPOSE_PATH/.env — skipping backup"
fi

# ── stop + remove containers ─────────────────────────────────────────────────

if [[ -f "$COMPOSE_PATH/docker-compose.yml" ]]; then
    run "docker compose -f '$COMPOSE_PATH/docker-compose.yml' down --remove-orphans"
else
    warn "$COMPOSE_PATH/docker-compose.yml missing — falling back to name-prefix teardown"
    while read -r name; do
        [[ -n "$name" ]] && run "docker rm -f '$name'"
    done < <(docker ps -a --filter 'name=^ai-company-' --format '{{.Names}}')
fi

# ── network ──────────────────────────────────────────────────────────────────

while read -r net; do
    [[ -n "$net" ]] && run "docker network rm '$net'"
done < <(docker network ls --filter 'name=ai-company' --format '{{.Name}}' || true)

# ── volumes (opt-in only) ────────────────────────────────────────────────────

say ""
say "== volumes retained =="
say "The following commands would delete companion data volumes. They are NOT"
say "executed unless you pass --purge-volumes, because removal is irreversible."
say ""
while read -r vol; do
    [[ -z "$vol" ]] && continue
    if [[ $PURGE_VOLUMES -eq 1 ]]; then
        run "docker volume rm '$vol'"
    else
        say "  docker volume rm '$vol'"
    fi
done < <(
    docker volume ls --format '{{.Name}}' \
        | grep -E '^(ai-company|ai_company_saudi)_' || true
)

# ── summary ──────────────────────────────────────────────────────────────────

say ""
say "== done =="
if [[ $APPLY -eq 1 ]]; then
    say "companion stack decommissioned."
    [[ $PURGE_VOLUMES -eq 0 ]] && say "data volumes retained — remove with --purge-volumes when ready."
else
    say "dry-run complete. re-run with --apply to execute the commands above."
fi
say ""
say "next: verify docs/project-merge-ai-company-saudi.md §5 checklist."
