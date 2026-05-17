# Forbidden Claims — الادعاءات الممنوعة

Claims an affiliate may **never** make about Dealix. The asset review gate
(`affiliate_os/asset_registry.review_asset_copy`) blocks copy containing these.

## Blocked outright

Any guaranteed-outcome promise:

- "guaranteed sales" / "guaranteed results" / "guaranteed ROI"
- "guaranteed revenue" / "guaranteed income"
- "risk-free returns"
- "نضمن لك" / "نضمن النتائج" / "أرباح مضمونة"

The blocked list lives in `affiliate_os/config/affiliate_rules.yaml` under
`forbidden_claims`, and is layered on top of two governance guards:
`governance_os/claim_safety.py` (forbidden-claim/term scan) and
`governance_os/runtime_decision.py` (regex guaranteed-outcome detection with
negation handling — "we do not guarantee X" is correctly **not** flagged).

## Requires an approved source

Even when phrased carefully, claims in these areas need an approved source
before they can be published:

security · compliance · legal · privacy · ROI · revenue increase · case-study
results.

## Why this is strict

The guards are deliberately shallow backstops — substring + regex. They catch
the obvious violations; they do not catch every novel phrasing. **Human review
of every affiliate asset remains mandatory.** A false positive is reviewed; a
false negative ships a violation. The gate errs toward review.

## Say this instead

Describe what Dealix *does*, not what it *guarantees*: "Dealix helps Saudi B2B
teams organize their revenue operations" — not "Dealix guarantees you more
revenue."
