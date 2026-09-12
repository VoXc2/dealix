---
name: dealix-website-audit
description: Audit the public Dealix surfaces (home, diagnostic, proof, partners) read-only for clarity, trust, SEO, accessibility, performance hints, and funnel integrity. No redesign, no publish.
---

# Dealix Website Audit

## Scope

- Preserve the approved identity: premium white, deep navy, cyan/turquoise, restrained gold.
- Audit dimensions: clarity, trust, mobile, RTL, accessibility, SEO, performance hints, funnel integrity, privacy.
- The free diagnostic must remain a primary, genuinely free entry point.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/verify_gtm_public_surfaces.py" 2>&1 | tail -8
"$PY" "$REPO/scripts/verify_commercial_launch_ready.py" 2>&1 | tail -8
"$PY" -m pytest "$REPO/tests/test_free_diagnostic_funnel_contract.py" -q --no-cov 2>&1 | tail -4
```

## Output contract

- Findings per dimension with file reference and severity.
- Funnel check: diagnostic is free, no card, no hidden paid requirement.
- No claim of production green from a local audit alone.

## Forbidden

- Publishing, deploying, changing DNS, or redesigning identity without approval.
