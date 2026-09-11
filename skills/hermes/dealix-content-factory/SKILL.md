---
name: dealix-content-factory
description: Generate Arabic-first, proof-safe sector content and repurpose it into channel queues (website, SEO, LinkedIn draft, X, newsletter). Drafts only: no publish, no send, no fake proof.
---

# Dealix Content Factory

## Scope

- Arabic first with English parity where it matters; Saudi context; sector packs as pattern knowledge only.
- Reuse one asset across channels instead of inventing per-channel claims.
- Every claim is `PATTERN`, `ESTIMATED`, or evidence-backed; customer proof needs permission.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/dealix_content_factory_daily.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_content_engine.py" --help 2>/dev/null || true
```

## Output contract

- Per asset: channel, ICP, format, CTA, consent rule, owner, success metric, stop-loss.
- Queue states: `DRAFT`, `QUEUED_FOR_APPROVAL`, `APPROVED`, `PUBLISHED` (last two only by founder).
- No fake ROI, fake urgency, or fake testimonials.

## Forbidden

- Publishing, scheduling external posts, scraping LinkedIn, or sending newsletters.
