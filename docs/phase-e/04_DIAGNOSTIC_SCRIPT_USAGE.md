# Diagnostic Script — Usage

`scripts/dealix_diagnostic.py` generates a bilingual Mini Diagnostic
in ~30 seconds, with **zero API keys** required.

## Quick start

```bash
python scripts/dealix_diagnostic.py \
  --company "[Customer-Slot-A]" \
  --sector "b2b_services" \
  --region "riyadh" \
  --pipeline-state "has leads but inconsistent follow-up"
```

The script writes a Markdown file to `docs/diagnostics/<slug>.md` and
prints the path on stdout.

## Required inputs

| Flag | Purpose | Example |
|---|---|---|
| `--company` | Placeholder name (NEVER real customer name in repo) | `Customer-Slot-A` |
| `--sector` | Industry vertical | `b2b_services`, `legal`, `consulting`, `retail` |
| `--region` | Saudi region or city | `riyadh`, `jeddah`, `eastern` |
| `--pipeline-state` | Free-text describing where they are | `has leads but inconsistent follow-up` |

## Optional inputs

| Flag | Purpose |
|---|---|
| `--language` | `ar` (default), `en`, or `bilingual` |
| `--output-dir` | Override the default `docs/diagnostics/` path |
| `--dry-run` | Print to stdout instead of writing to disk |

## What the output contains

1. Header (bilingual + date)
2. Snapshot of inputs
3. 3 ranked opportunities
4. 1 Arabic draft message
5. Recommended safe channel
6. 1 risk to avoid (bilingual)
7. Service recommendation (Dealix tier)
8. No-guarantee clause + action_mode markers

## What the script will NOT do

- ❌ Make any HTTP call to a customer's website / LinkedIn / scrape source
- ❌ Make an LLM call (it composes from local YAML rules)
- ❌ Write to a database
- ❌ Send any message to anyone
- ❌ Fabricate a metric or testimonial

## When the script lacks data

If the script hits a section where it has no rule for the input, the
output will say `insufficient_evidence` — that's the honest answer.
You then draft that section by hand (or skip it).

## Hard-rule perimeter

- Output is reviewed BEFORE you send it to the customer.
- Output is shared via WhatsApp/Email manually — Dealix does not send
  on your behalf.
- Output is treated as `internal_only` until the customer confirms
  receipt and gives feedback.
