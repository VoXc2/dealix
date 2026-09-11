---
name: dealix-customer-value
description: Track customer-validated value against the baseline and prepare expansion or referral candidates. Customer value is never the same as public proof or recognized revenue.
---

# Dealix Customer Value

## Scope

- Value = validated delta against the recorded baseline, with the customer as validator.
- `CUSTOMER_VALUE != PUBLIC_PROOF`; `PAYMENT != RECOGNIZED_REVENUE`.
- Expansion candidates only after validated value and customer satisfaction evidence.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/export_value_plan_snapshot.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/verify_value_plan_stack.py" 2>&1 | tail -5
```

## Output contract

- Value record: customer, baseline, intervention, measured delta, validation source, confidence.
- Expansion/referral candidates with consent status; referral needs explicit customer consent.
- Numeric claims labelled `MEASURED`, `ESTIMATED`, or `UNKNOWN`.

## Forbidden

- Publishing value claims, contacting referents, or recognizing revenue without verified payment.
