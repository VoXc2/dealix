---
name: dealix-sector-research
description: Research Saudi-first sector demand signals from permitted internal sources and produce a read-only targeting plan. Research is not relationship, consent, pipeline, or revenue.
---

# Dealix Sector Research

## Scope

- Internal, permitted sources only: existing targeting seeds, company directories, founder-provided lists. No scraping, no purchased lists.
- Output is research attention: sectors, pain hypotheses, offer fit, evidence level.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/commercial/generate_daily_targeting_plan.py"
"$PY" "$REPO/scripts/commercial/import_company_directory.py" --help
"$PY" "$REPO/scripts/merge_research_targets.py" --help
REPORT="$(ls -t "$REPO"/reports/commercial/*targeting* 2>/dev/null | head -1)"; [ -n "$REPORT" ] && sed -n '1,60p' "$REPORT"
```

## Output contract

- Every row: sector, pain_hypothesis, offer, evidence_level, next_internal_action.
- Mark `RESEARCH_ONLY`; public contact is not consent.
- No fixed prices, no invented statistics.

## Forbidden

- Scraping, purchased lists, cold outreach, CRM mutation, or claiming pipeline.
