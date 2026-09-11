---
name: dealix-go-broker
description: Plan every OpenCode Go job through the deterministic resource broker: cheapest adequate route, reserve capacity for emergencies, paid spill disabled unless the founder approves. Never calls a model.
---

# Dealix Go Resource Broker

## Scope

- Route order: R0 no model -> R1 deterministic -> R2 local Ollama -> R3 included light -> R4 included high -> R5 strong reasoning -> R6 paid exception.
- R6 requires explicit founder approval AND critical emergency value. No auto-top-up, no silent paid spill.
- Headroom that cannot be observed locally stays `UNKNOWN` and uses a conservative envelope.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/ops/go_resource_broker.py" --status
"$PY" "$REPO/scripts/ops/go_resource_broker.py" --plan CODE_ENGINEERING --complexity high --value high
"$PY" "$REPO/scripts/ops/go_resource_broker.py" --plan CONTENT_DRAFT --value medium --json
```

## Output contract

- Plan fields: route, reason, model_hint, paid_spill, off_peak_preferred, reserve_kept, headroom.
- Record executed jobs with `--record` so the daily envelope stays honest.
- Off-peak recommendation basis is `UNKNOWN_OFFICIAL_PEAK_DATA`; never claim exact Go quota.

## Forbidden

- Consuming direct paid balance, auto top-up, or claiming usage numbers that are not observable.
