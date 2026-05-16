# Evaluation Dominance Gates

Release gates must cover more than model accuracy.

## Mandatory evaluation domains

- `hallucination`
- `retrieval`
- `workflow_execution`
- `governance`
- `business_impact`
- `operational_efficiency`

## Promotion rule

A release can be promoted only if all required domains have passing evidence and no unresolved high-risk governance failures.
