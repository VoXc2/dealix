---
name: dealix-proposal-draft
description: Draft a customer-specific proposal from qualified discovery evidence using the canonical renderer. Draft-only: no send, no signature, no binding commitment, no invented pricing.
---

# Dealix Proposal Draft

## Scope

- Proposals are customer-specific and evidence-bound: problem, scope, acceptance criteria, timeline, proof plan.
- Pricing comes from the approved offer catalog or discovery; never invented here.
- Everything produced is a draft routed to the approval queue.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/render_diagnostic_proposal.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_proposal_generator.py" --help 2>/dev/null || true
```

## Output contract

- Proposal sections: problem, evidence, scope, acceptance criteria, timeline, investment, proof plan.
- Every number labelled `ESTIMATED` or sourced from the catalog; `UNKNOWN` stays unknown.
- Delivery state: `DRAFT_AWAITING_FOUNDER_APPROVAL`.

## Forbidden

- Sending, e-signature, spending, or promising guaranteed ROI or revenue.
