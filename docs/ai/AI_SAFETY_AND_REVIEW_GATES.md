# AI Safety and Review Gates (Dealix)

## Pre-output check
- Every prompt must include safety footer
- Every output is a draft

## Post-output check
- Run `check_output()` from `scripts/lib/ai_safety.py`
- Run `check_flags()` to ensure required safety flags present

## Block conditions
- Output contains "guarantee", "100% success", "ROI of X" → block
- Output missing "no_guarantee" flag → block
- Output missing "no_auto_send" flag → block
- Output missing "human_review_required" flag → block

## Who can override
- Only the founder
- Override logged in audit
