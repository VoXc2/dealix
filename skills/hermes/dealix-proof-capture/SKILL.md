---
name: dealix-proof-capture
description: Capture delivery evidence and build a proof pack with provenance, customer validation status, and permission gating. Proof is never public without explicit customer permission.
---

# Dealix Proof Capture

## Scope

- Every proof item carries: baseline, intervention, result, evidence source, customer validation, permission status.
- `PROOF_ELIGIBLE != PUBLIC_PROOF`; publishing requires recorded customer permission.
- No fabricated testimonials, logos, metrics, or case studies.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/add_proof_item.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_proof_pack.py" --help 2>/dev/null || true
```

## Output contract

- Proof item: id, source, measured result, validation owner, permission status, visibility.
- Visibility states: `INTERNAL_ONLY`, `CUSTOMER_APPROVED`, `PUBLIC_APPROVED`.
- Unvalidated results stay `DELIVERY_EVIDENCE_ONLY`.

## Forbidden

- Publishing, sending proof to third parties, or implying customer endorsement without permission.
