---
name: dealix-model-economics
description: Report Dealix model routing and token economics (Ollama, local router, included Go route, direct DeepSeek balance) without spending, topping up, or printing secrets. UNKNOWN stays UNKNOWN.
---

# Dealix Model Economics

## Scope

- Routing order: NO LLM -> LOCAL OLLAMA -> CHEAP/INCLUDED GO -> STRONG GO -> PAID FALLBACK.
- Direct paid DeepSeek balance is a fallback only. No auto-top-up, ever.
- Never print API keys or tokens. Report availability states only.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

curl -sS --max-time 5 http://127.0.0.1:11434/api/tags | head -c 500; echo
curl -sS --max-time 5 http://127.0.0.1:11999/v1/models | head -c 500; echo
```

Direct DeepSeek balance (read-only, no keys):

```bash
"$PY" -c "import json; from pathlib import Path; p=Path('/opt/dealix/company-os/founder-os/current/DEEPSEEK_ACCOUNT_BALANCE_LATEST.json'); d=json.loads(p.read_text()) if p.exists() else {}; print('direct_deepseek_available=', d.get('is_available')); print('balances=', [{k:v for k,v in b.items() if k != 'currency'} for b in d.get('balance_infos', [])])"
```

Deterministic work (no LLM): health, disk, RAM, SHA, timers, queue counts, certificate expiry, budget thresholds, numeric aggregation.

## Output contract

- Route used per task with `provider`, `model`, `tokens`, `cost`, `success` when available. `UNKNOWN` stays `UNKNOWN`.
- Explicitly state when a paid fallback was NOT used.

## Forbidden

- Auto top-up, purchases, printing keys, or silently consuming direct paid balance.
