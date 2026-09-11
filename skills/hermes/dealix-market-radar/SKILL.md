---
name: dealix-market-radar
description: Produce the read-only Universal Market Radar brief over permitted signals and playbooks. Radar ranks internal research attention only; it grants no relationship, consent, or send authority.
---

# Dealix Market Radar

## Scope

- Sources are normalized `MarketSignalReceipt` rows and the machine-readable radar/playbook registries.
- Output is internal attention ranking, never outreach or pipeline.
- No scraping, no purchased data, no follower/impression inflation.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/commercial/run_universal_market_radar_v1.py"
"$PY" "$REPO/scripts/verify_universal_market_radar.py" 2>&1 | tail -5
sed -n '1,50p' "$REPO/data/founder_briefs/universal_market_radar_latest.json" 2>/dev/null || true
```

## Output contract

- Top signals with source, evidence level, why-now, and the safe internal next step.
- `RESEARCH_ONLY` unless a real interaction already exists.
- Explicitly list what is NOT evidence.

## Forbidden

- Contacting targets, publishing, spending, or treating research as pipeline.
