#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# server_doctor.sh — diagnostics for a Dealix server.
#
# Read-only. Never stops or restarts anything. Checks for the specific
# problems seen during the ai-company-saudi merge:
#
#   - dealix-api.service state and /health
#   - Docker compose stacks running on the host
#   - Port conflicts on 5432 / 6379 / 8000 / 8001 / 27017
#   - Public exposure of Postgres / Redis / Mongo
#   - Ollama local-AI service status (optional)
#   - Nginx state and config test
#   - fail2ban jails
#
# Exit code is 0 if every probe is green, 1 if any check failed.
# ─────────────────────────────────────────────────────────────────────────────
set -u

PASS=0
FAIL=0

ok()    { printf '  \033[32m[ok]\033[0m    %s\n' "$*"; PASS=$((PASS+1)); }
miss()  { printf '  \033[33m[warn]\033[0m  %s\n' "$*"; }
bad()   { printf '  \033[31m[fail]\033[0m  %s\n' "$*"; FAIL=$((FAIL+1)); }
head()  { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

has()   { command -v "$1" >/dev/null 2>&1; }

# ── dealix-api.service ───────────────────────────────────────────────────────
head "dealix-api.service"
if has systemctl; then
    if systemctl list-unit-files dealix-api.service >/dev/null 2>&1; then
        state="$(systemctl is-active dealix-api.service 2>/dev/null || true)"
        if [[ "$state" == "active" ]]; then
            ok "systemd unit active"
        else
            bad "dealix-api.service is '$state' — expected 'active'"
        fi
    else
        miss "dealix-api.service not installed on this host"
    fi
else
    miss "systemctl not available"
fi

if has curl; then
    if curl -fsS --max-time 3 http://127.0.0.1:8000/health >/dev/null 2>&1; then
        ok "http://127.0.0.1:8000/health responds"
    else
        bad "http://127.0.0.1:8000/health is not responding"
    fi
fi

# ── Nginx ────────────────────────────────────────────────────────────────────
head "Nginx"
if has systemctl && systemctl list-unit-files nginx.service >/dev/null 2>&1; then
    [[ "$(systemctl is-active nginx 2>/dev/null)" == "active" ]] \
        && ok "nginx active" \
        || bad "nginx not active"
    if has nginx; then
        if nginx -t >/dev/null 2>&1; then ok "nginx -t config valid"; else bad "nginx -t reports errors"; fi
    fi
else
    miss "nginx systemd unit not installed"
fi

# ── fail2ban ─────────────────────────────────────────────────────────────────
head "fail2ban"
if has fail2ban-client; then
    jails="$(fail2ban-client status 2>/dev/null | awk -F: '/Jail list/ {print $2}' | xargs || true)"
    if [[ -n "$jails" ]]; then
        ok "jails active: $jails"
    else
        miss "fail2ban installed but no jails listed"
    fi
else
    miss "fail2ban-client not installed"
fi

# ── Docker stacks on this host ───────────────────────────────────────────────
head "Docker"
if has docker && docker info >/dev/null 2>&1; then
    running="$(docker ps --format '{{.Names}}' | wc -l)"
    ok "docker daemon reachable ($running containers running)"
    companion="$(docker ps --format '{{.Names}}' | grep -c '^ai-company-' || true)"
    if [[ "$companion" -gt 0 ]]; then
        bad "$companion companion ai-company-* containers still running — run scripts/server/decommission_ai_company_saudi.sh"
        docker ps --filter 'name=^ai-company-' --format '    {{.Names}} ({{.Image}}) — {{.Status}}'
    else
        ok "no ai-company-* containers running"
    fi
    dealix_ct="$(docker ps --format '{{.Names}}' | grep -c '^dealix-' || true)"
    [[ "$dealix_ct" -gt 0 ]] && miss "dealix-* containers present ($dealix_ct) alongside systemd service — choose ONE runtime"
else
    miss "docker not installed or daemon unreachable"
fi

# ── port conflicts / exposure ────────────────────────────────────────────────
head "listening sockets"
if ! has ss; then
    miss "ss (iproute2) not installed — skipping port checks"
else
    check_port() {
        local port="$1" expect_local="$2"
        local lines
        lines="$(ss -Hltn "( sport = :${port} )" 2>/dev/null || true)"
        if [[ -z "$lines" ]]; then
            miss "port ${port}: no listener"
            return
        fi
        local count
        count="$(printf '%s\n' "$lines" | wc -l)"
        # parse listen addresses
        local public=0
        while read -r addr; do
            [[ -z "$addr" ]] && continue
            case "$addr" in
                127.0.0.1:*|::1:*|[::ffff:127.0.0.1]:*) : ;;
                0.0.0.0:*|[::]:*|*:*) public=1 ;;
            esac
        done < <(printf '%s\n' "$lines" | awk '{print $4}')

        if [[ "$expect_local" == "1" && "$public" == "1" ]]; then
            bad "port ${port}: listener bound on a public address — expected localhost only"
        elif [[ "$count" -gt 1 ]]; then
            bad "port ${port}: ${count} listeners — likely conflict"
            printf '%s\n' "$lines" | awk '{print "      "$4}'
        else
            ok "port ${port}: single listener ($(printf '%s' "$lines" | awk '{print $4}'))"
        fi
    }

    check_port 5432  1   # Postgres — localhost only
    check_port 6379  1   # Redis    — localhost only
    check_port 27017 1   # Mongo    — should not be exposed
    check_port 8000  0   # Dealix API
    check_port 8001  0   # override port, optional
fi

# ── Ollama (optional) ────────────────────────────────────────────────────────
head "Ollama (optional, local AI)"
if has systemctl && systemctl list-unit-files ollama.service >/dev/null 2>&1; then
    [[ "$(systemctl is-active ollama 2>/dev/null)" == "active" ]] \
        && ok "ollama active" \
        || miss "ollama installed but not active"
    if has curl && curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
        ok "ollama api responds on 11434"
    fi
else
    miss "ollama not installed (ok if you don't use local AI)"
fi

# ── summary ──────────────────────────────────────────────────────────────────
printf '\n== summary ==\n  pass=%d  fail=%d\n' "$PASS" "$FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
