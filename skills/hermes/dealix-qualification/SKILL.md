---
name: dealix-qualification
description: Qualify an inbound or warm opportunity into an internal, evidence-bound disposition (accept, nurture, reject) without contacting anyone. Qualification creates drafts, never sends.
---

# Dealix Qualification

## Scope

- Inputs: inbound diagnostic request, warm reply, referral, or event interaction with evidence.
- Output: disposition + missing evidence + recommended next internal step (draft only).
- Consent rules: inbound and opt-in only. No cold WhatsApp, no LinkedIn automation.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/distribution_day.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_call_sheet.py" --help 2>/dev/null || true
sed -n '1,12p' /opt/dealix/company-os/founder-os/queues/ACTION_QUEUE.tsv
```

## Output contract

- Disposition: `QUALIFIED_FOR_DISCOVERY`, `NEEDS_EVIDENCE`, `NURTURE`, `REJECT_WITH_REASON`.
- List blockers explicitly; if consent is missing, the next step is `REQUEST_CONSENT`, not a send.
- Every commercial claim maps to evidence or stays a hypothesis.

## Forbidden

- Sending messages, booking on behalf of the customer, quoting prices, or charging.
