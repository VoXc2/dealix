---
name: dealix-production-truth
description: Read-only production truth for Dealix (web/API health, TLS, release parity, local services). HTTP 200 is not production green. Never deploys or mutates.
---

# Dealix Production Truth

## Scope

- Read-only verification only. No deploy, no DNS, no database mutation, no secret reads.
- Report states exactly: `PRODUCTION_VERIFIED`, `PRODUCTION_PARTIAL`, `BLOCKED`, `UNKNOWN`.
- `API_RELEASE_PARITY` compares the deployed API SHA with the expected release SHA; a mismatch is a finding, not a failure to fix here.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"

curl -sS -o /dev/null -w 'WEB=%{http_code}\n' --max-time 12 https://dealix.me/healthz || true
curl -sS -o /dev/null -w 'API=%{http_code}\n' --max-time 12 https://api.dealix.me/healthz || true
curl -sS --max-time 12 https://api.dealix.me/healthz || true

curl -sS -o /dev/null -w 'OLLAMA=%{http_code}\n' --max-time 5 http://127.0.0.1:11434/api/tags || true
curl -sS -o /dev/null -w 'ROUTER=%{http_code}\n' --max-time 5 http://127.0.0.1:11999/v1/models || true

systemctl list-timers dealix-* --all --no-pager | head -20
```

Runtime sentinel (read-only, if present):

```bash
/opt/dealix/control/autonomous-company/bin/dealix-server-sentinel 2>/dev/null | tail -20 || echo "SENTINEL=UNAVAILABLE"
```

## Output contract

- Report `HTTP_WEB`, `HTTP_API`, `TLS`, `API_RELEASE_SHA`, `API_RELEASE_PARITY`, local services, and the reason for any warning.
- Do not claim `PRODUCTION_GREEN` when warnings exist; use `PRODUCTION_PARTIAL` with the warning list.

## Forbidden

- Deploying, restarting production, changing DNS/certificates, or reading secret values.
